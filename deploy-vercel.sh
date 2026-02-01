#!/bin/bash
# Vercel Auto-Deploy Script for Jarvis Omega Website

echo "=========================================="
echo "  JARVIS OMEGA - Vercel Deployment"
echo "=========================================="
echo ""

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null
then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

echo "✓ Vercel CLI ready"
echo ""

# Check if website directory exists
if [ ! -d "website" ]; then
    echo "❌ Error: website directory not found!"
    exit 1
fi

echo "📦 Building deployment package..."
echo ""

# Create a temporary deployment directory
rm -rf .vercel-deploy
mkdir -p .vercel-deploy/website
mkdir -p .vercel-deploy/downloads

# Copy website files
cp -r website/* .vercel-deploy/website/

echo "✓ Website files copied"

# Check if dist folder exists (for built Jarvis executable)
if [ -d "dist" ]; then
    echo "✓ Found dist folder - copying executable..."
    # Copy the executable if it exists
    if [ -f "dist/Jarvis.exe" ]; then
        cp dist/Jarvis.exe .vercel-deploy/downloads/Jarvis-Omega.exe
        echo "✓ Jarvis.exe copied to downloads"
    fi
fi

echo ""
echo "🚀 Deploying to Vercel..."
echo ""

# Deploy to Vercel
cd .vercel-deploy
vercel --prod

echo ""
echo "=========================================="
echo "  ✓ Deployment Complete!"
echo "=========================================="
echo ""
echo "Your Jarvis Omega website is now live!"
echo ""
