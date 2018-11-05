# V09 -WIP04

'''

Dialog 2.0
Undo y ReDo
disclaimer
arreglar el largo del texto extra.
Extra Tab:
Custom space - / _
Replace string with other string?
Soporte para hijos de objs seleccionados? / toda la jerarquia?
Solo evitar repeticiones de nombres.


'''

import c4d
from c4d import gui

# main dialog
class OptionsDialog(gui.GeDialog): # name dialog class
    # dialog IDS
    IDC_LABELNAME = 1000
    IDC_EDITNAME  = 1001
    IDC_BOOL_01   = 1010
    IDC_BOOL_02   = 1011
    IDC_BOOL_03   = 1012
    IDC_BOOL_04   = 1013
    IDC_STR_01    = 1020
    IDC_STR_02    = 1021
    IDC_LBL_01    = 1030
    IDC_LBL_02    = 1031
    IDC_LBL_03    = 1032
    IDC_LBL_04    = 1033
    IDC_NUM_01    = 1040
    IDC_GRP_01    = 1050
    IDC_GRP_02    = 1051
    IDC_GRP_03    = 1052
    IDC_GRP_04    = 1053
    IDC_TAB_01    = 2000
    IDC_TAB_02    = 2001

    def CreateLayout(self):
        self.SetTitle('Rename Selection')

        #self.TabGroupBegin(self.IDC_TAB_01, c4d.BFH_SCALEFIT, tabtype=c4d.TAB_TABS)
        #self.GroupBegin(self.IDC_GRP_04, c4d.BFH_SCALEFIT, 4, 1, inith = 0)
        # ---- separator ---- Main Rename options
        self.AddStaticText(self.IDC_LABELNAME, c4d.BFH_LEFT, name ='Set the new selection name:')
        self.AddEditText(self.IDC_EDITNAME, c4d.BFH_SCALEFIT)
        #self.GroupEnd()

        self.GroupEnd()

        # ---- separator ----
        self.AddSeparatorH(20, c4d.BFH_SCALEFIT)

        # ---- separator ---- Type selection options
        self.AddStaticText(self.IDC_LBL_04, c4d.BFH_LEFT, name = 'Change the name on this selected objects:')
        self.GroupBegin(self.IDC_GRP_01, c4d.BFH_SCALEFIT, 4, 1, inith = 0)
        self.GroupBorderSpace(10, 4, 10, 4)
        self.AddCheckbox(self.IDC_BOOL_01, c4d.BFH_SCALEFIT, 5, 5, name = 'Objects.')
        self.AddCheckbox(self.IDC_BOOL_02, c4d.BFH_SCALEFIT, 5, 5, name = 'Materials.')
        self.AddCheckbox(self.IDC_BOOL_03, c4d.BFH_SCALEFIT, 5, 5, name = 'Tags.')
        self.GroupEnd()

        # ---- separator ---- Preffix and Suffix options
        self.AddSeparatorH(20, c4d.BFH_SCALEFIT)
        self.GroupBegin(self.IDC_GRP_02, c4d.BFH_SCALEFIT, 4, 1, inith = 0)
        self.GroupBorderSpace(10, 4, 10, 4)
        self.AddStaticText(self.IDC_LBL_01, c4d.BFH_LEFT, name = 'Preffix:')
        self.AddEditText(self.IDC_STR_01, c4d.BFH_SCALEFIT)
        self.AddStaticText(self.IDC_LBL_02, c4d.BFH_LEFT, name = 'Suffix:')
        self.AddEditText(self.IDC_STR_02, c4d.BFH_SCALEFIT)
        self.GroupEnd()

        # ---- separator ---- Extra options
        self.AddSeparatorH(20, c4d.BFH_SCALEFIT)
        self.GroupBegin(self.IDC_GRP_03, c4d.BFH_SCALEFIT, 4, 1, inith = 0)
        self.GroupBorderSpace(10, 4, 10, 4)
        self.AddStaticText(self.IDC_LBL_03, c4d.BFH_LEFT, name = 'First Number:')
        self.AddEditNumber(self.IDC_NUM_01, c4d.BFH_SCALEFIT, initw=80, inith=0)
        self.GroupEnd()
        self.AddCheckbox(self.IDC_BOOL_04, c4d.BFH_SCALEFIT, 5, 5, name = 'Reverse selection order.')

        # set dialog default values
        self.SetString(self.IDC_EDITNAME, 'Write here')
        self.SetBool(self.IDC_BOOL_01, True)

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
        # warning gui msg dialog
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
        dlg = OptionsDialog() ; dlg.Open(c4d.DLG_TYPE_MODAL, defaultw=100, defaulth=50)
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

# UnDo ReDo templates
"""""
#start undo action
doc.StartUndo()

#add undo
doc.AddUndo(c4d.UNDOTYPE_CHANGE,item)

#end undo action
doc.EndUndo()

#do redo action
doc.DoRedo()"""
