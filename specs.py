#The Dockerfile's LABELs, commands and comments will be searched for these terms and hopefully everything will be found

METADESC=[
    {
        "destLabel" : "base_image",
        "regex" : ".+",
        "context" : "FROM",
    },
    {
        "destLabel" : "software.version",
        "regex" : "((software)[\s]*(version))|(ANNOT.Version)",
        "context" : "comment,LABEL",
    },
    #{
    #    "destLabel" : "software",
    #    "regex" : "TODO",
    #    "context" : "path",
    #},
    {
        "destLabel" : "about.summary",
        "regex" : "(description)",
        "context" : "comment,LABEL",
    },
    {
        "destLabel" : "about.home",
        "regex" : "(website|homepage)",
        "context" : "comment,LABEL",
    },
    {
        "destLabel" : "about.documentation",
        "regex" : "(documentation)",
        "context" : "comment,LABEL",
    },
    {
        "destLabel" : "about.license",
        "regex" : "(license)",
        "context" : "comment,LABEL",
    },
    #{
    #    "destLabel" : "MAINTAINER",
    #    "regex" : "MAINTAINER",
    #    "context" : "MAINTAINER",
    #}
]
