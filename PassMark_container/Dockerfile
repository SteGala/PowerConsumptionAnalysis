# syntax=docker/dockerfile:1
FROM ubuntu:latest
COPY ./pt_linux_x64 .
RUN apt-get update
RUN apt-get install -y libncurses5
RUN apt-get install -y libcurl4
ENTRYPOINT ["bash"]