# Petition Verifier Lambda - 500 Error Fixes Summary

## What Was Done

### 1. Enhanced Error Handling ✓

**File**: `lambda_functions/petition_architect/handler.py`

Added comprehensive error handling with detailed error messages:

- **JSON parsing errors**: Now caught and return 400 with clear message
- **Empty request body**: Validated and returns 400 with clear message
- **Missing required fields**: Validated with helpful error messages
- **Bedrock API failures**: Wrapped in try/except, returns empty array instead of crashing
- **Textract failures**: Detailed ClientError handling with error codes
- **Storage failures**: Non-critical, won't break the request
- **All exceptions**: Include full stack traces in CloudWatch logs

### 2. Improved Logging ✓

Added detailed logging at every step:
- Incoming event structure
- Request body parsing
- Validation results
- Bedrock API calls and responses
- Textract extraction progress
- Verification logic execution
- Storage operations
- Full stack traces for all errors

### 3. Created Diagnostic Tools ✓

**check_lambda_config.py**:
- Shows Lambda configuration (runtime, memory, timeout, handler)
- Lists environment variables (with sensitive values masked)
- Shows attached Lambda layers
- Displays IAM role permissions (managed and inline policies)
- Shows recent invocation metrics and error counts

**check_lambda_logs.py**:
- Fetches recent CloudWatch logs (last 30 minutes)
- Shows all log streams
- Displays timestamps and messages
- Helps identify exact failure points

**test_petition_verifier.py**:
- Tests with minimal payload (quick validation)
- Tests with full petition containing outdated IPC/CrPC citations
- Shows detailed response including error messages
- Validates verification results structure

**deploy_petition_verifier.sh**:
- Installs dependencies in correct `python/` subdirectory
- Synthesizes CDK stack
- Deploys to AWS
- Shows next steps for testing

### 4. Documentation ✓

**PETITION_VERIFIER_FIXES.md**:
- Lists all changes made
- Explains dependency analysis
- Provides testing steps
- Documents common issues and solutions

**TROUBLESHOOTING_GUIDE.md**:
- Step-by-step troubleshooting process
- Common issues with detailed solutions
- Expected successful response format
- Quick diagnosis commands

## Permissions Already Configured ✓

The Lambda execution role already has all necessary permissions:

### Bedrock Permissions
```python
bedrock:InvokeModel
bedrock:InvokeModelWithResponseStream
```

### Textract Permissions
```python
textract:AnalyzeDocument
textract:DetectDocumentText
```

### S3 Permissions
- Full read/write access to `NyayaDocBucketV2`
- Full read/write access to `NyayaArchiveBucketV2`

### DynamoDB Permissions
- Full read/write access to `DocumentMetadataTable`
- Full read/write access to `SessionTable`
- Full read/write access to `GlossaryTable`

**Note**: No SSM permissions needed - the verifier doesn't use Sarvam API.

## Dependencies Analysis

### Built-in (No Action Needed)
- `boto3` - Included in Lambda Python runtime
- `json`, `os`, `uuid`, `re`, `datetime`, `typing`, `sys` - Python standard library

### Requires Lambda Layer
- `pydantic>=2.5.0` - Used for data models and validation

**Potential Issue**: If the Lambda layer doesn't have pydantic installed in the correct directory structure (`python/` subdirectory), you'll get a `ModuleNotFoundError`.

**Solution**: Run `./deploy_petition_verifier.sh` to fix the layer structure and redeploy.

## Next Steps

### 1. Diagnose the Current Error

Run the diagnostic scripts to identify the root cause:

```bash
# Check Lambda configuration and permissions
python3 check_lambda_config.py

# Check CloudWatch logs for error messages
python3 check_lambda_logs.py

# Test the API endpoint
python3 test_petition_verifier.py
```

### 2. Based on the Error

**If you see "No module named 'pydantic'"**:
```bash
./deploy_petition_verifier.sh
```

**If you see "AccessDeniedException"**:
- Check which service is denied (Bedrock, Textract, S3, DynamoDB)
- Verify permissions with `python3 check_lambda_config.py`
- Permissions should already be correct, but may need to wait for IAM propagation

**If you see other errors**:
- Check the full stack trace in CloudWatch logs
- The enhanced error handling should now show the exact issue
- Refer to TROUBLESHOOTING_GUIDE.md for solutions

### 3. After Fixing

Test again to verify:
```bash
python3 test_petition_verifier.py
```

Expected response:
- Status Code: 200
- Success: true
- Results with outdated citations detected
- Compliance score calculated
- Missing sections identified

## Files Modified

1. `lambda_functions/petition_architect/handler.py` - Enhanced error handling and logging
2. Created diagnostic tools:
   - `check_lambda_config.py`
   - `check_lambda_logs.py`
   - `test_petition_verifier.py`
   - `deploy_petition_verifier.sh`
3. Created documentation:
   - `PETITION_VERIFIER_FIXES.md`
   - `TROUBLESHOOTING_GUIDE.md`
   - `FIXES_SUMMARY.md` (this file)

## No Changes Needed

- `infrastructure/nyaya_dwarpal_stack.py` - Permissions already correct
- Lambda layer requirements - Already specified correctly
- API Gateway configuration - Already correct

## What to Share

When running the diagnostic scripts, share:

1. Output of `python3 check_lambda_config.py`
2. Output of `python3 check_lambda_logs.py`
3. Output of `python3 test_petition_verifier.py`

This will help identify the exact issue and provide the right solution.
