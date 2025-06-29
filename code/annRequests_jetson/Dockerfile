FROM nvcr.io/nvidia/l4t-cuda:10.2.460-runtime
 
# Copy application code into the container
COPY . /codeBase/

# Install system packages required by Tensorflow
RUN apt update && apt install -y libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran

# Install and upgrade pip3
RUN apt install -y python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install testresources 
RUN pip3 install setuptools==49.6.0

# Install Python package dependencies
RUN pip3 install matplotlib
RUN pip3 install pillow
RUN pip3 install paho-mqtt
RUN pip3 install numpy==1.19.5
RUN pip3 install scipy
RUN pip3 install future==0.18.2
RUN pip3 install mock==3.0.5
RUN pip3 install keras_preprocessing==1.1.2
RUN pip3 install keras_applications==1.0.8
RUN pip3 install gast==0.4.0
RUN pip3 install protobuf
RUN pip3 install pybind11
RUN pip3 install cython
RUN pip3 install pkgconfig
RUN pip3 install packaging
RUN pip3 install h5py==2.10.0
 
# Install Tensorflow
RUN pip3 install --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v461 tensorflow==1.15.5+nv22.1