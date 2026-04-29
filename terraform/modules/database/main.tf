# Instancia de Cloud SQL con PostgreSQL
resource "google_sql_database_instance" "postgres" {
  name             = "scorebank-db-instance"
  database_version = "POSTGRES_15"
  region           = var.region
  project          = var.project_id

  deletion_protection = false

  settings {
    tier = "db-f1-micro"

    ip_configuration {
      ipv4_enabled    = true  # IP pública para conexión SSH/remota
      #private_network = var.network_id

      # Permite conexiones remotas desde cualquier IP (requerido por la rúbrica)
      authorized_networks {
        name  = "all"
        value = "0.0.0.0/0"
      }
    }

    backup_configuration {
      enabled = true
    }

    database_flags {
      name  = "max_connections"
      value = "100"
    }
  }
}

# Base de datos
resource "google_sql_database" "database" {
  name     = "scorebank-db"
  instance = google_sql_database_instance.postgres.name
  project  = var.project_id
}

# Usuario de la base de datos
resource "google_sql_user" "user" {
  name     = "scorebank_user"
  instance = google_sql_database_instance.postgres.name
  password = var.db_password
  project  = var.project_id
}
