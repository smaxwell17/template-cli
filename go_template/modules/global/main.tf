data "aws_iam_policy_document" "instance_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "iam_for_lambda" {
  name = "send-events"
  assume_role_policy = data.aws_iam_policy_document.instance_assume_role_policy.json
  managed_policy_arns = [ 
      "arn:aws:iam::aws:policy/CloudWatchFullAccess",
   ]
   inline_policy {
     name = "get-parameter"
     policy = jsonencode({"Version":"2012-10-17","Statement":[{"Sid":"VisualEditor0","Effect":"Allow","Action":"ssm:GetParameter","Resource":"*"}]})
   }
   tags = {
    Application = "PATCh",
    Environment = "nonprod",
    Team = "PATCh",
    Creator = "terraform-PROJECT_NAME",
    APMId = "BA0001171"
  }
}

output "iam_for_lambda_arn" {
    value = aws_iam_role.iam_for_lambda.arn
}