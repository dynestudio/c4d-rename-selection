import c4d
from c4d import gui

def main():

    # get Active Objects
    activeObjects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    if not activeObjects:
        gui.MessageDialog('Please select one or more objects.')
        return

    i = 0

    for obj in activeObjects:
        i += 1
        obj[c4d.ID_BASELIST_NAME] = "0" + str(i)

    c4d.EventAdd()
    
if __name__=='__main__':
    main()
