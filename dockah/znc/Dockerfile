FROM fedora:latest
MAINTAINER Sayan Chowdhury <gmail@yudocaa.in>

RUN groupadd -r fedora -g 1000 && useradd -u 1000 -r -g fedora fedora
RUN dnf update -y
RUN dnf install znc htop vim -y && dnf clean all

VOLUME ["/home/fedora/.znc"]
EXPOSE 6667

WORKDIR ["/home/fedora"]
USER fedora
