output "api_docs_url" {
  description = "The URL of the API documentation"
  value       = "https://${aws_api_gateway_domain_name.ebapi.domain_name}/docs"
}
