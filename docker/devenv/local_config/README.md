# local_config
Place dot files which you want to copy to the container image
but do not want to share publicly here, like dot files containing user credentials.

This file exists here so that COPY command in Dockerfile succeeds if no files are placed in this directory.
