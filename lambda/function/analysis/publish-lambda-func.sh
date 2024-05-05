#!/bin/bash -ex
zip my_deployment_package.zip lambda_function.py

export FUNC_NAME="title_video_analysis"
aws lambda create-function --function-name ${FUNC_NAME} \
    --runtime python3.9 \
    --architectures "arm64" \
    --handler lambda_function.lambda_handler \
    --role arn:aws:iam::897855062982:role/lambda-ex \
    --zip-file fileb://my_deployment_package.zip
    
aws lambda update-function-configuration --function-name ${FUNC_NAME} \
    --cli-binary-format raw-in-base64-out \
    --layers "arn:aws:lambda:ap-northeast-2:897855062982:layer:python-requests-layer:1"

aws lambda invoke --function-name ${FUNC_NAME} \
    --cli-binary-format raw-in-base64-out \
    --payload '{ "key": "value" }' response.json