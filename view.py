import npyscreen
import dbhandler

#Default form delivered on startup.
class DefaultForm(npyscreen.Form):
    def create(self): 
        db = dbhandler.TSKDatabase()
        treeData = npyscreen.TreeData()
        for count, filesystem in enumerate(db.select_filesystems_from_tsk_fs_info()):
            """
            Let's make a horrible assumption in the interest of usability. 
            Limits correct displays to Windows boxes that follow sequential
            drive naming, C:\, D:\ , etc
            """
            treeData.new_child(content="{}:\\".format(chr(count+67)))

        treeView = self.add(npyscreen.MLTree, name="Filesystem", values=treeData)

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
