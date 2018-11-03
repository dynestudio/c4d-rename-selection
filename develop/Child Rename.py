import c4d
from c4d import gui

class OptionsDialog(gui.GeDialog):

    IDC_LABELNAME = 1000
    IDC_EDITNAME = 1001

    def CreateLayout(self):

        self.SetTitle('Crypto User AOV')

        self.AddStaticText(self.IDC_LABELNAME, c4d.BFH_LEFT, name='Set User Data Name:') 
        self.AddEditText(self.IDC_EDITNAME, c4d.BFH_SCALEFIT)
        self.SetString(self.IDC_EDITNAME, 'Write Crypto User Data AOV')

        # Ok/Cancel buttons
        self.AddDlgGroup(c4d.DLG_OK|c4d.DLG_CANCEL)
        self.ok = False
        return True

    def Command(self, id, msg):

        if id == c4d.IDC_OK:
            self.ok = True
            self.findGName = self.GetString(self.IDC_EDITNAME)
            self.Close()

        elif id == c4d.IDC_CANCEL:
            self.Close()
            gui.MessageDialog('Please select a user Cryptomatte input user data.')

        return True

def main():

    # get Active Objects
    activeObjects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    if not activeObjects:
        gui.MessageDialog('Please select one or more objects.')
        return

    # Open the options dialog to let users choose their options.
    dlg = OptionsDialog()
    dlg.Open(c4d.DLG_TYPE_MODAL, defaultw=300, defaulth=50)
    if not dlg.ok:
        return

    dialog = dlg.findGName

    i = 0

    for obj in activeObjects:
        i += 1
        obj[c4d.ID_BASELIST_NAME] = dialog + "0" + str(i)

    c4d.EventAdd()
    
if __name__=='__main__':
    main()
