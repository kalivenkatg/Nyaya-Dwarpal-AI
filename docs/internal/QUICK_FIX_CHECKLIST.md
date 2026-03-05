# Quick Fix Checklist - Petition Verifier 500 Error

## ✅ What's Already Done

- [x] Enhanced error handling in Lambda handler
- [x] Added comprehensive logging with stack traces
- [x] Added request validation (JSON parsing, empty body, required fields)
- [x] Made Bedrock failures non-critical (returns empty array)
- [x] Made storage failures non-critical (won't break request)
- [x] IAM permissions already configured (Bedrock, Textract, S3, DynamoDB)
- [x] Created diagnostic tools (config checker, log viewer, API tester)
- [x] Created deployment script with correct layer structure
- [x] Created comprehensive documentation

## 🔍 Next Steps (Run These Commands)

### 1. Diagnose the Issue

```bash
# Check Lambda configuration and permissions
python3 check_lambda_config.py

# Check CloudWatch logs for error messages  
python3 check_lambda_logs.py

# Test the API endpoint
python3 test_petition_verifier.py
```

### 2. Identify the Root Cause

Based on the output, identify which issue you have:

#### Issue A: "No module named 'pydantic'"

**Symptoms**:
- CloudWatch logs show `ModuleNotFoundError: No module named 'pydantic'`
- Test script returns 500 error

**Fix**:
```bash
./deploy_petition_verifier.sh
```

**Why**: Lambda layer needs pydantic installed in `python/` subdirectory.

#### Issue B: "AccessDeniedException"

**Symptoms**:
- CloudWatch logs show `AccessDeniedException` for Bedrock/Textract/S3/DynamoDB
- Test script returns 500 error

**Fix**: Permissions should already be correct. Check with:
```bash
python3 check_lambda_config.py
```

If permissions are missing, they'll be shown in the output. Wait a few minutes for IAM propagation, then test again.

#### Issue C: Other Errors

**Symptoms**:
- CloudWatch logs show different error
- Test script returns 500 error with detailed message

**Fix**: Check the error message in CloudWatch logs. The enhanced error handling should now show the exact issue. Refer to TROUBLESHOOTING_GUIDE.md for solutions.

### 3. Verify the Fix

After applying the fix, test again:

```bash
python3 test_petition_verifier.py
```

**Expected Result**:
- Status Code: 200
- Success: true
- Verification results with outdated citations detected

## 📋 Quick Reference

### Files Modified

| File | What Changed |
|------|--------------|
| `lambda_functions/petition_architect/handler.py` | Enhanced error handling, logging, validation |

### Files Created

| File | Purpose |
|------|---------|
| `check_lambda_config.py` | Check Lambda configuration and IAM permissions |
| `check_lambda_logs.py` | View recent CloudWatch logs |
| `test_petition_verifier.py` | Test API endpoint with sample requests |
| `deploy_petition_verifier.sh` | Redeploy with correct layer structure |
| `PETITION_VERIFIER_FIXES.md` | Detailed list of changes |
| `TROUBLESHOOTING_GUIDE.md` | Step-by-step troubleshooting |
| `FIXES_SUMMARY.md` | Summary of all fixes |
| `DIAGNOSTIC_TOOLS_README.md` | How to use diagnostic tools |
| `QUICK_FIX_CHECKLIST.md` | This file |

### Permissions Already Configured

| Service | Permissions |
|---------|-------------|
| Bedrock | `InvokeModel`, `InvokeModelWithResponseStream` |
| Textract | `AnalyzeDocument`, `DetectDocumentText` |
| S3 | Full read/write to both buckets |
| DynamoDB | Full read/write to all tables |

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/petition/generate` | POST | Verify petition from text |
| `/petition/clarify` | POST | Verify petition from PDF |

### Request Format

**Text Verification** (`/petition/generate`):
```json
{
  "petitionText": "Your petition text here...",
  "userId": "optional-user-id"
}
```

**PDF Verification** (`/petition/clarify`):
```json
{
  "s3Key": "path/to/petition.pdf",
  "userId": "optional-user-id"
}
```

### Response Format

**Success** (200):
```json
{
  "success": true,
  "message": "Verification completed",
  "data": {
    "verificationId": "uuid",
    "status": "completed",
    "results": {
      "status": "compliant|minor_defects|major_defects",
      "complianceScore": 0-100,
      "totalIssues": 0,
      "outdatedCitations": [...],
      "missingSections": [...],
      "proceduralDefects": [...],
      "summary": "..."
    }
  },
  "timestamp": "2024-01-20T10:30:00.000Z"
}
```

**Error** (400/500):
```json
{
  "success": false,
  "message": "Error message",
  "error": "Detailed error description",
  "timestamp": "2024-01-20T10:30:00.000Z"
}
```

## 🎯 Most Likely Issue

Based on the symptoms (500 error with no specific details), the most likely issue is:

**"No module named 'pydantic'"**

This happens when the Lambda layer doesn't have pydantic installed in the correct directory structure.

**Quick Fix**:
```bash
./deploy_petition_verifier.sh
```

This will:
1. Create `python/` subdirectory in the shared layer
2. Install pydantic and boto3 in the correct location
3. Synthesize and deploy the CDK stack
4. Update the Lambda function with the fixed layer

## 📞 Need Help?

If the issue persists after following this checklist:

1. Run all three diagnostic scripts
2. Share the output of each script
3. Share the exact error message from CloudWatch logs
4. Share the request payload you're sending
5. Share the full response body you're receiving

This will help identify the exact issue and provide the right solution.

## ✨ Success Criteria

You'll know it's working when:

- ✅ `python3 test_petition_verifier.py` returns Status Code 200
- ✅ Response has `"success": true`
- ✅ Verification results show outdated citations detected
- ✅ Compliance score is calculated (0-100)
- ✅ No errors in CloudWatch logs
