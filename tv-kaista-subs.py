#! /usr/bin/env python

import os
import re

MIRO_DL_DIR = "/home/iiska/Videos/tv-kaista"

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

yle_filter = re.compile(".*YLE.*")
print listfiles(MIRO_DL_DIR, yle_filter)
