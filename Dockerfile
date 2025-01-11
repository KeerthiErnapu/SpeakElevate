# Use OpenJDK image as base
FROM openjdk:17-jdk-slim

# Install Python 3 and dependencies
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip python3-venv && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    apt-get clean

# Verify Java and Python installations
RUN java -version
RUN python --version
RUN pip3 --version

# Set the working directory (adjust if your app is in another folder)
WORKDIR /app

# Copy the app files into the container (adjust the path as necessary)
COPY . /app

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Expose necessary port (adjust as needed for your application)
EXPOSE 5000

# Default command to run the Python app (using the CMD from Dockerfile)
CMD ["python", "app.py"]
