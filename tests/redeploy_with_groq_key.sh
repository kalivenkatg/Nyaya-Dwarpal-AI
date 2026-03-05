#!/bin/bash

# Redeploy Voice Triage Lambda with GROQ_API_KEY
# This script ensures the API key is set before deployment

echo "=========================================="
echo "Voice Triage Lambda Redeployment"
echo "=========================================="
echo ""

# Check if GROQ_API_KEY is set
if [ -z "$GROQ_API_KEY" ]; then
    echo "❌ ERROR: GROQ_API_KEY environment variable is not set!"
    echo ""
    echo "Please set it with:"
    echo "  export GROQ_API_KEY='your-groq-api-key-here'"
    echo ""
    echo "Then run this script again."
    exit 1
fi

echo "✓ GROQ_API_KEY is set (length: ${#GROQ_API_KEY})"
echo ""

# Confirm deployment
echo "This will deploy the Voice Triage Lambda with the GROQ_API_KEY."
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled."
    exit 0
fi

echo ""
echo "=========================================="
echo "Deploying CDK Stack..."
echo "=========================================="
echo ""

# Deploy
npx cdk deploy --require-approval never

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✓ Deployment Successful!"
    echo "=========================================="
    echo ""
    echo "Next steps:"
    echo "1. Test the voice triage endpoint with:"
    echo "   'Auto wale ne meter se 3 guna paisa manga'"
    echo ""
    echo "2. Check CloudWatch logs for:"
    echo "   - [Groq] Invoking model..."
    echo "   - [Groq] Response received..."
    echo "   - Parsed classification - Category: Consumer Rights"
    echo ""
    echo "3. Verify the response contains:"
    echo "   - category: 'Consumer Rights'"
    echo "   - NOT 'Other'"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "❌ Deployment Failed"
    echo "=========================================="
    echo ""
    echo "Check the error messages above."
    exit 1
fi
