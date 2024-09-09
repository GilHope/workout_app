### TESTING ENV ###

# Import VPC module for testing env
module "vpc" {
  source      = "../../modules/vpc"
  environment = var.environment
  tags         = merge(
    var.tags,
    {
      Name = var.environment
    }
  )
}

# Import SG module
module "security_groups" {
  source      = "../../modules/security_groups"
  environment = var.environment
  vpc_id      = module.vpc.vpc_id
  tags        = merge(
    var.tags,
    {
      Name = var.environment
    }
  )
}

# Import ECs module
module "ecs" {
  source            = "../../modules/ecs"
  environment       = var.environment
  tags              = var.tags
  docker_image      = "YOUR_DOCKER_IMAGE_URL"  # Replace with your actual Docker image URL
  public_subnets    = module.vpc.public_subnets
  security_group_id = module.security_groups.ecs_sg_id
}
