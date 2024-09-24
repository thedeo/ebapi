locals {
  # Name for resource creation
  name = "${var.project_name}-${var.env}"

  dist_path                  = "${path.module}/../dist"
  scripts_path               = "${path.module}/../scripts"
  openopi_export_script_path = "${local.scripts_path}/openapi_spec_export.py"
  openapi_spec_path          = "${local.dist_path}/openapi_with_extensions.json"
  apigateway_trigger_files = [
    local.openopi_export_script_path,
    "${local.dist_path}/lambda_function.zip"
  ]

  apigateway_trigger_hashes = {
    for file in local.apigateway_trigger_files :
    file => filebase64sha256(file)
  }

  combined_apigateway_trigger_hashes = join("", values(local.apigateway_trigger_hashes))

  api_gateway_stage_name = "prod"
}
