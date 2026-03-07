# Security Fix Complete

## Issue Identified
Hardcoded SARVAM_API_KEY found in `infrastructure/nyaya_dwarpal_stack.py`:
- Line 391: `"SARVAM_API_KEY": "sk_a07scrq0_Bx8WyEWNUGBLYx6OWXs4hrF7"`
- Line 349: `"SARVAM_AI_API_KEY": "REDACTED_API_KEY"`

## Actions Taken

### 1. Removed Hardcoded API Keys
- Updated `audio_transcribe_lambda` environment to use: `os.environ.get("SARVAM_API_KEY", "")`
- Updated `translation_lambda` environment to use: `os.environ.get("SARVAM_API_KEY", "")`
- Committed changes with message: "Security: Remove hardcoded SARVAM_API_KEY from infrastructure"
- Pushed to GitHub: commit `14ebd39`

### 2. Verified .gitignore
- Confirmed `.env` files are already excluded from version control
- `.gitignore` includes: `.env`, `.env.*`, `*.env`

## CRITICAL: Next Steps Required

### 1. Rotate the Exposed API Key
The key `sk_a07scrq0_Bx8WyEWNUGBLYx6OWXs4hrF7` is now exposed in your GitHub repository history.

**You MUST rotate this key immediately:**
1. Go to Sarvam AI dashboard: https://www.sarvam.ai/
2. Revoke the exposed key: `sk_a07scrq0_Bx8WyEWNUGBLYx6OWXs4hrF7`
3. Generate a new API key
4. Update your environment variable

### 2. Set Environment Variable for CDK Deployment
Before deploying with CDK, set the environment variable:

```bash
export SARVAM_API_KEY="your-new-api-key-here"
cdk deploy
```

Or create a `.env` file (already in .gitignore):
```bash
echo "SARVAM_API_KEY=your-new-api-key-here" > .env
source .env
cdk deploy
```

### 3. Update Lambda Environment Variables
After deployment, the Lambda functions will use the environment variable you set during `cdk deploy`.

## Status
✅ Hardcoded keys removed from code
✅ Changes committed and pushed to GitHub
⚠️ **ACTION REQUIRED**: Rotate exposed API key at Sarvam AI dashboard
⚠️ **ACTION REQUIRED**: Set SARVAM_API_KEY environment variable before next deployment

## Git History Note
The exposed key exists in previous commits. If this is a security concern, you may need to:
1. Use `git filter-branch` or BFG Repo-Cleaner to remove it from history
2. Force push to GitHub (this will rewrite history)
3. Notify all collaborators to re-clone the repository

For now, rotating the key is the most important step.
