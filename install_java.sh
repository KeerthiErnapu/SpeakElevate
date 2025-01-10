#!/bin/bash
# Install OpenJDK 11
echo "Installing OpenJDK 11"
apt-get update -y
apt-get install -y openjdk-11-jre
# Check Java version
java -version
