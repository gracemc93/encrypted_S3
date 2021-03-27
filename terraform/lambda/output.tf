output "cloudwatch_log_group" {
  description = "Cloudwatch log group used to log"
  value       = aws_cloudwatch_log_group.aws_lambda_function_log_group.name
}

output "aws_lambda_function" {
  description = "The created lambda function"
  value       = aws_lambda_function.aws_lambda_function
}
