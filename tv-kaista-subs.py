#! /usr/bin/env python

import os
import re
import urllib

import gconf # depends on python-gconf

# TODO:
#   * watch directories for changes with inotify
#   * find MIRO dir from settings
#

# http://alpha.tvkaista.fi/recordings/download/[:recording_id].srt
KAISTA_DL_URL = "http://alpha.tvkaista.fi/recordings/download/"
# Use this if Miro settings can't be found
FALLBACK_VIDEO_DIR = "~/Videos"

yle_filter = re.compile(".*YLE.*(srt){0}$")
id_filter = re.compile("_(\d+)\.[A-Za-z0-9]+\.[A-Za-z0-9]+$")

def get_mirodir():
    """ Finds Miro gconf settings and retries download directory """
    client = gconf.client_get_default()
    s = client.get_string("/apps/miro/MoviesDirectory")
    if s:
        return s
    else:
        return FALLBACK_VIDEO_DIR

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


for f in listfiles(get_mirodir(), yle_filter):
    download_srt(f)
    
