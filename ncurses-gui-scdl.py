import subprocess
#development version

def clear_screen():
    for _ in range(30):
        print("\n")

def get_choice():
    while True:
        try:
            choice = int(input("Choose an option: "))
            return choice
        except ValueError:
            clear_screen()
            print("Unknown command!\n")

def show_menu():
    print('Soundcloud downloader 0.1v\n')
    print('Current file path:', file_path)
    print('[1] Specify file path')
    print('[2] Download track/playlist from public URL')
    print('[3] Exit')

file_path = "None!"
track_url = ""

def download_track(track_url, file_path):
    try:
        subprocess.check_call(["scdl", "-l", track_url, "--path", file_path])
    except subprocess.CalledProcessError as e:
        print("Error occurred:", str(e))

while True:
    download = False
    if not download:
        clear_screen()
    show_menu()
    choice = get_choice()

    if choice == 1:
        clear_screen()
        file_path = input('Enter the file path to the music folder: ')
        clear_screen()
    elif choice == 2:
        clear_screen()
        track_url = input('Paste the URL: ')
        download_track(track_url, file_path)
        print("\n")
    elif choice == 3:
        break
    else:
        clear_screen()
        print('Unknown command!\n')
