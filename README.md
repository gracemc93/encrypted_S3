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
Terraform is an open source, infrastructure as code tool which can be used to deploy and maintain your AWS infrastucture.
The deployment/configuration of the resources used for this assessment is written using terraform, so they can be reproduced.

### Encryption Checker Lambda 
A simple lambda was created, written in python. The lambda takes a JSON object.
1. If empty, the lambda will return all buckets in the account and whether they are encrypted or not encrypted.
2. If it contains a list of buckets (1 or more bucket names) it will return the bucket(s) with the encryption status.
This Lambda's role is granted permission to `GetEncryptionConfiguration` and `ListAllMyBuckets`

### Gateway API
A Gateway API to provide an endpoint to access the lambda as a REST API.

### S3 Buckets
Two S3 buckets were created to test on. One which is encrypted and one not encrypted. 

### Integration Tests
These send requests to the API Gateway via the invoke URL created. These tests excercise the whole infrastrucuture, and test the communication and permissions between the resources.

### Unit Tests
The unit tests test the lambda code functionality itself locally. These are located under:
`encrypted_S3/test/unittests/`

![alt text](coverage_report.PNG?raw=true)

## How To Run
### Prequisites
In order to run, you will need:
1. You **MUST update** the var file needed for the Terraform to deploy. You will need to update the `aws_region` and `aws_account` to where you want to deploy. It is located under `encrypted_S3/terraform/test.tfvars`
2. Terraform installed https://www.terraform.io/downloads.html
3. AWS CLI installed, and logged into the account you want to deploy to.
4. Install the provided requirements.txt

### Integration Tests
The integration tests will create the AWS infrastructure with Terraform and send some requests to the Gateway API via the invoke url. These will test if everything is integrated and the correct permissions are in place to allow communication. It will then tear down the infrastructure. 
These will take a few minutes to complete.

1. Ensure you have updated the var file detailed in the prequisite section.
1. Navigate to `encrypted_S3/integration` and run 
2. Run `pytest -s test_integration.py`

### Terraform
If you would like to deploy the infrastructure, have a look at it and invoke the API yourself, you need to do the following:

1. Ensure you have updated the var file detailed in the prequisite section.
2. Navigate to `encrypted_S3/terraform/`
3. Run `terraform apply --var-file=test-tfvars`
4. A plan of what is to be created should be displayed, enter Yes to approve.
5. After they are created, you should see the URL for the REST API in the terminal under Outputs `url_to_encryption_checker`
6. You will also see two S3 buckets, one is encrypted one is not, you can use those to test the lambda.
7. Use a tool like Postman to call the API. You should do a POST request. An example of the request body should look like: 
 
 `{
   "Buckets":[
      "some_bucket_name_1",
      "some_bucket_name_2"
   ]
}`

8. When you are ready to destroy the infrastructure, just run
 `terraform destroy --var-file=test.tfvars`
