FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ="America/Denver"

RUN apt-get update && apt-get install --no-install-recommends -y \
    python3 python3-pip libgl1 libglib2.0-0 git sudo && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Ultralytics
RUN pip install --no-cache-dir ultralytics onnx PyYAML

WORKDIR /workspace

# We will mount these as volumes, but let's prep the entrypoint
COPY ./entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
COPY ./train.py /workspace/train.py

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]