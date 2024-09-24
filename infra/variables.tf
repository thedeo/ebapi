variable "project_name" {
  description = "The name used for resource creation"
  type        = string
  default     = "ebapi"
}

variable "env" {
  description = "The environment used for resource creation"
  type        = string
  default     = "dev"
}

variable "data_table_name" {
  description = "The name of the existing DynamoDB table"
  type        = string
}

variable "region" {
  default = "us-east-1"
}

variable "domain_name" {
  description = "The domain name used for API gateway"
  type        = string
}

variable "hosted_zone_id" {
  description = "The hosted zone ID for the domain name is optional"
  type        = string
  default     = ""
}

variable "certificate_arn" {
  description = "The ARN of the SSL certificate used for API gateway"
  type        = string
}

variable "rate_limit_allow_list" {
  description = "List of IPs to exclude from rate limiting"
  type        = list(string)
  default     = []
}
