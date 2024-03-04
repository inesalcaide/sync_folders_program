import os
import shutil
import logging
import filecmp
import argparse
import time

class SyncFolders:
    def __init__(self, src_folder, replica_folder, sync_interval, log_file):
        self._src_folder = src_folder
        self._replica_folder = replica_folder
        self._sync_interval = sync_interval
        self._log_file = log_file
        self._setup_logging()


    def _setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
                            handlers=[logging.FileHandler(self._log_file), logging.StreamHandler()])

    def run_folder_sync(self):
        if not os.path.isdir(self._src_folder):
            logging.error(f"Invalid source folder path: {self._src_folder}. Please provide a valid source folder path.")
            raise ValueError("Invalid source folder path")
        
        logging.info(f"Starting folder syncronyzation. Source:{self._src_folder}, Replica:{self._replica_folder},"\
                    f" Sync interval:{self._sync_interval} seconds, Log file:{self._log_file}")
        
        try:
            while True:
                logging.info("Logging a new synchronization event\n")
                self._synchronize_folders()
                time.sleep(self._sync_interval)
        except KeyboardInterrupt:
            logging.info("Keyboard interrupt received. Exiting")
            raise SystemExit
        except Exception as e:
            logging.exception(f"An error occurred during folder synchronization: {e}. Exiting")
            raise SystemExit
        
    def _synchronize_folders(self):
        for path, dirs, files in os.walk(self._src_folder):
            relative_path = os.path.relpath(path, self._src_folder)
            replica_path = os.path.join(self._replica_folder, relative_path)
            os.makedirs(replica_path, exist_ok=True)
            self._compare_files_in_folders(files, path, replica_path)

        for path, dirs, files in os.walk(self._replica_folder):
            relative_path = os.path.relpath(path, self._replica_folder)
            src_path = os.path.join(self._src_folder, relative_path)
            self._cleanup_files(src_path=src_path, replica_path=path, files=files)
            self._cleanup_directories(src_path=src_path, replica_path=path, dirs=dirs)

    def _compare_files_in_folders(self, files: str, root_path: str, replica_path: str):
        for file in files:
            src_file = os.path.join(root_path, file)
            replica_file = os.path.join(replica_path, file)
            if os.path.exists(replica_file):
                if self._are_files_equal(src_file, replica_file):
                    message = f"{replica_file} file is up to date."
                else:
                    os.remove(replica_file)
                    shutil.copy2(src_file, replica_file)
                    message = f"{replica_file} file has been updated."
            else:
                shutil.copy2(src_file, replica_file)
                message = f"{replica_file} file has been copied."
            
            logging.info(message)

    @staticmethod
    def _are_files_equal(file1: str, file2: str) -> bool:
        return filecmp.cmp(file1, file2, shallow=False)

    @staticmethod
    def _cleanup_files(src_path: str, replica_path: str, files: str):
        for file in files:
            if not os.path.exists(os.path.join(src_path, file)):
                replica_file = os.path.join(replica_path, file)
                os.remove(replica_file)
                logging.info(f"{replica_file} file has been deleted.")

    @staticmethod
    def _cleanup_directories(src_path:str, replica_path: str, dirs: str):
        for dir in dirs:
            if not os.path.exists(os.path.join(src_path, dir)):
                dir_path = os.path.join(replica_path, dir)
                shutil.rmtree(dir_path)
                logging.info(f"{dir_path} directory has been deleted.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Folder synchronization program')
    parser.add_argument("-s", "--source", type=str, required=True, help="Source folder path")
    parser.add_argument("-r", "--replica", type=str, required=True, help="Replica folder path")
    parser.add_argument("-i", "--sync-interval", type=int, default=300, help="Time interval for synchronization in seconds (default: 300)")
    parser.add_argument("-l", "--log-file", type=str, default="log_file.log", help="Log file path (default: log_file.log)")
    args = parser.parse_args()

    sync_folfers = SyncFolders(src_folder=args.source, replica_folder=args.replica, sync_interval=args.sync_interval, log_file=args.log_file)
    sync_folfers.run_folder_sync()