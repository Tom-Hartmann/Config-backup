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
        path_obj = Path(file_path)
        backup_dir = path_obj.parent / self.backup_folder
        if not backup_dir.exists():
            backup_dir = self.script_location / self.backup_folder
            backup_dir.mkdir(exist_ok=True)
        
        # Create a backup file with version
        version = 1
        backup_path = backup_dir / f"{path_obj.stem}.v{version}.bak"
        while backup_path.exists() and version <= self.max_versions:
            version += 1
            backup_path = backup_dir / f"{path_obj.stem}.v{version}.bak"
        
        # If we've exceeded the max_versions, delete the oldest one
        if version > self.max_versions:
            oldest_version_path = backup_dir / f"{path_obj.stem}.v1.bak"
            if oldest_version_path.exists():
                oldest_version_path.unlink()

            # Rename all other backup versions to shift them down
            for i in range(2, self.max_versions + 1):
                old_path = backup_dir / f"{path_obj.stem}.v{i}.bak"
                new_path = backup_dir / f"{path_obj.stem}.v{i-1}.bak"
                if old_path.exists():
                    old_path.rename(new_path)
            version = self.max_versions
        
        with open(file_path, 'r') as original, open(backup_path, 'w') as backup:
            backup.write(original.read())
            print(f"Backed up: {file_path} to {backup_path}")

def monitor_directory(paths, extensions, backup_folder, max_versions):
    script_location = Path(__file__).parent
    event_handler = TxtFileHandler(extensions, backup_folder, max_versions, script_location)
    observer = Observer()
    for path in paths:
        observer.schedule(event_handler, path, recursive=True)
    
    observer.start()

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
