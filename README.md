## Overview

Scales all ecs service to 0 or 1 on a specific schedule

## Architecture

The lambda receives an 'action' value from Cloudwatch which is set to 'start' or 'stop'.
Additionally, the Cloudwatch rules submit the ECS Cluster name to the lambda.

Lambda uses the cluster name to query all services and put them into a list. Afterward
it iterates over this list and set the 'desired task count' to 1 or 0, depending on the 'action' value as shown in the figure below.

![architecture](./docs/architecture.drawio.svg)

## Prerequisite

Create S3 bucket in advance to store your Cloudformation and Lambda code.
## How to setup

Follow the instruction from the following command:
```shell
bash ./bin/configure.sh
```

## Manual invocation

Sometimes, you might need to start non-production ECS cluster manually.
Please, use the following command to start your cluster:
```shell
bash bin/manually.sh start ECS_CLUSTER_NAME
```
or to stop:
```shell
bash bin/manually.sh stop ECS_CLUSTER_NAME
```

## Code and Configs


<details>
<summary>CloudFormation: main.yaml</summary>

Deploys the following resources to AWS:
1. AWS Lambda -> for scaling the ECS Services
1. AWS Cloudwatch rules -> one to send start command to Lambda, one for sending a stop command
1. AWS IAM Role -> IAM Role to attach to the Lambda Function
1. AWS IAM Policy -> Permissions for Lambda to write to CloudWatch Loggroups, and full ECS permissions

</details>

<details>
<summary>Lambda: lambda_function.py</summary>

Python3.9 script to scale all ECS services of a specific cluster either to 0 or 1.
The lambda takes the Cloudwatch Rule parameter for 'action' and 'cluster' to determine,
if the services should start or stop and on which cluster.

The zip file of `lambda_function.py` will be uploaded to an S3 bucket before we run the Cloudformation code by `bash ./bin/configure.sh` command. 
The bucket name and the file key, needs to be entered in cloudformation. The cloudformation template
uses this information to pass the python code to the lambda function during its creation.

</details>


