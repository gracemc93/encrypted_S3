//File from which we call the
locals {
  bucket_name                    = "s3-${var.aws_region}-${terraform.workspace}-encrypted-bucket-test"
  encryption_checker_api_gateway = "api-${var.aws_region}-${terraform.workspace}-encryption-checker"
}
module "encryption_checker_lambda" {
  aws_region    = var.aws_region
  source        = "./lambda"
  function_name = "encryption_checker"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.7"
  timeout       = 30
  source_dir = "../encryption_checker_lambda"
}

module "encrypted_s3_bucket" {
  source      = "./s3"
  aws_region  = var.aws_region
  bucket_name = local.bucket_name
}

module "encryption_checker_api" {
  source               = "./api-gateway"
  api_gateway_name     = local.encryption_checker_api_gateway
  lambda_arn           = module.encryption_checker_lambda.aws_lambda_function
  lambda_function_name = module.encryption_checker_lambda.aws_lambda_name
  aws_region           = var.aws_region
  aws_account          = var.aws_account
}
