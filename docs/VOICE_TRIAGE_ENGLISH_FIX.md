# Voice Triage English Language Prompt Fix

## Problem Identified

CloudWatch logs showed: `"Prompt preview: YOU MUST RESPOND ONLY IN en NATIVE SCRIPT"`

When language was English (`en`), the prompt incorrectly instructed Groq to use "NATIVE SCRIPT" which is confusing since English already uses Latin script. This caused Groq to return improperly formatted responses.

## Root Cause

The `build_legal_triage_prompt()` method in `bedrock_client.py` was using a generic template that said "NATIVE SCRIPT" for all languages, including English.

## Solution Implemented

### 1. Language-Specific Prompt Instructions

Updated `lambda_functions/shared/bedrock_client.py` and `lambda_functions/shared/python/bedrock_client.py`:

**Added language mapping:**
```python
language_map = {
    'en': {'name': 'English', 'script': 'Latin script'},
    'hi': {'name': 'Hindi', 'script': 'Devanagari script (देवनागरी अक्षर)'},
    'te': {'name': 'Telugu', 'script': 'Telugu script (తెలుగు అక్షరాలు)'},
    'ta': {'name': 'Tamil', 'script': 'Tamil script (தமிழ் எழுத்துக்கள்)'},
    # ... more languages
}
```

**English-specific instruction:**
```python
if language == 'en':
    language_instruction = """Respond in clear, professional English.

JSON keys must be in English. All content values must be in English."""
```

**Non-English with native script:**
```python
elif use_native_script:
    language_instruction = f"""YOU MUST RESPOND ONLY IN {language_name.upper()} USING {script_name.upper()}.

For {language_name}: Use ONLY {script_name}.

ABSOLUTELY NO English or Roman letters in your response content. JSON keys must stay in English but ALL values must be in {script_name}."""
```

**Non-English with romanized text:**
```python
else:
    language_instruction = f"""Respond in {language_name} using English/Roman letters (romanized/transliterated text).

JSON keys must be in English. All content values must be in romanized {language_name}."""
```

### 2. Improved JSON Parsing

Updated `lambda_functions/voice_triage/handler.py` with robust JSON parsing:

**Multiple fallback strategies:**
1. **Direct parse**: Try parsing response as-is
2. **Markdown removal**: Strip ```json and ``` markers
3. **Boundary extraction**: Find first `{` and last `}` to extract JSON object

**Enhanced logging:**
```python
print(f"[GROQ RAW RESPONSE] First 500 chars: {response_text[:500]}...")
print("[JSON PARSE] Success on direct parse")  # or other status
```

### 3. Clearer Prompt Instructions

Added to prompt:
```
CRITICAL INSTRUCTIONS:
- Your recommendation MUST be at least 500 words with specific, actionable steps
- DO NOT give generic advice
- Be as detailed as a real lawyer consultation
- Choose the MOST SPECIFIC category - avoid "Other"
- Return ONLY valid JSON - NO markdown backticks, NO preamble, NO extra text
```

## Files Modified

1. `lambda_functions/shared/bedrock_client.py` - Main bedrock client
2. `lambda_functions/shared/python/bedrock_client.py` - Lambda layer copy
3. `lambda_functions/voice_triage/handler.py` - Improved JSON parsing

## Deployment

Deployed via CDK:
```bash
npx cdk deploy --require-approval never
```

Deployment successful - all Lambda functions updated.

## Testing

To test the fix:

1. **English query:**
   ```bash
   curl -X POST https://ked0qedvxi.execute-api.ap-south-2.amazonaws.com/prod/voice/triage \
     -H "Content-Type: application/json" \
     -d '{
       "userId": "test-user",
       "transcribedText": "The auto driver charged me 3 times the meter fare",
       "language": "en",
       "useNativeScript": true
     }'
   ```

2. **Hindi query:**
   ```bash
   curl -X POST https://ked0qedvxi.execute-api.ap-south-2.amazonaws.com/prod/voice/triage \
     -H "Content-Type: application/json" \
     -d '{
       "userId": "test-user",
       "transcribedText": "Auto wale ne meter se 3 guna paisa manga",
       "language": "hi",
       "useNativeScript": true
     }'
   ```

3. **Check CloudWatch logs** for:
   - `[GROQ RAW RESPONSE]` - Raw Groq response
   - `[JSON PARSE]` - Parse status
   - Category should be specific (e.g., "Consumer Rights - Service Deficiency"), NOT "Other"

## Expected Results

- **English queries**: Clear English prompt, no "NATIVE SCRIPT" confusion
- **Hindi queries**: Proper Devanagari script instruction
- **All queries**: Specific legal categories, detailed recommendations (500+ words)
- **JSON parsing**: Robust handling of markdown and formatting issues

## Benefits

1. **Clearer prompts** - No confusing "NATIVE SCRIPT" for English
2. **Better categorization** - Stronger emphasis on specific categories
3. **Robust parsing** - Multiple fallback strategies for JSON extraction
4. **Better logging** - Easier debugging with raw response logging
5. **Multilingual support** - Proper script names for 10+ Indian languages

## Status

✅ **COMPLETE** - Deployed and ready for testing
