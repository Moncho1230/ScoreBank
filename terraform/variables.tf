variable "project_id" {
  description = "ID del proyecto en GCP"
  type        = string
  default     = "score-bank-devops-cloud"
}

variable "region" {
  description = "Región de GCP"
  type        = string
  default     = "us-central1"
}

variable "project_name" {
  description = "Nombre del proyecto para nombrar recursos"
  type        = string
  default     = "score-bank-devops-cloud"
}

variable "db_password" {
  description = "Contraseña del usuario de la base de datos"
  type        = string
  sensitive   = true
}


variable "image" {
  description = "Imagen Docker de la API en Artifact Registry"
  type        = string
  default     = "us-central1-docker.pkg.dev/score-bank-devops-cloud/score-bank-devops-cloud-repo/scorebank-api:latest"
}