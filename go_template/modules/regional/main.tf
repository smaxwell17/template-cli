variable "iam_for_lambda_arn" {
  type = string
}

resource "aws_lambda_function" "events_lambda" {
  filename      = "./main.zip"
  function_name = "{LAMBDA_NAME}"
  role          = var.iam_for_lambda_arn
  handler       = "main.lambda_handler"
  source_code_hash = filebase64sha256("./main.zip")
  runtime = "python3.10"
  publish = false #create versions with changes
  tracing_config {
    mode = "Active"
  }
  lifecycle {
    create_before_destroy = true
  }
  timeout = 900
  tags = {
    Application = "PATCh",
    Environment = "nonprod",
    Team = "PATCh",
    Creator = "terraform-{PROJECT_NAME}",
    APMId = "BA0001171"
  }
}
