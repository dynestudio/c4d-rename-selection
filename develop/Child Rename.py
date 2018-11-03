import c4d
from c4d import gui

class OptionsDialog(gui.GeDialog):

    IDC_LABELNAME = 1000
    IDC_EDITNAME = 1001

    def CreateLayout(self):

        self.SetTitle('Rename Selection')

        self.AddStaticText(self.IDC_LABELNAME, c4d.BFH_LEFT, name='Set the new selection name:') 
        self.AddEditText(self.IDC_EDITNAME, c4d.BFH_SCALEFIT)
        self.SetString(self.IDC_EDITNAME, 'Write you selection new name')

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
            gui.MessageDialog('Please write a name, if you want you can leave empty to get only numers too.')

        return True

def no_sel_dlg():
    gui.MessageDialog('Please select one or more objects / materials.')
    return 

def get_active_objs():
    # get active objects
    activeObjects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    if not activeObjects:
        no_sel_dlg()
        return None

    return activeObjects

def get_active_mats():
    # get active materials
    activeMaterials = doc.GetActiveMaterials()
    if not activeMaterials:
        no_sel_dlg()
        return None

    return activeMaterials

def main():
    # get active selection 
    sel_objs = get_active_objs()
    sel_type = 0

    if sel_objs == None:
        sel_objs = get_active_mats()
        sel_type = 1

        if sel_objs == None:
            no_sel_dlg()
            return

    # key input event
    bc = c4d.BaseContainer()
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD,c4d.BFM_INPUT_CHANNEL,bc):
        if  bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QSHIFT:
            print "shift input"

        elif  bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: 
            print "alt input"

        elif  bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QCTRL: 
            print "ctrl input"

        else:
            None

    # Open the options dialog to let users choose their options.
    dlg = OptionsDialog()
    dlg.Open(c4d.DLG_TYPE_MODAL, defaultw=300, defaulth=50)
    if not dlg.ok:
        return

    # new selection nanme
    sel_name_new = dlg.findGName


    # wip to do:
    # que reconozca el final del string para a;adir un _ o - o espacio en caso que no haya nada en el string del dialog
    # sirva tambien para materiales
    # BaseDocument.GetActiveMaterials

    i = 0 # number iterator

    for obj in sel_objs:
        i += 1
        obj[c4d.ID_BASELIST_NAME] = sel_name_new + "0" + str(i)

    c4d.EventAdd()
    
if __name__=='__main__':
    main()
