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
}

module "webpages" {
  for_each = fileset(local.selected_content_path, "**")

  source = "./tf_modules/s3_webpage"

  bucket_name   = var.bucket
  resource_name = substr(each.key, -5, -1) == ".html" ? substr(each.key, 0, length(each.key) -5) : each.key
  content_path  = "${local.selected_content_path}${each.key}"
}
