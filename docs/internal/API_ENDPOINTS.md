# Nyaya-Dwarpal API Endpoints Documentation

**Base URL**: `https://ked0qedvxi.execute-api.ap-south-2.amazonaws.com/prod`  
**Region**: ap-south-2 (Hyderabad)  
**API Gateway ID**: ked0qedvxi

---

## 📋 Complete Endpoint List

### 1. Voice Triage (Feature 1)

**Endpoint**: `POST /voice/triage`  
**Full URL**: `https://ked0qedvxi.execute-api.ap-south-2.amazonaws.com/prod/voice/triage`  
**Lambda**: NyayaDwarpal-VoiceTriage  
**Purpose**: Process voice input, classify legal problem, detect urgency

**Request Body**:
```json
{
  "userId": "string",
  "transcribedText": "string",
  "language": "en|hi|ta|te|bn|..."
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Triage completed",
  "data": {
    "triageId": "uuid",
    "category": "civil|criminal|family|property|...",
    "severity": "low|medium|high|critical",
    "emotion": "calm|anxious|angry|distressed",
    "summary": "Brief description of the legal issue",
    "nextSteps": ["Step 1", "Step 2", "..."]
  }
}
```

---

### 2. Document Translation (Feature 2)

**Endpoint**: `POST /translate/document`  
**Full URL**: `https://ked0qedvxi.execute-api.ap-south-2.amazonaws.com/prod/translate/document`  
**Lambda**: NyayaDwarpal-DocumentTranslation  
**Purpose**: Extract text from vernacular documents, translate to English

**Request Body**:
```json
{
  "userId": "string",
  "s3Key": "string",
  "sourceLanguage": "hi|ta|te|bn|...",
  "targetLanguage": "en"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Translation completed",
  "data": {
    "translationId": "uuid",
    "originalText": "string",
    "translatedText": "string",
    "legalTerms": [
      {
        "term": "string",
        "translation": "string",
        "definition": "string"
      }
    ],
    "s3Location": "s3://bucket/key"
  }
}
```

---

### 3. Petition Verifier - Text Input (Feature 4)

**Endpoint**: `POST /petition/generate`  
**Full URL**: `https://ked0qedvxi.execute-api.ap-south-2.amazonaws.com/prod/petition/generate`  
**Lambda**: NyayaDwarpal-PetitionArchitect  
**Purpose**: Verify petition text for defects, outdated citations, compliance

**Request Body**:
```json
{
  "userId": "string",
  "petitionText": "string"
}
```

**Response** (200 OK):
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
      "totalIssues": 3,
      "outdatedCitations": [
        {
          "type": "outdated_ipc",
          "original": "IPC Section 302",
          "suggested": "BNS Section 103",
          "location": "Position 415-430",
          "severity": "high",
          "description": "IPC Section 302 has been replaced by BNS Section 103..."
        }
      ],
      "missingSections": [
        {
          "section": "Verification",
          "severity": "critical",
          "description": "Petition must include a verification statement..."
        }
      ],
      "proceduralDefects": [],
      "summary": "Petition has 3 defect(s) requiring attention..."
    }
  }
}
```

---

### 4. Petition Verifier - PDF Input (Feature 4)

**Endpoint**: `POST /petition/clarify`  
**Full URL**: `https://ked0qedvxi.execute-api.ap-south-2.amazonaws.com/prod/petition/clarify`  
**Lambda**: NyayaDwarpal-PetitionArchitect  
**Purpose**: Verify petition from PDF document using Textract

**Request Body**:
```json
{
  "userId": "string",
  "s3Key": "string",
  "documentId": "string (optional)"
}
```

**Response** (200 OK):
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
      "totalIssues": 3,
      "outdatedCitations": [...],
      "missingSections": [...],
      "proceduralDefects": [...],
      "summary": "..."
    },
    "extractedText": "First 500 characters of extracted text..."
  }
}
```

---

## 🔧 Additional Endpoints (Placeholders)

### 5. Review Endpoint (Not Implemented)

**Endpoint**: `POST /review`  
**Status**: ⚠️ Placeholder - No Lambda attached  
**Purpose**: Reserved for future citation review feature

---

### 6. Validate Endpoint (Not Implemented)

**Endpoint**: `POST /validate`  
**Status**: ⚠️ Placeholder - No Lambda attached  
**Purpose**: Reserved for future filing validation feature

---

## 📊 Endpoint Status Summary

| Endpoint | Method | Status | Lambda | Feature |
|----------|--------|--------|--------|---------|
| `/voice/triage` | POST | 🔄 Fixed | VoiceTriage | Voice Access |
| `/translate/document` | POST | 🔄 Fixed | DocumentTranslation | File Interrogation |
| `/petition/generate` | POST | ✅ Working | PetitionArchitect | Petition Verifier |
| `/petition/clarify` | POST | ✅ Working | PetitionArchitect | Petition Verifier |
| `/review` | POST | ⚠️ Placeholder | None | Future |
| `/validate` | POST | ⚠️ Placeholder | None | Future |

---

## 🔐 Authentication

**Current**: No authentication required (open API)  
**Future**: AWS Cognito integration recommended for production

---

## 🌍 CORS Configuration

All endpoints support CORS with:
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Headers: Content-Type,Authorization`
- `Access-Control-Allow-Methods: POST,OPTIONS`

---

## 📝 Common Request Headers

```
Content-Type: application/json
```

---

## ⚠️ Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "message": "Error description",
  "error": "Detailed error message"
}
```

### 500 Internal Server Error
```json
{
  "message": "Internal server error"
}
```

### 502 Bad Gateway
```json
{
  "message": "Internal server error"
}
```
*Indicates Lambda function error - check CloudWatch logs*

---

## 🧪 Testing

### Test Scripts Available:
- `test_voice_triage.py` - Test voice triage endpoint
- `test_document_translator.py` - Test document translation endpoint
- `test_petition_verifier.py` - Test petition verification endpoint

### Run Tests:
```bash
python3 test_voice_triage.py
python3 test_document_translator.py
python3 test_petition_verifier.py
```

---

## 📦 S3 Integration

### Document Upload Bucket:
**Name**: `nyayadwarpalstack-nyayadocbucketv24eb39526-yskr4fmijdf4`

### S3 Event Trigger:
- Petition Architect Lambda automatically processes files uploaded to S3
- Supported formats: `.txt`, `.pdf`
- Results stored in DynamoDB with verification ID

---

## 💾 DynamoDB Tables

### DocumentMetadataTable:
**Name**: `NyayaDwarpalStack-DocumentMetadataTable6ED808AA-VLIQBPG6HLE5`  
**Purpose**: Store verification results, document metadata  
**Partition Key**: `documentId` (String)  
**GSI**: `CaseNumberIndex` for case number queries

### SessionTable:
**Purpose**: Store user session data  
**Partition Key**: `sessionId` (String)

### GlossaryTable:
**Purpose**: Store legal term translations  
**Partition Key**: `term` (String)

---

## 🚀 Deployment

### Deploy Stack:
```bash
npx cdk deploy --require-approval never
```

### View Outputs:
```bash
aws cloudformation describe-stacks \
  --stack-name NyayaDwarpalStack \
  --region ap-south-2 \
  --query 'Stacks[0].Outputs'
```

---

## 📊 CloudWatch Logs

### Log Groups:
- `/aws/lambda/NyayaDwarpal-VoiceTriage`
- `/aws/lambda/NyayaDwarpal-DocumentTranslation`
- `/aws/lambda/NyayaDwarpal-PetitionArchitect`

### View Latest Logs:
```bash
aws logs tail /aws/lambda/NyayaDwarpal-PetitionArchitect \
  --region ap-south-2 \
  --follow
```

---

## 🎯 For Frontend Development

### Recommended Integration Order:
1. **Petition Verifier** (`/petition/generate`) - Already working
2. **Voice Triage** (`/voice/triage`) - Fixed, needs testing
3. **Document Translator** (`/translate/document`) - Fixed, needs testing

### Example Frontend API Client:
```javascript
const API_BASE_URL = 'https://ked0qedvxi.execute-api.ap-south-2.amazonaws.com/prod';

async function verifyPetition(petitionText) {
  const response = await fetch(`${API_BASE_URL}/petition/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      userId: 'user-123',
      petitionText: petitionText
    })
  });
  return response.json();
}
```

---

**Last Updated**: March 2, 2026  
**Generated by**: Kiro AI
