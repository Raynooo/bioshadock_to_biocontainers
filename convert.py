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
EXTRAREGEX="(\s)*(:|=)*(\s)*"
EMPTY_RE = re.compile("^[\s]*$")
OUTROOT = "./myDockerfiles"
TOTALCOUNT = 0
INST_PARSE = re.compile("(\s){3,}")

##############Acquiring the original Dockerfiles#################

def get_tools_ids (url,ignoreRegex):
    r = requests.get (url)
    myTools=list()
    global TOTALCOUNT

    for crt_entry in r.json():
        if crt_entry.get("visible"):
            if crt_entry.get("meta").get("Dockerfile"):
                TOTALCOUNT = TOTALCOUNT + 1
                if not ignoreRegex.search(crt_entry.get("id")):
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
        if "comment" in crt_meta.get("context") and crt_expr.search(line):
            #split_regex = re.compile(crt_meta.get("regex")+EXTRAREGEX, re.IGNORECASE)
            #crt_value = split_regex.split(line)[-1]
            #if not EMPTY_RE.search(crt_value):
            #    return [crt_meta.get("destLabel"), crt_value]
            return extract_meta_from_string(crt_meta, line)
    return None

def look_for_this_meta(metadata_desc, dfp):
    for crt_inst in dfp.structure:
        #if crt_inst.get("instruction")==metadata_desc.get("context"):
        #print (crt_inst)
        if crt_inst.get("instruction") in metadata_desc.get("context"):
            #print (crt_inst.get("value"))
            ###There could be multiple lines to that instruction, each line must be parsed separately
            subInst = INST_PARSE.split(crt_inst.get("value"))
            #print (subInst)
            return find_meta_in_instruction (metadata_desc, subInst)
            #return [metadata_desc.get("destLabel"), crt_inst.get("value")]
    return None

def find_meta_in_instruction (meta_desc, instPieces):
    crt_expr = re.compile(meta_desc.get("regex"), re.IGNORECASE)
    for crt_piece in instPieces:
        #print (crt_piece)
        if crt_expr.search (crt_piece):
            crt_piece = crt_piece.replace ('"', '')
            return extract_meta_from_string(meta_desc, crt_piece)

def extract_meta_from_string (meta_desc, string_with_meta):
    #print (string_with_meta)
    split_regex = re.compile(meta_desc.get("regex")+EXTRAREGEX, re.IGNORECASE)
    crt_value = split_regex.split(string_with_meta)[-1]
    if not EMPTY_RE.search(crt_value):
        print ("META "+meta_desc.get("destLabel")+" <---- ["+repr(crt_value)+"]")
        return [meta_desc.get("destLabel"), crt_value]
    return None

#####################Misc####################

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
            print ("    VERSION FOUND "+repr(clean_version)+" NEW NAME "+repr(software))
            version = clean_version
        else:
            print ("    UPDATING TOOL NAME TO "+repr(software)+ " (version is "+repr(version)+")")
            if not clean_version == version:
                print ("        Warning, conflicting version name "+repr(clean_version))
    if not version:
        version = "DEFAULT"
    ##Updating entry label
    labels["software"]=software
    labels["software.version"]=version
    ##Returning updated labels
    return labels



#################Writing output#####################

def create_labels_line (labelsDict):
    if len(labelsDict) == 0:
        print ("No labels found for this tool")
        return ("#No labels found for this tool")
    labels = "LABELS autogen=\"yes\""
    for crt_meta in labelsDict.keys():
        #print (crt_meta)
        labels = labels+" \\ \n\t"+crt_meta+"=\""+labelsDict.get(crt_meta)+"\""
    return labels

def print_in_order (labels, dfparsed, target_dfile):
    ##We only need to insert our labels at the start, after the FROM command
    ##To keep the order and the comments, we'll use dockerfile.content instead of dockerfile.json
    from_passed = False
    lines = dfparsed.content.split("\n")
    for line in lines:
        target_dfile.write(line+"\n")
        if re.search("^[\s]*FROM", line):
            from_passed = True
            myLabels = create_labels_line (labels)
            target_dfile.writelines(["\n","#####AUTO GENERATED LABELS#####\n",myLabels,"\n#####END OF INSERTION#####\n"])


def output_dockerfile (labels, dfparsed, path):
    labels = update_version_and_name (labels)
    crt_path = os.path.join(path,labels.get("software"),labels.get("software.version"))
    if not os.path.exists(crt_path):
        os.makedirs(crt_path)
    dockerfile = open (os.path.join(crt_path, "Dockerfile"), 'w')

    print_in_order (labels, dfparsed, dockerfile)

    dockerfile.close()

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
print ("THERE ARE "+ str(TOTALCOUNT) +" DOCKERFILES TOTAL IN BIOSHADOCK")

for crt_id in ids:
    #this_tools_labels = list()
    this_tools_labels = {}
    ##Adding the tool's name to the labels
    #this_tools_labels.append(["software",crt_id.split("/")[-1]])
    this_tools_labels["software"]= crt_id.split("/")[-1]
    print ("#####Current tool: "+repr(this_tools_labels["software"])+"#####")
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
    #print (this_tools_labels)
    output_dockerfile (this_tools_labels, dfp, OUTROOT)
    print ("##########")

