SHELL := /bin/bash

RED=\033[0;31m
GREEN=\033[0;32m
YELLOW=\033[0;33m
LBLUE=\033[0;94m
PURPLE=\033[0;35m
NC=\033[0m

# Define variables
TF_FILES := $(shell find infra -type f -name '*.tf')
PYTHON_FILES := $(shell find app -type f -name '*.py')
ZIP_EXCLUDE := --exclude=*.pyc --exclude=__pycache__ --exclude=tests
POETRY_VERSION := $(shell poetry version --short)
LAMBDA_ZIP := lambda_function.zip
LAMBDA_LAYER := lambda_layer.zip
BUILD_OUTPUT := dist
LAYER_BUILD_DIR := ${BUILD_OUTPUT}/layer_build/python
S3_BUCKET := ebapi-terraform-state
S3_KEY := ebapi/terraform.tfstate

# Targets

init:
	@printf "[${GREEN}Init${NC}]\n"
	scripts/init.sh

install:
	@printf "[${GREEN}Install${NC}]\n"
	poetry install

seed:
	@printf "[${GREEN}Seeding${NC}]\n"
	poetry run python scripts/seed.py

run:
	@printf "[${GREEN}Run Local${NC}]\n"
	poetry run uvicorn app.main:app --reload


.PHONY: all
all: build test deploy


.PHONY: lint
lint:
	@printf "[${GREEN}Run Pylint${NC}]\n"
	poetry run pylint --recursive=y app/ app/api/ app/db/models/


.PHONY: test
test:
	@printf "[${GREEN}Run Unit Test with Coverage${NC}]\n"
	poetry run pytest --cov=app --cov-report=term-missing --cov-fail-under=80


.PHONY: test-verbose
test-verbose:
	@printf "[${GREEN}Run Verbose Unit Test with Coverage${NC}]\n"
	poetry run coverage run -m pytest tests/ -vvv

.PHONY: trivy
trivy:
	@printf "[${GREEN}Scan Terraform IaC with Trivy${NC}]\n"
	trivy fs --severity MEDIUM,HIGH,CRITICAL --scanners vuln,secret,misconfig --quiet infra/

.PHONY: deploy
deploy: lint test trivy build build-layer terraform-init terraform-apply

.PHONY: build
build:
	@printf "[${GREEN}BUILD Lambda Function${NC}]\n"
	rm -rf ${BUILD_OUTPUT}/$(LAMBDA_ZIP)
	mkdir -p ${BUILD_OUTPUT}
	# Package the application code, preserving structure but excluding the app root
	find app -type f -not -path "*/tests/*" -not -path "*/__pycache__/*" -not -name "*.pyc" -exec zip -r ${BUILD_OUTPUT}/$(LAMBDA_ZIP) {} \;
	@echo "Lambda function package built: ${BUILD_OUTPUT}/$(LAMBDA_ZIP)"
	
.PHONY: build-layer
build-layer:
	@printf "[${GREEN}BUILD Lambda Layer${NC}]\n"
	rm -f ${BUILD_OUTPUT}/$(LAMBDA_LAYER)
	mkdir -p ${BUILD_OUTPUT}/layer_build
	# Export only runtime dependencies from Poetry
	poetry run poetry export --without-hashes -f requirements.txt --only runtime > ${BUILD_OUTPUT}/requirements.txt
	# Use pip to install runtime dependencies into the target directory, ignoring boto3 and botocore
	poetry run pip install -r ${BUILD_OUTPUT}/requirements.txt --target ${LAYER_BUILD_DIR} --ignore-installed boto3 --ignore-installed botocore
	# Remove unwanted directories
	rm -rf ${LAYER_BUILD_DIR}/boto3 ${LAYER_BUILD_DIR}/botocore ${LAYER_BUILD_DIR}/__pycache__ ${LAYER_BUILD_DIR}/*.dist-info
	# Change into the layer_build directory to zip from there, excluding .dist-info files
	cd ${BUILD_OUTPUT}/layer_build && find . -type f | zip -@ ../$(LAMBDA_LAYER)
	rm -rf ${BUILD_OUTPUT}/layer_build
	@echo "Lambda Layer built: ${BUILD_OUTPUT}/$(LAMBDA_LAYER)"

.PHONY: terraform-init
terraform-init:
	@printf "[${LBLUE}Terraform - Init${NC}]\n"
	terraform -chdir=infra init

.PHONY: terraform-plan
terraform-plan:
	@printf "[${YELLOW}Terraform - Apply${NC}]\n"
	terraform -chdir=infra plan

.PHONY: terraform-apply
terraform-apply:
	@printf "[${LBLUE}Terraform - Apply${NC}]\n"
	terraform -chdir=infra apply -auto-approve

.PHONY: terraform-destroy
terraform-destroy:
	@printf "[${RED}Terraform - Destroy${NC}]\n"
	terraform -chdir=infra destroy -auto-approve

.PHONY: setup-s3
setup-s3:
	@printf "[${RED}S3 - Setup${NC}]\n"
	aws s3 mb s3://$(S3_BUCKET) --region us-east-1
	aws s3api put-object --bucket $(S3_BUCKET) --key $(S3_KEY) --body /dev/null

.PHONY: clean
clean:
	@printf "[${YELLOW}Clean files${NC}]\n"
	rm -rf dist/
	rm -rf infra/.terraform/