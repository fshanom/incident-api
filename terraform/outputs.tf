output "app_url" {
  description = "URL pública do serviço, usada para o health check pós-deploy"
  value       = digitalocean_app.incident_api.live_url
}

output "app_id" {
  description = "ID do app no DigitalOcean App Platform"
  value       = digitalocean_app.incident_api.id
}

output "registry_endpoint" {
  description = "Endpoint do registro de contêineres usado pelo pipeline para publicar novas imagens"
  value       = digitalocean_container_registry.incident_api.endpoint
}
