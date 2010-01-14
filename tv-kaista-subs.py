#! /usr/bin/env python

import os
import re
import urllib

# TODO:
#   * watch directories for changes with inotify
#   * find MIRO dir from settings
#

# http://alpha.tvkaista.fi/recordings/download/[:recording_id].srt
KAISTA_DL_URL = "http://alpha.tvkaista.fi/recordings/download/"

MIRO_DL_DIR = "/home/iiska/Videos/tv-kaista"

yle_filter = re.compile(".*YLE.*(srt){0}$")
id_filter = re.compile("_(\d+)\.[A-Za-z0-9]+\.[A-Za-z0-9]+$")

def listfiles(p, file_filter = None):
    """ Traverse directory recursively and find normal files.
    If file_filter is specifed as a regex then return only files
    which match

    p: path to list
    file_filter: regex to filter only wanted files
    """
    ret = []
    for f in os.listdir(p):
        abs_path = os.path.join(p,f);
        if os.path.isdir(abs_path):
            ret.extend(listfiles(abs_path, file_filter))
        elif os.path.isfile(abs_path) and (
            (file_filter == None) or (file_filter.match(abs_path))):
            ret.append(abs_path)

    return ret

def download_srt(videofile):
    f = urllib.urlopen("%s%s%s" % (KAISTA_DL_URL,
                               id_filter.search(videofile).group(1),
                               ".srt"))
    if f.getcode() == 200:
        output = open("%s%s" % (os.path.splitext(videofile)[0], ".srt"), "w")
        output.write(f.read())
        output.close()
    else:
        print f.getcode()



for f in listfiles(MIRO_DL_DIR, yle_filter):
    download_srt(f)
    
