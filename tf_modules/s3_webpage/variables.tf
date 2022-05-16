variable "bucket_name" {
  type        = string
  description = "Name of the S3 bucket to put the pages"
}

variable "resource_name" {
  type        = string
  description = "Name of the webpage should have in the S3 bucket / on the web"
}

variable "content_type" {
  type        = string
  default     = "text/html"
  description = "MIME type the browser receives when querying for this page"
}

variable "content_path" {
  type        = string
  description = "Path to the file that should be put on S3 as a webpage"
}
