# ECR Image Repo
resource "aws_ecr_repository" "app_repo" {
  name = "531-image-repo"
  
  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Environment = var.environment
    Name        = "${var.environment}-ecr-repo"
  }
}

# 
output "ecr_repository_url" {
  value = aws_ecr_repository.app_repo.repository_url
  description = "The URL of the ECR repo"
}