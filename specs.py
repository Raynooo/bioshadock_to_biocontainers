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

METADESC=[
    {
        "destLabel" : "base_image",
        "regex" : "FROM",
        "context" : "FROM",
    },
    {
        "destLabel" : "software.version",
        "regex" : "(software)[\s]*(version)",
        "context" : "comment",
    },
    #{
    #    "destLabel" : "software",
    #    "regex" : "TODO",
    #    "context" : "path",
    #},
    {
        "destLabel" : "about.summary",
        "regex" : "(description)",
        "context" : "comment",
    },
    {
        "destLabel" : "about.home",
        "regex" : "(website)",
        "context" : "comment",
    },
    {
        "destLabel" : "about.documentation",
        "regex" : "(documentation)",
        "context" : "comment",
    },
    {
        "destLabel" : "about.license",
        "regex" : "(license)",
        "context" : "comment",
    },
    {
        "destLabel" : "MAINTAINER",
        "regex" : "MAINTAINER",
        "context" : "MAINTAINER",
    }
]
