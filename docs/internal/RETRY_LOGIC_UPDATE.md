# Bedrock Retry Logic Update

## Changes Made

### 1. Added ResourceNotFoundException Retry Logic

Updated both bedrock_client.py files to automatically retry when encountering `ResourceNotFoundException`:

**Files Updated:**
- `lambda_functions/shared/bedrock_client.py`
- `lambda_functions/shared/python/bedrock_client.py`

**Retry Behavior:**
```python
# Handle ResourceNotFoundException with 2-second delay retry
if error_code == "ResourceNotFoundException" and attempt < retry_attempts - 1:
    time.sleep(2.0)  # Wait 2 seconds before retry
    continue
```

**Retry Configuration:**
- Default retry attempts: 3
- Delay for ResourceNotFoundException: 2 seconds (fixed)
- Delay for ThrottlingException: Exponential backoff (1s, 2s, 4s)

### 2. Verified Model ID

Confirmed both files use the correct US inference profile:
```python
MODEL_ID = "us.anthropic.claude-haiku-4-5-20251001-v1:0"
```

### 3. Deployment

Successfully deployed with:
```bash
npx cdk deploy --require-approval never
```

**Deployment Status:** ✅ Success
**Deployment Time:** 67.1s
**API Endpoint:** https://ked0qedvxi.execute-api.ap-south-2.amazonaws.com/prod/

## Test Results

### Voice Triage Test
```bash
curl -X POST https://ked0qedvxi.execute-api.ap-south-2.amazonaws.com/prod/voice/triage \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "test-user-retry-001",
    "transcribedText": "My landlord has not returned my security deposit for 3 months and is threatening me when I ask for it back",
    "language": "en"
  }'
```

**Response:** API returned fallback values (confidence 0.5, category "Other")

**CloudWatch Logs:**
```
Error in emotion detection: An error occurred (ResourceNotFoundException) when calling the InvokeModel operation: Model use case details have not been submitted for this account. Fill out the Anthropic use case details form before using the model. If you have already filled out the form, try again in 15 minutes.
```

## Current Status

### ✅ Completed
- Retry logic for ResourceNotFoundException added
- Model ID verified and correct
- Deployment successful
- API endpoint responding

### ⚠️ Known Issue
The AWS account still requires Anthropic use case approval. The error message indicates:
> "Model use case details have not been submitted for this account. Fill out the Anthropic use case details form before using the model."

### How Retry Logic Helps

When the use case is approved and the model becomes intermittently available:
1. First call fails with ResourceNotFoundException → Wait 2 seconds
2. Second call attempts → If still fails, wait 2 seconds
3. Third call attempts → If still fails, return error to user

This handles temporary availability issues once the account has basic access.

## Next Steps

1. **Submit Anthropic Use Case Form** (if not already done)
2. **Wait 15 minutes** after form submission
3. **Test again** to verify retry logic works with intermittent access
4. **Monitor CloudWatch logs** to see retry attempts in action

## Files Modified

```
lambda_functions/shared/bedrock_client.py
lambda_functions/shared/python/bedrock_client.py
```

## Deployment Command

```bash
source venv/bin/activate
npx cdk deploy --require-approval never
```

---

**Date:** March 2, 2026
**Status:** Retry logic implemented and deployed
**Next Action:** Wait for AWS Bedrock use case approval
