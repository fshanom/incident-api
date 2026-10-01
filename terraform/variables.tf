variable "do_token" {
  description = "Token de API da DigitalOcean (fornecido via variável de ambiente TF_VAR_do_token, nunca em texto plano no código)"
  type        = string
  sensitive   = true
}

variable "image_tag" {
  description = "Tag da imagem no DigitalOcean Container Registry a ser implantada (o pipeline de CI/CD usa o SHA do commit, garantindo que cada deploy seja rastreável até a mudança de código que o originou)"
  type        = string
  default     = "latest"
}
