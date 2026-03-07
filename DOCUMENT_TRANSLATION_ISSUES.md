# Document Translation Feature - Issues Found

## Critical Issues Identified

### Issue 1: UI - Fake S3 Upload (CRITICAL)
**Location:** `ui/enhanced-index.html` lines 1162-1210

**Problem:**
```javascript
// This function SIMULATES upload but doesn't actually upload the file
async function uploadFileToS3(file) {
    // ... generates S3 key ...
    console.log(`Uploading ${file.name} to S3 key: ${s3Key}`);
    
    // Simulate upload progress
    // ... fake progress bar ...
    
    // Wait for simulated upload
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    return s3Key;  // Returns key but file was NEVER uploaded!
}
```

**Impact:** 
- Lambda receives S3 key but file doesn't exist in S3
- Lambda fails when trying to read the file
- Translation never works

**Fix Required:**
- Option 1: Upload file as base64 in request body directly to Lambda
- Option 2: Get pre-signed URL from backend and upload to S3
- Option 3: Use API Gateway binary support with multipart/form-data

### Issue 2: Lambda - Wrong Sarvam AI Endpoint
**Location:** `lambda_functions/document_translator/handler.py` line 329

**Problem:**
```python
response = requests.post(
    'https://api.sarvam.ai/translate',  # Hardcoded endpoint
    headers=headers,
    json=payload,
    timeout=30
)
```

**Environment Variable:**
```python
SARVAM_AI_ENDPOINT = os.environ.get('SARVAM_AI_ENDPOINT', 'https://api.sarvam.ai/v1')
```

**Impact:**
- Endpoint doesn't include `/v1` path
- API calls may fail with 404

**Fix Required:**
- Use `f'{SARVAM_AI_ENDPOINT}/translate'` instead of hardcoded URL

### Issue 3: Lambda - Model Name Verification Needed
**Location:** `lambda_functions/document_translator/handler.py` line 336

**Current:**
```python
payload = {
    'input': chunk,
    'source_language_code': source_lang_code,
    'target_language_code': target_lang_code,
    'model': 'mayura:v1',  # Is this correct?
    'mode': 'formal'
}
```

**Question:** Is `mayura:v1` the correct model name for Sarvam AI?
- Need to verify against Sarvam AI documentation
- Might need to be `mayura-v1` or just `mayura`

## Recommended Fix Strategy

### Approach: Direct File Upload in Request Body

**Why:** Simplest solution that doesn't require S3 pre-signed URLs or complex CORS setup

**Changes Required:**

1. **UI Changes:**
   - Read file as base64
   - Send file content directly in POST body
   - Remove fake S3 upload function

2. **Lambda Changes:**
   - Accept file content in request body (base64)
   - Decode and process file directly
   - Skip S3 read step for inline files
   - Fix Sarvam AI endpoint URL

## Next Steps

1. Fix UI to send file as base64 in request body
2. Fix Lambda to accept file content directly
3. Fix Sarvam AI endpoint URL
4. Test with actual file upload
5. Deploy both UI and Lambda
