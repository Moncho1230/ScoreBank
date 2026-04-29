output "db_connection_name" {
  value = google_sql_database_instance.postgres.connection_name
}

output "db_public_ip" {
  value = google_sql_database_instance.postgres.public_ip_address
}

output "db_name" {
  value = google_sql_database.database.name
}

output "db_user" {
  value = google_sql_user.user.name
}