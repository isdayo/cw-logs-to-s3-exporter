# LogGroup exporter to S3 bucket
The automation exports logs from a specific AWS LogGroup to S3 bucket. The directory contains the following.

```.
    ├── IAM permissions
    │   ├── bucket_policy.json
    │   └── iam_role.json
    ├── README.md
    ├── diagram
    │   └── logs-to-s3-archi.png
    └── log-to-s3-exporter.py
```
The `IAM permissions` directory contains the bucket policy for the destination S3 bucket and the IAM role permissions for the automation (AWS Lambda). The `iam_role.json` file contains the IAM policy for the lambda role and the service trust relationship policy.

Set the following environment variables in the Lambda Configuration before executing the lambda function:
* LOG_GROUP_TO_EXPORT
* S3_BUCKET


TODO:
 - EventBridge scheduling for the Lambda automation to export the bucket at regular intervals
 - Create a parameter to store the last export time in ParameterStore
 - Add ParameterStore permission to retrieve ssm_value to the IAM role
 - IaC to roll-out and tear-down all the design components - Lambda function, IAM role, bucket creation and bucket policy, EventBridge scheduler


References:
1. Tool for architectural diagram - https://app.diagrams.net/?src=about
2. https://dnx.solutions/exporting-cloudwatch-logs-automatically-to-s3-with-a-lambda-function/
3. https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/S3ExportTasksConsole.html