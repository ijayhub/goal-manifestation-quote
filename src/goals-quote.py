import os
import json
import urllib.request
import boto3

def fetch_random_quote():
    """Fetches a random quote from the ZenQuotes API."""
    api_url = "https://zenquotes.io/api/random"
    try:
        with urllib.request.urlopen(api_url) as response:
            data = json.loads(response.read().decode())
            if data and isinstance(data, list):
                # Format the quote and author
                quote = data[0].get("q", "No quote available")
                author = data[0].get("a", "Unknown author")
                return f'"{quote}" - {author}'
            else:
                return "No quote available."
    except Exception as e:
        print(f"Error fetching random quote: {e}")
        return "Failed to fetch quote."

def lambda_handler(event, context):
    # Get the SNS topic ARN from environment variables
    sns_topic_arn = os.getenv("SNS_TOPIC_ARN")
    sns_client = boto3.client("sns")
    
    # Fetch a random quote
    quote = fetch_random_quote()
    print(f"Fetched Quote: {quote}")
    
    # Publish the quote to SNS
    try:
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=quote,
            Subject="Daily Random Quote to help you stay motivated and inspired to achieve your goals",
        )
        print("Quote published to SNS successfully.")
    except Exception as e:
        print(f"Error publishing to SNS: {e}")
        return {"statusCode": 500, "body": "Error publishing to SNS"}
    
    return {"statusCode": 200, "body": "Quote sent to SNS"}

