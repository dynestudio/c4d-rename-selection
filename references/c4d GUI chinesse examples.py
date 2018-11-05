'''
スクリプトでダイアログのタブのテスト
'''
import c4d
from c4d import gui


#ダイアログの設定
class MyDialogs(gui.GeDialog):
    #ダイアログレイアウトの設定
    def CreateLayout(self):
        self.SetTitle('TestScript')

        #ウィジェット等の設定
        self.GroupBegin(50000, c4d.BFH_SCALEFIT, 1, title = 'test')
        self.GroupBorder(c4d.BORDER_GROUP_IN)
        self.GroupBorderSpace(20, 5, 20, 5)

        #ここへ
        #TabGroup--------------------------------------------------------
        self.GroupBegin(10000, c4d.BFH_SCALEFIT, 1, title = 'TAB_TABS')
        self.GroupBorder(c4d.BORDER_GROUP_IN)
        self.GroupBorderSpace(20, 5, 20, 5)

        self.TabGroupBegin(100, c4d.BFH_SCALEFIT, tabtype = c4d.TAB_TABS)

        #TAB-1
        self.GroupBegin(1000, c4d.BFH_SCALEFIT, 1, title = 'tab-1')
        self.AddCheckbox(10, c4d.BFH_SCALEFIT, 0, 0, 'Checkbox')
        self.GroupEnd()

        #TAB-2
        self.GroupBegin(1001, c4d.BFH_SCALEFIT, 1, title = 'tab-2')
        self.AddButton(11, c4d.BFH_SCALEFIT, 0, 0, 'Button')
        self.GroupEnd()

        #TAB-3
        self.GroupBegin(1002, c4d.BFH_SCALEFIT, 1, title = 'tab-3')
        self.AddEditText(12, c4d.BFH_SCALEFIT, 100, 0)
        self.GroupEnd()

        self.GroupEnd() #TabGroupEnd

        self.GroupEnd()

        #TabGroup--------------------------------------------------------
        self.GroupBegin(20000, c4d.BFH_SCALEFIT, 1, title = 'TAB_NOSELECT')
        self.GroupBorder(c4d.BORDER_GROUP_IN)
        self.GroupBorderSpace(20, 5, 20, 5)

        self.TabGroupBegin(200, c4d.BFH_SCALEFIT, tabtype = c4d.TAB_NOSELECT)

        #TAB-1
        self.GroupBegin(2000, c4d.BFH_SCALEFIT, 1, title = 'tab-1')
        self.AddCheckbox(20, c4d.BFH_SCALEFIT, 0, 0, 'Checkbox')
        self.GroupEnd()

        #TAB-2
        self.GroupBegin(2001, c4d.BFH_SCALEFIT, 1, title = 'tab-2')
        self.AddButton(21, c4d.BFH_SCALEFIT, 0, 0, 'Button')
        self.GroupEnd()

        #TAB-3
        self.GroupBegin(2002, c4d.BFH_SCALEFIT, 1, title = 'tab-3')
        self.AddEditText(22, c4d.BFH_SCALEFIT, 100, 0)
        self.GroupEnd()

        self.GroupEnd() #TabGroupEnd

        self.GroupEnd()

        #TabGroup--------------------------------------------------------
        self.GroupBegin(30000, c4d.BFH_SCALEFIT, 1, title = 'TAB_CYCLE')
        self.GroupBorder(c4d.BORDER_GROUP_IN)
        self.GroupBorderSpace(20, 5, 20, 5)

        self.TabGroupBegin(300, c4d.BFH_SCALEFIT, tabtype = c4d.TAB_CYCLE)

        #TAB-1
        self.GroupBegin(3000, c4d.BFH_SCALEFIT, 1, title = 'tab-1')
        self.AddCheckbox(30, c4d.BFH_SCALEFIT, 0, 0, 'Checkbox')
        self.GroupEnd()

        #TAB-2
        self.GroupBegin(3001, c4d.BFH_SCALEFIT, 1, title = 'tab-2')
        self.AddButton(31, c4d.BFH_SCALEFIT, 0, 0, 'Button')
        self.GroupEnd()

        #TAB-3
        self.GroupBegin(3002, c4d.BFH_SCALEFIT, 1, title = 'tab-3')
        self.AddEditText(32, c4d.BFH_SCALEFIT, 100, 0)
        self.GroupEnd()

        self.GroupEnd() #TabGroupEnd

        self.GroupEnd()

        #TabGroup--------------------------------------------------------
        self.GroupBegin(40000, c4d.BFH_SCALEFIT, 1, title = 'TAB_RADIO')
        self.GroupBorder(c4d.BORDER_GROUP_IN)
        self.GroupBorderSpace(20, 5, 20, 5)

        self.TabGroupBegin(400, c4d.BFH_SCALEFIT, tabtype = c4d.TAB_RADIO)

        #TAB-1
        self.GroupBegin(4000, c4d.BFH_SCALEFIT, 1, title = 'tab-1')
        self.AddCheckbox(40, c4d.BFH_SCALEFIT, 0, 0, 'Checkbox')
        self.GroupEnd()

        #TAB-2
        self.GroupBegin(4001, c4d.BFH_SCALEFIT, 1, title = 'tab-2')
        self.AddButton(41, c4d.BFH_SCALEFIT, 0, 0, 'Button')
        self.GroupEnd()

        #TAB-3
        self.GroupBegin(4002, c4d.BFH_SCALEFIT, 1, title = 'tab-3')
        self.AddEditText(42, c4d.BFH_SCALEFIT, 100, 0)
        self.GroupEnd()

        self.GroupEnd() #TabGroupEnd

        self.GroupEnd()

        #---------------------------------------------------------------
        self.GroupEnd()

        #OK/キャンセルボタンの設置---------------------------------------------
        self.AddDlgGroup(c4d.DLG_OK|c4d.DLG_CANCEL)
        return True


def main():
    dlg = MyDialogs()
    dlg.Open(c4d.DLG_TYPE_MODAL)


if __name__=='__main__':
    main()
    c4d.EventAdd()
