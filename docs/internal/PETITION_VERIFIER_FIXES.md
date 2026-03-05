# Petition Verifier Lambda - 500 Error Fixes

## Changes Made

### 1. Enhanced Error Handling

Added comprehensive try/except blocks with detailed logging throughout the Lambda handler:

- **Main handler**: Catches JSON parsing errors, empty body, and invalid paths
- **Text verification**: Validates petition text, handles verification failures gracefully
- **Bedrock calls**: Wrapped in try/except with traceback logging
- **Textract calls**: Added ClientError handling with error code extraction
- **Storage operations**: Non-critical failures don't break the request

### 2. Improved Logging

Added detailed print statements at key points:
- Incoming event logging
- Request validation steps
- Bedrock API calls and responses
- Textract extraction progress
- Error tracebacks for debugging

### 3. Dependency Analysis

**Current Dependencies:**
- `boto3` - Built into Lambda runtime ✓
- `pydantic` - Needs to be in Lambda layer

**Potential Issues:**
- Lambda layer structure may be incorrect (needs `python/` subdirectory)
- Pydantic may not be properly packaged in the layer

## Testing Steps

### 1. Check CloudWatch Logs

Run the log checker to see the actual error:

```bash
python3 check_lambda_logs.py
```

This will show you the exact error message from the Lambda execution.

### 2. Test the API

Run the test script to invoke the Lambda:

```bash
python3 test_petition_verifier.py
```

This will:
- Test with a minimal payload
- Test with a full petition containing outdated citations
- Show detailed response including error messages

### 3. Redeploy with Fixed Layer

If the issue is with the Lambda layer (pydantic not found), redeploy:

```bash
./deploy_petition_verifier.sh
```

This will:
- Install dependencies in the correct `python/` subdirectory
- Synthesize the CDK stack
- Deploy to AWS

## Common Issues and Solutions

### Issue 1: "No module named 'pydantic'"

**Cause**: Lambda layer doesn't have pydantic installed correctly

**Solution**: 
```bash
cd lambda_functions/shared
mkdir -p python
pip install -r requirements.txt -t python/ --upgrade
cd ../..
npx cdk deploy
```

### Issue 2: "Unable to import module 'handler'"

**Cause**: Import path issues or missing dependencies

**Solution**: Check that:
- `sys.path.insert(0, '/opt/python')` is in handler.py
- All imports are available in the layer
- Layer is attached to the Lambda function

### Issue 3: Bedrock Access Denied

**Cause**: Lambda role doesn't have Bedrock permissions

**Solution**: Already fixed in CDK stack - Lambda role has:
```python
bedrock:InvokeModel
bedrock:InvokeModelWithResponseStream
```

### Issue 4: Textract Access Denied

**Cause**: Lambda role doesn't have Textract permissions

**Solution**: Already fixed in CDK stack - Lambda role has:
```python
textract:AnalyzeDocument
textract:DetectDocumentText
```

## Next Steps

1. Run `python3 check_lambda_logs.py` to see the actual error
2. Based on the error, either:
   - Redeploy with `./deploy_petition_verifier.sh` if it's a dependency issue
   - Check IAM permissions if it's an access denied error
   - Review the error message for other issues

## API Endpoints

- **POST /petition/generate**: Verify petition from text
  - Request: `{ "petitionText": "..." }`
  - Response: Verification results with outdated citations, missing sections, compliance score

- **POST /petition/clarify**: Verify petition from PDF
  - Request: `{ "s3Key": "path/to/petition.pdf" }`
  - Response: Verification results + extracted text

## Error Response Format

All errors now return detailed information:

```json
{
  "success": false,
  "message": "Failed to verify petition",
  "error": "Detailed error message with context",
  "timestamp": "2024-01-20T10:30:00.000Z"
}
```
