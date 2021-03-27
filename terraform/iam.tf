data "aws_iam_policy_document" "encryption_checker_s3_policy" {
  statement {
    actions = [
      "s3:*",
    ]
    resources = [
      "*"
    ]
  }
}