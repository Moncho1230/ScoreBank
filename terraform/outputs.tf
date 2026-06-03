output "aks_cluster_name" {
  description = "Nombre del cluster AKS"
  value       = module.compute.aks_cluster_name
}

output "acr_login_server" {
  description = "URL del Azure Container Registry"
  value       = module.storage.acr_login_server
}

output "resource_group_name" {
  description = "Nombre del resource group"
  value       = module.network.resource_group_name
}

output "vnet_id" {
  description = "ID de la Virtual Network"
  value       = module.network.vnet_id
}

output "aks_credentials_command" {
  description = "Comando para conectar kubectl al cluster"
  value       = "az aks get-credentials --resource-group ${var.resource_group_name} --name ${module.compute.aks_cluster_name}"
}

output "db_host" {
  value = module.database.db_host
}