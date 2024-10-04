import os
import board
import supervisor

# Number of entries per page
n_entries = 7

# Try importing SD card libraries
try:
    import sdcardio
    import storage
    sd_card_available = True
except ImportError:
    sd_card_available = False

# Helper functions to mimic os.path behavior
def path_exists(path):
    """Check if a path exists."""
    try:
        os.listdir(path)
        return True
    except OSError:
        return False

def path_basename(file_path):
    """Get the filename from a full path."""
    return file_path.split("/")[-1]

class Menu:
    def __init__(self, paths, page_size=n_entries):
        self.paths = paths
        self.page_size = page_size
        self.scripts = self.get_all_scripts()
        self.current_page = 0

    def get_all_scripts(self):
        """Return a sorted list of .py files from all paths."""
        all_files = []
        for path in self.paths:
            if path_exists(path):
                files = [f"{path}/{f}" for f in os.listdir(path) if f.endswith(".py")]
                all_files.extend(files)
        return sorted(all_files)

    def show_page(self):
        """Display the current page of menu items."""
        start = self.current_page * self.page_size
        end = start + self.page_size
        page_files = self.scripts[start:end]

        print(f"\n--- Page {self.current_page + 1}/{self.total_pages()} ---")
        for idx, script in enumerate(page_files, start=1):
            print(f"{idx}. {path_basename(script)}")
        print("Run(#), (n)ext, (p)revious or (q)uit")

    def total_pages(self):
        """Return total number of pages."""
        return (len(self.scripts) + self.page_size - 1) // self.page_size

    def next_page(self):
        """Go to next page, if available."""
        if self.current_page < self.total_pages() - 1:
            self.current_page += 1

    def prev_page(self):
        """Go to previous page, if available."""
        if self.current_page > 0:
            self.current_page -= 1

    def run_script(self, index):
        """Run the selected script."""
        script_to_run = self.scripts[index]
        print(f"Running {path_basename(script_to_run)}...\n")
        supervisor.set_next_code_file(script_to_run)
        supervisor.reload()

# Internal and external paths configuration
internal_sketches_path = "/scripts"
paths = [internal_sketches_path]

# Try mounting the SD card and add paths if available
if sd_card_available:
    try:
        sd = sdcardio.SDCard(board.SD_SPI(), board.SD_CS)
        vfs = storage.VfsFat(sd)
        storage.mount(vfs, "/sd")
        paths.append("/sd/scripts")

    except Exception:
        print("no sd-card detected")

# Create menu instance with both internal and external paths
menu = Menu(paths)

# Main loop to handle user input
while True:
    menu.show_page()
    choice = input(">>> ").lower()

    if choice == 'q':
        break
    elif choice == 'n':  # Next page
        menu.next_page()
    elif choice == 'p':  # Previous page
        menu.prev_page()
    elif choice.isdigit():  # Running selected script
        idx = int(choice) - 1
        if 0 <= idx < menu.page_size:
            absolute_index = menu.current_page * menu.page_size + idx
            if absolute_index < len(menu.scripts):
                menu.run_script(absolute_index)
            else:
                print("Invalid choice!")
        else:
            print("Invalid choice!")
    else:
        print("Invalid input, try again.")
