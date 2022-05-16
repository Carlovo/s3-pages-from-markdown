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
  selected_content_path = "content/product/${var.topic}-${var.bucket}/"
  html_articles_path    = "${local.selected_content_path}${var.topic}/"
  js_app_path           = "${local.html_articles_path}main.js"
}

module "index" {
  source = "./tf_modules/s3_webpage"

  bucket_name   = var.bucket
  resource_name = "${var.topic}.html"
  content_path  = "${local.selected_content_path}index.html"
}

module "script" {
  count = fileexists(local.js_app_path) ? 1 : 0

  source = "./tf_modules/s3_webpage"

  bucket_name   = var.bucket
  resource_name = "${var.topic}/main.js"
  content_type  = "text/javascript"
  content_path  = local.js_app_path
}

module "articles" {
  for_each = fileset(local.html_articles_path, "*.html")

  source = "./tf_modules/s3_webpage"

  bucket_name   = var.bucket
  resource_name = "${var.topic}/${each.key}"
  content_path  = "${local.html_articles_path}${each.key}"
}
