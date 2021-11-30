FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -y libncurses5
RUN apt-get install -y libcurl4
RUN apt-get install -y unzip

RUN curl https://www.passmark.com/downloads/pt_linux_x64.zip -O
RUN unzip pt_linux_x64.zip

ENTRYPOINT ["bash"]