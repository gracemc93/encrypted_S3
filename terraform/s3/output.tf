output "encrypted_bucket_name" {
  description = "S3 bucket name created"
  value       = aws_s3_bucket.s3-bucket-encrypted.bucket
}

output "non_encrypted_bucket_name" {
    description = "S3 bucket name created"
    value       = aws_s3_bucket.s3-bucket-non-encrypted.bucket
}

//output "bucket_arn" {
//  description = "S3 bucket arn created"
//  value       = aws_s3_bucket.s3-bucket-encrypted.arn
//}
