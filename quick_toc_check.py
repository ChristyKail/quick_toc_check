#!/usr/bin/env python3

import os
import sys

# copyright Christy Kail and Cinelab Film and Digital, 2022
# Software is provided as is, without warranty of any kind, express or implied.

__version__ = "0.2.0"

# 0.2.0
# Reports count at end of run


class QuickTocCheck:

    def __init__(self, root_folder, toc_folder):

        self.missing = 0
        self.toc_entries = get_entries_from_tocs(toc_folder)
        self.file_entries = get_entries_from_files(root_folder)
        self.compare_entries()
        self.report()

    def compare_entries(self):
        print("\nComparing")

        missing = list(set(self.file_entries) - set(self.toc_entries))

        missing.sort()

        for x in missing:

            if x.startswith("."):
                continue
            print("{}Missing {}{}".format(PrintColors.FAIL, x, PrintColors.ENDC))
            self.missing += 1

    def report(self):

        if self.missing:
            print("\n{}{}/{} files missing in TOC{}".format(PrintColors.FAIL, self.missing, len(self.toc_entries),
                                                            PrintColors.ENDC))
        else:
            print("\n{}{}/{} files missing in TOC{}".format(PrintColors.OKGREEN, self.missing, len(self.toc_entries),
                                                            PrintColors.ENDC))


class PrintColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_entries_from_tocs(folder):

    """loads tocs or csvs from a folder and returns a list of files in them"""

    toc_entries = []

    for toc_f in os.listdir(folder):

        # load txt toc files
        if toc_f.endswith(".txt"):

            with open(os.path.join(folder, toc_f), "r") as toc_file_handler:

                # parse toc file, adding each file name to the list
                for line in toc_file_handler:
                    toc_entries.append(line.split("/")[-1].strip())

        # load S3 csv files
        elif toc_f.endswith(".csv"):

            with open(os.path.join(folder, toc_f), "r") as toc_file_handler:

                # parse csv file, adding each file name to the list
                for line in toc_file_handler:

                    # skip folders
                    if line.endswith("/"):
                        continue

                    toc_entries.append(line.split("/")[-1].strip())

    # exit if no toc or csv files found
    if not toc_entries:
        print("{}No TOCs found here!{}".format(PrintColors.FAIL, PrintColors.ENDC))
        sys.exit(1)

    return toc_entries


def get_entries_from_files(folder):

    """scans a folder recursively and returns a list of files in it"""

    file_entries = []
    print("Scanning folder")

    for root, dirs, files in os.walk(folder):

        # print each folder name as it is scanned
        for directory in dirs:
            print(os.path.join(root, directory))

        for name in files:
            file_entries.append(name)

    # exit if no files found
    if not file_entries:
        print("{}No files found here!{}".format(PrintColors.FAIL, PrintColors.ENDC))
        sys.exit(1)

    return file_entries


if __name__ == "__main__":

    print("{}Quick TOC checker version {}".format(PrintColors.BOLD, __version__))
    print("Note - this tool works on file names only, not on file contents, hashes, or folder structure.")
    print("Do not use if you expect duplicate file names!")
    print("\n{}".format(PrintColors.ENDC))

    input_files_folder = input("Drag folder to check here:")
    toc_files_folder = input("Drag folder of TOCs here:")

    input_files_folder = input_files_folder.replace("\\ ", " ").strip()
    toc_files_folder = toc_files_folder.replace("\\ ", " ").strip()

    QuickTocCheck(input_files_folder, toc_files_folder)
