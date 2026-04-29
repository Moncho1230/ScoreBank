module "network" {
  source       = "./modules/network"
  project_id   = var.project_id
  region       = var.region
  project_name = var.project_name
}

module "security" {
  source = "./modules/security"
  vpc_id = module.network.vpc_id
}

module "storage" {
  source       = "./modules/storage"
  project_id   = var.project_id
  region       = var.region
  project_name = var.project_name
}

module "database" {
  source      = "./modules/database"
  project_id  = var.project_id
  region      = var.region
  db_password = var.db_password
  network_id  = module.network.vpc_id
}

module "compute" {
  source              = "./modules/compute"
  project_id          = var.project_id
  region              = var.region
  image               = var.image
  vpc_connector_id    = module.network.vpc_connector_id
  db_connection_name  = module.database.db_connection_name
  db_password         = var.db_password
 
  depends_on = [module.database, module.network, module.storage]
}
