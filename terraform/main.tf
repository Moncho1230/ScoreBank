module "network" {
  source              = "./modules/network"
  location            = var.location
  project_name        = var.project_name
  resource_group_name = var.resource_group_name
}

module "storage" {
  source              = "./modules/storage"
  location            = var.location
  project_name        = var.project_name
  resource_group_name = module.network.resource_group_name

  depends_on = [module.network]
}

module "compute" {
  source              = "./modules/compute"
  location            = var.location
  project_name        = var.project_name
  resource_group_name = module.network.resource_group_name
  subnet_id           = module.network.aks_subnet_id
  acr_id              = module.storage.acr_id

  depends_on = [module.network, module.storage]
}

module "database" {
  source              = "./modules/database"
  project_name        = var.project_name
  resource_group_name = module.network.resource_group_name
  location            = var.location
  db_password         = var.db_password
}
