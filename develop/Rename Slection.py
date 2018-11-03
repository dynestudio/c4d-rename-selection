# V08 -WIP01

# wip to do notes
# Undo y ReDo
# disclaimer

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
            gui.MessageDialog('Please write one name, you can leave empty to get only numbers too.')
        return True

def no_sel_dlg(): # no selection dialog
    gui.MessageDialog('Please select one or more objects / materials / tags.') ; return

def get_active_objs(): # get active objects from obj manager
    activeObjects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    if not activeObjects:
        return None
    return activeObjects

def get_active_mats(): # get active materials from material manager
    activeMaterials = doc.GetActiveMaterials()
    if not activeMaterials:
        return None
    return activeMaterials

def get_active_tags(): # get active tags from material manager
    activeTags = doc.GetActiveTags()
    if not activeTags:
        return None
    return activeTags

def apply_Renames(sel_list, sel_name_new): # apply the selected name + iterator number
    i = 0 # iterator number
    for item in sel_list:
        i += 1 # iterator re asignment
        item[c4d.ID_BASELIST_NAME] = sel_name_new + "0" + str(i) # asign new name

def sel_msgs(sel_objs, sel_mats, sel_tags):
    if sel_objs and sel_mats and sel_tags:
        gui.MessageDialog('Warning: ' + 'You have some object(s), material(s) and tag(s) selected.') ; return

    sel_names = ['object(s)', 'material(s)', 'tag(s)'] ; sel_ID = [] # main ID names

    # combination options
    if sel_objs and sel_mats:
        sel_ID = [sel_names[0], sel_names[1]]
    if sel_objs and sel_tags:
        sel_ID = [sel_names[0], sel_names[2]]
    if sel_mats and sel_tags:
        sel_ID = [sel_names[1], sel_names[2]]

    if not sel_ID:
        return
    else:
        gui.MessageDialog('Warning: ' + 'You have a ' + sel_ID[0] + ' and a ' + sel_ID[1] + 'selected.')

def main():
    # key input event
    bc = c4d.BaseContainer()
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD,c4d.BFM_INPUT_CHANNEL,bc):
        if  bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QSHIFT:
            print "shift input"
            key = 1
        elif  bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: 
            print "alt input"
            key = 2
        elif  bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QCTRL: 
            print "ctrl input"
            key = 3
        else:
            key = 0

    # get active selection 
    sel_objs = get_active_objs()
    sel_mats = get_active_mats()
    sel_tags = get_active_tags()
    # execute different messages based on selected items
    sel_msgs(sel_objs, sel_mats, sel_tags)
    
    if not sel_objs and not sel_mats and not sel_tags: # return if both selection list are None
        no_sel_dlg() ; return

    # main name definitionns
    if  key == 1:
        sel_name_new = ""
    elif  key == 2:
        sel_name_new = "_"
    elif  key == 3:
        sel_name_new = "-"
    else:
        # Open the options dialog to let users choose their options.
        dlg = OptionsDialog() ; dlg.Open(c4d.DLG_TYPE_MODAL, defaultw=300, defaulth=50)
        if not dlg.ok:
            return
        sel_name_new = dlg.findGName # new selection nanme

        # automatically add a separator in the name
        last_character = ["_", "-", " ", "*", ".", "+", "/" ]
        if sel_name_new:
            if not sel_name_new[-1] in last_character:
                sel_name_new = sel_name_new + "_"

    # set names to active selection
    if sel_objs:
        apply_Renames(sel_objs, sel_name_new)
    if sel_mats:
        apply_Renames(sel_mats, sel_name_new)
    if sel_tags:
        apply_Renames(sel_tags, sel_name_new)

    # update the scene
    c4d.EventAdd()
    if key == 0:
        gui.MessageDialog('Rename finished.')
    
if __name__=='__main__':
    main()


"""""
#start undo action
doc.StartUndo()

#add undo
doc.AddUndo(c4d.UNDOTYPE_CHANGE,item)

#end undo action
doc.EndUndo()

#do redo action
doc.DoRedo()"""