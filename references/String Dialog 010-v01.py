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
    # Open the options dialog to let users choose their options.
    dlg = OptionsDialog()
    dlg.Open(c4d.DLG_TYPE_MODAL, defaultw=300, defaulth=50)
    if not dlg.ok:
        return

    dialog = dlg.findGName

    print dialog

if __name__=='__main__':
 main()