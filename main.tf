provider "aws" {
  region = "eu-central-1"
}

variable "bucket" {
  type = string
}

variable "topic" {
  type = string
}

locals {
  selected_content_path = "content/${var.topic}/"
  file_endings          = toset(["", "/", ".html"])
}

resource "aws_s3_bucket_object" "index" {
  for_each = local.file_endings

  bucket       = var.bucket
  key          = "${var.topic}${each.key}"
  content_type = "text/html"

  content = file("${local.selected_content_path}index.html")
}

resource "aws_s3_bucket_object" "articles" {
  for_each = { for product in setproduct(fileset(path.module, "${local.selected_content_path}articles/html/*.html"), local.file_endings) : "${var.topic}/${split(".", split("/", product[0])[4])[0]}${product[1]}" => product[0] }

  bucket       = var.bucket
  key          = each.key
  content_type = "text/html"

  content = file(each.value)
}
