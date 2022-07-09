#!/usr/bin/env bash

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color


echo -e "\nSpecify the ${GREEN}S3 bucket name${NC} for storing the templates."
read -r S3_BUCKET_NAME

echo -e "Enter the ${GREEN}AWS REGION${NC} to deploy the Cloudformation Stack [default: ${BLUE}ap-southeast-1${NC}]"
read -r AWS_REGION
if [[ -z "$AWS_REGION" ]]; then
    AWS_REGION=ap-southeast-1
fi

#cd templates || exit
#zip -r templates.zip ./* -x *~
#aws s3 cp templates.zip s3://${S3_BUCKET_NAME}/
#rm templates.zip
#cp ../infrastructure-pipeline.yaml .
sed -i -e "s@S3_BUCKET_NAME@${S3_BUCKET_NAME}@g" main.yaml
#TAG_NAME=$(echo "${S3_BUCKET_NAME}" | cut -d'-' -f2)
#sed -i -e "s@TAG_NAME@${TAG_NAME}@g" infrastructure-pipeline.yaml
aws s3 cp main.yaml s3://${S3_BUCKET_NAME}/
aws s3 cp lambda_function.py s3://${S3_BUCKET_NAME}/

URL="https://console.aws.amazon.com/cloudformation/home?region=${AWS_REGION}#/stacks/new?templateURL=https://s3.amazonaws.com/${S3_BUCKET_NAME}/main.yaml"
echo -e "\nOpen the Link in Browser:\n${GREEN}${URL}${NC}"