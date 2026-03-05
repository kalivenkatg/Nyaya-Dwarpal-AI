# Diagnostic Tools for Petition Verifier Lambda

## Quick Start

Run these commands in order to diagnose and fix the 500 error:

```bash
# 1. Check Lambda configuration
python3 check_lambda_config.py

# 2. Check recent logs
python3 check_lambda_logs.py

# 3. Test the API
python3 test_petition_verifier.py
```

## Tool Descriptions

### 1. check_lambda_config.py

**Purpose**: Verify Lambda function configuration and IAM permissions

**What it shows**:
- Function name, runtime, handler, memory, timeout
- Environment variables (with sensitive values masked)
- Attached Lambda layers
- IAM role name and permissions
- Recent invocation metrics and error counts

**When to use**: 
- First step in troubleshooting
- Verify permissions are correct
- Check if layer is attached
- See if function has been invoked recently

**Example output**:
```
=== Lambda Function Configuration ===

Function Name: NyayaDwarpal-PetitionArchitect
Runtime: python3.11
Handler: handler.lambda_handler
Memory: 1024 MB
Timeout: 60 seconds
Role: arn:aws:iam::307907075420:role/...

=== Environment Variables ===
  DOCUMENT_BUCKET: nyayadwarpalstack-nyayadocbucketv2...
  SESSION_TABLE: nyayadwarpalstack-sessiontable...
  BEDROCK_REGION: us-east-1

=== Layers ===
  - arn:aws:lambda:ap-south-1:307907075420:layer:NyayaDwarpal-Shared:1

=== IAM Role Permissions ===
...
```

### 2. check_lambda_logs.py

**Purpose**: Fetch recent CloudWatch logs to see error messages

**What it shows**:
- Last 30 minutes of logs from all log streams
- Timestamps for each log entry
- Error messages and stack traces
- Lambda execution details

**When to use**:
- After seeing a 500 error
- To identify the exact failure point
- To see full stack traces
- To understand what the Lambda is doing

**Example output**:
```
=== Recent logs for NyayaDwarpal-PetitionArchitect (last 30 minutes) ===

--- Log Stream: 2024/01/20/[$LATEST]abc123 ---
[2024-01-20 10:30:00] START RequestId: abc-123
[2024-01-20 10:30:00] Received event: {"path": "/petition/generate", ...}
[2024-01-20 10:30:01] Error in lambda_handler: No module named 'pydantic'
[2024-01-20 10:30:01] Traceback (most recent call last):
...
[2024-01-20 10:30:01] END RequestId: abc-123
```

### 3. test_petition_verifier.py

**Purpose**: Test the API endpoint with sample requests

**What it does**:
- Sends a minimal test request
- Sends a full petition with outdated citations
- Shows detailed response including error messages
- Validates response structure

**When to use**:
- After making changes to verify they work
- To reproduce the 500 error
- To see the exact error message returned by the API
- To validate verification results

**Example output**:
```
Testing minimal petition verification...
URL: https://ked0qedvxi.../petition/generate
Payload: {
  "petitionText": "This is a test petition..."
}

Status Code: 200
Response Body:
{
  "success": true,
  "message": "Verification completed",
  "data": {
    "verificationId": "uuid-here",
    "status": "completed",
    "results": {
      "status": "major_defects",
      "complianceScore": 90,
      "totalIssues": 1,
      "outdatedCitations": [...]
    }
  }
}
```

### 4. deploy_petition_verifier.sh

**Purpose**: Redeploy Lambda with correct dependency structure

**What it does**:
- Creates `python/` subdirectory in shared layer
- Installs pydantic and other dependencies
- Synthesizes CDK stack
- Deploys to AWS

**When to use**:
- When you see "No module named 'pydantic'" error
- After making code changes
- To fix Lambda layer structure

**Usage**:
```bash
./deploy_petition_verifier.sh
```

## Troubleshooting Workflow

### Step 1: Check Configuration

```bash
python3 check_lambda_config.py
```

**Look for**:
- ✓ Runtime is `python3.11`
- ✓ Handler is `handler.lambda_handler`
- ✓ Layer is attached
- ✓ Environment variables are set
- ✓ IAM permissions include Bedrock, Textract, S3, DynamoDB

### Step 2: Check Logs

```bash
python3 check_lambda_logs.py
```

**Look for**:
- `ModuleNotFoundError: No module named 'pydantic'` → Run `./deploy_petition_verifier.sh`
- `AccessDeniedException` → Check IAM permissions (should already be correct)
- `KeyError` or `AttributeError` → Code logic issue, check stack trace
- Other errors → See TROUBLESHOOTING_GUIDE.md

### Step 3: Test API

```bash
python3 test_petition_verifier.py
```

**Look for**:
- Status Code 200 → Success! ✓
- Status Code 400 → Bad request, check payload format
- Status Code 500 → Check logs from Step 2

### Step 4: Fix and Redeploy

Based on the error:

**For "No module named 'pydantic'"**:
```bash
./deploy_petition_verifier.sh
```

**For code issues**:
1. Edit `lambda_functions/petition_architect/handler.py`
2. Run `npx cdk deploy`

**For permission issues**:
1. Edit `infrastructure/nyaya_dwarpal_stack.py`
2. Run `npx cdk deploy`

### Step 5: Verify Fix

```bash
python3 test_petition_verifier.py
```

Should see Status Code 200 with verification results.

## Common Error Patterns

### Pattern 1: Module Not Found

**Logs show**:
```
ModuleNotFoundError: No module named 'pydantic'
```

**Solution**:
```bash
./deploy_petition_verifier.sh
```

### Pattern 2: Access Denied

**Logs show**:
```
AccessDeniedException: User: arn:aws:sts::... is not authorized to perform: bedrock:InvokeModel
```

**Solution**: Check IAM permissions with `python3 check_lambda_config.py`. Should already be correct.

### Pattern 3: JSON Decode Error

**Logs show**:
```
JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

**Solution**: Check request body format. Must be valid JSON with `petitionText` field.

### Pattern 4: Empty Response

**API returns**: Empty body or malformed JSON

**Solution**: Check CloudWatch logs for the actual error. The enhanced error handling should now return proper error messages.

## Requirements

All scripts require:
- Python 3.x
- boto3 (for AWS scripts)
- requests (for test script)

Install with:
```bash
pip install boto3 requests
```

## AWS Credentials

Scripts use your default AWS credentials. Ensure you have:
- AWS CLI configured (`aws configure`)
- Or environment variables set (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
- Or IAM role attached (if running on EC2)

## Region

All scripts use `ap-south-2` (Hyderabad) region. If your Lambda is in a different region, edit the scripts:

```python
# Change this line in each script
region_name='ap-south-2'  # Change to your region
```
