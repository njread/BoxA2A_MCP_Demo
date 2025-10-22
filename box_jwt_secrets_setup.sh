#!/bin/bash
# box_jwt_secrets_setup.sh
# 
# This script sets up Box JWT credentials in Google Secret Manager
# for secure, production-ready authentication without local config files.
#
# Usage: ./box_jwt_secrets_setup.sh

echo "🔐 Setting up Box JWT secrets in Google Secret Manager..."
echo ""

# Prompt for credentials
read -p "Enter Box Client ID: " BOX_CLIENT_ID
read -p "Enter Box Client Secret: " BOX_CLIENT_SECRET
read -p "Enter Box Public Key ID: " BOX_PUBLIC_KEY_ID
read -p "Enter Box Enterprise ID: " BOX_ENTERPRISE_ID
read -s -p "Enter Box Private Key Passphrase: " BOX_PASSPHRASE
echo ""
read -p "Enter path to Box Private Key PEM file: " BOX_PRIVATE_KEY_PATH

# Set project (update this to your actual project ID)
read -p "Enter your Google Cloud Project ID: " PROJECT_ID

echo ""
echo "📝 Creating secrets in project: $PROJECT_ID"
echo ""

# Check if project ID is provided
if [ -z "$PROJECT_ID" ]; then
    echo "❌ Error: Project ID is required"
    exit 1
fi

# Check if private key file exists
if [ ! -f "$BOX_PRIVATE_KEY_PATH" ]; then
    echo "❌ Error: Private key file not found: $BOX_PRIVATE_KEY_PATH"
    exit 1
fi

echo "🔍 Verifying gcloud authentication..."
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ Error: Not authenticated with gcloud. Please run 'gcloud auth login' first."
    exit 1
fi

echo "✅ Authentication verified"
echo ""

# Create secrets
echo "Creating box-client-id..."
if echo -n "$BOX_CLIENT_ID" | gcloud secrets create box-client-id --data-file=- --project="$PROJECT_ID" 2>/dev/null; then
    echo "✅ Created box-client-id"
else
    echo "⚠️  box-client-id already exists, updating..."
    echo -n "$BOX_CLIENT_ID" | gcloud secrets versions add box-client-id --data-file=- --project="$PROJECT_ID"
fi

echo "Creating box-client-secret..."
if echo -n "$BOX_CLIENT_SECRET" | gcloud secrets create box-client-secret --data-file=- --project="$PROJECT_ID" 2>/dev/null; then
    echo "✅ Created box-client-secret"
else
    echo "⚠️  box-client-secret already exists, updating..."
    echo -n "$BOX_CLIENT_SECRET" | gcloud secrets versions add box-client-secret --data-file=- --project="$PROJECT_ID"
fi

echo "Creating box-public-key-id..."
if echo -n "$BOX_PUBLIC_KEY_ID" | gcloud secrets create box-public-key-id --data-file=- --project="$PROJECT_ID" 2>/dev/null; then
    echo "✅ Created box-public-key-id"
else
    echo "⚠️  box-public-key-id already exists, updating..."
    echo -n "$BOX_PUBLIC_KEY_ID" | gcloud secrets versions add box-public-key-id --data-file=- --project="$PROJECT_ID"
fi

echo "Creating box-enterprise-id..."
if echo -n "$BOX_ENTERPRISE_ID" | gcloud secrets create box-enterprise-id --data-file=- --project="$PROJECT_ID" 2>/dev/null; then
    echo "✅ Created box-enterprise-id"
else
    echo "⚠️  box-enterprise-id already exists, updating..."
    echo -n "$BOX_ENTERPRISE_ID" | gcloud secrets versions add box-enterprise-id --data-file=- --project="$PROJECT_ID"
fi

echo "Creating box-private-key-passphrase..."
if echo -n "$BOX_PASSPHRASE" | gcloud secrets create box-private-key-passphrase --data-file=- --project="$PROJECT_ID" 2>/dev/null; then
    echo "✅ Created box-private-key-passphrase"
else
    echo "⚠️  box-private-key-passphrase already exists, updating..."
    echo -n "$BOX_PASSPHRASE" | gcloud secrets versions add box-private-key-passphrase --data-file=- --project="$PROJECT_ID"
fi

echo "Creating box-private-key..."
if gcloud secrets create box-private-key --data-file="$BOX_PRIVATE_KEY_PATH" --project="$PROJECT_ID" 2>/dev/null; then
    echo "✅ Created box-private-key"
else
    echo "⚠️  box-private-key already exists, updating..."
    gcloud secrets versions add box-private-key --data-file="$BOX_PRIVATE_KEY_PATH" --project="$PROJECT_ID"
fi

echo ""
echo "🎉 All Box JWT secrets created/updated successfully!"
echo "🔒 Your credentials are now securely stored in Google Secret Manager"
echo ""
echo "📋 Next steps:"
echo "1. Update your requirements.txt to include: google-cloud-secret-manager>=2.0.0"
echo "2. Update your box_auth.py to use Secret Manager instead of local config"
echo "3. Update your .gitignore to exclude box_jwt_config.json"
echo "4. Deploy your updated agent to Cloud Run"
echo ""
echo "🔍 To verify secrets were created:"
echo "   gcloud secrets list --project=$PROJECT_ID | grep box-"
echo ""
echo "📖 For more information, see the README.md file" 