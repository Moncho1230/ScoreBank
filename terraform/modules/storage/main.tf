# Azure Container Registry — registro de imágenes Docker
resource "azurerm_container_registry" "acr" {
  name                = "${var.project_name}registry"
  resource_group_name = var.resource_group_name
  location            = var.location
  sku                 = "Basic"
  admin_enabled       = true
}
