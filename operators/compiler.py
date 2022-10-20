import bpy
import re
import os

from .utils.strips import *
from .utils.mrkp import *
from .utils.audio import *


def compilemarkupclip(clip: bpy.types.TextSequence):
    query = mrkpquery(clip.text)
    if not query.valid:
        return False

    newtemplate = replacemarkupclip(clip, query.name)

    if not newtemplate:
        return False

    compiletemplate(newtemplate)


def compiletemplate(clip: bpy.types.MetaSequence):

    if clip["pcontent"] == None:
        return False
    placeholders = get_placeholders(clip)

    query = mrkpquery(clip["pcontent"])
    if not query.valid:
        return False

    for i in placeholders:
        holderindex = getplaceholderindex(i)
        if len(query.arguments) <= holderindex:
            break
        compileplaceholder(i, query.arguments[holderindex])

    templatelength = clip.frame_final_duration
    adjustlength(clip, clip["templatelength"])

    # I have no idea why this awful hack is needed, but it is
    bpy.ops.transform.seq_slide(value=(0, 0))
    clip.frame_final_duration = templatelength

    return True


# get parameter index for placeholder
def getplaceholderindex(placeholder):
    indexregex = re.compile('^:([0-9]*):')
    return int(indexregex.match(placeholder.name).group(0).replace(':', ''))


def adjustlength(clip, oldlength):
    clips = clip.sequences.values()
    for i in clips:
        if i.frame_final_start == clip.frame_final_start:
            # clip fills entire template
            if i.frame_final_duration == oldlength:
                i.frame_final_duration = clip.frame_final_duration
                adjustkeyframes(i, oldlength)
        elif i.frame_final_start > clip.frame_final_start + (oldlength / 2):
            i.frame_start += clip.frame_final_duration - oldlength


def compileplaceholder(clip: bpy.types.Sequence, param):
    cliptype = type(clip)
    # param as content for text clip
    if cliptype == bpy.types.TextSequence:
        clip.text = param
    # multiple choice metaclips, delete all except with name choice.param
    elif cliptype == bpy.types.MetaSequence:
        choices = clip.sequences.values()
        for i in choices:
            if i.name.startswith('choice.'):
                if i.name.removeprefix('choice.') != param:
                    removeclip(i)
    # TODO: give index to choice
    # TODO: compile color clips with hex color code parameter

# get list of all clips inside metaclip that are to be replaced by parameters
def get_placeholders(clip: bpy.types.MetaSequence):
    placeholders = []
    placeholderregex = re.compile('^:[0-9][0-9]*:')
    counter = 0

    for i in clip.sequences.values():
        if placeholderregex.match(i.name):
            if int(i.name[1]) <= counter:
                placeholders.append(i)
                counter += 1
    return placeholders


# convert normal #ffffff syntax to blender's color syntax
def rgbtocolor(rgbcode):
    if not re.compile('^#[0-f][0-f][0-f][0-f][0-f][0-f]').match(rgbcode):
        return None

    colorcode = rgbcode.removeprefix('#').lower()
    colortuple = tuple(int(colorcode[i:i+2], 16) for i in (0, 2, 4))
    retcolor = Color((
        float(colortuple[0]) / 255,
        float(colortuple[1]) / 255,
        float(colortuple[2]) / 255
    ))
    return retcolor


def into_meta(clip, metaclip):
    selection = saveselection()
    bpy.ops.sequencer.copy()
    bpy.ops.sequencer.select(deselect_all=True)
    metaclip.select = True
    currentframe = bpy.context.scene.frame_current
    bpy.context.scene.sequence_editor.active_strip = metaclip
    bpy.ops.sequencer.meta_toggle()
    bpy.context.scene.frame_set(metaclip.frame_final_start)
    bpy.ops.sequencer.paste()
    bpy.ops.sequencer.meta_toggle()
    bpy.context.scene.frame_set(currentframe)
    restoreselection(selection)
    # TODO deal with nested meta clips

class PROCEDITOR_OT_compiler(bpy.types.Operator):
    bl_idname = "proceditor.compile"
    bl_label = "compile text"



    def execute(self, context):
        selectedclips = saveselection()

        rawsequences = getmarkupsequences()

        for i in rawsequences:
            if i.text[0] == ';':
                compilemarkupclip(i)

        # bpy.ops.sequencer.select(deselect_all=True)
        # for i in selectedclips:
        #     i.select = True
        return {'FINISHED'}
