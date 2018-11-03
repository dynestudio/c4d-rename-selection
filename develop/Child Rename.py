import c4d
from c4d import gui

class OptionsDialog(gui.GeDialog): # name dialog class

    IDC_LABELNAME = 1000
    IDC_EDITNAME = 1001

    def CreateLayout(self):

        self.SetTitle('Rename Selection')

        self.AddStaticText(self.IDC_LABELNAME, c4d.BFH_LEFT, name='Set the new selection name:') 
        self.AddEditText(self.IDC_EDITNAME, c4d.BFH_SCALEFIT)
        self.SetString(self.IDC_EDITNAME, 'Write here')

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

def no_sel_dlg(): # no selection dialog
    gui.MessageDialog('Please select one or more objects / materials / tags.') ; return 

def get_active_objs(): # get active objects from obj manager
    activeObjects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    if not activeObjects:
        no_sel_dlg() ; return None
    return activeObjects

def get_active_mats(): # get active materials from material manager
    activeMaterials = doc.GetActiveMaterials()
    if not activeMaterials:
        no_sel_dlg() ; return None
    return activeMaterials

def get_active_tags(): # get active tags from material manager
    activeTags = doc.GetActiveTags()
        if not activeMaterials:
            no_sel_dlg() ; return None
    return activeTags

def main():
    # get active selection 
    sel_objs = get_active_objs()
    sel_mats = get_active_mats()
    sel_tags = get_active_tags()

    if not sel_objs and not sel_mats and not sel_tags: # return if both selection list are None
        no_sel_dlg() ; return

    # key input event
    bc = c4d.BaseContainer()
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD,c4d.BFM_INPUT_CHANNEL,bc):
        if  bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QSHIFT:
            print "shift input"
            sel_name_new = ""

        elif  bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: 
            print "alt input"
            sel_name_new = "_"

        elif  bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QCTRL: 
            print "ctrl input"
            sel_name_new = "-"

        else:
            # Open the options dialog to let users choose their options.
            dlg = OptionsDialog()
            dlg.Open(c4d.DLG_TYPE_MODAL, defaultw=300, defaulth=50)
            if not dlg.ok:
                return
            sel_name_new = dlg.findGName # new selection nanme

            # automatically add a separator in the name
            last_character = ["_", "-", " ", "*", ".", "+", "/" ]
            if not sel_name_new[-1] in last_character:
                sel_name_new = sel_name_new + "_"

    i = 0 # iterator number

    # set names to selected objects
    if sel_objs:
        for obj in sel_objs:
            i += 1 # iterator re asignment
            obj[c4d.ID_BASELIST_NAME] = sel_name_new + "0" + str(i) # asign new name

    if sel_mats:
        for obj in sel_objs:
            i += 1 # iterator re asignment
            obj[c4d.ID_BASELIST_NAME] = sel_name_new + "0" + str(i) # asign new name

    # update the scene
    c4d.EventAdd()
    
if __name__=='__main__':
    main()