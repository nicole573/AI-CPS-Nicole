FROM nvcr.io/nvidia/l4t-base:r32.7.6-tf2.7-py3

# Set working directory
WORKDIR /app

# Copy application code into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir \
    matplotlib \
    Pillow \
    paho-mqtt \
    numpy

# Install TensorFlow for Jetson Nano (prebuilt wheel)
RUN pip3 install --no-cache-dir \
    https://developer.download.nvidia.com/compute/redist/jp/v46/tensorflow/tensorflow-2.11.0+nv22.06-cp36-cp36m-linux_aarch64.whl

