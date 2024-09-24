data "aws_caller_identity" "current" {}
data "aws_route53_zone" "selected" {
  count   = var.hosted_zone_id != "" ? 1 : 0
  zone_id = var.hosted_zone_id
}
