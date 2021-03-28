resource "aws_s3_bucket" "s3-bucket-encrypted" {
  bucket = "${var.bucket_name}-1"
  region = var.aws_region
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

resource "aws_s3_bucket" "s3-bucket-non-encrypted" {
  bucket = "${var.bucket_name}-2"
  region = var.aws_region
}


resource "aws_s3_bucket_public_access_block" "bucket_access_encrypted" {
  bucket                  = aws_s3_bucket.s3-bucket-encrypted.bucket
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_public_access_block" "bucket_access_non_encrypted" {
  bucket                  = aws_s3_bucket.s3-bucket-non-encrypted.bucket
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}