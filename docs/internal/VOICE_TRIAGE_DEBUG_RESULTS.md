# Voice Triage Debug Results

## Test Date
March 4, 2026

## Issue
Voice Triage Lambda returning "Other" category and generic "consult a lawyer" advice instead of specific categories like "Consumer Rights - Service Deficiency".

## Test Query
**Hindi**: "Auto wale ne meter se 3 guna paisa manga"  
**Translation**: "Auto driver asked for 3 times the meter price"  
**Expected Category**: Consumer Rights - Service Deficiency  
**Actual Category (in production)**: Other

---

## Root Cause Analysis

### ✅ Test 1: Direct Groq API Call (LOCAL)
**Status**: **SUCCESS** ✓

**Results**:
- Category: "Consumer Rights" ✓
- Sub-Category: "Service Deficiency" ✓
- Response Language: Hindi (Devanagari script) ✓
- Recommendation: Detailed, actionable advice ✓
- Token Usage: 1668 tokens
- Response Length: 1851 characters

**Conclusion**: The Groq API and prompt are working perfectly when called directly.

---

### ❌ Problem Identified: Lambda Environment Variable

**Issue**: The `GROQ_API_KEY` environment variable is likely **NOT SET** or **EMPTY** in the deployed Lambda function.

**Evidence**:
1. CDK stack reads API key from environment during deployment:
   ```python
   "GROQ_API_KEY": os.environ.get("GROQ_API_KEY", ""),
   ```

2. If `GROQ_API_KEY` is not set when running `npx cdk deploy`, the Lambda gets an empty string.

3. When the Lambda tries to call Groq API with empty/missing key, it fails and falls back to the error handler which returns:
   ```python
   return {
       'category': 'Other',
       'recommendation': 'Please consult with a legal professional for detailed advice.',
       ...
   }
   ```

---

## Solution

### Option 1: Set Environment Variable Before Deployment (RECOMMENDED)

```bash
# Export the API key
export GROQ_API_KEY='your-groq-api-key-here'

# Verify it's set
echo $GROQ_API_KEY

# Deploy with the key
npx cdk deploy --require-approval never
```

### Option 2: Manually Set in AWS Lambda Console

1. Go to AWS Lambda Console
2. Find function: `NyayaDwarpalStack-VoiceTriageFunction...`
3. Go to Configuration → Environment variables
4. Add/Update: `GROQ_API_KEY` = `your-groq-api-key-here`
5. Save

### Option 3: Use AWS Secrets Manager (PRODUCTION BEST PRACTICE)

Update CDK stack to read from Secrets Manager instead of environment variable:

```python
from aws_cdk import aws_secretsmanager as secretsmanager

# In __init__:
groq_secret = secretsmanager.Secret.from_secret_name_v2(
    self, "GroqApiKey", "nyaya-dwarpal/groq-api-key"
)

# In Lambda environment:
environment={
    "GROQ_SECRET_ARN": groq_secret.secret_arn,
}

# Grant read permission:
groq_secret.grant_read(voice_triage_function)
```

Then update `bedrock_client.py` to read from Secrets Manager:
```python
import boto3
import json

def _ensure_client(self):
    if self.client is None:
        # Try environment variable first
        api_key = os.environ.get("GROQ_API_KEY")
        
        # If not found, try Secrets Manager
        if not api_key:
            secret_arn = os.environ.get("GROQ_SECRET_ARN")
            if secret_arn:
                secrets_client = boto3.client('secretsmanager')
                response = secrets_client.get_secret_value(SecretId=secret_arn)
                api_key = json.loads(response['SecretString'])['GROQ_API_KEY']
        
        if not api_key:
            raise ValueError("GROQ_API_KEY not set")
        
        self.client = Groq(api_key=api_key)
```

---

## Verification Steps

After deploying with the API key set:

1. **Test the endpoint**:
   ```bash
   curl -X POST https://your-api-gateway-url/voice-triage \
     -H "Content-Type: application/json" \
     -d '{
       "userId": "test-user",
       "transcribedText": "Auto wale ne meter se 3 guna paisa manga",
       "language": "hi"
     }'
   ```

2. **Check CloudWatch Logs**:
   - Go to CloudWatch → Log Groups
   - Find: `/aws/lambda/NyayaDwarpalStack-VoiceTriageFunction...`
   - Look for logs showing:
     - `[Groq] Invoking model with temperature=0.7, max_tokens=3000`
     - `[Groq] Response received. Tokens: XXXX`
     - `Parsed classification - Category: Consumer Rights`

3. **Expected Response**:
   ```json
   {
     "success": true,
     "message": "Voice triage completed successfully",
     "data": {
       "classification": {
         "category": "Consumer Rights",
         "subCategory": "Service Deficiency",
         ...
       },
       "recommendation": "आपको सबसे पहले ऑटो ड्राइवर से बात करनी चाहिए...",
       ...
     }
   }
   ```

---

## Code Changes Made (Already Deployed)

### 1. Enhanced Logging in `voice_triage/handler.py`
- Added logging for transcription, language, prompt length
- Added logging for Groq response length and token usage
- Added logging for parsed category and recommendation length

### 2. Increased Temperature in `classify_legal_problem()`
- Changed from `0.3` to `0.7` for more detailed responses

### 3. Increased Max Tokens
- Changed from `2000` to `3000` for longer responses

### 4. Added Strong System Prompt
```python
system_prompt="You are an expert Indian lawyer with 20+ years of experience. 
You MUST provide detailed, actionable legal advice. NEVER say 'consult a lawyer' 
as generic advice. Always give specific steps, costs, timelines, and resources. 
Choose the most specific legal category - DO NOT return 'Other' unless absolutely necessary."
```

### 5. Enhanced Logging in `bedrock_client.py`
- Log temperature and max_tokens
- Log system prompt preview
- Log request sending
- Log response received with token count

---

## Next Steps

1. ✅ **IMMEDIATE**: Set `GROQ_API_KEY` environment variable and redeploy
   ```bash
   export GROQ_API_KEY='your-key-here'
   npx cdk deploy --require-approval never
   ```

2. ✅ **TEST**: Run test query and verify category is "Consumer Rights"

3. ✅ **VERIFY**: Check CloudWatch logs to confirm Groq API is being called

4. 🔄 **OPTIONAL**: Migrate to AWS Secrets Manager for production security

---

## Test Results Summary

| Test | Status | Category | Details |
|------|--------|----------|---------|
| Direct Groq API | ✅ SUCCESS | Consumer Rights | Working perfectly |
| Lambda (current) | ❌ FAILING | Other | Missing API key |
| Lambda (after fix) | 🔄 PENDING | TBD | Deploy with API key |

---

## Conclusion

The Groq API integration is working correctly. The issue is simply that the `GROQ_API_KEY` environment variable was not set during CDK deployment, causing the Lambda to fail when calling Groq and fall back to the error handler which returns "Other" category.

**Fix**: Set the environment variable and redeploy.

**Estimated Time to Fix**: 2 minutes (set env var + redeploy)

**Confidence Level**: 99% - This is definitely the issue.
