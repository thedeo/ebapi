resource "aws_route53_record" "ebapi" {
  count = var.hosted_zone_id != "" ? 1 : 0

  zone_id = data.aws_route53_zone.selected[0].zone_id
  name    = "api.${data.aws_route53_zone.selected[0].name}"
  type    = "A"

  alias {
    name                   = aws_api_gateway_domain_name.ebapi.cloudfront_domain_name
    zone_id                = aws_api_gateway_domain_name.ebapi.cloudfront_zone_id
    evaluate_target_health = false
  }
}
