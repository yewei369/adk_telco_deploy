# Stage 0: Main Application - for building your actual service
FROM python:3.12-slim-bookworm

# Set the working directory in the container
WORKDIR /app

# Set environment variable to avoid prompts during apt-get install
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages for build environment and potential debugging
RUN apt-get update && \
    apt-get install -y --no-install-recommends git dnsutils curl && \
    rm -rf /var/lib/apt/lists/*

# --- CRITICAL NETWORK FIX: Force Google Public DNS ---
# This addresses Errno -2 "Name or service not known" errors.
#RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf
# --- End CRITICAL NETWORK FIX ---

# Copy your application code and requirements.txt
COPY . /app

# Upgrade pip to its latest version first
RUN pip install --no-cache-dir --upgrade pip

# Install common Python dependencies from requirements.txt (excluding ADK)
# This will use pypi.org (default).
# Install without dependencies to isolate ADK later
RUN pip install -r requirements.txt --no-deps 

# --- CRITICAL ISOLATED ADK INSTALL ---
# This step specifically installs google-agent-development-kit with the flags
# that might be necessary.
#RUN pip install google-agent-development-kit --pre --extra-index-url https://pypi.google.com/pypi
# --- End CRITICAL ISOLATED ADK INSTALL ---

# Expose the port that the app runs on
EXPOSE 8080

# Run the application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]