import os
import boto3
import urllib3
import json

DEFAULT_REGION = 'us-west-2'
DEFAULT_CLUSTER = 'minecraft'
DEFAULT_SERVICE = 'minecraft-server'

REGION = os.environ.get('REGION', DEFAULT_REGION)
CLUSTER = os.environ.get('CLUSTER', DEFAULT_CLUSTER)
SERVICE = os.environ.get('SERVICE', DEFAULT_SERVICE)
DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL', None)

if not DISCORD_WEBHOOK_URL:
    raise ValueError("Missing DISCORD_WEBHOOK_URL environment variable")

http = urllib3.PoolManager()

def lambda_handler(event, context):
    """Updates the desired count for a service."""

    ecs = boto3.client('ecs', region_name=REGION)
    response = ecs.describe_services(
        cluster=CLUSTER,
        services=[SERVICE],
    )

    desired = response["services"][0]["desiredCount"]

    if desired == 0:
        ecs.update_service(
            cluster=CLUSTER,
            service=SERVICE,
            desiredCount=1,
        )
        print("Updated desiredCount to 1")
        send_discord_message('Server starting (please wait 1 minute before attempting again) ...')
    else:
        print("desiredCount already at 1")


def send_discord_message(message):
    """Sends a message to a Discord webhook."""
    data = {
        "content": message
    }
    encoded_data = json.dumps(data).encode('utf-8')
    response = http.request(
        'POST',
        DISCORD_WEBHOOK_URL,
        body=encoded_data,
        headers={'Content-Type': 'application/json'}
    )
    if response.status != 204:
        print(f"Failed to send message to Discord: {response.status} - {response.data.decode('utf-8')}")
    else:
        print("Notification sent to Discord.")
