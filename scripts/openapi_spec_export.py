import os
import json
from app.main import app

def export_openapi_spec():
    # Export the OpenAPI spec from FastAPI
    openapi_spec = app.openapi()
    
    openapi_spec['paths']['/docs'] = {
        'get': {
            'summary': 'Swagger UI',
            'description': 'Serves the Swagger UI',
            'operationId': 'get_docs',
            'responses': {
                '200': {
                    'description': 'Successful response',
                    'content': {
                        'text/html': {
                            'schema': {
                                'type': 'string'
                            }
                        }
                    }
                }
            }
        }
    }
    
    openapi_spec['paths']['/openapi.json'] = {
        'get': {
            'summary': 'OpenAPI Specification',
            'description': 'Returns the OpenAPI specification for this API',
            'operationId': 'get_openapi_spec',
            'responses': {
                '200': {
                    'description': 'Successful response',
                    'content': {
                        'application/json': {
                            'schema': {
                                'type': 'object'
                            }
                        }
                    }
                }
            }
        }
    }
    
    return openapi_spec

# Function to update OpenAPI spec for Lambda proxy integration
def update_openapi_with_lambda_proxy(openapi_spec, lambda_arn, region):
    for path, path_info in openapi_spec.get('paths', {}).items():
        for method, method_info in path_info.items():
            method_info['x-amazon-apigateway-integration'] = {
                "type": "aws_proxy",
                "httpMethod": "POST",
                "uri": f"arn:aws:apigateway:{region}:lambda:path/2015-03-31/functions/{lambda_arn}/invocations",
                "cache_key_parameters": ["method.request.path.proxy"],
                "passthroughBehavior": "when_no_match",
                "contentHandling": "CONVERT_TO_TEXT",
                "timeoutInMillis": 29000,
                "responses": {
                    "default": {
                        "statusCode": "200"
                    }
                }
            }
    return openapi_spec

def save_openapi_spec(openapi_spec, output_file):
    with open(output_file, 'w') as file:
        json.dump(openapi_spec, file, indent=2)

def main():
    lambda_arn = os.environ.get("LAMBDA_ARN")
    output_file = os.environ.get("OUTPUT_FILE")
    region = os.environ.get("AWS_REGION")
    
    openapi_spec = export_openapi_spec()
    updated_spec = update_openapi_with_lambda_proxy(openapi_spec, lambda_arn, region)
    
    save_openapi_spec(updated_spec, output_file)
    print(f"Updated OpenAPI spec saved to {output_file}")

if __name__ == "__main__":
    main()