# Petition Verifier Lambda - Troubleshooting Guide

## Quick Diagnosis

Run these three scripts in order to diagnose the 500 error:

```bash
# 1. Check Lambda configuration and permissions
python3 check_lambda_config.py

# 2. Check recent CloudWatch logs for error messages
python3 check_lambda_logs.py

# 3. Test the API endpoint
python3 test_petition_verifier.py
```

## What Was Fixed

### 1. Enhanced Error Handling in Lambda

**File**: `lambda_functions/petition_architect/handler.py`

**Changes**:
- Added comprehensive try/except blocks with detailed error messages
- Added JSON parsing validation
- Added empty body validation
- Added petition text validation
- Added traceback logging for all exceptions
- Made storage failures non-critical (won't break the request)

**Benefits**:
- 500 errors now return detailed error messages in the response
- CloudWatch logs show full stack traces
- Easier to identify the root cause

### 2. Improved Logging

Added detailed logging at every step:
- Request parsing
- Validation checks
- Bedrock API calls
- Textract operations
- Verification logic
- Storage operations

### 3. Created Diagnostic Tools

**check_lambda_config.py**:
- Shows Lambda configuration (runtime, memory, timeout)
- Lists environment variables
- Shows attached Lambda layers
- Displays IAM role permissions
- Shows recent invocation metrics

**check_lambda_logs.py**:
- Fetches recent CloudWatch logs
- Shows error messages and stack traces
- Helps identify the exact failure point

**test_petition_verifier.py**:
- Tests the API with minimal payload
- Tests with full petition containing outdated citations
- Shows detailed response including error messages

## Common Issues and Solutions

### Issue 1: "No module named 'pydantic'"

**Symptoms**:
- 500 Internal Server Error
- CloudWatch logs show: `ModuleNotFoundError: No module named 'pydantic'`

**Root Cause**: Lambda layer doesn't have pydantic installed in the correct directory structure

**Solution**:
```bash
cd lambda_functions/shared
mkdir -p python
pip install -r requirements.txt -t python/ --upgrade
cd ../..
npx cdk deploy
```

**Why**: Lambda layers must have dependencies in a `python/` subdirectory, not at the root level.

### Issue 2: "Unable to import module 'handler'"

**Symptoms**:
- 500 Internal Server Error
- CloudWatch logs show: `Unable to import module 'handler': No module named 'handler'`

**Root Cause**: Handler file not found or import path issues

**Solution**:
1. Verify handler path in CDK stack: `handler="handler.lambda_handler"`
2. Verify file exists: `lambda_functions/petition_architect/handler.py`
3. Check layer path in handler: `sys.path.insert(0, '/opt/python')`

### Issue 3: Bedrock Access Denied

**Symptoms**:
- 500 Internal Server Error
- CloudWatch logs show: `AccessDeniedException` or `UnauthorizedException` for Bedrock

**Root Cause**: Lambda execution role doesn't have Bedrock permissions

**Solution**: Already fixed in CDK stack. Verify with:
```bash
python3 check_lambda_config.py
```

Should show:
```
Actions:
  - bedrock:InvokeModel
  - bedrock:InvokeModelWithResponseStream
```

### Issue 4: Textract Access Denied

**Symptoms**:
- 500 Internal Server Error when using `/petition/clarify` endpoint
- CloudWatch logs show: `AccessDeniedException` for Textract

**Root Cause**: Lambda execution role doesn't have Textract permissions

**Solution**: Already fixed in CDK stack. Verify with:
```bash
python3 check_lambda_config.py
```

Should show:
```
Actions:
  - textract:AnalyzeDocument
  - textract:DetectDocumentText
```

### Issue 5: S3 Access Denied

**Symptoms**:
- 500 Internal Server Error when using `/petition/clarify` endpoint
- CloudWatch logs show: `AccessDeniedException` for S3

**Root Cause**: Lambda can't read from document bucket

**Solution**: Already fixed in CDK stack. The Lambda role has full read/write access to both buckets.

### Issue 6: DynamoDB Access Denied

**Symptoms**:
- Request succeeds but warning in logs about storage failure
- CloudWatch logs show: `AccessDeniedException` for DynamoDB

**Root Cause**: Lambda can't write to session table

**Solution**: Already fixed in CDK stack. The Lambda role has full read/write access to all tables.

## Step-by-Step Troubleshooting

### Step 1: Check Lambda Configuration

```bash
python3 check_lambda_config.py
```

**Look for**:
- Runtime: Should be `python3.11`
- Handler: Should be `handler.lambda_handler`
- Layers: Should have `NyayaDwarpal-Shared` layer
- Environment Variables: Should have `DOCUMENT_BUCKET`, `SESSION_TABLE`, `BEDROCK_REGION`
- IAM Permissions: Should have Bedrock, Textract, S3, DynamoDB permissions

### Step 2: Check CloudWatch Logs

```bash
python3 check_lambda_logs.py
```

**Look for**:
- `ModuleNotFoundError` → Dependency issue (see Issue 1)
- `AccessDeniedException` → Permission issue (see Issues 3-6)
- `KeyError` or `AttributeError` → Code logic issue
- Stack traces → Identify the exact line causing the error

### Step 3: Test the API

```bash
python3 test_petition_verifier.py
```

**Look for**:
- Status Code 200 → Success
- Status Code 400 → Bad request (check payload format)
- Status Code 500 → Server error (check logs from Step 2)
- Error message in response body → Detailed error description

### Step 4: Fix and Redeploy

Based on the error identified:

**For dependency issues**:
```bash
./deploy_petition_verifier.sh
```

**For code issues**:
1. Fix the code in `lambda_functions/petition_architect/handler.py`
2. Run `npx cdk deploy`

**For permission issues**:
1. Fix IAM policies in `infrastructure/nyaya_dwarpal_stack.py`
2. Run `npx cdk deploy`

## Testing After Fix

After redeploying, test again:

```bash
# Test with minimal payload
python3 test_petition_verifier.py

# Check logs to verify no errors
python3 check_lambda_logs.py
```

## Expected Successful Response

```json
{
  "success": true,
  "message": "Verification completed",
  "data": {
    "verificationId": "uuid-here",
    "status": "completed",
    "results": {
      "status": "major_defects",
      "complianceScore": 70,
      "totalIssues": 3,
      "outdatedCitations": [
        {
          "type": "outdated_ipc",
          "original": "IPC Section 302",
          "suggested": "BNS Section 103",
          "severity": "high"
        }
      ],
      "missingSections": [],
      "proceduralDefects": [],
      "summary": "Petition has 3 defect(s) requiring attention..."
    }
  },
  "timestamp": "2024-01-20T10:30:00.000Z"
}
```

## Need More Help?

If the issue persists after following this guide:

1. Share the output of all three diagnostic scripts
2. Share the exact error message from CloudWatch logs
3. Share the request payload you're sending
4. Share the full response body you're receiving
