FROM debian:stable-backports
MAINTAINER bioshadock <support@genouest.org>
LABEL    debian.description="short-read assembly method to build de novo draft assembly" \ 
    debian.homepage="http://soap.genomics.org.cn/soapdenovo.html" \ 
    debian.version="1.05-2" \ 
    debian.copyright="2008-2010 BGI-Shenzhen" \ 
    debian.license="GPL-3+" \ 
    debian.binaries="/usr/bin/soapdenovo-127mer,/usr/bin/soapdenovo-31mer,/usr/bin/soapdenovo-63mer,/usr/bin/soapdenovo2-127mer,/usr/bin/soapdenovo2-63mer" \ 
    bioshadock.Vendor="bioshadock"

ENV DEBIAN_FRONTEND noninteractive
RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "soapdenovo"]
