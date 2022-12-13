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
    && mkdir data

###############################################################################
# Copy needed files
###############################################################################
COPY ./* ./SplatStats/

###############################################################################
# Run
###############################################################################
# CMD ["python /SplatStats/demos/main.py"]
# ENTRYPOINT ["python","./SplatStats/demos/main.py"]
ENTRYPOINT ["python", "./SplatStats/dockerRoutines/main.py"]
