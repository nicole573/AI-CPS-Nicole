FROM nvcr.io/nvidia/l4t-cuda:12.6.11-runtime

# Set working directory
WORKDIR /app

# Copy application code into the container
COPY . /codeBase/

# Install pip
RUN apt-get update
RUN apt-get install -y python3-pip

# Install Python dependencies
RUN pip3 install --no-cache-dir \
    matplotlib \
    Pillow \
    paho-mqtt \
    numpy \
    scipy \
    tensorflow


