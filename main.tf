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
  selected_content_path = "content/product/${var.topic}/"
  html_articles_path    = "${local.selected_content_path}${var.topic}/"
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
  for_each = { for product in setproduct(fileset(local.html_articles_path, "*.html"), local.file_endings) : "${var.topic}/${split(".", product[0])[0]}${product[1]}" => product[0] }

  bucket       = var.bucket
  key          = each.key
  content_type = "text/html"

  content = file("${local.html_articles_path}${each.value}")
}
