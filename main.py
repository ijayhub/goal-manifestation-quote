import boto3
# define the AWS service you want to use in my case s3
client = boto3.client('s3')


# Request syntax
response = client.create_bucket(
    Bucket='string', #change to your bucket name
    CreateBucketConfiguration={
        'LocationConstraint': 'eu-west-2', #change to your region
    },

)