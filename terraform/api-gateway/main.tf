resource "aws_api_gateway_rest_api" "api_gateway" {
  name = var.api_gateway_name
    endpoint_configuration {
    types = ["REGIONAL"]
  }
}

resource "aws_api_gateway_resource" "api_gateway_resource" {
  rest_api_id = aws_api_gateway_rest_api.api_gateway.id
  parent_id   = aws_api_gateway_rest_api.api_gateway.root_resource_id
  path_part   = "demo"
}

//resource "aws_api_gateway_method" "get-method" {
//  rest_api_id   = aws_api_gateway_rest_api.api_gateway.id
//  resource_id   = aws_api_gateway_resource.api_gateway_resource.id
//  http_method   = "GET"
//  authorization = "NONE"
//}

resource "aws_api_gateway_method" "post-method" {
  rest_api_id   = aws_api_gateway_rest_api.api_gateway.id
  resource_id   = aws_api_gateway_resource.api_gateway_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

//resource "aws_api_gateway_integration" "get-integration" {
//  rest_api_id             = aws_api_gateway_rest_api.api_gateway.id
//  resource_id             = aws_api_gateway_resource.api_gateway_resource.id
//  http_method             = aws_api_gateway_method.get-method.http_method
//  integration_http_method = "GET"
//  type                    = "AWS"
//  uri                     = var.lambda_arn
//}

resource "aws_api_gateway_integration" "post-integration" {
  rest_api_id             = aws_api_gateway_rest_api.api_gateway.id
  resource_id             = aws_api_gateway_resource.api_gateway_resource.id
  http_method             = aws_api_gateway_method.post-method.http_method
  integration_http_method = "POST"
  type                    = "AWS"
  uri                     = var.lambda_arn
}

resource "aws_lambda_permission" "apigw_lambda" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_function_name
  principal     = "apigateway.amazonaws.com"

  # More: http://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-control-access-using-iam-policies-to-invoke-api.html
  source_arn = "arn:aws:execute-api:${var.aws_region}:${var.aws_account}:${aws_api_gateway_rest_api.api_gateway.id}/*/${aws_api_gateway_method.post-method.http_method}${aws_api_gateway_resource.api_gateway_resource.path}"
}

resource "aws_api_gateway_method_response" "gateway_method_response" {
  rest_api_id = aws_api_gateway_rest_api.api_gateway.id
  resource_id = aws_api_gateway_resource.api_gateway_resource.id
  http_method = aws_api_gateway_method.post-method.http_method
  status_code = "200"
}

resource "aws_api_gateway_integration_response" "gateway_integration_response" {
  rest_api_id = aws_api_gateway_rest_api.api_gateway.id
  resource_id = aws_api_gateway_resource.api_gateway_resource.id
  http_method = aws_api_gateway_method.post-method.http_method
  status_code = aws_api_gateway_method_response.gateway_method_response.status_code
  depends_on = [
    aws_api_gateway_integration.post-integration
  ]
}

resource "aws_api_gateway_deployment" "gateway_deployment" {
  rest_api_id = aws_api_gateway_rest_api.api_gateway.id
  depends_on = [
    aws_api_gateway_method.post-method,
    aws_api_gateway_integration.post-integration
  ]
}

resource "aws_api_gateway_stage" "api_gateway_stage" {
  deployment_id = aws_api_gateway_deployment.gateway_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.api_gateway.id
  stage_name    = "Demo"
  lifecycle {
    # a new deployment needs to be created on every resource change so we do it outside of terraform
    ignore_changes = [deployment_id]
  }
}
