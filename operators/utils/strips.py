import bpy
import re
import os

def getsequences():
    return list(bpy.context.scene.sequence_editor.sequences_all)

def saveselection():
    returnlist = []
    for i in getsequences():
        if i.select:
            returnlist.append(i)
    return returnlist

def restoreselection(selectlist):
    bpy.ops.sequencer.select(deselect_all=True)
    for i in selectlist:
        i.select = True

# return newly added sequence
def getnewsequence(previoussequences):
    return list(set(getsequences()) - set(previoussequences))[0]

# get sequences witout the compiler marker _c$, optionally filter through regex
def getmarkupsequences(regex='', compiled=False):
    sequences = bpy.context.scene.sequence_editor.sequences
    returnlist = []
    # compiled sequences have a _c at the end but may also have an auto assigned
    # number
    tpattern = re.compile('.*(_c|_c\.[0-9]*)$')
    if not regex == '':
        fpattern = re.compile(regex)
    for i in sequences:
        if type(i) == bpy.types.TextSequence and \
                (not compiled and not tpattern.match(i.name) or (compiled and tpattern.match(i.name))):
            # with custom search string
            if not regex == '':
                if not fpattern.match(i.text):
                    continue
            returnlist.append(i)
    return returnlist


# get template clip with format template.name
def gettemplate(tname):
    templatename = 'template.' + tname
    for i in getsequences():
        if i.name == templatename:
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
def replacetemplate(clip: bpy.types.TextSequence, templatename: str):
    markupcontent = clip.text
    templateclip = gettemplate(templatename)
    if not templateclip:
        return False

    bpy.ops.sequencer.select(deselect_all=True)
    templateclip.select = True
    bpy.ops.sequencer.duplicate_move(SEQUENCER_OT_duplicate={},
                                     TRANSFORM_OT_seq_slide={"value": (0, 1), "snap": False, "snap_target": 'CLOSEST', "snap_point": (
                                         0, 0, 0), "snap_align": False, "snap_normal": (0, 0, 0), "release_confirm": False, "use_accurate": False})

    activateselection()
    newclip = bpy.context.scene.sequence_editor.active_strip

    # move template clip to position of markup clip
    newclip.channel = clip.channel + 1
    newclip.frame_start = clip.frame_start
    newclip.frame_final_end = clip.frame_final_end

    # remove markup clip
    newclip.name = clip.name + '_c'
    bpy.context.scene.sequence_editor.sequences.remove(clip)

    newclip.select = True
    newclip.channel -= 1
    # save markup content in compiled version
    newclip["pcontent"] = markupcontent
    adjustkeyframes(newclip)

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
    bpy.context.scene.sequence_editor.sequences.remove(clip)

# move keyframes at the end of the clip towards the end
def adjustkeyframes(clip):
    frames = getkeyframes(clip.name)
    if len(frames) == 0:
        return
    beginframes = []
    endframes = []

    middle = (max(i.co[0] for i in frames) + min(i.co[0] for i in frames)) / 2

    for i in frames:
        frametime = i.co[0]
        if (frametime > middle):
            endframes.append(i)
        else:
            beginframes.append(i)
    if len(endframes) == 0:
        return
    frameoffset = clip.frame_final_end - max(i.co[0] for i in endframes)
    beginoffset = min(i.co[0] for i in beginframes) - clip.frame_start

    for i in endframes:
        i.co[0] += frameoffset

    for i in beginframes:
        i.co[0] += beginoffset