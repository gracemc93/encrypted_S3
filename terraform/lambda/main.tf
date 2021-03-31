//we create a role for the lambda function
resource "aws_iam_role" "aws_lambda_function_role" {
  name               = local.aws_lambda_function_role_name
  assume_role_policy = data.aws_iam_policy_document.aws_lambda_function_assume_role_policy_doc.json
}

//the policy grants the lambda function permission to assume the role above
data "aws_iam_policy_document" "aws_lambda_function_assume_role_policy_doc" {
  statement {
    actions = [
      "sts:AssumeRole",
    ]
    principals {
      identifiers = [
      "lambda.amazonaws.com"]
      type = "Service"
    }
  }
}

//Minimum policies needed by Lambda to access S3
resource "aws_iam_policy" "encryption_checker_policy" {
  name        = "test-policy"
  description = "A test policy"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "s3:GetEncryptionConfiguration",
            "Resource": "arn:aws:s3:::*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": "s3:ListAllMyBuckets",
            "Resource": "*"
        }
    ]
}
EOF
}

//Attach policy to role
resource "aws_iam_role_policy_attachment" "attach_encryption_policy" {
  role       = aws_iam_role.aws_lambda_function_role.name
  policy_arn = aws_iam_policy.encryption_checker_policy.arn
}

//////////////////////////// LAMBDA FUNCTION CODE ////////////////////////////

//Create the deployment package for the lambda function
data "archive_file" "aws_lambda_function_zip" {
  type        = "zip"
  source_dir  = var.source_dir
  output_path = "temp/${local.aws_lambda_function_name}.zip"
}

//Lambda function definition
resource "aws_lambda_function" "aws_lambda_function" {
  function_name    = local.aws_lambda_function_name
  handler          = var.handler
  role             = aws_iam_role.aws_lambda_function_role.arn
  runtime          = var.runtime
  filename         = data.archive_file.aws_lambda_function_zip.output_path
  source_code_hash = filebase64sha256(data.archive_file.aws_lambda_function_zip.output_path)
  timeout          = var.timeout
}