#!/bin/bash -ex

aws lambda publish-layer-version --layer-name python-requests-layer \
    --zip-file fileb://layer_content.zip \
    --compatible-runtimes python3.9 \
    --compatible-architectures "arm64"