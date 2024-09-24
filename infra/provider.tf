terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    region = "us-east-1"
    bucket = "ebapi-terraform-state"
    key    = "ebapi/terraform.tfstate"
  }
}

provider "aws" {
  region = "us-east-1"
}
