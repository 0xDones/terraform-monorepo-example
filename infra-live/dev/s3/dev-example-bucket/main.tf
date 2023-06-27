terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}
provider "aws" {
  profile = "default"
  region  = "us-west-2"
}
resource "aws_s3_bucket" "examplebucket" {
  bucket = "examplebuckettftest"
  acl    = "private"
  versioning {
    mfa_delete = false
  }
  logging {
    target_bucket = aws_s3_bucket.log_bucket.id
    target_prefix = "log/"
    }
}
