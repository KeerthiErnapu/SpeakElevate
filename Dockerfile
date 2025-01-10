# Use a base image with an OS (e.g., Debian) or Java-specific image
FROM openjdk:17-jdk-slim

# Update package lists
RUN apt-get update -y

# Install Java Development Kit (JDK)
RUN apt-get install -y openjdk-17-jdk

# Verify installation
RUN java -version

# Default command (this can be customized based on your use case)
CMD ["bash"]
