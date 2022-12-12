import os
import re

import bpy


def getsequences():
    return list(bpy.context.scene.sequence_editor.sequences_all)


def getnearbysequences(clip, range):
    """
    get clips above clip and within time boundaries of clip
    """
    returnlist = []
    clipparent = clip.parent_meta()
    for i in getsequences():
        if i.parent_meta() != clipparent.parent_meta():
            continue
        if (
            i.channel >= (clip.channel - range)
            and i.channel < clip.channel
            and i.frame_start >= clip.frame_start
            and i.frame_final_end <= clip.frame_final_end
        ):
            returnlist.append(i)
            if len(returnlist) >= range:
                break
    returnlist.sort(key=lambda x: x.channel, reverse=True)
    return returnlist


# TODO comment difference between this and getsequences
def gettopsequences():
    return list(bpy.context.scene.sequence_editor.sequences)


# some things don't have a good API so proceditor needs to emulate a user by
# selecting and doing stuff with the clips
# This is needed to restore the selection afterwards
def saveselection():
    returnlist = []
    for i in getsequences():
        if i.select:
            returnlist.append(i)
    return returnlist


# restore clip selection after emulating a user due to lack of good API
def restoreselection(selectlist):
    bpy.ops.sequencer.select(deselect_all=True)
    for i in selectlist:
        i.select = True


def savesequences():
    returnlist = []
    for i in gettopsequences():
        returnlist.append(i.name)
    return returnlist


# return newly added sequences
def getnewsequences(sequencelist):
    returnlist = []
    for i in sequencelist:
        if i not in returnlist:
            returnlist.append(bpy.context.scene.sequence_editor.sequences[i])
    return returnlist


# get sequences witout the compiler marker _c$, optionally filter through regex
def getmarkupsequences(regex="", compiled=False):
    sequences = bpy.context.scene.sequence_editor.sequences
    returnlist = []
    # compiled sequences have a _c at the end but may also have an auto assigned
    # number
    tpattern = re.compile(".*(_c|_c\\.[0-9]*)$")
    if not regex == "":
        fpattern = re.compile(regex)
    for i in sequences:
        if type(i) == bpy.types.TextSequence and (
            not compiled
            and not tpattern.match(i.name)
            or (compiled and tpattern.match(i.name))
        ):
            # with custom search string
            if not regex == "":
                if not fpattern.match(i.text):
                    continue
            returnlist.append(i)
    return returnlist


# get template clip with format template.name
def gettemplate(tname):
    templatename = "template_" + tname
    for i in gettopsequences():
        if i.name.startswith(templatename):
            os.system("echo " + i.name + " >> /tmp/test.txt")
            return i

    return False


# get all sequeces that match the given regex
def getresequences(regex, stype=0):
    retsequences = []
    pattern = re.compile(regex)
    for i in getsequences():
        if pattern.match(i.name):
            if stype == 0:
                retsequences.append(i)
            elif type(i) == stype:
                retsequences.append(i)
    return retsequences


# restore graphical clip highlight
def activateselection():
    for i in getsequences():
        if i.select:
            bpy.context.scene.sequence_editor.active_strip = i
            return


# replace markup clip with matching template
def replacemarkupclip(clip: bpy.types.TextSequence, templatename: str):

    sequences = bpy.context.scene.sequence_editor.sequences
    if not templatename or templatename == "":
        return False

    markupcontent = clip.text
    startframe = clip.frame_final_start
    markupduration = clip.frame_final_duration
    markupchannel = clip.channel
    clipname = clip.name

    removeclip(clip)

    templateclip = gettemplate(templatename)
    templatelength = templateclip.frame_final_duration

    if not templateclip:
        return False

    bpy.ops.sequencer.select_all(action="DESELECT")

    sequences[templateclip.name].select = True

    # maybe replace ops with api
    bpy.ops.sequencer.duplicate_move(
        SEQUENCER_OT_duplicate={},
        TRANSFORM_OT_seq_slide={
            "value": (
                startframe - templateclip.frame_final_start,
                markupchannel - templateclip.channel,
            ),
            "release_confirm": False,
            "use_accurate": False,
        },
    )

    newclip = list(
        filter(
            lambda element: element.select,
            list(bpy.context.scene.sequence_editor.sequences),
        )
    )[0]
    newclip.frame_final_duration = markupduration
    newclip.name = clipname + "_c"
    newclip["pcontent"] = markupcontent
    newclip["templatelength"] = templatelength

    return newclip


def getkeyframes(clipname):
    returnlist = []
    matchpath = 'sequence_editor.sequences_all["' + clipname + '"]'
    for action in bpy.data.actions:
        for curve in list(action.fcurves):
            if curve.data_path.startswith(matchpath):
                returnlist += list(curve.keyframe_points)
    return returnlist


def removeclip(clip):
    bpy.ops.sequencer.select(deselect_all=True)
    clip.select = True
    bpy.ops.sequencer.delete()


# move keyframes at the end of the clip towards the end


def adjustkeyframes(clip, oldduration):
    frames = getkeyframes(clip.name)

    if len(frames) == 0:
        return

    beginframes = []
    endframes = []

    for i in frames:
        frametime = i.co[0]
        if frametime > (clip.frame_final_start + oldduration / 2):
            endframes.append(i)
        else:
            beginframes.append(i)

    if len(endframes) == 0:
        return

    endoffset = clip.frame_final_duration - oldduration
    for i in endframes:
        i.co[0] += endoffset


def gettopchannel(frame):
    channel = 0
    for i in getsequences():
        if i.frame_final_start <= frame and i.frame_final_end >= frame:
            if i.channel > channel:
                channel = i.channel
    return channel + 1
