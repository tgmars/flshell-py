import dbhandler
import sqlite3


def main():
    """
    Test some methods and object creation.
    I promise I'll do test cases.
    """
    db = dbhandler.TSKDatabase()
    print(db.select_headers_tsk_files()[0])

    item_type = {"3":"d","5":"r"}
    print(item_type["5"])

"""
    for count, filesystem in enumerate(db.select_filesystems_from_tsk_fs_info()):
        print(type(filesystem[0]))
        print("Filesystem",filesystem)
        print("Filesystem[0]",filesystem[0])
        print("Filesystem[0]",str(filesystem[0]))

        #help(filesystem)

        a = db.select_files_from_filesystem_id_tsk_files(str(filesystem[0]))
        print("Start of A",a,"end of A")
        numentries = 0
        for row in db.select_files_from_filesystem_id_tsk_files(str(filesystem[0])):
            numentries=numentries+1
        print("Numentries", numentries)
     """   
if __name__ == "__main__":
    main()


