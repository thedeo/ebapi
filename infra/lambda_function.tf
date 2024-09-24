resource "aws_lambda_function" "ebapi" {
  filename         = "${local.dist_path}/lambda_function.zip"
  source_code_hash = filebase64sha256("${local.dist_path}/lambda_function.zip")
  function_name    = local.name
  role             = aws_iam_role.ebapi.arn
  handler          = "app.main.lambda_handler"
  runtime          = "python3.12"
  timeout          = 30
  layers           = [aws_lambda_layer_version.ebapi.arn]

  environment {
    variables = {
      env            = var.env
      API_DATA_TABLE = "${local.name}-data"
    }
  }
}

resource "aws_lambda_layer_version" "ebapi" {
  filename            = "${local.dist_path}/lambda_layer.zip"
  source_code_hash    = filebase64sha256("${local.dist_path}/requirements.txt")
  layer_name          = "${local.name}-fastapi"
  compatible_runtimes = ["python3.12"]
}

resource "aws_iam_role_policy" "ebapi" {
  name = "${local.name}-lambda"
  role = aws_iam_role.ebapi.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = "lambda:InvokeFunction"
        Resource = "arn:aws:lambda:*:*:function:${local.name}"
      },
      {
        Effect = "Allow"
        Action = [
          "dynamodb:Query",
          "dynamodb:Scan",
          "dynamodb:GetItem",
        ]
        Resource = "arn:aws:dynamodb:${var.region}:${data.aws_caller_identity.current.account_id}:table/${var.data_table_name}*"
      }
    ]
  })
}

resource "aws_iam_role" "ebapi" {
  name = "${local.name}-lambda-exec"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}
resource "aws_iam_role_policy_attachment" "ebapi" {
  role       = aws_iam_role.ebapi.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_permission" "ebapi" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ebapi.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_rest_api.ebapi.execution_arn}/*/*"
}
