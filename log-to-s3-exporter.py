import boto3
import os
import logging
import time

LOG_GROUP_TO_EXPORT = os.environ.get("LOG_GROUP_TO_EXPORT")
S3_BUCKET = os.environ.get("S3_BUCKET")


logger = logging.getLogger()
logger.setLevel(logging.INFO)

log_client = boto3.client("logs")

def lambda_handler(event, context):
    log_group_to_export = get_log_group()
    # TODO: 
    # 1. Create ssm_value to store current time in ParameterStore
    # 2. Add ParameterStore permission to retrieve ssm_value to the IAM role 
    # 3. Update ssm_value to value from parameter store
    ssm_value = int((3600*2 + 60*30 + 5)*1000)
    export_to_time = int(time.time() *1000)
    try:
        response = log_client.create_export_task(
            logGroupName=log_group_to_export,
            fromTime=int(ssm_value),
            to=export_to_time,
            destination=S3_BUCKET
        )
        logger.info("Done. {} export to {} S3 bucket is completed!".format(log_group_to_export, S3_BUCKET))
    except Exception as e:
        logger.error("Task failed to be exported")
        print("Exporting error: {}".format(e))

def get_log_group():
    parameters_dict = dict()
    log_groups = []
    
    logger.info('Retrieving logGroup to export ...')
    while True:
        res = log_client.describe_log_groups(**parameters_dict)
        log_groups.append(res["logGroups"])
        if not "nextToken" in res:
            break
        else:
            parameters_dict['nextToken'] = res["nextToken"]
    for log_group in log_groups[0]:
        if log_group['logGroupName'] ==  LOG_GROUP_TO_EXPORT:
            logger.info("logGroup retrieved!")
            return log_group['logGroupName']
