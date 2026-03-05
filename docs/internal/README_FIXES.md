# Petition Verifier Lambda - 500 Error Fix

## 🚀 Quick Start (One Command)

Run this single command to diagnose and fix the issue:

```bash
./diagnose_and_fix.sh
```

This will:
1. Check Lambda configuration and permissions
2. Analyze CloudWatch logs for errors
3. Test the API endpoint
4. Suggest the appropriate fix
5. Optionally apply the fix automatically

## 📋 What Was Fixed

### 1. Enhanced Error Handling
- Added comprehensive try/except blocks throughout the Lambda handler
- All errors now return detailed error messages in the API response
- Full stack traces logged to CloudWatch for debugging

### 2. Improved Logging
- Detailed logging at every step (request parsing, validation, API calls)
- Error messages include context and suggestions
- Stack traces for all exceptions

### 3. Request Validation
- JSON parsing errors caught and return 400 with clear message
- Empty request body validation
- Required field validation with helpful error messages
- Empty petition text validation

### 4. Graceful Degradation
- Bedrock API failures return empty array instead of crashing
- Storage failures are non-critical (won't break the request)
- Textract errors include detailed error codes

## 🔧 Diagnostic Tools

### All-in-One Tool
```bash
./diagnose_and_fix.sh
```
Runs all diagnostics and suggests fixes automatically.

### Individual Tools

**Check Lambda Configuration**:
```bash
python3 check_lambda_config.py
```
Shows configuration, environment variables, layers, and IAM permissions.

**Check CloudWatch Logs**:
```bash
python3 check_lambda_logs.py
```
Fetches recent logs to see error messages and stack traces.

**Test API Endpoint**:
```bash
python3 test_petition_verifier.py
```
Sends test requests and shows detailed responses.

**Redeploy with Fix**:
```bash
./deploy_petition_verifier.sh
```
Fixes Lambda layer structure and redeploys.

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| `QUICK_FIX_CHECKLIST.md` | Step-by-step checklist to fix the issue |
| `TROUBLESHOOTING_GUIDE.md` | Detailed troubleshooting for all common issues |
| `DIAGNOSTIC_TOOLS_README.md` | How to use each diagnostic tool |
| `PETITION_VERIFIER_FIXES.md` | Technical details of all changes |
| `FIXES_SUMMARY.md` | Summary of fixes and permissions |

## 🎯 Most Likely Issue

Based on the 500 error, the most likely issue is:

**Missing pydantic module in Lambda layer**

**Quick Fix**:
```bash
./deploy_petition_verifier.sh
```

This installs pydantic in the correct directory structure (`python/` subdirectory) and redeploys.

## ✅ Permissions Already Configured

The Lambda execution role already has all necessary permissions:

- ✅ Bedrock: `InvokeModel`, `InvokeModelWithResponseStream`
- ✅ Textract: `AnalyzeDocument`, `DetectDocumentText`
- ✅ S3: Full read/write to both buckets
- ✅ DynamoDB: Full read/write to all tables

**Note**: No SSM permissions needed - the verifier doesn't use Sarvam API.

## 📝 API Endpoints

### POST /petition/generate
Verify petition from text input.

**Request**:
```json
{
  "petitionText": "Your petition text here...",
  "userId": "optional-user-id"
}
```

**Response** (200):
```json
{
  "success": true,
  "message": "Verification completed",
  "data": {
    "verificationId": "uuid",
    "status": "completed",
    "results": {
      "status": "compliant|minor_defects|major_defects",
      "complianceScore": 85,
      "totalIssues": 2,
      "outdatedCitations": [
        {
          "type": "outdated_ipc",
          "original": "IPC Section 302",
          "suggested": "BNS Section 103",
          "severity": "high",
          "description": "IPC Section 302 has been replaced..."
        }
      ],
      "missingSections": [],
      "proceduralDefects": [],
      "summary": "Petition has 2 defect(s) requiring attention..."
    }
  },
  "timestamp": "2024-01-20T10:30:00.000Z"
}
```

### POST /petition/clarify
Verify petition from PDF document.

**Request**:
```json
{
  "s3Key": "path/to/petition.pdf",
  "userId": "optional-user-id"
}
```

**Response**: Same as `/petition/generate` plus `extractedText` field.

## 🔍 Verification Features

The verifier checks for:

### 1. Outdated Citations
- **IPC → BNS**: Maps old IPC sections to new BNS sections (2023)
- **CrPC → BNSS**: Maps old CrPC sections to new BNSS sections (2023)
- Provides suggested replacements with explanations

### 2. Missing Sections
- **Prayer**: Relief sought from the court
- **Grounds**: Legal basis for the claim
- **Facts**: Chronological narrative
- **Verification**: Required verification statement

### 3. Procedural Compliance
- Uses Bedrock AI to check for procedural defects
- Identifies missing mandatory clauses
- Checks formatting and structure
- Validates party details and dates

### 4. Compliance Score
- Calculated based on total issues found
- Range: 0-100 (higher is better)
- Status: compliant, minor_defects, major_defects

## 🧪 Testing

After fixing, test with:

```bash
python3 test_petition_verifier.py
```

**Expected Result**:
- Status Code: 200
- Success: true
- Verification results with outdated citations detected
- Compliance score calculated

## 🐛 Common Issues

### Issue 1: "No module named 'pydantic'"
**Fix**: `./deploy_petition_verifier.sh`

### Issue 2: "AccessDeniedException"
**Fix**: Permissions should already be correct. Wait for IAM propagation.

### Issue 3: Other errors
**Fix**: Check CloudWatch logs with `python3 check_lambda_logs.py`

See `TROUBLESHOOTING_GUIDE.md` for detailed solutions.

## 📞 Need Help?

If the issue persists:

1. Run `./diagnose_and_fix.sh`
2. Share the output
3. Share the error message from CloudWatch logs
4. Refer to `TROUBLESHOOTING_GUIDE.md`

## 🎉 Success Criteria

You'll know it's working when:

- ✅ API returns Status Code 200
- ✅ Response has `"success": true`
- ✅ Verification results show outdated citations
- ✅ Compliance score is calculated
- ✅ No errors in CloudWatch logs

## 📦 Files Modified

- `lambda_functions/petition_architect/handler.py` - Enhanced error handling

## 📦 Files Created

- `diagnose_and_fix.sh` - All-in-one diagnostic tool
- `check_lambda_config.py` - Configuration checker
- `check_lambda_logs.py` - Log viewer
- `test_petition_verifier.py` - API tester
- `deploy_petition_verifier.sh` - Deployment script
- Documentation files (see above)

## 🚀 Next Steps

1. Run `./diagnose_and_fix.sh`
2. Follow the suggested fix
3. Test with `python3 test_petition_verifier.py`
4. Verify success ✓
