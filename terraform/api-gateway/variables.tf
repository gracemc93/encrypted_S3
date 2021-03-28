variable "api_gateway_name" {
  type        = string
  description = "Name for API gateway"
}

variable "lambda_arn" {
  type = string
  description = "arn for lambda"
}

variable "lambda_function_name" {
  type = string
}

variable "aws_region" {
  type = string
}

variable "aws_account" {
  type = string
}