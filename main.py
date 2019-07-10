import dbhandler
import sqlite3


def main():
    """
    Test some methods and object creation.
    I promise I'll do test cases.
    """
    db = dbhandler.TSKDatabase()
    print(db.select_headers_tsk_files()[0])

    for count, filesystem in enumerate(db.select_filesystems_from_tsk_fs_info()):
        print(type(filesystem[0]))

if __name__ == "__main__":
    main()


