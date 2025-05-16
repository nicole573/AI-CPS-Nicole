# Use TensorFlow base image with CPU support
FROM tensorflow/tensorflow:latest

# Set working directory
WORKDIR /app

# Copy application code into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir \
    matplotlib \
    Pillow \
    tflite-runtime \
    paho-mqtt \
    numpy

# If using Coral USB or Dev Board Edge-TPU, install runtime library
# (Uncomment if needed)
# RUN echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" \
#     | tee /etc/apt/sources.list.d/coral-edgetpu.list && \
#     apt-get update && apt-get install -y libedgetpu1-std && rm -rf /var/lib/apt/lists/*

# Default command to execute your script (adjust filenames/args)
CMD ["python3", "apply_annSolution_custom.py", "sender1", "receiver1"]
