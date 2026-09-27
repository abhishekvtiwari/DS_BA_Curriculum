# Riverstone's sensor-archive storage, defined as code (Chapter 52, section 52.4).
# This is illustrative Terraform, not applied in this book: see the chapter's note on execution.
# Riverstone Supplies is fictional; every name and number is invented.

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  description = "AWS region for Riverstone's data platform"
  type        = string
  default     = "ap-south-1"          # Mumbai, closest region to Riverstone's operations
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "production"
}

resource "aws_s3_bucket" "sensor_archive" {
  bucket = "riverstone-sensor-archive-${var.environment}"

  tags = {
    Project     = "analyst-to-architect"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_s3_bucket_versioning" "sensor_archive" {
  bucket = aws_s3_bucket.sensor_archive.id
  versioning_configuration {
    status = "Enabled"                # protects against the Chapter 49 "table nobody could fix" scenario
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "sensor_archive" {
  bucket = aws_s3_bucket.sensor_archive.id
  rule {
    id     = "archive-old-versions"
    status = "Enabled"
    noncurrent_version_transition {
      noncurrent_days = 90
      storage_class   = "GLACIER"     # cold storage for anything older than 90 days (Chapter 49, section 49.8)
    }
  }
}

resource "aws_iam_role" "pipeline_role" {
  name = "riverstone-pipeline-${var.environment}"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy" "pipeline_s3_access" {
  name = "sensor-archive-read-write"
  role = aws_iam_role.pipeline_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["s3:GetObject", "s3:PutObject", "s3:ListBucket"]
      Resource = [
        aws_s3_bucket.sensor_archive.arn,
        "${aws_s3_bucket.sensor_archive.arn}/*"
      ]
    }]
  })
}

output "bucket_name" {
  value = aws_s3_bucket.sensor_archive.bucket
}
