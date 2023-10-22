import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import configparser
from pathlib import Path

class TxtFileHandler(FileSystemEventHandler):

    def __init__(self, extensions, backup_folder, max_versions, script_location):
        self.extensions = extensions
        self.backup_folder = backup_folder
        self.max_versions = max_versions
        self.script_location = script_location

    def on_modified(self, event):
        if event.is_directory:
            return
        if any(event.src_path.endswith(ext) for ext in self.extensions):
            self.backup_file(event.src_path)

    def backup_file(self, file_path):
        folder_path, file_name = os.path.split(file_path)
        base_name, _ = os.path.splitext(file_name)
        
        # Ensure the backup folder exists.
        backup_dir = os.path.join(self.script_location, self.backup_folder)
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        # Create a new backup file.
        backup_file_name = os.path.join(backup_dir, f"{base_name}_backup_1.txt")
        if os.path.exists(backup_file_name):
            # Rename existing backups, if they exist.
            for version in range(self.max_versions - 1, 0, -1):
                current_backup = os.path.join(backup_dir, f"{base_name}_backup_{version}.txt")
                next_backup = os.path.join(backup_dir, f"{base_name}_backup_{version + 1}.txt")
                if os.path.exists(current_backup):
                    if os.path.exists(next_backup):
                        os.remove(next_backup)
                    os.rename(current_backup, next_backup)
        
        # Copy the current modified file to backup_1.
        with open(file_path, 'r', encoding='utf-8') as original:
            with open(backup_file_name, 'w', encoding='utf-8') as backup:
                backup.write(original.read())
        
        # Remove backups beyond max_versions.
        oldest_backup = os.path.join(backup_dir, f"{base_name}_backup_{self.max_versions + 1}.txt")
        if os.path.exists(oldest_backup):
            os.remove(oldest_backup)

def monitor_directory(paths, extensions, backup_folder, max_versions):
    script_location = Path(__file__).parent
    event_handler = TxtFileHandler(extensions, backup_folder, max_versions, script_location)
    observer = Observer()
    for path in paths:
        observer.schedule(event_handler, path, recursive=True)
    
    observer.start()

    print("Script launched and now monitoring specified directories.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    paths = [p.strip() for p in config['DEFAULT']['paths'].split(',')]
    extensions = [e.strip() for e in config['DEFAULT']['extensions'].split(',')]
    backup_folder = config['DEFAULT'].get('backup_folder', 'backup')
    max_versions = int(config['DEFAULT'].get('max_versions', 10))
    
    monitor_directory(paths, extensions, backup_folder, max_versions)
