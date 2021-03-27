locals {
  aws_lambda_function_name                        = "lmb-${var.aws_region}-${terraform.workspace}-${var.function_name}"
  aws_lambda_function_role_policy_name            = "pol-${var.aws_region}-${terraform.workspace}-${var.function_name}"
  aws_lambda_function_role_name                   = "role-${var.aws_region}-${terraform.workspace}-${var.function_name}"
}
