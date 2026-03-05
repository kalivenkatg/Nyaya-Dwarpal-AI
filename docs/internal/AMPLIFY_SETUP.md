# AWS Amplify Deployment Setup

## Environment Variables

To deploy this application to AWS Amplify, you need to set the following environment variable in the Amplify Console:

### Required Environment Variable

- **SARVAM_API_KEY**: Your Sarvam AI API key

## Setup Instructions

1. **Go to AWS Amplify Console**
   - Navigate to your app in the Amplify Console
   - Go to "App settings" → "Environment variables"

2. **Add Environment Variable**
   - Click "Manage variables"
   - Add a new variable:
     - Key: `SARVAM_API_KEY`
     - Value: Your actual Sarvam AI API key (e.g., `sk_xxxxx_xxxxxxxxxx`)
   - Click "Save"

3. **Deploy**
   - The `amplify.yml` build configuration will automatically inject the API key during build
   - The key will be replaced in the meta tag: `<meta name="sarvam-key" content="REPLACE_AT_BUILD">`
   - JavaScript reads the key at runtime: `document.querySelector('meta[name="sarvam-key"]').content`

## Build Configuration

The `amplify.yml` file contains:

```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - sed -i "s/REPLACE_AT_BUILD/$SARVAM_API_KEY/g" ui/enhanced-index.html
    build:
      commands:
        - echo "Build complete"
  artifacts:
    baseDirectory: ui
    files:
      - '**/*'
```

## Security Notes

- The API key is injected at build time, not stored in the repository
- The key is only visible in the deployed HTML (not in source code)
- For production, consider using a backend proxy to hide the API key completely
- Rotate your API key regularly

## Testing Locally

To test locally with your API key:

1. Open `ui/enhanced-index.html`
2. Replace `REPLACE_AT_BUILD` in the meta tag with your actual key
3. Open the file in your browser
4. **Important**: Don't commit this change!

## Alternative: Backend Proxy (Recommended for Production)

For better security, consider:
1. Create a Lambda function that calls Sarvam AI
2. Store the API key in AWS Secrets Manager
3. Have the frontend call your Lambda instead of Sarvam AI directly
4. This keeps the API key completely hidden from the client
