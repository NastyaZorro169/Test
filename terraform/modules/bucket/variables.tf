variable "bucket_name" {
  description = "Имя бакета для хранения артефактов ML"
  type        = string
}

variable "s3_key" {
  description = "Access key для Yandex Object Storage"
  type        = string
}

variable "s3_secret" {
  description = "Secret key для Yandex Object Storage"
  type        = string
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
    project     = "unidoc"
  }
} 