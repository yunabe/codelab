# References:
# https://docs.docker.com/engine/reference/builder/

FROM ubuntu

# apt-get
RUN apt-get update && apt-get install -y curl
RUN apt-get update && apt-get install -y screen
RUN apt-get update && apt-get install -y emacs
RUN apt-get update && apt-get install -y git
RUN apt-get update && apt-get install -y zsh
RUN apt-get update && apt-get install -y python
RUN apt-get update && apt-get install -y golang-go=2:1.6-1ubuntu4
RUN apt-get update && apt-get install -y gcc
RUN apt-get update && apt-get install -y clang
RUN apt-get update && apt-get install -y wget
RUN apt-get update && apt-get install -y openjdk-8-jdk
RUN apt-get update && apt-get install -y python-pip && pip install --upgrade pip

# Install ML libraries.
# Note: Use scikit-learn, not sklearn.
RUN pip install --upgrade pip && pip install -U numpy scipy matplotlib pandas scikit-learn jupyter

# https://docs.docker.com/engine/reference/builder/#arg
# Do not move this to the head of Dockerfile because
# the definition of ARG causes cache-miss in following RUN commands
# regardless of whether they refer an arg or not.
ARG user=yunabe

# The guidline recommends us to execute commands in non-root.
# https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/#user
#
# You should not change the owner of the home dir or set USER before COPY operations
# because COPY ignores USER (https://github.com/docker/docker/issues/6119).
RUN groupadd -r developer && useradd -r -g developer $user
RUN mkdir -p /home/$user
WORKDIR /home/$user

# Set up .ssh keys
COPY _ssh .ssh
RUN chmod 700 .ssh

# Finally, change the owner of the home dir and set USER.
RUN chown -R $user:developer /home/$user
USER $user

# Set up public dot files as $user.
RUN git clone git@github.com:yunabe/linux-user-config.git config && ./config/setup.sh

# Misc
RUN mkdir -p src && git clone git@github.com:yunabe/codelab.git src/codelab

# bash
CMD ["bash"]
