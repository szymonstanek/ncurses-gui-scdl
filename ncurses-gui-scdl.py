import curses as c
import subprocess
def run_command(stdscr, command):
    stdscr.clear()
    stdscr.addstr(0, 0, f"Executing command: {command}")
    stdscr.refresh()

    # Uruchomienie procesu z przekierowaniem wyjścia do zmiennej pipe
    pipe = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    # Odczytywanie wyjścia procesu i wypisywanie go na ekranie ncurses
    row = 2
    while True:
        output = pipe.stdout.readline()
        if not output:
            break
        stdscr.addstr(row, 0, output.strip())
        stdscr.refresh()
        row += 1

    # Oczekiwanie na zakończenie procesu
    pipe.wait()

    stdscr.addstr(row, 0, "Press any key to exit.")
    stdscr.refresh()
    stdscr.getch()


#============
track_url = ""

def main(stdscr):
    c.curs_set(0)
    c.init_pair(1, c.COLOR_BLACK, c.COLOR_WHITE)  # Define color pair for highlighted text
    c.init_pair(2, c.COLOR_WHITE, c.COLOR_BLACK)  # Define color pair for normal text

    head = "scdl gui 0.2v"
    str1 = "Specify file path to save downloads: "
    str2 = "Download track/playlist from public URL: "
    str3 = "Quit"
    footer = "Current Path: "
    file_path = "None!"
    

    iterator = 0

    while True:
        stdscr.clear()
        stdscr.refresh()

        if(len(file_path)==0):
            file_path = "None!"

        # Handling window dimensions
        length, width = stdscr.getmaxyx()

        # Create a new window for the menu
        menu = stdscr.subwin(length - 2, width - 4, 1, 2)
        menu.box()

        # Add header and footer to the menu
        menu.addstr(0, (width - len(head)) // 2, head, c.A_REVERSE)
        menu.addstr(length - 4, 4, footer + str(file_path))

        # Highlight the selected option
        if iterator == 0:
            menu.addstr(4, 4, str1, c.color_pair(1))
            menu.addstr(5, 4, str2, c.color_pair(2))
            menu.addstr(6, 4, str3, c.color_pair(2))
        elif iterator == 1:
            menu.addstr(4, 4, str1, c.color_pair(2))
            menu.addstr(5, 4, str2, c.color_pair(1))
            menu.addstr(6, 4, str3, c.color_pair(2))
        elif iterator == 2:
            menu.addstr(4, 4, str1, c.color_pair(2))
            menu.addstr(5, 4, str2, c.color_pair(2))
            menu.addstr(6, 4, str3, c.color_pair(1))

        # Refresh the menu window
        menu.refresh()

        # Get user input
        input_key = stdscr.getch()

        # Process user input
        if input_key == c.KEY_UP:
            iterator = max(0, iterator - 1)
        elif input_key == c.KEY_DOWN:
            iterator = min(2, iterator + 1)
        elif input_key == ord('\n'):
            if iterator == 2:
                c.endwin()
                break
            elif iterator == 0:
                stdscr.clear()
                c.curs_set(1)
                c.echo()
                menu = stdscr.subwin(length - 2, width - 4, 1, 2)
                menu.box()

                # Add header and footer to the menu
                menu.addstr(0, (width - len(head)) // 2, head, c.A_REVERSE)
                menu.addstr(4, 4, str1, c.color_pair(2))                
                file_path = stdscr.getstr(6,6,100)
                file_path = file_path.decode('utf8')
                c.curs_set(0)
            elif iterator == 1:
                stdscr.clear()
                c.curs_set(1)
                c.echo()
                menu = stdscr.subwin(length - 2, width - 4, 1, 2)
                menu.box()

                # Add header and footer to the menu
                menu.addstr(0, (width - len(head)) // 2, head, c.A_REVERSE)
                menu.addstr(5, 4, str2, c.color_pair(2))                
                track_url = stdscr.getstr(5,6,100)
                track_url = track_url.decode('utf8')
                download_track = "scdl -l " +track_url+" --path "+file_path
                run_command(stdscr,download_track)
                c.curs_set(0)


        elif input_key == ord('q'):
            # Clean up before exiting
            c.endwin()
            break

if __name__ == "__main__":
    c.wrapper(main)
