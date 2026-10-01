terraform {
  required_version = ">= 1.5"

  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.52"
    }
  }

  # Backend local (não remoto): decisão de escopo documentada no TCC.
  # O backend remoto originalmente planejado (S3) dependia de uma conta AWS
  # que se mostrou inviável para o estudo (ver Metodologia — migração de
  # provedor de nuvem). Dado o cronograma do projeto, o estado é persistido
  # entre execuções do pipeline via cache do GitHub Actions (actions/cache),
  # em vez de um backend remoto dedicado — simplificação registrada como
  # limitação do estudo, não como boa prática recomendada para produção.
}

provider "digitalocean" {
  token = var.do_token
}

# Registro de imagens de container da aplicação na DigitalOcean Container
# Registry (DOCR). O plano "starter" é gratuito e suficiente para um único
# repositório de imagens, adequado ao escopo do estudo.
resource "digitalocean_container_registry" "incident_api" {
  name                   = "incident-api-tcc"
  subscription_tier_slug = "starter"
  region                 = "fra1"
}
