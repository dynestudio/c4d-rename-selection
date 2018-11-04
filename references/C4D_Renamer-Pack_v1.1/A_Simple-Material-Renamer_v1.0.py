#www.lasseclausen.com/lab/
#Use at your own risk
#Last-Modified: 16/11/2016
"""
Name-US:A_Simple-Material-Renamer_v1.0
Description-US:Renames selected Materials.

The Script works best, if added to a shortcut.
Use Shift+Y for example.

------------------------ CHANGELOG ---------------------------
v1.0:
- New Layout for Renamer + New Numbering System
- Replace/With Feature in Dialog
- Added Objects-Name functionality
--------------------------------------------------------------

"""
import c4d
from c4d import documents, gui, bitmaps

def GetModifiers():
    # Check all keys
    bc = c4d.BaseContainer()
    ctrl, shift, alt = False, False, False
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.BFM_INPUT_CHANNEL, bc):
        if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QSHIFT:
            shift = True
        if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QCTRL:
            ctrl = True
        if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT:
            alt = True

    return ctrl, shift, alt

# Unique id numbers for each of the GUI elements:
LBL_INFO1 = 1001
GROUP_TEXT = 10000
GROUP_NUMBERING = 20000
GROUP_PREFIX = 30000
GROUP_REPLACE = 40000
GROUP_MATCHCASE = 45000
PREFIX = 25002
SUFFIX = 25004
REPLACE = 25003
WITH = 25005
MATCH_CASE = 25007
NEWNAME= 10001
CHK_APPEND_TO_EXISTING = 10003
CHK_BEFORE_EXISTING = 10004
START_NUMBER = 10005
LEADING_ZERO = 10006
LEADING_ZERO_1 = 100
LEADING_ZERO_01 = 101
LEADING_ZERO_001 = 102
LEADING_ZERO_0001 = 103
GROUP_OPTIONS = 50000
BTN_OK = 50001
BTN_CANCEL = 50002
     
class OptionsDialog(gui.GeDialog):
    def CreateLayout(self):
        self.SetTitle('A_Simple-Material-Renamer')
        
        # DIALOG
        self.GroupBegin(GROUP_TEXT, c4d.BFH_SCALEFIT, 1, 1, inith=0)
        self.GroupBorderSpace(10, 0, 10, 0)
        self.AddStaticText(LBL_INFO1, c4d.BFH_CENTER, name='New Name:') 
        self.AddEditText(NEWNAME, c4d.BFH_SCALEFIT, initw=150)
        self.SetString(NEWNAME, '')  
        self.GroupEnd()
        
        self.AddSeparatorH(c4d.BFH_CENTER)  
        
        # NUMBERING
        self.GroupBegin(GROUP_NUMBERING, c4d.BFH_SCALEFIT, 5, 1, inith=0)
        self.GroupBorderSpace(10, 0, 10, 0)
        self.AddComboBox(LEADING_ZERO, c4d.BFH_LEFT, initw=40)
        self.AddChild(LEADING_ZERO, LEADING_ZERO_1, "#1")
        self.AddChild(LEADING_ZERO, LEADING_ZERO_01, "#01")
        self.AddChild(LEADING_ZERO, LEADING_ZERO_001, "#001")
        self.AddChild(LEADING_ZERO, LEADING_ZERO_0001, "#0001")
        self.SetLong(10006, LEADING_ZERO_1)
        
        self.AddStaticText(LBL_INFO1, c4d.BFH_LEFT, name='Start:')
        self.AddEditText(START_NUMBER, c4d.BFH_SCALEFIT, initw=20)
        self.SetString(START_NUMBER, '1')
              
        self.AddCheckbox(CHK_BEFORE_EXISTING, c4d.BFH_RIGHT, initw=0, inith=0, name='##_Name')
        self.AddCheckbox(CHK_APPEND_TO_EXISTING, c4d.BFH_RIGHT, initw=0, inith=0, name='Name_##')
        self.SetBool(CHK_BEFORE_EXISTING, False)
        self.SetBool(CHK_APPEND_TO_EXISTING, False)
        self.GroupEnd()
        
        self.AddSeparatorH(c4d.BFH_CENTER)   
        
        # PREFIX / SUFFIX
        self.GroupBegin(GROUP_PREFIX, c4d.BFH_SCALEFIT, 4, 1, inith=0)
        self.GroupBorderSpace(10, 0, 10, 0)
        self.AddStaticText(LBL_INFO1, c4d.BFH_LEFT, name='Prefix: . . . .') 
        self.AddEditText(PREFIX, c4d.BFH_SCALEFIT, initw=85)
        self.AddStaticText(LBL_INFO1, c4d.BFH_LEFT, name='Suffix:') 
        self.AddEditText(SUFFIX, c4d.BFH_SCALEFIT, initw=85)
        self.GroupEnd()

        self.AddSeparatorH(c4d.BFH_CENTER)   

        # REPLACE / WITH
        self.GroupBegin(GROUP_REPLACE, c4d.BFH_SCALEFIT, 4, 1, inith=0)
        self.GroupBorderSpace(10, 0, 10, 0)
        self.AddStaticText(LBL_INFO1, c4d.BFH_LEFT, name='Replace: . .') 
        self.AddEditText(REPLACE, c4d.BFH_SCALEFIT, initw=85)
        self.AddStaticText(LBL_INFO1, c4d.BFH_LEFT, name='With:') 
        self.AddEditText(WITH, c4d.BFH_SCALEFIT, initw=85)
        self.GroupEnd()
        
        # OK and CANCEL button:
        self.GroupBegin(GROUP_OPTIONS, c4d.BFH_CENTER, 2, 1)
        self.GroupBorderSpace(0, 10, 0, 10)
        self.AddButton(BTN_CANCEL, c4d.BFH_SCALE, name='Cancel', inith=15)
        self.AddButton(BTN_OK, c4d.BFH_SCALE, name='OK', inith=15)
        
        self.GroupEnd()
        self.ok = False
        return True
    
    # React to user's input:
    def Command(self, id, msg):
        bc=c4d.BaseContainer()
        c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ESC, bc)
        if bc[c4d.BFM_INPUT_VALUE]:
            self.Close()
        if id==BTN_CANCEL:
          self.Close()
        elif id==BTN_OK:
          self.ok = True
          self.option_prefix=self.GetString(PREFIX)
          self.option_suffix=self.GetString(SUFFIX)
          self.option_newname=self.GetString(NEWNAME)
          if self.GetLong(10006)==100:
            self.option_zero = ''
          elif self.GetLong(10006)==101:
            self.option_zero = '0'
          elif self.GetLong(10006)==102:
            self.option_zero = '00'
          elif self.GetLong(10006)==103:
            self.option_zero = '000'
          self.option_startnumber=self.GetString(START_NUMBER)
          self.option_before=self.GetBool(CHK_BEFORE_EXISTING)
          self.option_append=self.GetBool(CHK_APPEND_TO_EXISTING)
          self.option_replace=self.GetString(REPLACE)
          self.option_with=self.GetString(WITH)
          self.option_matchcase=self.GetBool(MATCH_CASE)
          self.Close()

        c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ENTER, bc)
        if bc[c4d.BFM_INPUT_VALUE]:
          self.ok = True
          self.option_prefix=self.GetString(PREFIX)
          self.option_suffix=self.GetString(SUFFIX)
          self.option_newname=self.GetString(NEWNAME)
          if self.GetLong(10006)==100:
            self.option_zero = ''
          elif self.GetLong(10006)==101:
            self.option_zero = '0'
          elif self.GetLong(10006)==102:
            self.option_zero = '00'
          elif self.GetLong(10006)==103:
            self.option_zero = '000'
          self.option_zero=self.GetString(LEADING_ZERO)
          self.option_startnumber=self.GetString(START_NUMBER)
          self.option_before=self.GetBool(CHK_BEFORE_EXISTING)
          self.option_append=self.GetBool(CHK_APPEND_TO_EXISTING)
          self.option_replace=self.GetString(REPLACE)
          self.option_with=self.GetString(WITH)
          self.option_matchcase=self.GetBool(MATCH_CASE)
          self.Close()
        
        return True

def Numeric(sel, n):
    doc.StartUndo()
    for x in sel: 
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, x)
        x.SetName(n)
        n += 1
    doc.EndUndo()
    c4d.EventAdd()

def CurrentName(sel, n):
    doc.StartUndo()
    for x in sel[:9]: 
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, x)
        name=x.GetName()
        x.SetName(name+'_0'+str(n))
        n += 1   
    for x in sel[9:]: 
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, x)
        name=x.GetName()
        x.SetName(name+'_'+str(n))
        n += 1
    doc.EndUndo()      
    c4d.EventAdd()
    
def TextureTags(obj, children, sel):
    if not obj: return
    
    for x in sel:
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, x)
        for tag in obj.GetTags():
            if tag[c4d.TEXTURETAG_MATERIAL]==x:
                x.SetName(obj.GetName())
    
    TextureTags(obj.GetNext(), children, sel)
    if children:
      TextureTags(obj.GetDown(), children, sel)    
      
def MaterialtoObjectName(obj, children, sel):
    if not obj: return
    
    for x in sel:
        for tag in obj.GetTags():
            if tag[c4d.TEXTURETAG_MATERIAL]==x:
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
                obj.SetName(x.GetName())
    
    MaterialtoObjectName(obj.GetNext(), children, sel)
    if children:
      MaterialtoObjectName(obj.GetDown(), children, sel)    

def Reset(sel):
    doc.StartUndo()
    for x in sel: 
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, x)
        typename=x.GetTypeName()
        x.SetName(typename)
    doc.EndUndo()
    c4d.EventAdd()

def Dialog(sel):
    # Open the options dialogue to let users choose their options.
    doc.StartUndo()
    dlg = OptionsDialog()
    dlg.Open(c4d.DLG_TYPE_MODAL, defaultw=250, defaulth=50)
    if not dlg.ok:
        return

    nameinput=str(dlg.option_newname)
    prefix=str(dlg.option_prefix)
    suffix=str(dlg.option_suffix)
    zero=str(dlg.option_zero)
    startnumber=int(dlg.option_startnumber)
    re_replace=str(dlg.option_replace)
    re_with=str(dlg.option_with)
    
    for x in sel:
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, x)
        name=x.GetName()
        x.SetName(prefix+name+suffix)
        if dlg.option_newname!='':
            x.SetName(prefix+nameinput+suffix)

        if dlg.option_replace!='':
            new_name=x.GetName().replace(re_replace, re_with)
            x.SetName(prefix+new_name+suffix)

        if dlg.option_append==True:
            name=x.GetName()
            x.SetName(name + '_' + zero + str(startnumber))
            startnumber += 1
            
        if dlg.option_before==True:
            name=x.GetName()
            x.SetName(zero + str(startnumber) + '_' + name)
            startnumber += 1

    doc.EndUndo()
    c4d.EventAdd()
                
def main():
    first=doc.GetFirstObject()
    n=1
    sel=doc.GetActiveMaterials()
    bc=c4d.BaseContainer()
    
    if not sel:
        return

    #Icons
    icon = "&i"+str(c4d.IDM_PASTE)+"&"
    ico_renamer = "&i1019952&"
    materialtoobject = "&i"+str(c4d.OUTLINEMAT_LINE_MOTION_FADE_THICKNESS_STRENGTH)+"&"
    objecttomaterial = "&i"+str(c4d.IDM_SELECTNONE)+"&"
    objectsname = "&i"+str(c4d.PRIM_OILTANK_RADIUS)+"&"
    reset = "&i"+str(c4d.RESOURCEIMAGE_CLEARSELECTION)+"&"
    
    ########### Menu ###########
    entries = c4d.BaseContainer()
    
    entries.SetString(10, icon + ":::. Open Dialog .:::")
    entries.SetString(11, ico_renamer + "#, #, # ")
    entries.SetString(12, ico_renamer + "CurrentName_##")
    entries.SetString(13, materialtoobject + "Material --> Object")
    entries.SetString(14, objecttomaterial + "Object <-- Material")
    entries.SetString(15, reset + "Reset to Default")
    
    result = gui.ShowPopupDialog(cd=None, bc=entries, x=c4d.MOUSEPOS, y=c4d.MOUSEPOS, flags = c4d.POPUP_RIGHT)
    if result == 10:
        Dialog(sel)
    elif result == 11:
        Numeric(sel, n)
    elif result == 12:
        CurrentName(sel, n)
    elif result == 13:
        doc.StartUndo()
        TextureTags(first, True, sel)
        doc.EndUndo()
        c4d.EventAdd()
    elif result == 14:
        doc.StartUndo()    
        MaterialtoObjectName(first, True, sel)
        doc.EndUndo()
        c4d.EventAdd()    
    elif result == 15:
        Reset(sel)
    else:
        return

if __name__=='__main__':
    main()