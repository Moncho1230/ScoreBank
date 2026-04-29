output "cloud_run_url" {
  description = "URL pública de la API en Cloud Run"
  value       = module.compute.cloud_run_url
}

output "cloud_sql_public_ip" {
  description = "IP pública de Cloud SQL para conexión SSH"
  value       = module.database.db_public_ip
}

output "cloud_sql_connection_name" {
  description = "Connection name de Cloud SQL para el proxy"
  value       = module.database.db_connection_name
}

output "artifact_registry_url" {
  description = "URL del repositorio de Artifact Registry"
  value       = module.storage.artifact_registry_url
}

output "vpc_id" {
  description = "ID de la VPC creada"
  value       = module.network.vpc_id
}
