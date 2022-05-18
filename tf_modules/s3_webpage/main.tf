resource "aws_s3_bucket_object" "this" {
  bucket       = var.bucket_name
  key          = var.resource_name
  content_type = substr(var.resource_name, -3, -1) == ".js" ? "text/javascript" : "text/html"
  content      = file(var.content_path)
  etag         = filemd5(var.content_path)
  acl          = "public-read"
}
