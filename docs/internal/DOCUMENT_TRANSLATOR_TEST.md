# Document Translator Lambda Test Results

## Test Setup

**Test File Created:** `test_legal_notice.txt`
**S3 Upload:** Successfully uploaded to `s3://nyayadwarpalstack-nyayadocbucketv24eb39526-yskr4fmijdf4/documents/test_legal_notice.txt`
**File Size:** 1234 bytes

## API Request

```bash
POST https://ked0qedvxi.execute-api.ap-south-2.amazonaws.com/prod/translate/document
```

**Payload:**
```json
{
  "userId": "test-user-001",
  "s3Key": "documents/test_legal_notice.txt",
  "sourceLanguage": "en",
  "targetLanguage": "hi",
  "documentType": "Legal Notice"
}
```

## API Response

```json
{
  "success": false,
  "message": "Internal server error",
  "data": null,
  "error": "An error occurred (InvalidS3ObjectException) when calling the AnalyzeDocument operation: Unable to get object metadata from S3. Check object key, region and/or access permissions.",
  "timestamp": "2026-03-02T15:39:53.243577"
}
```

## CloudWatch Logs

```
INIT_START Runtime Version: python:3.11.mainlinev2.v3
[INFO] 2026-03-02T15:39:52.916Z Found credentials in environment variables.
START RequestId: da585257-a66f-490e-9b56-75f5bdc867de Version: $LATEST

Extracting text from document: documents/test_legal_notice.txt

[ERROR] 2026-03-02T15:39:53.241Z Non-retryable error: An error occurred (InvalidS3ObjectException) when calling the AnalyzeDocument operation: Unable to get object metadata from S3. Check object key, region and/or access permissions.

Error in document translation: An error occurred (InvalidS3ObjectException) when calling the AnalyzeDocument operation: Unable to get object metadata from S3. Check object key, region and/or access permissions.

Traceback (most recent call last):
  File "/var/task/handler.py", line 69, in lambda_handler
    textract_response = textract_helper.analyze_document(
  File "/opt/python/aws_helpers.py", line 406, in analyze_document
    return exponential_backoff_retry(_analyze)
  File "/opt/python/aws_helpers.py", line 52, in exponential_backoff_retry
    return func()
  File "/opt/python/aws_helpers.py", line 396, in _analyze
    response = self.client.analyze_document(
  File "/opt/python/botocore/client.py", line 602, in _api_call
    return self._make_api_call(operation_name, kwargs)
  File "/opt/python/botocore/client.py", line 1078, in _make_api_call
    raise error_class(parsed_response, operation_name)
  botocore.errorfactory.InvalidS3ObjectException: An error occurred (InvalidS3ObjectException) when calling the AnalyzeDocument operation: Unable to get object metadata from S3. Check object key, region and/or access permissions.

END RequestId: da585257-a66f-490e-9b56-75f5bdc867de
REPORT RequestId: da585257-a66f-490e-9b56-75f5bdc867de
  Duration: 113.72 ms
  Billed Duration: 1341 ms
  Memory Size: 1024 MB
  Max Memory Used: 107 MB
  Init Duration: 1226.49 ms
```

## Root Cause Analysis

### Issue: AWS Textract Region Mismatch

**Problem:**
- S3 bucket is in `ap-south-2` (Hyderabad)
- TextractHelper is configured for `ap-south-1` (Mumbai) by default
- **AWS Textract is NOT available in ap-south-2 region**

**Evidence:**
```bash
$ aws textract list-adapters --region ap-south-2
Could not connect to the endpoint URL: "https://textract.ap-south-2.amazonaws.com/"
```

### Code Location

**File:** `lambda_functions/shared/aws_helpers.py`
```python
class TextractHelper:
    def __init__(self, region: str = "ap-south-1"):  # Defaults to ap-south-1
        self.client = boto3.client("textract", region_name=region)
```

**File:** `lambda_functions/document_translator/handler.py`
```python
textract_helper = TextractHelper()  # Uses default ap-south-1
```

## Solutions

### Option 1: Cross-Region Textract (Recommended for Production)
Update the document translator to:
1. Copy S3 object to ap-south-1 temporarily
2. Process with Textract in ap-south-1
3. Delete temporary copy
4. Return results

### Option 2: Smart Text Extraction
Update the handler to detect file type:
- `.txt` files: Read directly from S3 (no Textract needed)
- `.pdf`, `.jpg`, `.png`: Use Textract in ap-south-1 with cross-region access

### Option 3: Move Infrastructure to ap-south-1
Redeploy entire stack to ap-south-1 where Textract is available.

## Recommended Fix

Add file type detection to the document translator:

```python
import os

def extract_text_from_document(s3_key: str, bucket: str) -> str:
    """Extract text based on file type"""
    file_extension = os.path.splitext(s3_key)[1].lower()
    
    if file_extension == '.txt':
        # Read directly from S3
        s3_client = boto3.client('s3', region_name='ap-south-2')
        response = s3_client.get_object(Bucket=bucket, Key=s3_key)
        return response['Body'].read().decode('utf-8')
    else:
        # Use Textract for PDFs and images
        # Copy to ap-south-1 bucket temporarily
        textract_helper = TextractHelper(region='ap-south-1')
        # ... process with Textract
```

## AWS Textract Regional Availability

**Available in India:**
- ✅ ap-south-1 (Mumbai)
- ❌ ap-south-2 (Hyderabad) - NOT AVAILABLE

**Reference:** https://docs.aws.amazon.com/general/latest/gr/textract.html

## Test File Content

```
LEGAL NOTICE UNDER SECTION 138 OF THE NEGOTIABLE INSTRUMENTS ACT, 1881

To,
Mr. Rajesh Kumar
123 MG Road
Bangalore - 560001

Dear Sir,

SUBJECT: Legal Notice for Dishonour of Cheque

This is to inform you that a cheque bearing number 456789 dated 15th January 2026...
[Full content in test_legal_notice.txt]
```

## Next Steps

1. Implement Option 2 (Smart Text Extraction) for immediate fix
2. Add cross-region Textract support for PDF/image files
3. Update CDK stack to grant Lambda permissions for cross-region S3 access
4. Test with both .txt and .pdf files

---

**Date:** March 2, 2026
**Status:** Issue identified - Textract not available in ap-south-2
**Action Required:** Implement smart text extraction or cross-region Textract
