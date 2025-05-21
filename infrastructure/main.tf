provider "aws" {
  region = var.region

  default_tags {
    tags = {
      Environment = var.environment
      Project     = "fraud-detection"
      ManagedBy   = "terraform"
    }
  }
}

# KMS Key for encryption
resource "aws_kms_key" "main" {
  description             = "KMS key for fraud detection solution"
  deletion_window_in_days = 7
  enable_key_rotation     = true

  tags = {
    Name = "${var.project_name}-kms-key"
  }
}

resource "aws_kms_alias" "main" {
  name          = "alias/${var.project_name}-kms-key"
  target_key_id = aws_kms_key.main.key_id
}

# VPC Module
module "vpc" {
  source = "./modules/vpc"

  name             = "${var.project_name}-vpc"
  environment      = var.environment
  vpc_cidr         = var.vpc_cidr
  availability_zones = var.availability_zones

  tags = {
    Name = "${var.project_name}-vpc"
  }
}

# EKS Module
module "eks" {
  source = "./modules/eks"

  cluster_name            = "${var.project_name}-cluster"
  kubernetes_version      = var.kubernetes_version
  subnet_ids             = module.vpc.private_subnet_ids
  cluster_security_group_id = module.vpc.eks_cluster_security_group_id
  kms_key_arn            = aws_kms_key.main.arn
  node_desired_size      = var.node_desired_size
  node_max_size          = var.node_max_size
  node_min_size          = var.node_min_size
  node_instance_types    = var.node_instance_types

  tags = {
    Name = "${var.project_name}-eks"
  }
}

# S3 Module
module "s3" {
  source = "./modules/s3"

  bucket_name      = "${var.project_name}-${var.environment}-${random_string.suffix.result}"
  kms_key_arn      = aws_kms_key.main.arn
  eks_node_role_arn = module.eks.node_role_arn
  allowed_origins  = var.s3_allowed_origins

  tags = {
    Name = "${var.project_name}-s3"
  }
}

# Random string for unique S3 bucket name
resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
}
