# AKS Cluster
resource "azurerm_kubernetes_cluster" "aks" {
  name                = "${var.project_name}-aks"
  location            = var.location
  resource_group_name = var.resource_group_name
  dns_prefix          = "${var.project_name}-aks"

default_node_pool {
  name           = "default"
  node_count     = 1
  vm_size        = "Standard_D2s_v3"
  vnet_subnet_id = var.subnet_id
}

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin    = "azure"
    load_balancer_sku = "standard"
      service_cidr      = "10.1.0.0/16"
  dns_service_ip    = "10.1.0.10"
  }

  tags = {
    project = var.project_name
  }
}

# Permiso para que AKS pueda hacer pull de imágenes del ACR
resource "azurerm_role_assignment" "aks_acr_pull" {
  principal_id                     = azurerm_kubernetes_cluster.aks.kubelet_identity[0].object_id
  role_definition_name             = "AcrPull"
  scope                            = var.acr_id
  skip_service_principal_aad_check = true
}
