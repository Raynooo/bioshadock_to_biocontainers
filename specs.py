#The following dictionnary associates a term (keys) with a regular expression (values) to be searched
#The Dockerfile's LABELs and comments will be searched for these terms and hopefully everything will be found

SPECDICT={
    #"base_image":"TODO",
    "software.version":"(software)[\s]*(version)",
    "software":"(name)",
    "about.summary":"(description)",
    "about.home":"(website)",
    "about.documentation":"TODO",
    "about.license":"(license)",
    #"MAINTAINER":"MAINTAINER"
}
