# Petition Architect Feature - Deployment Guide

## Overview

Feature 2 (Petition Architect) has been implemented and is ready for deployment. This feature generates structured legal petitions from user narratives with conversational clarification.

## What Was Implemented

### 1. Lambda Function
- **Location**: `lambda_functions/petition_architect/handler.py`
- **Features**:
  - Petition generation using AWS Bedrock (Claude 3.5 Sonnet)
  - Conversational clarification (max 5 questions)
  - Session management with DynamoDB
  - Petition storage in S3
  - Two endpoints: `/petition/generate` and `/petition/clarify`

### 2. Infrastructure Updates
- **File**: `infrastructure/nyaya_dwarpal_stack.py`
- **Changes**:
  - Added `PetitionArchitectLambda` function
  - Added API Gateway endpoints:
    - `POST /petition/generate`
    - `POST /petition/clarify`
  - Added CloudFormation outputs for new endpoints

### 3. Shared Utilities
- **File**: `lambda_functions/shared/aws_helpers.py`
- **Changes**:
  - Added `put_object()` method to S3Helper for JSON storage

## Deployment Steps

### 1. Verify Prerequisites

Ensure you have:
- AWS CDK installed and configured
- AWS credentials with appropriate permissions
- Python 3.11 runtime available
- Existing infrastructure from Phase 1 deployed

### 2. Deploy Updated Infrastructure

```bash
# Navigate to project root
cd /path/to/nyaya-dwarpal

# Install dependencies (if not already done)
pip install -r requirements.txt

# Synthesize CloudFormation template
npx cdk synth

# Deploy to AWS
npx cdk deploy

# Confirm deployment when prompted
```

### 3. Verify Deployment

After deployment completes, you should see outputs including:

```
Outputs:
NyayaDwarpalStack.PetitionGenerateEndpoint = https://[API_ID].execute-api.ap-south-1.amazonaws.com/prod/petition/generate
NyayaDwarpalStack.PetitionClarifyEndpoint = https://[API_ID].execute-api.ap-south-1.amazonaws.com/prod/petition/clarify
```

### 4. Test the Endpoints

#### Test Petition Generation

```bash
# Save this as test_petition_generate.json
cat > test_petition_generate.json << 'EOF'
{
  "userId": "test-user-123",
  "sessionId": "test-session-456",
  "language": "en",
  "triageData": {
    "extractedFacts": {
      "who": ["ABC Corporation", "XYZ Limited"],
      "what": "Breach of contract for non-payment of services rendered",
      "when": "2024-01-15",
      "where": "Mumbai, Maharashtra",
      "why": "Defendant failed to pay for consulting services as per agreement"
    },
    "classification": {
      "category": "Civil",
      "subCategory": "Contract Dispute",
      "confidence": 0.95,
      "relevantSections": [
        {
          "act": "CPC",
          "section": "Order 37",
          "description": "Summary suit for recovery of money"
        }
      ],
      "severity": "medium"
    }
  },
  "additionalContext": {
    "claim_amount": 500000,
    "relief_sought": "Recovery of outstanding payment with interest and costs"
  }
}
EOF

# Test the endpoint
curl -X POST https://[YOUR_API_ENDPOINT]/prod/petition/generate \
  -H "Content-Type: application/json" \
  -d @test_petition_generate.json
```

#### Test Clarification Flow

If the response indicates clarification is needed:

```bash
curl -X POST https://[YOUR_API_ENDPOINT]/prod/petition/clarify \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "test-session-456",
    "answers": {
      "incident_date": "2024-01-15",
      "parties": "ABC Corporation (Plaintiff) vs XYZ Limited (Defendant)"
    }
  }'
```

## Expected Behavior

### Scenario 1: Complete Information
If all required information is provided in the initial request, the function will:
1. Generate a complete petition immediately
2. Store it in S3
3. Return the petition with `status: "ready"`

### Scenario 2: Missing Information
If critical information is missing, the function will:
1. Identify missing fields (date, parties, location, amount, relief)
2. Generate up to 5 clarifying questions
3. Return questions with `status: "pending_clarification"`
4. Wait for user to call `/petition/clarify` with answers
5. Repeat up to 5 times or until all information is gathered

### Scenario 3: Maximum Clarifications Reached
After 5 clarification rounds:
1. Generate petition with available information
2. Mark any gaps in the petition
3. Return with `status: "ready"` but may have incomplete sections

## Integration with Existing Features

The Petition Architect integrates with:

1. **Voice Triage Lambda**: Receives triage data as input
2. **DynamoDB Sessions Table**: Stores conversation state
3. **S3 Document Bucket**: Stores generated petitions
4. **Bedrock (Claude 3.5)**: Generates petition content and clarification questions

## Monitoring

Monitor the function using:

```bash
# View Lambda logs
aws logs tail /aws/lambda/NyayaDwarpal-PetitionArchitect --follow

# Check CloudWatch metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=NyayaDwarpal-PetitionArchitect \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z \
  --period 3600 \
  --statistics Sum
```

## Troubleshooting

### Issue: "Session not found" error
**Solution**: Ensure the sessionId matches between `/generate` and `/clarify` calls

### Issue: Bedrock throttling errors
**Solution**: The function includes automatic retry with exponential backoff. If persistent, check Bedrock quotas.

### Issue: S3 access denied
**Solution**: Verify the Lambda execution role has permissions to write to the document bucket

### Issue: DynamoDB errors
**Solution**: Check that the Sessions table exists and the Lambda role has read/write permissions

## Cost Considerations

Estimated costs per petition generation:
- Lambda execution: ~$0.0001 (60s at 1024MB)
- Bedrock API call: ~$0.015 (Claude 3.5 Sonnet)
- DynamoDB writes: ~$0.000001
- S3 storage: ~$0.000001

**Total per petition**: ~$0.015

## Next Steps

After successful deployment:

1. **Test with real data**: Use actual triage output from Voice Triage Lambda
2. **Monitor performance**: Check CloudWatch logs and metrics
3. **Implement remaining features**:
   - Feature 3: Document Translation
   - Feature 4: Citation Reviewer
   - Feature 5: Filing Validator
4. **Set up CI/CD**: Automate deployment pipeline
5. **Configure production security**: Add API authentication, WAF rules, etc.

## Rollback

If you need to rollback:

```bash
# Revert infrastructure changes
git checkout HEAD~1 infrastructure/nyaya_dwarpal_stack.py

# Redeploy
npx cdk deploy
```

## Support

For issues or questions:
1. Check CloudWatch logs for detailed error messages
2. Review the README in `lambda_functions/petition_architect/`
3. Verify all environment variables are set correctly
4. Ensure Bedrock access is enabled in your AWS account (us-east-1 region)

---

**Status**: ✅ Ready for Deployment
**Last Updated**: 2024
**Version**: 1.0.0
