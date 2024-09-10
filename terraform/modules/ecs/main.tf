# Create ECS cluster 
resource "aws_ecs_cluster" "this" {
  name = "${var.environment}-ecs-cluster"
  tags = merge(
    {
      Name = "${var.environment}-ecs-cluster"
    },
    var.tags
  )
}

# Create IAM role for ECS for permissions to AWS resources
resource "aws_iam_role" "ecs_task_execution" {
  name = "${var.environment}-ecs-task-execution-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

# Attaches the IAM policy to the IAM role to allow task execution
resource "aws_iam_role_policy_attachment" "ecs_task_execution_policy" {
  role       = aws_iam_role.ecs_task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# Defines ECS task (specify docker config, resource limits, and environment settings)
resource "aws_ecs_task_definition" "app" {
  family                   = "${var.environment}-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn

  container_definitions = jsonencode([
    {
      name        = "app"
      image       = "${aws_ecr_repository.app_repo.repository_url}:latest"
      cpu         = 256
      memory      = 512
      essential   = true
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
        }
      ]
    }
  ])
  tags = merge(
    {
      Name = "${var.environment}-task"
    },
    var.tags
  )
}

# Deploy and manage ECS based off the task, specify instance number, and networking info)
resource "aws_ecs_service" "app" {
  name            = "${var.environment}-ecs-service"
  cluster         = aws_ecs_cluster.this.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = var.public_subnets
    security_groups = [var.security_group_id]
    assign_public_ip = true
  }

  tags = merge(
    {
      Name = "${var.environment}-ecs-service"
    },
    var.tags
  )
}
