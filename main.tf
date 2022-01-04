provider "aws" {
  region = "eu-central-1"
}

variable "bucket" {
  type = string
}

variable "topic" {
  type = string
}

resource "aws_s3_bucket_object" "index" {
  for_each = toset(["", "/", ".html"])

  bucket       = var.bucket
  key          = "${var.topic}${each.key}"
  content_type = "text/html"

  content = file("content/${var.topic}/index.html")
}

resource "aws_s3_bucket_object" "articles" {
  for_each = fileset(path.module, "content/${var.topic}/articles/html/*.html")

  bucket       = var.bucket
  key          = "${var.topic}/${split("/", each.key)[4]}"
  content_type = "text/html"

  content = file(each.key)
}
