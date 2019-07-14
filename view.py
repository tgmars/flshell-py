import npyscreen
import dbhandler
import curses.ascii

#Default form delivered on startup.


class MyTreeData(npyscreen.TreeData):
    
    def h_expand_dir(self, _input):
        self.expanded=True

class MyTreeView(npyscreen.MLTree):

    db = dbhandler.TSKDatabase()

    def h_expand_tree(self, _input):
        if not self.values[self.cursor_line].expanded:
            self.values[self.cursor_line].expanded = True


            ##Override
            for child in self.values[self.cursor_line]._children:
                #Retrieve just the object id to use it as the parent for the query.
                par_obj_id=child.content.split("\t")[3]
                rows = self.db.select_files_from_parent_tsk_files(par_obj_id)
                for file_entry in rows:
                    try:
                        #Something here is throwing an exception
                        item_type = {3:"d",5:"r"}
                        if file_entry[5]=="." or file_entry[5]=="..":
                            pass
                        else:
                            child.new_child("{}\t{}-{}-{}:\t{}\t{}".format(item_type.get(file_entry[11]),
                                file_entry[6],file_entry[3],file_entry[4],file_entry[5],file_entry[0]))
                            child.expanded = False
                            child.selectable=False
                    except:
                        pass

                """
                getchildinodes
                query tskfiles based off child inodes
                set_the childrens children content to the resullts of the query
                """
        else:
            for v in self._walk_tree(self.values[self.cursor_line], only_expanded=False):
                v.expanded = True
        self._cached_tree = None
        self.display()
        self.db.close()


class DefaultForm(npyscreen.Form):
  
    db = dbhandler.TSKDatabase()
    treeData = MyTreeData()

    def h_enter_dir(self, _input):
        pass

    def writeToFile(self, content):
        f= open("output.txt","a+")
        f.write(content)
        f.close
    #def preload_dir(self):


    def create(self): 
        
        #Set keypress_timeout so that while_waiting(self) will trigger.
        self.keypress_timeout=5
        for partition_index, filesystem in enumerate(self.db.select_filesystems_from_tsk_fs_info()):
            """
            Let's make a horrible assumption in the interest of usability. 
            Limits correct displays to Windows boxes that follow sequential
            drive naming, C:\, D:\ , etc. Convert the first drive to C:\
            """
            self.treeData.new_child(content="{}:\\".format(chr(partition_index+67)))
            for file_entry in self.db.select_root_files_from_filesystem_id_tsk_files(str(filesystem[0])):
                # Add filenames to the tree.
                self.treeData._children[partition_index].expanded = False
                self.treeData._children[partition_index].selectable = False

                #dir_type(3=dir,5=file, xx?), entry_number, filename, db_object_id
                item_type = {3:"d",5:"r"}
                if file_entry[5]=="." or file_entry[5]=="..":
                    pass
                else:
                    #If the format of the children being added is changed, h_expand_tree needs to be updated with how the 
                    #obj_id entry is parsed out. Should use the ntfs entries instead of the primary database key, but it's
                    #a stopgap to get some code working.
                    self.treeData._children[partition_index].new_child("{}\t{}-{}-{}:\t{}\t{}".format(item_type.get(file_entry[11]),
                        file_entry[6],file_entry[3],file_entry[4],file_entry[5],file_entry[0]))
                    for grandchildren in self.treeData._children[partition_index]._children:
                        grandchildren.expanded=False
                        grandchildren.selectable=False

        self.db.close()
        treeView = self.add(MyTreeView, name="Filesystem", values=self.treeData)

        treeView.add_handlers({curses.KEY_RIGHT : treeView.h_expand_tree,
                                curses.KEY_LEFT : treeView.h_collapse_tree})
    def query_down(self):
        pass

    def while_waiting(self):
        pass

    # Required for closing cleanly on OK press.
    def afterEditing(self):
        self.parentApp.setNextForm(None)  

    #Code that catches when we go into a directory
    #def check
    #        for entry in db.select_files_from_parent_tsk_files("6"):
    #        treeData.new_child(content=entry[6])

#View that forms are rendered into
class Flshell(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', DefaultForm, name='FLShell v2.0')


if __name__ == '__main__':
    application = Flshell().run()


