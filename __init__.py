import bpy
import os

addon_keymaps = []

bl_info = {
    "name": "proceditor",
    "blender": (2, 93, 0),
    "category": "Sequencer"
}

from .operators.texter import PROCEDITOR_OT_add_text
from .operators.compiler import PROCEDITOR_OT_compiler

def register():
    classes = (PROCEDITOR_OT_add_text, PROCEDITOR_OT_compiler)
    for i in classes:
        bpy.utils.register_class(i)
    wm = bpy.context.window_manager
    # Note that in background mode (no GUI available), keyconfigs are not available either,
    # so we have to check this to avoid nasty errors in background case.
    kc = wm.keyconfigs.addon

    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='SequencerCommon', space_type='SEQUENCE_EDITOR')

        kmi = km.keymap_items.new(PROCEDITOR_OT_compiler.bl_idname, 'C', 'PRESS', ctrl=True, shift=True)
        addon_keymaps.append((km, kmi))
        kmi = km.keymap_items.new(PROCEDITOR_OT_add_text.bl_idname, 'A', 'PRESS', ctrl=True, shift=True)
        addon_keymaps.append((km, kmi))


def unregister():
    for i in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.utils.unregister_class(PROCEDITOR_OT_add_text)
    bpy.utils.unregister_class(PROCEDITOR_OT_compiler)

if __name__ == "main":
    register()
