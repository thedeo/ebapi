resource "aws_wafv2_web_acl" "ebapi" {
  name        = "ebapi"
  description = "WAF for ebapi rate limiting"
  scope       = "REGIONAL"

  default_action {
    allow {}
  }

  rule {
    name     = "exclude_specific_ips"
    priority = 1
    action {
      allow {}
    }

    statement {
      ip_set_reference_statement {
        arn = aws_wafv2_ip_set.allow_list.arn
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "ExcludeSpecificIPs"
      sampled_requests_enabled   = true
    }
  }

  rule {
    name     = "rate_limit_rule"
    priority = 2
    action {
      block {
        custom_response {
          response_code            = 429
          custom_response_body_key = "rateLimitResponse"
          response_header {
            name  = "Retry-After"
            value = "300"
          }
        }
      }
    }

    statement {
      rate_based_statement {
        limit              = 20 # Limit to 20 requests per 5 minutes
        aggregate_key_type = "IP"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "RateLimitRule"
      sampled_requests_enabled   = true
    }
  }

  custom_response_body {
    key          = "rateLimitResponse"
    content_type = "TEXT_PLAIN"
    content      = "You have exceeded the rate limit. Please try again in 5 minutes."
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = "ebapiWAF"
    sampled_requests_enabled   = true
  }
}

resource "aws_wafv2_ip_set" "allow_list" {
  name               = "${local.name}-allow-list"
  description        = "IP addresses to exclude from rate limiting"
  scope              = "REGIONAL"
  ip_address_version = "IPV4"

  addresses = var.rate_limit_allow_list
}
