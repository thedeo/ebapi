resource "null_resource" "generate_openapi_spec" {
  provisioner "local-exec" {
    command = "poetry run python ${local.openopi_export_script_path}"
    environment = {
      PYTHONPATH  = "${path.module}/../"
      LAMBDA_ARN  = aws_lambda_function.ebapi.arn
      OUTPUT_FILE = "${local.openapi_spec_path}"
      REGION      = var.region
    }
  }

  triggers = {
    always_run = local.combined_apigateway_trigger_hashes
  }
}

data "local_file" "openapi_spec" {
  # Reference file before created to avoid bug in aws_api_gateway_rest_api resource
  depends_on = [null_resource.generate_openapi_spec]
  filename   = local.openapi_spec_path
}

resource "aws_api_gateway_rest_api" "ebapi" {
  name = local.name
  body = data.local_file.openapi_spec.content

  depends_on = [null_resource.generate_openapi_spec]
}

resource "aws_api_gateway_method_settings" "ebapi_all" {
  rest_api_id = aws_api_gateway_rest_api.ebapi.id
  stage_name  = aws_api_gateway_stage.ebapi.stage_name
  method_path = "*/*"

  settings {
    caching_enabled      = false # Caching doesn't handle query parameters
    cache_ttl_in_seconds = 3600
    metrics_enabled      = true
    logging_level        = "INFO"
  }
}

resource "aws_cloudwatch_log_group" "ebapi" {
  name              = "/aws/api-gateway/${local.name}/access-logs"
  retention_in_days = 90
}

resource "aws_api_gateway_stage" "ebapi" {
  deployment_id = aws_api_gateway_deployment.ebapi.id
  rest_api_id   = aws_api_gateway_rest_api.ebapi.id
  stage_name    = local.api_gateway_stage_name

  cache_cluster_enabled = false
  cache_cluster_size    = 0.5

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.ebapi.arn
    format = jsonencode({
      requestId      = "$context.requestId",
      ip             = "$context.identity.sourceIp",
      requestTime    = "$context.requestTime",
      httpMethod     = "$context.httpMethod",
      resourcePath   = "$context.resourcePath",
      status         = "$context.status",
      protocol       = "$context.protocol",
      responseLength = "$context.responseLength"
    })
  }
}

resource "aws_api_gateway_deployment" "ebapi" {
  depends_on  = [aws_api_gateway_rest_api.ebapi]
  rest_api_id = aws_api_gateway_rest_api.ebapi.id

  triggers = {
    redeployment = local.combined_apigateway_trigger_hashes
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_domain_name" "ebapi" {
  domain_name     = var.hosted_zone_id != "" ? "api.${data.aws_route53_zone.selected[0].name}" : var.domain_name
  certificate_arn = var.certificate_arn
  security_policy = "TLS_1_2"
  endpoint_configuration {
    types = ["EDGE"]
  }
}

resource "aws_api_gateway_base_path_mapping" "ebapi" {
  api_id      = aws_api_gateway_rest_api.ebapi.id
  stage_name  = aws_api_gateway_stage.ebapi.stage_name
  domain_name = aws_api_gateway_domain_name.ebapi.domain_name
}

resource "aws_wafv2_web_acl_association" "ebapi" {
  resource_arn = "arn:aws:apigateway:${var.region}::/restapis/${aws_api_gateway_rest_api.ebapi.id}/stages/${aws_api_gateway_stage.ebapi.stage_name}"
  web_acl_arn  = aws_wafv2_web_acl.ebapi.arn
}
