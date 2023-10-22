# Backup Monitor

Backup Monitor is a Python script that watches specified directories for changes to text files. Whenever a tracked file is modified, the script creates a backup of that file. Users can specify multiple paths, extensions, the number of backup versions to retain, and a backup directory through a `config.ini` file.

## Features:

- **Multiple Paths:** Monitor multiple directories for changes.
- **Custom Extensions:** Specify which file extensions to monitor.
- **Versioned Backups:** Retain multiple versions of each backup.
- **Configurable:** Easily adjust settings through a `config.ini` file.
- **Auto Install:** Includes an `install.bat` file that sets up the required environment and dependencies automatically.

## Installation:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Tom-Hartmann/Config-backup
   ```

2. **Run the `install.bat` file:**
   Before running, ensure you have administrative privileges. This script will:

   - Install Node.js
   - Install Python
   - Install necessary Python libraries
   - Install PM2 for managing the Python script
   - Set the Python script to auto-start using PM2

   Navigate to the repository folder in your terminal and run:

   ```bash
   install.bat
   ```

   You will be prompted to confirm the installations. Type "yes" to proceed.

3. **Modify the `config.ini` file (optional):**
   Adjust the settings in the `config.ini` file to suit your needs. Here you can set:
   - Paths to monitor
   - File extensions to watch
   - Backup folder name
   - Maximum backup versions to retain

## Usage:

Once installed, the Python script will automatically start in the background, and PM2 will manage it. You can check the status of all PM2-managed scripts with:

```bash
pm2 list
```

## Support:

For issues or additional assistance, please [raise an issue](https://github.com/Tom-Hartmann/Config-backup/issues).
