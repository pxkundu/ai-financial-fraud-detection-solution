terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

# This is just for syntax validation
provider "aws" {
  region = "us-east-1"
  # Using dummy credentials for validation
  access_key = "dummy"
  secret_key = "dummy"
} 