variable "aws_region" {
  type        = string
  description = "The AWS region"
}

variable "function_name" {
  type        = string
  description = "A unique name for your Lambda Function"
}

variable "handler" {
  type        = string
  description = "The function entrypoint in your code"
  default     = "lambda_function.handle"
}

variable "runtime" {
  type        = string
  description = "The identifier of the function's runtime. https://docs.aws.amazon.com/lambda/latest/dg/API_CreateFunction.html#SSS-CreateFunction-request-Runtime"
}

variable "timeout" {
  type        = number
  description = "The amount of time your Lambda Function has to run in seconds"
  default     = 900
}

variable "source_dir" {
  type = string
  description = "Source directory for lambda code"
}