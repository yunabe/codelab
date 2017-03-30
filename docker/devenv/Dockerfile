# References:
# https://docs.docker.com/engine/reference/builder/

FROM ubuntu

#############
#  apt-get  #
#############
# Install openssh-server and set up server keys first to minimize the chance to invalidate
# the cache and regenerate server keys.
RUN apt-get update && apt-get install -y openssh-server

# Install other apt-packages.
RUN apt-get update && apt-get install -y\
  zip unzip curl wget screen emacs git zsh rsyslog\
  python python-pip gcc clang openjdk-8-jdk golang-go=2:1.6-1ubuntu4

# Install Python ML libraries.
# Note: Use scikit-learn, not sklearn.
RUN pip install --upgrade pip && pip install -U numpy scipy matplotlib pandas scikit-learn jupyter tensorflow

# Install gcloud (https://cloud.google.com/sdk/downloads#apt-get)
# lsb-release is for lsb_release. apt-transport-https is necessary to apt-get with https.
RUN apt-get update && apt-get install -y lsb-release apt-transport-https
RUN export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)" && echo "deb https://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && apt-get update && apt-get install -y google-cloud-sdk

# Install Go Appengine
RUN cd /opt && wget -q https://storage.googleapis.com/appengine-sdks/featured/go_appengine_sdk_linux_amd64-1.9.48.zip &&\
  unzip -qq go_appengine_sdk_linux_amd64-1.9.48.zip

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
RUN chsh -s /bin/zsh $user
RUN mkdir -p /home/$user
WORKDIR /home/$user

# Set up .ssh keys
COPY _ssh .ssh
RUN chmod 700 .ssh

# Copy dot files in local_config then remove local_config/README.md.
COPY local_config/* ./
RUN rm README.md

# Finally, change the owner of the home dir and set USER.
RUN chown -R $user:developer /home/$user
USER $user

# Set up public dot files as $user.
RUN git clone git@github.com:yunabe/linux-user-config.git config && ./config/setup.sh

# Misc as the user
RUN mkdir -p local/gocode/src/github.com/$user && git clone git@github.com:yunabe/gae-codelab.git local/gocode/src/github.com/$user/gae-codelab

USER root
# Add additional setup as root with minimum cache invalidation.

# Apply root_config.patch to rewrite root configurations.
COPY root_config.patch /root_config.patch
RUN cd / && patch -p0 < /root_config.patch && rm -f /root_config.patch

# Run services as root and sleep.
# - ssh: ssh server
# - rsyslog: Record /var/log/auth.log from sshd.
CMD service ssh start && service rsyslog start && sleep infinity
