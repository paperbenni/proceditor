import bpy
import os
import hashlib
import re

# download music from link, 
# keep cache of already downloaded files


def downloadclip(link):
    if not link:
        return False
    os.system('[ -e ~/.cache/proceditor/music/ ] || mkdir -p ~/.cache/proceditor/music/')
    hash = hashlib.sha256(link.encode('utf-8')).hexdigest()
    tmppath = os.environ['HOME'] + '/.cache/proceditor/music/' + hash
    if os.path.isdir(tmppath):
        for i in os.listdir(tmppath):
            if re.compile('.*\.wav').match(i):
                return tmppath + '/' + i
    else:
        os.system('mkdir -p ' + tmppath)
        os.system('cd ' + tmppath + ' && youtube-dl -x --audio-format wav "' + link + '"')
        for i in os.listdir(tmppath):
            if re.compile('.*\.wav').match(i):
                return tmppath + '/' + i
        return False

def addmusic(link):
    filename = downloadclip(link)
    if not filename:
        return False
    bpy.ops.sequencer.sound_strip_add(filepath=filename, frame_start = bpy.context.frame_current)