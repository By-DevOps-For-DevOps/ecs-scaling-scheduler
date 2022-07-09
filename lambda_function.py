import json
import boto3


def lambda_handler(event, context):
    ### The cloudwatch alarm sends a parameter called 'action' which is set to 'start' or 'stop'
    ### Lambda decides depending on the value whether to start or stop the container
    cwValue = event.get('action')

    ### The cloudwatch alarm sends a parameter called 'cluster' which contains the ecs cluster name
    clusterName = event.get('cluster')

    client = boto3.client('ecs')

    ### Query to the ECS API to get all running services
    ### Output limit is currently set to 50
    try:
        response = client.list_services(
            cluster=clusterName,
            maxResults=50,
            launchType='FARGATE',
            schedulingStrategy='REPLICA'
        )
    except:
        print("didn't worked")

    ### Retrieves only the plain service arns from the output
    ### Values are stored in a list
    serviceList = response['serviceArns']
    print(serviceList)

    print(cwValue)

    if 'start' == cwValue:
        spawncontainer(serviceList, clusterName)
    elif 'stop' == cwValue:
        stopcontainer(serviceList, clusterName)

    return {
        'statusCode': 200,
        'body': json.dumps('Script finished')
    }


### Sets the desired count of tasks per service to 1
### Container will spawn after a few moments
def spawncontainer(servicearns, clusterName):
    client = boto3.client('ecs')
    for srv in servicearns:
        responseUpdate = client.update_service(
            cluster=clusterName,
            service=srv,
            desiredCount=1,
        )


### Sets the desired count of tasks per service to 0
### Services still runs but without any container
def stopcontainer(servicearns, clusterName):
    client = boto3.client('ecs')
    for srv in servicearns:
        responseUpdate = client.update_service(
            cluster=clusterName,
            service=srv,
            desiredCount=0,
        )
