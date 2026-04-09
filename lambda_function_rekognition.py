"""
CS 178 - Lab 15: STRETCH GOAL — Lambda Function with AWS Rekognition
lambda_function_rekognition.py

This is a MODIFIED version of the Lab 15 Lambda function.
Instead of (or in addition to) flipping the image, it calls
AWS Rekognition to automatically generate a text description
of what's in the image — like auto alt-text for accessibility.

Your job: fill in the Rekognition API call (marked with TODO below).

What is Rekognition?
  AWS Rekognition is a managed computer vision service. You send it
  an image and it returns labels (e.g. "Dog", "Outdoor", "Sunset")
  with confidence scores, without you training any ML model yourself.

Docs: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/detect_labels.html
"""

import boto3
import json
import os
from io import BytesIO
from PIL import Image

PROCESSED_BUCKET = os.environ.get("PROCESSED_BUCKET", "YOUR-INITIALS-image-source-processed")


def lambda_handler(event, context):
    # ── Extract file info from the S3 trigger event ───────────────────────────
    record = event["Records"][0]
    source_bucket = record["s3"]["bucket"]["name"]
    filename = record["s3"]["object"]["key"]

    print(f"Triggered by upload: s3://{source_bucket}/{filename}")

    # ── Download the image from S3 ────────────────────────────────────────────
    s3 = boto3.client("s3")
    response = s3.get_object(Bucket=source_bucket, Key=filename)
    image_data = response["Body"].read()

    # ── Flip the image (same as the main lab) ─────────────────────────────────
    image = Image.open(BytesIO(image_data))
    flipped = image.transpose(Image.FLIP_TOP_BOTTOM)
    buffer = BytesIO()
    image_format = image.format if image.format else "JPEG"
    flipped.save(buffer, format=image_format)
    buffer.seek(0)

    s3.put_object(
        Bucket=PROCESSED_BUCKET,
        Key=filename,
        Body=buffer,
        ContentType=f"image/{image_format.lower()}",
    )
    print(f"Flipped image saved to: s3://{PROCESSED_BUCKET}/{filename}")

    # ── TODO (Stretch Exercise): Call AWS Rekognition ─────────────────────────
    #
    # Create a Rekognition client and call detect_labels on the ORIGINAL image
    # (still in source_bucket with key=filename).
    #
    # The call looks like this:
    #
    #   rekognition = boto3.client("rekognition", region_name="us-east-1")
    #   result = rekognition.detect_labels(
    #       Image={
    #           "S3Object": {
    #               "Bucket": ???,   # which bucket is the original image in?
    #               "Name": ???,     # what is the S3 key (filename)?
    #           }
    #       },
    #       MaxLabels=10,            # return at most 10 labels
    #       MinConfidence=70,        # only labels Rekognition is ≥70% confident about
    #   )
    #
    # Once you have the result, extract the label names and confidence scores.
    # result["Labels"] is a list of dicts, each with "Name" and "Confidence" keys.
    #
    # Then save a JSON file called f"{filename}_labels.json" to PROCESSED_BUCKET
    # containing the list of labels. Use s3.put_object() like above.
    #
    # Your code here:



    # ── After you complete the TODO, check your processed bucket ──────────────
    # You should see TWO new files for each upload:
    #   1. The flipped image (e.g. "dog.jpg")
    #   2. A labels file    (e.g. "dog.jpg_labels.json")
    # ─────────────────────────────────────────────────────────────────────────

    return {
        "statusCode": 200,
        "body": f"Processed {filename}"
    }
