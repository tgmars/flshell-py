import sqlite3

class TSKDatabase(object):
    def __init__(self, filename="/home/tom/Desktop/recruitment.db"):
        self.dbfilename = filename
        self.conn = sqlite3.connect(self.dbfilename)
        self.conn.row_factory = sqlite3.Row

    def select_all_tsk_files(self):
        """
        Query all rows in the tsk_files table
        :param conn: the Connection object
        :return:
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tsk_files")
    
        rows = cur.fetchall()
    
        for row in rows:
            print(row)
    
    def select_files_from_parent_tsk_files(self, par_obj_id):
        """
        Query entries from tsk_files that are
        direct descendants of the given parent
        object id.
        :param conn: SQLite DB connection object
        :param par_obj_id: Entry in tsk_objects
        :return: Results of SQLite query as a list of rows.
        """
        query = """SELECT * FROM tsk_files 
                    JOIN tsk_objects ON tsk_files.obj_id = tsk_objects.obj_id 
                    WHERE tsk_objects.par_obj_id = ? AND tsk_files.type != ?;"""

        cur = self.conn.cursor()
        cur.execute(query, (par_obj_id,"7"))
        return cur.fetchall()

    def select_files_from_filesystem_id_tsk_files(self, filesystem_obj_id):
        """
        Query entries from tsk_files that are
        direct descendants of the given parent
        object id.
        :param conn: SQLite DB connection object
        :param par_obj_id: Entry in tsk_objects
        :return: Results of SQLite query as a list of rows.
        """
        query = """SELECT * FROM tsk_files
                    JOIN tsk_fs_info ON tsk_files.fs_obj_id = tsk_fs_info.obj_id
                    WHERE tsk_fs_info.obj_id = ?;"""

        cur = self.conn.cursor()
        cur.execute(query, (filesystem_obj_id,))
        return cur.fetchall()

    def select_root_files_from_filesystem_id_tsk_files(self, filesystem_obj_id):
        """
        Query entries from tsk_files that are
        direct descendants of the given parent
        object id.
        :param conn: SQLite DB connection object
        :param par_obj_id: Entry in tsk_objects
        :return: Results of SQLite query as a list of rows.
        """
        query = """SELECT * FROM tsk_files
                    JOIN tsk_fs_info ON tsk_files.fs_obj_id = tsk_fs_info.obj_id
                    JOIN tsk_objects ON tsk_files.obj_id = tsk_objects.obj_id 
                    WHERE tsk_fs_info.obj_id = ? AND tsk_objects.par_obj_id = ? AND tsk_files.type != ?;"""

        cur = self.conn.cursor()
        cur.execute(query, (filesystem_obj_id,str(int(filesystem_obj_id)+1),"7"))
        return cur.fetchall()


    def select_filesystems_from_tsk_fs_info(self):
        """
        Select all filesystems that TSK identifies.
        :param conn: SQLite DB connection object
        :param par_obj_id: Entry in tsk_objects
        :return: Results of SQLite query as a list of rows.
        """
        query = "SELECT obj_id, img_offset, fs_type FROM tsk_fs_info"

        cur = self.conn.cursor()
        cur.execute(query)
        return cur.fetchall()



    def select_headers_tsk_files(self):
        """
        Query a table and return a list containg
        the headers of the table.
        """

        query = "SELECT * FROM tsk_files"

        cur = self.conn.cursor()
        cur.execute(query)
        return cur.fetchone().keys()

    def close(self):
        self.conn.close

