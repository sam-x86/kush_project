#!/bin/bash
# Kush Framework - OSXCross Installation Script

set -e

echo "🔧 Installing OSXCross for macOS cross-compilation..."

# Check if we're on Linux
if [[ "$(uname)" != "Linux" ]]; then
    echo "❌ This script must be run on Linux for cross-compilation"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
sudo apt-get update
sudo apt-get install -y \
    clang \
    gcc \
    g++ \
    zlib1g-dev \
    libssl-dev \
    libxml2-dev \
    liblzma-dev \
    libmpc-dev \
    libmpfr-dev \
    libgmp-dev \
    cmake \
    git \
    patchelf \
    python3 \
    python3-pip

# Create build directory
mkdir -p build
cd build

# Clone OSXCross
if [ ! -d "osxcross" ]; then
    echo "📥 Cloning OSXCross..."
    git clone https://github.com/tpoechtrager/osxcross.git
fi

cd osxcross

# Download macOS SDK
echo "📦 Downloading macOS SDK..."
if [ ! -f "tarballs/MacOSX10.15.sdk.tar.xz" ]; then
    wget -nc https://github.com/joseluo/osxcross-sdk/releases/download/10.15/MacOSX10.15.sdk.tar.xz -O tarballs/MacOSX10.15.sdk.tar.xz
fi

# Build OSXCross
echo "🏗️ Building OSXCross..."
UNATTENDED=1 ./build.sh

echo "✅ OSXCross installation complete!"
echo ""
echo "Usage examples:"
echo "  x86_64-apple-darwin19-clang -o payload_macos payload.c"
echo "  x86_64-apple-darwin19-clang++ -o payload_macos payload.cpp"

# Add to PATH
echo 'export PATH="$PATH:'$(pwd)'/target/bin"' >> ~/.bashrc
echo "📝 Added OSXCross to PATH. Run: source ~/.bashrc"