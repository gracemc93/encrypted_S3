variable "aws_account" {
  type        = string
  description = "The AWS acount to use"
}

variable "aws_region" {
  type        = string
  description = "The region in which to initialize the aws provider"
}

variable "aws_region_map" {
  description = "AWS region name by AWS region"
  type = map(string)
}