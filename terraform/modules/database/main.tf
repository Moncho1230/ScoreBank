resource "azurerm_mssql_server" "sql_server" {
  name                         = "${var.project_name}-sqlserver"
  resource_group_name          = var.resource_group_name
  location                     = var.location
  version                      = "12.0"
  administrator_login          = "scorebank_admin"
  administrator_login_password = var.db_password

  tags = {
    project = var.project_name
  }
}

resource "azurerm_mssql_database" "database" {
  name      = "scorebank-db"
  server_id = azurerm_mssql_server.sql_server.id
  sku_name  = "Basic"
}

resource "azurerm_mssql_firewall_rule" "allow_all" {
  name             = "allow-all"
  server_id        = azurerm_mssql_server.sql_server.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "255.255.255.255"
}