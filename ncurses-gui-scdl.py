import curses as c
import subprocess

def run_command(stdscr, command):
    stdscr.clear()
    stdscr.addstr(0, 0, f"Executing command: {command}")
    stdscr.refresh()
    pipe = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    row = 2
    while True:
        output = pipe.stdout.readline()
        if not output:
            break
        stdscr.addstr(row, 0, output.strip())
        stdscr.refresh()
        row += 1
    pipe.wait()
    stdscr.addstr(row, 0, "Press any key to exit.")
    stdscr.refresh()
    stdscr.getch()

def main(stdscr):
    c.curs_set(0)
    c.init_pair(1, c.COLOR_BLACK, c.COLOR_WHITE)
    c.init_pair(2, c.COLOR_WHITE, c.COLOR_BLACK)
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
        if not file_path:
            file_path = "None!"
        length, width = stdscr.getmaxyx()
        menu = stdscr.subwin(length - 2, width - 4, 1, 2)
        menu.box()
        menu.addstr(0, (width - len(head)) // 2, head, c.A_REVERSE)
        menu.addstr(length - 4, 4, footer + str(file_path))
        menu.addstr(4 + iterator, 4, [str1, str2, str3][iterator], c.color_pair(1))
        for i in range(3):
            if i != iterator:
                menu.addstr(4 + i, 4, [str1, str2, str3][i], c.color_pair(2))
        menu.refresh()
        input_key = stdscr.getch()
        if input_key == c.KEY_UP:
            iterator = max(0, iterator - 1)
        elif input_key == c.KEY_DOWN:
            iterator = min(2, iterator + 1)
        elif input_key == ord('\n'):
            if iterator == 2:
                break
            elif iterator == 0:
                file_path = stdscr.getstr(6, 6, 100).decode('utf-8')
            elif iterator == 1:
                track_url = stdscr.getstr(5, 6, 100).decode('utf-8')
                download_track = f"scdl -l {track_url} --path {file_path}"
                run_command(stdscr, download_track)
        elif input_key == ord('q'):
            break

if __name__ == "__main__":
    c.wrapper(main)
