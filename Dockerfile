FROM python:3.10-slim-buster
LABEL maintainer="Hector M. Sanchez C. <sanchez.hmsc@berkeley.edu>"


###############################################################################
# Install Linux, SplatStats and Make Folders
###############################################################################
RUN apt-get update \
    && python -m pip install --upgrade pip \
    && pip install beautifulsoup4 msgpack_python packaging Pillow requests \
    && mkdir SplatStats \
    && mkdir other \
    && mkdir data 

###############################################################################
# Copy needed files
###############################################################################
COPY ./ ./SplatStats
COPY ./other ./other

###############################################################################
# Install SplatStats
###############################################################################
RUN pip install SplatStats/.

###############################################################################
# Run
###############################################################################
ENTRYPOINT ["/bin/bash", "./SplatStats/SplatStats/dockerRoutines/dockerMain.sh"]
