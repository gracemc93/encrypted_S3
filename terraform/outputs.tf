output "encrypted_bucket" {
  value = module.encrypted_s3_bucket.encrypted_bucket_name
}

output "non_encrypted_bucket" {
  value = module.encrypted_s3_bucket.non_encrypted_bucket_name
}

output "url_to_encryption_checker" {
  value = "${module.encryption_checker_api.url}${module.encryption_checker_api.method}"
}