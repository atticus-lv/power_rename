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
            obj.SetName(new_name)

        return True


class BatchRename(c4d.plugins.CommandData):

    def Execute(self, doc):
        dialog = BatchDialog()
        dialog._doc = doc
        dialog.Open(c4d.DLG_TYPE_MODAL_RESIZEABLE, 132456, -1, -1, 200, 100)
        return True


STR_PREFIX = 10
STR_SUFFIX = 20
STR_REPLACE_OLD = 30
STR_REPLACE_NEW = 40
STR_SET = 50

BTN_PREFIX = 100
BTN_SUFFIX = 200
BTN_REPLACE = 300
BTN_SET = 400

CHECKBOX_SET = 500


class BatchDialog(gui.GeDialog):
    # DialogLayoutSettings

    _doc = None

    def CreateLayout(self):
        self.SetTitle('Batch Rename')

        self.GroupBegin(10000, c4d.BFH_SCALEFIT, 1, title='Method')

        self.TabGroupBegin(5000, c4d.BFH_SCALEFIT, tabtype=c4d.TAB_CYCLE)

        self.GroupBegin(1000, c4d.BFH_SCALEFIT, 1, title='Set')
        self.AddEditText(STR_SET, c4d.BFH_SCALEFIT, 100, 0)
        self.AddCheckbox(CHECKBOX_SET, c4d.BFH_SCALEFIT, 0, 0, 'Add Index as Suffix')
        self.AddButton(BTN_SET, c4d.BFH_SCALEFIT, 0, 0, 'Execute')
        self.GroupEnd()

        # TAB-1
        self.GroupBegin(1001, c4d.BFH_SCALEFIT, 1, title='Prefix')
        self.AddEditText(STR_PREFIX, c4d.BFH_SCALEFIT, 100, 0)
        self.AddButton(BTN_PREFIX, c4d.BFH_SCALEFIT, 0, 0, 'Execute')
        self.GroupEnd()

        # TAB-2
        self.GroupBegin(1002, c4d.BFH_SCALEFIT, 1, title='Suffix')
        self.AddEditText(STR_SUFFIX, c4d.BFH_SCALEFIT, 100, 0)
        self.AddButton(BTN_SUFFIX, c4d.BFH_SCALEFIT, 0, 0, 'Execute')
        self.GroupEnd()

        # TAB-3
        self.GroupBegin(1003, c4d.BFH_SCALEFIT, 1, title='Replace')
        self.AddEditText(STR_REPLACE_OLD, c4d.BFH_SCALEFIT, 100, 0)
        self.AddStaticText(4000, c4d.BFH_CENTER, 0, 0, name='↓')
        self.AddEditText(STR_REPLACE_NEW, c4d.BFH_SCALEFIT, 100, 0)
        self.AddButton(BTN_REPLACE, c4d.BFH_SCALEFIT, 0, 0, 'Execute')
        self.GroupEnd()

        self.GroupEnd()  # TabGroupEnd

    def Command(self, id, msg):
        self.doc = c4d.documents.GetActiveDocument()
        selected_objects = self.doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
        if len(selected_objects) == 0: return

        if id == 5000:
            pass

        if id == BTN_PREFIX:
            value = self.GetString(STR_PREFIX)
            self.add_prefix(selected_objects, value)

            self.Close()


        elif id == BTN_SUFFIX:
            value = self.GetString(STR_SUFFIX)
            self.add_suffix(selected_objects, value)

            self.Close()


        elif id == BTN_REPLACE:
            value1 = self.GetString(STR_REPLACE_OLD)
            value2 = self.GetString(STR_REPLACE_NEW)
            self.replace_string(selected_objects, value1, value2)

            self.Close()


        elif id == BTN_SET:
            add_index = self.GetInt32(CHECKBOX_SET)
            value = self.GetString(STR_SET)
            self.set_name(selected_objects, value, add_index=add_index)

            self.Close()

        c4d.EventAdd()

        return True

        # custom function

    def set_name(self, objs, name, add_index=False):
        for i, obj in enumerate(objs):
            obj.SetName(name if not add_index else name + '.' + str(i))
            self.doc.AddUndo(c4d.UNDOTYPE_CHANGE_SMALL, obj)

    def add_prefix(self, objs, prefix):
        for i, obj in enumerate(objs):
            obj.SetName(prefix + obj.GetName())
            self.doc.AddUndo(c4d.UNDOTYPE_CHANGE_SMALL, obj)

    def add_suffix(self, objs, suffix):
        for i, obj in enumerate(objs):
            obj.SetName(obj.GetName(), suffix)
            self.doc.AddUndo(c4d.UNDOTYPE_CHANGE_SMALL, obj)

    def replace_string(self, objs, old, new):
        for i, obj in enumerate(objs):
            old_name = obj.GetName()
            if old in old_name:
                new_name = old_name.replace(old, new)
                obj.SetName(new_name)
                self.doc.AddUndo(c4d.UNDOTYPE_CHANGE_SMALL, obj)


SIMPLE_RENAME_ID = 1058816
BATCH_RENAME_ID = 1058849


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
    c4d.plugins.RegisterCommandPlugin(id=SIMPLE_RENAME_ID,
                                      str="Power Rename",
                                      info=0,
                                      help="Viewport object rename",
                                      dat=SimpleRename(),
                                      icon=icon)
    c4d.plugins.RegisterCommandPlugin(id=BATCH_RENAME_ID,
                                      str="Power Batch Rename",
                                      info=0,
                                      help="Viewport multiple object rename",
                                      dat=BatchRename(),
                                      icon=icon)
