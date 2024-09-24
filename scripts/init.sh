#!/bin/bash

# Function to check if a command is installed
check_installed() {
  if command -v $1 >/dev/null 2>&1; then
    echo -e "\n✅ $1 is already installed."
    $1 --version
  else
    echo "🚫 $1 is not installed. Installing $1... ⏳"
    install_$1
  fi
}

# Check if Homebrew is installed (macOS only)
check_brew() {
  if [[ "$OSTYPE" == "darwin"* ]]; then
    if ! command -v brew >/dev/null 2>&1; then
      echo "🍺 Homebrew is not installed on your system."
      echo "👉 Please install Homebrew first: https://brew.sh"
      exit 1
    fi
    echo "🍺 Homebrew is installed."
  fi
}

# Install Poetry
install_poetry() {
  if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "📦 Installing Poetry via Homebrew (macOS detected)..."
    brew install poetry
    if [[ $? -ne 0 ]]; then
      echo "❌ Poetry installation via Homebrew failed!"
      exit 1
    fi
  else
    echo "📦 Installing Poetry via Python..."
    curl -sSL https://install.python-poetry.org | python3 -
    if [[ $? -ne 0 ]]; then
      echo "❌ Poetry installation failed!"
      exit 1
    fi
  fi
  echo "📦 Installing Poetry plugin..."
  poetry run pip install poetry-plugin
  echo "✅ Poetry installation completed successfully!"
}


# Install AWS CLI
install_aws() {
  echo "📦 Installing AWS CLI..."
  if [[ "$OSTYPE" == "darwin"* ]]; then
    brew install awscli
  else
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
    rm -rf awscliv2.zip aws
  fi
  if [[ $? -ne 0 ]]; then
    echo "❌ AWS CLI installation failed!"
    exit 1
  fi
  echo "✅ AWS CLI installation completed successfully!"
}

# Install Terraform
install_terraform() {
  echo "📦 Installing Terraform..."
  if [[ "$OSTYPE" == "darwin"* ]]; then
    brew tap hashicorp/tap
    brew install hashicorp/tap/terraform
  else
    sudo dnf install -y dnf-plugins-core
    sudo dnf config-manager --add-repo https://rpm.releases.hashicorp.com/fedora/hashicorp.repo
    sudo dnf -y install terraform
  fi
  if [[ $? -ne 0 ]]; then
    echo "❌ Terraform installation failed!"
    exit 1
  fi
  echo "✅ Terraform installation completed successfully!"
}

# Install Trivy with Homebrew (macOS only)
install_trivy() {
  echo "📦 Installing Trivy via Homebrew..."
  brew install trivy
  if [[ $? -ne 0 ]]; then
    echo "❌ Trivy installation failed!"
    exit 1
  fi
  echo "✅ Trivy installation completed successfully!"
}

# Check if Homebrew is installed on macOS before continuing
check_brew

# Check and install Poetry, AWS CLI, and Terraform if not installed
echo "🔍 Checking if Poetry, AWS CLI, and Terraform are installed..."

check_installed poetry
check_installed aws
check_installed terraform
check_installed trivy

echo "🎉 All done! Script completed successfully. 🚀"
