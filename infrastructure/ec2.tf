# Configure AWS Provider
provider "aws" {
  region = "us-east-1"
}

# Get default VPC
data "aws_vpc" "default" {
  default = true
}

# Get default subnet
data "aws_subnet" "default" {
  vpc_id = data.aws_vpc.default.id
  filter {
    name   = "default-for-az"
    values = ["true"]
  }
}

# Get default security group
data "aws_security_group" "default" {
  vpc_id = data.aws_vpc.default.id
  name   = "default"
}

# Create EC2 Instance
resource "aws_instance" "devops_instance" {
  ami           = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2 AMI ID in us-east-1
  instance_type = "t2.micro"
  key_name      = "devops-key"
  subnet_id     = data.aws_subnet.default.id

  tags = {
    Name        = "DevOpsInstance"
    Environment = "Dev"
  }

  # Use default security group
  vpc_security_group_ids = [data.aws_security_group.default.id]

  # Root volume configuration
  root_block_device {
    volume_size = 8
    volume_type = "gp2"
    tags = {
      Name = "DevOpsInstance-root"
    }
  }
}

# Output the instance public IP
output "instance_public_ip" {
  value       = aws_instance.devops_instance.public_ip
  description = "Public IP address of the DevOps instance"
} 