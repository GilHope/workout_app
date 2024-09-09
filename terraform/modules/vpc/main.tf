data "aws_availability_zones" "available" {}

# Creates VPC
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  tags = merge(
    {
      Name = "${var.environment}-vpc"
    },
    var.tags
  )
}

# Create subnets within VPC
resource "aws_subnet" "public" {
  count = 2
  vpc_id = aws_vpc.main.id
  cidr_block = cidrsubnet(aws_vpc.main.cidr_block, 4, count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true
  tags = merge(
    {
      Name = "${var.environment}-public-subnet-${count.index + 1}"
    },
    var.tags
  )
}

# Attaches IGW for access to internet
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  tags = merge(
    {
      Name = "${var.environment}-igw"
    },
    var.tags
  )
}
