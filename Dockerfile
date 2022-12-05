FROM python:3.10-slim-buster
LABEL maintainer="Hector M. Sanchez C. <sanchez.hmsc@berkeley.edu>"

###############################################################################
# Install Linux
###############################################################################
RUN apt-get update \
    && python -m pip install --upgrade pip \
    && pip install SplatStats

###############################################################################
# Copy needed files and install package
###############################################################################
RUN mkdir SplatStats
COPY ./* ./SplatStats/
RUN cd SplatStats \
    pip install .

###############################################################################
# Run
###############################################################################
CMD ["python"]