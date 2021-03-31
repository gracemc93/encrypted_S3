variable "api_gateway_name" {
  type        = string
  description = "Name for API gateway"
}

variable "lambda_arn" {
  type        = string
  description = "ARN for lambda"
}

variable "lambda_function_name" {
  type = string
  description = "The name of the lambda function"
}

variable "aws_region" {
  type = string
  description = "Region of deployment"
}

variable "aws_account" {
  type = string
  string = "Account to deploy in"
}