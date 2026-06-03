variable "subscription_id" {
  description = "Azure Subscription ID"
  type        = string
  default     = "72deae3a-cbbf-4b1a-91f3-6aa0c8f7669a"
}

variable "location" {
  description = "Región de Azure"
  type        = string
  default     = "East US"
}

variable "project_name" {
  description = "Nombre del proyecto"
  type        = string
  default     = "scorebank"
}

variable "resource_group_name" {
  description = "Nombre del resource group"
  type        = string
  default     = "scorebank-rg"
}

variable "db_password" {
  description = "Contraseña del usuario de la base de datos"
  type        = string
  sensitive   = true
}