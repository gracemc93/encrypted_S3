# Encrypted-S3


![alt text](https://github.com/gracemc93/Encrypted-S3/blob/master/arch.png?raw=true)

## Requirements
Create a simple AWS lambda function that shows the encryption status of S3 buckets.

1. With no input, shows all S3 buckets.

2. If given an S3 bucket name, shows information for that S3 bucket.

3. Returns the bucket(s), and whether those buckets are encrypted.

 

Write at least one unit and integration test for the lambda.

 

**Bonus points**

Create (or just design) a simple REST API around the lambda function that can return:

* All S3 buckets

* Information for a single S3 bucket

## Solution

### Terraform
Terraform is an open source, infrastrucure as code tool which can be used to deploy and maintain your AWS infrastucture.
The deploymeny/configuration of the resources used for this assessment is written using terraform, so they can be reproduced.

### Encryption Checker Lambda 
A simple lambda was created, written in python. The lambda takes a JSON object.
1. If the object is empty, the lambda will return all buckets in the account and whether they are encrypted or not encrypted.
2. If the object contains a list of buckets (1 or more bucket names) it will return that bucket(s) with the encryption status.
This Lambda's role is granted permission to `GetEncryptionConfiguration` and `ListAllMyBuckets`

## Gateway API
A Gateway API to provide an endpoint to access the lambda as a REST API.

## S3 Buckets
Two S3 buckets were created to test on. One which is encrypted and one not encrypted. 

## Integration Tests
**Please Note:** For the integration tests, the resources need to be deployed. You will need to be logged in via the AWS CLI and have Terraform installed.
These send requests to the API Gateway via the invoke URL created. These tests excercise the whole system, and test the communication and permissions between the resources.

## Unit Tests
The unit tests test the lambda functionality itself locally. It does not need to be deployed. 

## How To Run
In order to run, you will need:
1. Terraform installed https://www.terraform.io/downloads.html
2. AWS CLI installed, and logged into the account you want to deploy to.
