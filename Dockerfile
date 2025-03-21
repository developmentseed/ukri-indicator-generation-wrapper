FROM amazonlinux:latest

# Install dependencies
RUN yum install -y awscli

# Set working directory
WORKDIR /app

# Copy the Bash script into the container
COPY prepare-output.sh /prepare-output.sh

# Ensure script is executable
RUN chmod +x /prepare-output.sh

# Set entrypoint to use the script
ENTRYPOINT ["bash", "/prepare-output.sh"]
