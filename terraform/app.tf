# Serviço de orquestração de contêineres em nuvem (DigitalOcean App
# Platform) que executa a API REST.
#
# O App Platform provisiona e gerencia automaticamente a infraestrutura de
# apoio (balanceamento de carga, HTTPS, auto scaling horizontal, métricas e
# health checks), a partir da imagem publicada no registro de contêineres.
#
# Cada execução do pipeline de CI/CD publica uma nova imagem no registro com
# a tag correspondente ao SHA do commit (var.image_tag) e roda
# `terraform apply` apontando para essa tag, o que gera uma nova implantação
# (deployment) do serviço — esse evento é o "deploy" medido pelas métricas
# inspiradas no DORA (frequência de deploy e lead time).
resource "digitalocean_app" "incident_api" {
  spec {
    name   = "incident-api"
    region = "fra"

    service {
      name               = "api"
      instance_count     = 1
      instance_size_slug = "apps-s-1vcpu-0.5gb"
      http_port          = 8080

      image {
        registry_type = "DOCR"
        registry      = digitalocean_container_registry.incident_api.name
        repository    = "incident-api"
        tag           = var.image_tag
      }

      health_check {
        http_path = "/incidents/health/check"
      }
    }
  }
}
