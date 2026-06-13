variable "aws_region" {
  description = "Região AWS onde os recursos serão provisionados"
  type        = string
  default     = "us-east-1"
}

variable "cpu" {
  description = "Quantidade de CPU alocada para o serviço do App Runner"
  type        = string
  default     = "0.25 vCPU"
}

variable "memory" {
  description = "Quantidade de memória alocada para o serviço do App Runner"
  type        = string
  default     = "0.5 GB"
}
