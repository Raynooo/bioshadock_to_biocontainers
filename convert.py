#!/usr/bin/python

from dockerfile_parse import DockerfileParser
from pprint import pprint

import sys
import os
import re
import requests

from specs import *

BLACKLIST=re.compile("^(bioconda|debian)")
TOOLSPATH="https://docker-ui.genouest.org/container/all?light=true"
DOCKERFILESROOt="https://docker-ui.genouest.org/container/"

##############Acquiring the original Dockerfiles#################

def get_tools_ids (url,ignoreRegex):
    r = requests.get (url)
    myTools=list()

    for crt_entry in r.json():
        if crt_entry.get("visible"):
            if not ignoreRegex.search(crt_entry.get("id")):
                if crt_entry.get("meta").get("Dockerfile"):
                    myTools.append(crt_entry.get("id"))

    #print myTools
    #print len(myTools)
    return myTools

def get_tool_dockerfile (url, id):
    r = requests.get (url+id)
    #print r.json().get("meta").get("Dockerfile")
    return r.json().get("meta").get("Dockerfile")

###########Treating them##############

def treat_this_label (crtKey, crtVal):
    return 1

def parsing_labels (crtLabels):
    #print type(crtLabels)
    #print crtLabels.keys()
    for key in crtLabels.keys():
        #print key
        #print crtLabels.get(key)
        newPair = treat_this_label (key, crtLabels.get(key))


#################MAIN#####################


cmt_line_re = "^[\s]*#"

#docker_file = None

ids=get_tools_ids(TOOLSPATH, BLACKLIST)

for crt_id in ids:
    crt_Dockerfile=get_tool_dockerfile(DOCKERFILESROOt, crt_id)
    #print crt_id
    dfp = DockerfileParser()
    dfp.content = crt_Dockerfile
    #pprint (dfp.labels)
    lines = crt_Dockerfile.split("\n")
    for line in lines:
        if re.search(cmt_line_re, line):
            print line
            #TODO: search comment line for metadata


    #pprint (dfp.json)
    #print dfp.labels
    #pprint (dfp.structure)
    #parsing_labels (dfp.labels)

