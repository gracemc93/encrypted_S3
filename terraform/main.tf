module "encryption_checker_lambda" {
  aws_region    = var.aws_region
  source        = "git::https://github.com/gracemc93/Encryptd-S3/blob/master/encryption-checker-lambda/lambda_function.py"
  function_name = "encryption_checker"
  policies_json_str = [
    data.aws_iam_policy_document.encryption_checker_s3_policy
  ]
  handler           = "encryption_checker/lambda_function.lambda_handler"
  runtime           = "python3.7"
}