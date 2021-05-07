import bpy
import re


def getsequences():
    return list(bpy.context.scene.sequence_editor.sequences_all)


def getnewsequence(previoussequences):
    return list(set(getsequences()) - set(previoussequences))[0]


def replacetemplate(clip: bpy.types.TextSequence, templatename: str):
    sequences = getsequences()
    templatematch = 'template:' + templatename
    for i in sequences:
        if i.name == templatematch:
            templateclip = i
            break
    if not templateclip:
        return NULL
    bpy.ops.sequencer.select(deselect_all=True)
    templateclip.select = True
    bpy.ops.sequencer.duplicate_move(SEQUENCER_OT_duplicate={},
                                     TRANSFORM_OT_seq_slide={"value": (0, 1), "snap": False, "snap_target": 'CLOSEST', "snap_point": (
                                         0, 0, 0), "snap_align": False, "snap_normal": (0, 0, 0), "release_confirm": False, "use_accurate": False})

    newclip = getnewsequence(sequences)
    newclip.channel = clip.channel + 1
    newclip.frame_start = clip.frame_start
    bpy.ops.sequencer.select(deselect_all=True)
    clip.select = True
    bpy.ops.sequencer.delete()
    newclip.select = True
    return newclip
    
