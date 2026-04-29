# Regla SSH — acceso remoto por puerto 22
resource "google_compute_firewall" "allow_ssh" {
  name    = "scorebank-allow-ssh"
  network = var.vpc_id

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["scorebank-ssh"]
}

# Regla HTTP/HTTPS — tráfico web
resource "google_compute_firewall" "allow_http" {
  name    = "scorebank-allow-http"
  network = var.vpc_id

  allow {
    protocol = "tcp"
    ports    = ["80", "443", "8000"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["scorebank-http"]
}

# Regla PostgreSQL — acceso a la DB desde la VPC y SSH externo
resource "google_compute_firewall" "allow_postgres" {
  name    = "scorebank-allow-postgres"
  network = var.vpc_id

  allow {
    protocol = "tcp"
    ports    = ["5432"]
  }

  # Permite desde cualquier IP para poder conectarse via SSH desde local
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["scorebank-db"]
}

# Regla interna — todo el tráfico dentro de la VPC
resource "google_compute_firewall" "allow_internal" {
  name    = "scorebank-allow-internal"
  network = var.vpc_id

  allow {
    protocol = "tcp"
    ports    = ["0-65535"]
  }

  allow {
    protocol = "udp"
    ports    = ["0-65535"]
  }

  allow {
    protocol = "icmp"
  }

  source_ranges = ["10.0.0.0/8"]
}
