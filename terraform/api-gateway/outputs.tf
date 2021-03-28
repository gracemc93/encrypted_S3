output "api_invoke_url" {
  value = aws_api_gateway_deployment.gateway_deployment.invoke_url
}

output "url" {
  value = aws_api_gateway_stage.api_gateway_stage.invoke_url
}

output "method" {
  value = aws_api_gateway_resource.api_gateway_resource.path
}
