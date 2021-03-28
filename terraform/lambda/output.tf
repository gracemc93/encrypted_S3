output "aws_lambda_function" {
  description = "The created lambda function"
  value       = aws_lambda_function.aws_lambda_function.invoke_arn
}

output "aws_lambda_name" {
  value = aws_lambda_function.aws_lambda_function.function_name
}
