variable "yc_token" {
  description = "Yandex Cloud API token"
  type        = string
  sensitive   = true
}

variable "cloud_id" {
  description = "Yandex Cloud ID"
  type        = string
}

variable "folder_id" {
  description = "Yandex Cloud Folder ID"
  type        = string
}

variable "zone" {
  description = "Yandex Cloud Zone"
  type        = string
  default     = "ru-central1-a"
}

variable "bucket_name" {
  description = "Имя бакета для хранения артефактов ML"
  type        = string
}

variable "s3_key" {
  description = "Access key для Yandex Object Storage"
  type        = string
  sensitive   = true
}

variable "s3_secret" {
  description = "Secret key для Yandex Object Storage"
  type        = string
  sensitive   = true
}

variable "region" {
  description = "Регион Yandex Cloud"
  type        = string
  default     = "ru-central1"
}

variable "labels" {
  description = "Метки для ресурса"
  type        = map(string)
  default     = {
    environment = "dev"
    project     = "mlflow"
  }
} 