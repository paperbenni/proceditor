import bpy

def getsequences():
    return list(bpy.context.scene.sequence_editor.sequences_all)

def getnewsequence(previoussequences):
    return list(set(getsequences()) - set(previoussequences))[0]
