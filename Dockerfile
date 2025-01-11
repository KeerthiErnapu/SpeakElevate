# Use OpenJDK image as base for LanguageTool
FROM openjdk:17-jdk-slim

# Install Python 3 and dependencies
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip python3-venv curl unzip && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    apt-get clean

# Verify Java and Python installations
RUN java -version
RUN python --version
RUN pip3 --version

# Set the working directory
WORKDIR /app

# Copy the app files into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download LanguageTool binary for language_tool_python
RUN mkdir -p ~/.cache/language_tool_python && \
    curl -L -o ~/.cache/language_tool_python/LanguageTool-stable.zip https://languagetool.org/download/LanguageTool-stable.zip && \
    unzip ~/.cache/language_tool_python/LanguageTool-stable.zip -d ~/.cache/language_tool_python/

# Expose necessary port
EXPOSE 5000

# Default command to run the Python app
CMD ["python", "app.py"]
