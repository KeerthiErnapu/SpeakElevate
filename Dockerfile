# Use an official base image with Java support
FROM openjdk:17-jdk-slim

# Set the working directory inside the container
WORKDIR /app

# Copy your application code to the container
COPY . /app

# Install additional dependencies if needed
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Expose the port your application runs on (adjust as necessary)
EXPOSE 8080

# Command to run your Java application
# Replace 'App' with your compiled Java class name (if using .class files) 
# or JAR file name (if using a packaged JAR)
CMD ["java", "-jar", "your-application.jar"]
