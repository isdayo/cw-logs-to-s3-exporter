import boto3
import os
import logging
import time

LOG_GROUP_TO_EXPORT = os.environ.get("LOG_GROUP_TO_EXPORT")
S3_BUCKET = os.environ.get("S3_BUCKET")


logger = logging.getLogger()
logger.setLevel(logging.INFO)

log_client = boto3.client("logs")
ssm_client = boto3.client("ssm")

def lambda_handler(event, context):
    log_group_to_export = get_log_group()
    ssm_parameter = "last_export_time"
    export_from_time = int(get_last_export(ssm_parameter))
    export_to_time = int(time.time() * 1000)
    if not ((export_to_time - export_from_time) < (24 * 60 * 60 * 1000)):
        try:
            response = log_client.create_export_task(
                logGroupName=log_group_to_export,
                fromTime=export_from_time,
                to=export_to_time,
                destination=S3_BUCKET
            )
            logger.info("Done. {} export to {} S3 bucket is completed!".format(log_group_to_export, S3_BUCKET))
        except Exception as e:
            logger.error("Task failed to be exported")
            print("Exporting error: {}".format(e))
        finally:
            ssm_response = ssm_client.put_parameter(
            Name=ssm_parameter,
            Type="String",
            Value=str(export_to_time),
            Overwrite=True)

def get_last_export(ssm_parameter):
    ssm_parameter_name = ssm_parameter
    try:
        ssm_response = ssm_client.get_parameter(Name=ssm_parameter_name)
        ssm_value = ssm_response['Parameter']['Value']
        return ssm_value
    except Exception as e:
        logger.error("Fail to get last export time from SSM")
        print("Error: {}".format(e))

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
