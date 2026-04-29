variable "project_id" {
  type = string
}

variable "region" {
  type = string
}

variable "image" {
  type = string
}

variable "vpc_connector_id" {
  type = string
}

variable "db_connection_name" {
  type = string
}

variable "db_password" {
  type      = string
  sensitive = true
}
