# Riverstone's sensor-archive storage and the pipeline's identity, as code (Chapter 52, section 52.4).
# Checked with terraform init -backend=false, fmt and validate; never applied to a real AWS account in this book.
# Riverstone Supplies is fictional; every name and number is invented.

# --- Part 1: settings, state, provider, variables ---

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }

  backend "s3" {
    bucket       = "riverstone-tfstate"
    key          = "platform/terraform.tfstate"
    region       = "ap-south-1"
    use_lockfile = true
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  description = "AWS region for Riverstone's data platform"
  type        = string
  default     = "ap-south-1" # Mumbai
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "production"
}

# --- Part 2: the bucket, with versioning ---

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
    status = "Enabled"
  }
}

# --- Part 3: what happens to old versions ---

resource "aws_s3_bucket_lifecycle_configuration" "sensor_archive" {
  bucket = aws_s3_bucket.sensor_archive.id

  rule {
    id     = "old-versions-to-cold-storage"
    status = "Enabled"

    filter {}

    noncurrent_version_transition {
      noncurrent_days = 90
      storage_class   = "GLACIER"
    }
  }
}

# --- Part 4: the pipeline's identity ---

resource "aws_iam_role" "pipeline_role" {
  name = "riverstone-pipeline-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "pipeline_s3_access" {
  name = "sensor-archive-read-write"
  role = aws_iam_role.pipeline_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = ["s3:GetObject", "s3:PutObject", "s3:ListBucket"]
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
