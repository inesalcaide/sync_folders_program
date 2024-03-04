# Folder Synchronization Program

This Python program performs one-way synchronization of two folders. It continuously monitors the source folder and updates the replica folder to match it based on the specified time interval.

## Description

- Synchronization is performed periodically, and changes (file updates, copying, removal operations) are logged to a file and the console output.
- If the source folder does not exist, the script will raise an error and stop.
- If the replica folder does not exist, the script will create it.

## Requirements

- Python 3.x
- Libraries: os, time, shutil, argparse, logging, filecmp

## Usage

```
python3 main.py [-h] -s SOURCE -r REPLICA [-i SYNC_INTERVAL] [-l LOG_FILE]
```

Options:

- `-s, --source SOURCE`: Path to the source folder.
- `-r, --replica REPLICA`: Path to the replica folder that will be updated to match the source folder.
- `-i, --sync-interval SYNC_INTERVAL`: Time interval for synchronization in seconds (default: 300).
- `-l, --log-file LOG_FILE`: Log file path (default: log_file.log).

##Examples

1. Synchronize folders with default options:

```
python3 main.py -s /path/to/source -r /path/to/replica
```
2. Synchronize folders with a custom sync interval and log file path:

```
python3 main.py -s /path/to/source -r /path/to/replica -i 600 -l /path/to/custom.log
```
