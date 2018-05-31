#!/usr/bin/python

from dockerfile_parse import DockerfileParser
from pprint import pprint

import sys
import os
import re

from specs import *

def treat_this_label (crtKey, crtVal):
    if crtKey.endswith("description"):
        print "Description found!"
        return 1
    elif crtKey.endswith("homepage"):
        print "URL found!"
        return 1
    return 0

def parsing_labels (crtLabels):
    #print type(crtLabels)
    #print crtLabels.keys()
    for key in crtLabels.keys():
        #print key
        #print crtLabels.get(key)
        newPair = treat_this_label (key, crtLabels.get(key))








docker_file = None
if len(sys.argv) > 1 and sys.argv[1]:
    docker_file = sys.argv[1]

if not docker_file or not os.path.exists(docker_file):
    print("Could not find Dockerfile "+str(docker_file))
    sys.exit(1)

with open(docker_file, 'r') as content_file:
    content = content_file.read()

dfp = DockerfileParser()
dfp.content = content
labels = dfp.labels

#pprint (labels)
#pprint (dfp.structure)
#pprint (dfp.json)
#print labels

parsing_labels (labels)

print SPECDICT
