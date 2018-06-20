#!/usr/bin/python3

from dockerfile_parse import DockerfileParser
from pprint import pprint

import argparse
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
OUTROOT = "./"

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
#####################Misc####################

def extract_version_from_name (name):
    version_re = re.compile("((\.|_|-)*[\d]+)+$")
    onlyV_re = re.compile("([\d]+(\.|_|-)*)+$")
    match = version_re.search (name)
    if match:
        clean_software = name[0:match.start(0)]
        clean_version = onlyV_re.search(match.group(0)).group(0)
        print ("    VERSION FOUND "+clean_version+" NEW NAME "+clean_software)
        return [clean_software, clean_version]
    return [name, "DEFAULT"]

def update_version_and_name (software, version):
    version_re = re.compile("((\.|_|-)*[\d]+)+$")
    onlyV_re = re.compile("([\d]+(\.|_|-)*)+$")
    match = version_re.search (software)
    if match:
        clean_version = onlyV_re.search(match.group(0)).group(0)
        software = software[0:match.start(0)]
        if not version:
            print ("    VERSION FOUND "+clean_version+" NEW NAME "+software)
            version = clean_version
        else:
            print ("    UPDATING TOOL NAME TO "+software+ " (version is "+version+")")
            if not clean_version == version:
                print ("    Warning, conflicting version name "+clean_version)
    if not version:
        version = "DEFAULT"
    return [software, version]

def update_version_and_name (labels):
    ##Initializing vars
    software = labels.get("software")
    version = labels.get("software.version")
    ##Actually doing stuff
    version_re = re.compile("((\.|_|-)*[\d]+)+$")
    onlyV_re = re.compile("([\d]+(\.|_|-)*)+$")
    match = version_re.search (software)
    if match:
        clean_version = onlyV_re.search(match.group(0)).group(0)
        software = software[0:match.start(0)]
        if not version:
            print ("    VERSION FOUND "+clean_version+" NEW NAME "+software)
            version = clean_version
        else:
            print ("    UPDATING TOOL NAME TO "+software+ " (version is "+version+")")
            if not clean_version == version:
                print ("        Warning, conflicting version name "+clean_version)
    if not version:
        version = "DEFAULT"
    ##Updating entry label
    labels["software"]=software
    labels["software.version"]=version
    ##Returning updated labels
    return labels



#################Writing output#####################

def output_dockerfile (labels, dfparsed, path):
    #if not labels.get("software.version"):
        #print ("No version for "+labels.get("software"))
        #update=extract_version_from_name (labels.get("software"))
        #labels["software"] = update[0]
        #labels["software.version"] = update[1]
        #print (labels)
    #software_and_version = update_version_and_name (labels.get("software"), labels.get("software.version"))
    #labels["software"]=software_and_version[0]
    #labels["software.version"]=software_and_version[1]
    labels = update_version_and_name (labels)
    crt_path = os.path.join(path,labels.get("software"),labels.get("software.version"))
    if not os.path.exists(crt_path):
        #os.makedirs(crt_path)
        i=1


#################MAIN#####################

parser = argparse.ArgumentParser()
parser.add_argument("-o", help="root directory for the output dockerfile(s)")
args = parser.parse_args()
if args.o:
    OUTROOT = args.o
    print("Output root is "+OUTROOT)


cmt_line_re = "^[\s]*#"

#docker_file = None

ids=get_tools_ids(TOOLSPATH, BLACKLIST)
#print len(ids)

for crt_id in ids:
    #this_tools_labels = list()
    this_tools_labels = {}
    ##Adding the tool's name to the labels
    #this_tools_labels.append(["software",crt_id.split("/")[-1]])
    this_tools_labels["software"]= crt_id.split("/")[-1]

    crt_Dockerfile=get_tool_dockerfile(DOCKERFILESROOt, crt_id)
    lines = crt_Dockerfile.split("\n")
    ##Extracting what we can from the comments
    for line in lines:
        if re.search(cmt_line_re, line):
            crt_label=parse_comment_line (line, METADESC)
            if not crt_label==None:
                #this_tools_labels.append(crt_label)
                this_tools_labels[crt_label[0]]=crt_label[1]
    ##Parsing the Dockerfile with DockerfileParser library
    dfp = DockerfileParser()
    dfp.content = crt_Dockerfile
    ##Extracting labels coming from instructions
    for crt_meta in METADESC:
        if not crt_meta.get("context")=="comment":
            crt_label=look_for_this_meta(crt_meta, dfp)
            if not crt_label==None:
                #this_tools_labels.append(crt_label)
                this_tools_labels[crt_label[0]]=crt_label[1]
    ###TODO: write the modified Dockerfile into the proper directory (following BioContainers logic)
    #print (this_tools_labels)
    output_dockerfile (this_tools_labels, dfp, OUTROOT)

