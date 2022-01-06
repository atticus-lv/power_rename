# log
# v0.1 simple rename

import c4d
from c4d import plugins, gui

class SimpleRename(c4d.plugins.CommandData):

    def Execute(self, doc):
        selected_objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
        if len(selected_objects) == 0: return

        obj_name = selected_objects[0].GetName()
        title = f'[{obj_name}]' if len(selected_objects) == 1 else f"[{len(selected_objects)} Elements]"
        new_name = gui.InputDialog("Rename" + " " + title, obj_name)

        for i, obj in enumerate(selected_objects):
            obj.SetName(new_name if i == 0 else new_name + str(i))

        c4d.EventAdd()

        return True


PLUGIN_ID = 1058816


def register_icon():
    import os
    # Retrieves the icon path
    directory, _ = os.path.split(__file__)
    icon = os.path.join(directory, "res", "rename_c.tif")
    bitmap = c4d.bitmaps.BaseBitmap()
    # Init the BaseBitmap with the icon
    if bitmap.InitWith(icon)[0] != c4d.IMAGERESULT_OK: raise MemoryError("Failed to initialize the BaseBitmap.")

    return bitmap


if __name__ == '__main__':
    icon = register_icon()
    c4d.plugins.RegisterCommandPlugin(id=PLUGIN_ID,
                                      str="Power Rename",
                                      info=0,
                                      help="Viewport multiple object rename",
                                      dat=SimpleRename(),
                                      icon=icon)
