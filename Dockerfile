# Use an official Python runtime as a parent image
FROM python:3

MAINTAINER Steve Markstrom <markstro@usgs.gov>

COPY prms_verifier.py ./

RUN set -x \
    && mkdir /work

# Run app.py when the container launches
CMD ["python", "prms_verifier.py"]

