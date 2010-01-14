#! /usr/bin/env python

import os

MIRO_DL_DIR = "/home/iiska/Videos/tv-kaista"

def listfiles(p, filt = None):
""" Traverse directory recursively and find normal files.
    If filt is specifed as a regex then return only files
    which match

    p: path to list
    filter: regex to filter only wanted files
"""
    ret = []
    for f in os.listdir(p):
        abs_path = os.path.join(p,f);
        if os.path.isdir(abs_path):
            ret.append(listfiles(abs_path, fil))
        else if os.path.isfile(abs_path):
            ret.append(abs_path)

    return ret
 
print listfiles(MIRO_DL_DIR)
