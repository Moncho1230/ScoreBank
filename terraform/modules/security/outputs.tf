output "ssh_firewall_name" {
  value = google_compute_firewall.allow_ssh.name
}

output "http_firewall_name" {
  value = google_compute_firewall.allow_http.name
}

output "postgres_firewall_name" {
  value = google_compute_firewall.allow_postgres.name
}