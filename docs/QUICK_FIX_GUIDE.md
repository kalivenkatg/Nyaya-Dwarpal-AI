# Voice Triage Quick Fix Guide

## 🎯 Problem
Voice Triage returns "Other" category instead of specific categories like "Consumer Rights".

## ✅ Solution
The `GROQ_API_KEY` environment variable is not set in Lambda.

## 🚀 Fix in 3 Steps

### 1. Set API Key
```bash
export GROQ_API_KEY='your-groq-api-key-here'
```

### 2. Deploy
```bash
./redeploy_with_groq_key.sh
```
or
```bash
npx cdk deploy --require-approval never
```

### 3. Test
```bash
./test_voice_triage_endpoint.sh
```

## ✅ Success Indicators

- Category: "Consumer Rights" (NOT "Other")
- Response: Detailed Hindi advice
- CloudWatch logs show Groq API calls

## 📊 Test Results

**Local Test**: ✅ SUCCESS
- Query: "Auto wale ne meter se 3 guna paisa manga"
- Category: "Consumer Rights"
- Sub-Category: "Service Deficiency"
- Response: Detailed Hindi advice (1143 chars)

This proves the code works - just need to set the API key!

## ⏱️ Time: 5 minutes

## 🎯 Confidence: 99%

---

**Full details**: See `docs/internal/VOICE_TRIAGE_FINAL_DIAGNOSIS.md`
