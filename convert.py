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
EXTRAREGEX="(:)*(\s)*"
EMPTY_RE = re.compile("^[\s]*$")


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

def parse_comment_line (line, metadataList):
    for crt_meta in metadataList:
        crt_expr=re.compile(crt_meta.get("regex"), re.IGNORECASE)
        if crt_meta.get("context")=="comment" and crt_expr.search(line):
            #print crt_meta.get("destLabel") + " found in " + line
            split_regex = re.compile(crt_meta.get("regex")+EXTRAREGEX, re.IGNORECASE)
            crt_value = split_regex.split(line)[-1]
            if not EMPTY_RE.search(crt_value):
                #print crt_meta.get("destLabel") + " found: " + crt_value
                #crt_meta["value"]=crt_value
                return [crt_meta.get("destLabel"), crt_value]
    return None

def look_for_this_meta(metadata_desc, dfp):
    for crt_inst in dfp.structure:
        if crt_inst.get("instruction")==metadata_desc.get("context"):
            #print crt_inst.get("value")
            return [metadata_desc.get("destLabel"), crt_inst.get("value")]
    return None

#################MAIN#####################


cmt_line_re = "^[\s]*#"

#docker_file = None

ids=get_tools_ids(TOOLSPATH, BLACKLIST)
#print len(ids)

for crt_id in ids:
    this_tools_labels = list()
    ##Adding the tool's name to the labels
    this_tools_labels.append(["software",crt_id.split("/")[-1]])

    crt_Dockerfile=get_tool_dockerfile(DOCKERFILESROOt, crt_id)
    lines = crt_Dockerfile.split("\n")
    ##Extracting what we can from the comments
    for line in lines:
        if re.search(cmt_line_re, line):
            crt_label=parse_comment_line (line, METADESC)
            if not crt_label==None:
                this_tools_labels.append(crt_label)
    ##Parsing the Dockerfile with DockerfileParser library
    dfp = DockerfileParser()
    dfp.content = crt_Dockerfile
    ##Extracting labels coming from instructions
    for crt_meta in METADESC:
        if not crt_meta.get("context")=="comment":
            crt_label=look_for_this_meta(crt_meta, dfp)
            if not crt_label==None:
                this_tools_labels.append(crt_label)
    ###TODO: write the modified Dockerfile into the proper directory (following BioContainers logic)
    print this_tools_labels

