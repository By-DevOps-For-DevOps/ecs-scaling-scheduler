import json
import boto3


def lambda_handler(event, context):
    # The cloudwatch alarm sends a parameter called 'action' which is set to 'start' or 'stop'
    # Lambda decides depending on the value whether to start or stop the container
    action = event.get('action')

    # The cloudwatch alarm sends a parameter called 'cluster' which contains the ecs cluster name
    cluster_name = event.get('cluster')

    client = boto3.client('ecs')

    # Query to the ECS API to get all running services
    # Output limit is currently set to 50
    response = client.list_services(
        cluster=cluster_name,
        maxResults=50,
        launchType='FARGATE',
        schedulingStrategy='REPLICA'
    )

    # Retrieves only the plain service arns from the output
    # Values are stored in a list
    service_list = response['serviceArns']
    print(service_list)

    print(action)

    if 'start' == action:
        start_container(service_list, cluster_name)
    elif 'stop' == action:
        stop_container(service_list, cluster_name)

    return {
        'statusCode': 200,
        'body': json.dumps('Script finished')
    }


# Sets the desired count of tasks per service to 1
# Container will spawn after a few moments
def start_container(servicearns, clusterName):
    client = boto3.client('ecs')
    for srv in servicearns:
        response_update = client.update_service(
            cluster=clusterName,
            service=srv,
            desiredCount=1,
        )


# Sets the desired count of tasks per service to 0
# Services still runs but without any container
def stop_container(servicearns, clusterName):
    client = boto3.client('ecs')
    for srv in servicearns:
        response_update = client.update_service(
            cluster=clusterName,
            service=srv,
            desiredCount=0,
        )
