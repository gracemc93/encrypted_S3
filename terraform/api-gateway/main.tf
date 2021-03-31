//Create API gateway
resource "aws_api_gateway_rest_api" "api_gateway" {
  name = var.api_gateway_name
  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

//Create gateway resource
resource "aws_api_gateway_resource" "api_gateway_resource" {
  rest_api_id = aws_api_gateway_rest_api.api_gateway.id
  parent_id   = aws_api_gateway_rest_api.api_gateway.root_resource_id
  path_part   = "demo"
}

//Create POST method
resource "aws_api_gateway_method" "post-method" {
  rest_api_id   = aws_api_gateway_rest_api.api_gateway.id
  resource_id   = aws_api_gateway_resource.api_gateway_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

//Integrate POST method with lambda
resource "aws_api_gateway_integration" "post-integration" {
  rest_api_id             = aws_api_gateway_rest_api.api_gateway.id
  resource_id             = aws_api_gateway_resource.api_gateway_resource.id
  http_method             = aws_api_gateway_method.post-method.http_method
  integration_http_method = "POST"
  type                    = "AWS"
  uri                     = var.lambda_arn
}

//Define method response for status code 200
resource "aws_api_gateway_method_response" "gateway_method_response" {
  rest_api_id = aws_api_gateway_rest_api.api_gateway.id
  resource_id = aws_api_gateway_resource.api_gateway_resource.id
  http_method = aws_api_gateway_method.post-method.http_method
  status_code = "200"
}

//Define method response for status code 400
resource "aws_api_gateway_method_response" "gateway_method_response_error" {
  rest_api_id = aws_api_gateway_rest_api.api_gateway.id
  resource_id = aws_api_gateway_resource.api_gateway_resource.id
  http_method = aws_api_gateway_method.post-method.http_method
  status_code = "400"
}

//Integration response for status code 200
resource "aws_api_gateway_integration_response" "gateway_integration_response" {
  rest_api_id       = aws_api_gateway_rest_api.api_gateway.id
  resource_id       = aws_api_gateway_resource.api_gateway_resource.id
  http_method       = aws_api_gateway_method.post-method.http_method
  status_code       = aws_api_gateway_method_response.gateway_method_response.status_code
  depends_on = [
    aws_api_gateway_integration.post-integration
  ]
}

//Deployment for the rest api
resource "aws_api_gateway_deployment" "gateway_deployment" {
  rest_api_id = aws_api_gateway_rest_api.api_gateway.id
  depends_on = [
    aws_api_gateway_method.post-method,
    aws_api_gateway_integration.post-integration
  ]
}

//Stage for rest api
resource "aws_api_gateway_stage" "api_gateway_stage" {
  deployment_id = aws_api_gateway_deployment.gateway_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.api_gateway.id
  stage_name    = "Demo"
  lifecycle {
    # a new deployment needs to be created on every resource change so we do it outside of terraform
    ignore_changes = [deployment_id]
  }
}

//Give permission to gateway to invoke lambda
resource "aws_lambda_permission" "apigw_lambda" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_function_name
  principal     = "apigateway.amazonaws.com"
  source_arn = "arn:aws:execute-api:${var.aws_region}:${var.aws_account}:${aws_api_gateway_rest_api.api_gateway.id}/*/${aws_api_gateway_method.post-method.http_method}${aws_api_gateway_resource.api_gateway_resource.path}"
  depends_on = [aws_api_gateway_rest_api.api_gateway]
}