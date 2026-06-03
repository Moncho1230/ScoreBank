output "db_host" {
  value = azurerm_mssql_server.sql_server.fully_qualified_domain_name
}

output "db_name" {
  value = azurerm_mssql_database.database.name
}

output "db_connection_string" {
  value     = "Server=${azurerm_mssql_server.sql_server.fully_qualified_domain_name};Database=scorebank-db;User Id=scorebank_admin;Password=${var.db_password};"
  sensitive = true
}