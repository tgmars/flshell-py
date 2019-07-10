import npyscreen
import dbhandler
import curses.ascii

#Default form delivered on startup.
class DefaultForm(npyscreen.Form):
  
    def h_enter_dir(self, _input):
        print("test")
        

    def create(self): 
        db = dbhandler.TSKDatabase()
        treeData = npyscreen.TreeData()
        
        for count, filesystem in enumerate(db.select_filesystems_from_tsk_fs_info()):
            """
            Let's make a horrible assumption in the interest of usability. 
            Limits correct displays to Windows boxes that follow sequential
            drive naming, C:\, D:\ , etc. Convert the first drive to C:\
            """
            currentTree = treeData.new_child(content="{}:\\".format(chr(count+67)))
            print(str(filesystem[0]))
            for file in enumerate(db.select_files_from_filesystem_id_tsk_files(str(filesystem[0]))):
                currentTree.new_child(file[0:5])
        
        treeView = self.add(npyscreen.MLTree, name="Filesystem", values=treeData)
        treeView.add_handlers({curses.KEY_RIGHT : self.h_enter_dir})

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

class CustomHandlers():
    def h_enter_dir(self):
        print("h_enter_dir")
