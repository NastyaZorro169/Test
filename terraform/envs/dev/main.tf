terraform {
  required_providers {
    yandex = {
      source  = "yandex-cloud/yandex"
      version = ">= 0.87"
    }
  }
}

provider "yandex" {
  token     = var.yc_token
  cloud_id  = var.cloud_id
  folder_id = var.folder_id
  zone      = var.zone
}

module "s3_bucket" {
  source = "../../modules/bucket"

  bucket_name = var.bucket_name
  s3_key      = var.s3_key
  s3_secret   = var.s3_secret
  region      = var.region
  labels      = var.labels
} 