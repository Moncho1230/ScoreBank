output "artifact_registry_url" {
  value = "${var.region}-docker.pkg.dev/${var.project_id}/${var.project_name}-repo"
}

output "bucket_name" {
  value = google_storage_bucket.bucket.name
}