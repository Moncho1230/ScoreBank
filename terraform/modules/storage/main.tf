# Artifact Registry — repositorio de imágenes Docker
resource "google_artifact_registry_repository" "docker_repo" {
  location      = var.region
  repository_id = "${var.project_name}-repo"
  description   = "Repositorio de imágenes Docker para ScoreBank"
  format        = "DOCKER"
  project       = var.project_id
}

# Cloud Storage — bucket para backups y archivos estáticos
resource "google_storage_bucket" "bucket" {
  name          = "${var.project_name}-storage-${var.project_id}"
  location      = var.region
  project       = var.project_id
  force_destroy = true

  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete"
    }
  }
}
