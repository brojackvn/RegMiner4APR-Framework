# Use Ubuntu 20.04 as the base image
FROM ubuntu:20.04

# Maintainer information (using LABEL instead of MAINTAINER)
LABEL maintainer="ngocpq <phungquangngoc@gmail.com>"

#############################################################################
# Requirements
#############################################################################
ENV TZ=Australia/Melbourne
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Update package list and install required packages
RUN apt-get update && \
    apt-get install -y openjdk-8-jdk git python3 wget tar

# Set environment variables for Java
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Maven 3.9.8 installation
RUN cd /opt && \
    wget https://dlcdn.apache.org/maven/maven-3/3.9.8/binaries/apache-maven-3.9.8-bin.tar.gz && \
    tar -xzf apache-maven-3.9.8-bin.tar.gz && \
    mv apache-maven-3.9.8 maven

# Set environment variables for Maven
ENV M2_HOME=/opt/maven
ENV PATH=$M2_HOME/bin:$PATH

# Install Gradle
RUN apt-get install -y gradle

# Install xvfb
RUN apt-get install -y xvfb

#############################################################################
# Setup RegMiner4APR
#############################################################################
WORKDIR /
RUN git clone https://github.com/brojackvn/RegMiner4APR-Regression-Bugs-Database.git RegMiner4APR-Regression-Bugs-Database
WORKDIR /RegMiner4APR-Regression-Bugs-Database
RUN /bin/bash -c "source activate"

