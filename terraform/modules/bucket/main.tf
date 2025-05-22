resource "yandex_storage_bucket" "artifacts" {
  bucket     = var.bucket_name
  access_key = var.s3_key
  secret_key = var.s3_secret

  versioning {
    enabled = true
  }
}