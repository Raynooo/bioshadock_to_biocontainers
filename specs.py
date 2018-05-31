#The following dictionnary associates a term (keys) with a regular expression (values) to be searched
#The Dockerfile's LABELs and comments will be searched for these terms and hopefully everything will be found

SPECDICT={
    "base_image":"TODO",
    "software.version":"[[V|v]ersion]+",
    "software":"[[N|n]ame]+",
    "about.summary":"TODO",
    "about.home":"TODO",
    "about.documentation":"TODO",
    "about.license":"TODO",
    "MAINTAINER":"MAINTAINER"
}
