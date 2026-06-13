terraform {
  required_version = ">= 1.5"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Backend remoto S3: mantém o state compartilhado entre execuções e
  # entre membros da equipe, evitando divergências de estado local
  # (governança de mudanças em IaC).
  backend "s3" {
    bucket = "tcc-tfstate-bucket"
    key    = "incident-api/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region
}

# Repositório de imagens de container da aplicação.
#
# scan_on_push = true é uma prática de DevSecOps: a cada push de uma nova
# imagem, o ECR executa automaticamente um scan de vulnerabilidades
# conhecidas (CVEs), permitindo identificar problemas de segurança antes
# de a imagem ser implantada em produção.
resource "aws_ecr_repository" "incident_api" {
  name                 = "incident-api"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

# Serviço de orquestração de contêineres serverless (AWS App Runner) que
# executa a API REST.
#
# auto_deployments_enabled = true simula um fluxo GitOps: ao detectar uma
# nova imagem publicada no repositório ECR, o App Runner inicia
# automaticamente um novo deploy do serviço, sem intervenção manual,
# refletindo a entrega contínua medida pelas métricas inspiradas no DORA
# (frequência de deploy e lead time).
resource "aws_apprunner_service" "incident_api" {
  service_name = "incident-api"

  source_configuration {
    auto_deployments_enabled = true

    image_repository {
      image_identifier      = "${aws_ecr_repository.incident_api.repository_url}:latest"
      image_repository_type = "ECR"

      image_configuration {
        port = "8000"
      }
    }
  }

  instance_configuration {
    cpu    = var.cpu
    memory = var.memory
  }

  tags = {
    Project = "tcc-incident-api"
  }
}
