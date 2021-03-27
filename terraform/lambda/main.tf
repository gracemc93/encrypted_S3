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

///////////// POLICIES REQUIRED BY THE LAMBDA FUNCTION CODE //////////////////

//we attach the policies (required for the lambda function) to the role above
resource "aws_iam_role_policy" "aws_lambda_function_role_policy" {
  name   = "${local.aws_lambda_function_role_policy_name}-${count.index}"
  count  = length(var.policies_json_str)
  policy = var.policies_json_str[count.index]
  role   = aws_iam_role.aws_lambda_function_role.id
}

//////////////////////////// LAMBDA FUNCTION CODE ////////////////////////////

//we create the deployment package for the lambda function
data "archive_file" "aws_lambda_function_zip" {
  type        = "zip"
  source_dir  = var.source_dir
  output_path = "temp/${local.aws_lambda_function_name}.zip"
}

//we define the lambda function, based on the deployment package
resource "aws_lambda_function" "aws_lambda_function" {
  function_name    = local.aws_lambda_function_name
  handler          = var.handler
  role             = aws_iam_role.aws_lambda_function_role.arn
  runtime          = var.runtime
  filename         = data.archive_file.aws_lambda_function_zip.output_path
  source_code_hash = filebase64sha256(data.archive_file.aws_lambda_function_zip.output_path)
  timeout          = var.timeout
}