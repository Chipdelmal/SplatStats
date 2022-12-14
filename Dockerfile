FROM python:3.10-slim-buster
LABEL maintainer="Hector M. Sanchez C. <sanchez.hmsc@berkeley.edu>"

###############################################################################
# Install Linux, SplatStats and Make Folders
###############################################################################
RUN apt-get update \
    && python -m pip install --upgrade pip \
    && pip install beautifulsoup4 msgpack_python packaging Pillow requests \
    && pip install SplatStats \
    && mkdir SplatStats \
    && mkdir other \
    && mkdir data

###############################################################################
# Copy needed files
###############################################################################
COPY ./SplatStats ./SplatStats
COPY ./other ./other

###############################################################################
# Run
###############################################################################
# CMD ["python /SplatStats/demos/main.py"]
# ENTRYPOINT ["python", "./SplatStats/dockerRoutines/dockerPlots.py"]
ENTRYPOINT ["/bin/bash", "./SplatStats/dockerRoutines/dockerMain.sh"]
