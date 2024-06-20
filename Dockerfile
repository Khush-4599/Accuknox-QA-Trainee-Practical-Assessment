# Use an official Ubuntu as a parent image
FROM ubuntu:20.04

# Set environment variables to non-interactive for apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Update and install dependencies
RUN apt-get update && apt-get install -y \
    cowsay \
    fortune \
    netcat \
    && rm -rf /var/lib/apt/lists/*

# Create a working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Make the script executable
RUN chmod +x wisecow.sh

# Expose the port the server will run on
EXPOSE 4499

# Run the script
CMD ["./wisecow.sh"]
