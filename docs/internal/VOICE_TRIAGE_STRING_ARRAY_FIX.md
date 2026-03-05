# Voice Triage String-to-Array Fix

**Date**: March 5, 2026  
**Issue**: Frontend receives empty nextSteps and requiredDocuments  
**Root Cause**: Groq returns strings instead of arrays

---

## Problem Identified

CloudWatch logs show Groq is returning "Consumer Rights" category correctly, but the frontend receives empty `nextSteps` and `requiredDocuments` arrays.

### Root Cause

Groq API is returning these fields as **comma-separated strings** instead of **JSON arrays**:

**Groq Response**:
```json
{
  "nextSteps": "ऑटो ड्राइवर से बात करना, शहर के ट्रांसपोर्ट ऑफिस में शिकायत दर्ज करना",
  "requiredDocuments": "ऑटो का नंबर, ड्राइवर का नाम, ओवरचार्ज की गई राशि का प्रमाण"
}
```

**Expected Format**:
```json
{
  "nextSteps": [
    "ऑटो ड्राइवर से बात करना",
    "शहर के ट्रांसपोर्ट ऑफिस में शिकायत दर्ज करना"
  ],
  "requiredDocuments": [
    "ऑटो का नंबर",
    "ड्राइवर का नाम",
    "ओवरचार्ज की गई राशि का प्रमाण"
  ]
}
```

---

## Solution Implemented

Added string-to-array parsing in `lambda_functions/voice_triage/handler.py` in the `classify_legal_problem()` function:

```python
# Parse nextSteps - Groq might return string instead of array
next_steps = classification.get('nextSteps', [])
if isinstance(next_steps, str):
    # Split by comma and clean up
    next_steps = [step.strip() for step in next_steps.split(',') if step.strip()]
elif not isinstance(next_steps, list):
    next_steps = []

# Parse requiredDocuments - Groq might return string instead of array
required_docs = classification.get('requiredDocuments', [])
if isinstance(required_docs, str):
    # Split by comma and clean up
    required_docs = [doc.strip() for doc in required_docs.split(',') if doc.strip()]
elif not isinstance(required_docs, list):
    required_docs = []

# Parse resources - Groq might return string instead of array
resources = classification.get('resources', [])
if isinstance(resources, str):
    # If it's a string, wrap it in a list
    resources = [{'name': 'Resource', 'action': resources, 'cost': '', 'timeline': ''}]
elif not isinstance(resources, list):
    resources = []
```

---

## What This Fixes

### Before Fix
```json
{
  "nextSteps": "Step 1, Step 2, Step 3",  // String
  "requiredDocuments": "Doc 1, Doc 2"      // String
}
```

Frontend tries to iterate over a string, which fails or shows nothing.

### After Fix
```json
{
  "nextSteps": ["Step 1", "Step 2", "Step 3"],  // Array
  "requiredDocuments": ["Doc 1", "Doc 2"]        // Array
}
```

Frontend can properly iterate and display each item.

---

## Testing

### Test Case 1: String Input
```python
next_steps = "ऑटो ड्राइवर से बात करना, शहर के ट्रांसपोर्ट ऑफिस में शिकायत दर्ज करना"
# After parsing:
# ["ऑटो ड्राइवर से बात करना", "शहर के ट्रांसपोर्ट ऑफिस में शिकायत दर्ज करना"]
```

### Test Case 2: Array Input (Already Correct)
```python
next_steps = ["Step 1", "Step 2"]
# After parsing:
# ["Step 1", "Step 2"]  (unchanged)
```

### Test Case 3: Empty/Missing
```python
next_steps = None
# After parsing:
# []  (empty array)
```

---

## Deployment

```bash
# Set API key if not already set
export GROQ_API_KEY='your-api-key-here'

# Deploy
npx cdk deploy --require-approval never
```

---

## Verification

After deployment, test with:
```
Query: "Auto wale ne meter se 3 guna paisa manga"
```

Expected frontend display:
- ✅ Category: "Consumer Rights"
- ✅ Next Steps: List of actionable items (not empty)
- ✅ Required Documents: List of documents (not empty)
- ✅ Recommendation: Detailed Hindi text

---

## Files Modified

1. `lambda_functions/voice_triage/handler.py`
   - Added string-to-array parsing for `nextSteps`
   - Added string-to-array parsing for `requiredDocuments`
   - Added string-to-array parsing for `resources`

---

## Impact

- ✅ Fixes empty nextSteps display
- ✅ Fixes empty requiredDocuments display
- ✅ Handles both string and array responses from Groq
- ✅ Backward compatible (works with arrays too)
- ✅ No breaking changes

---

## Related Issues

This fix also addresses:
- Frontend showing "undefined" for list items
- Console errors about iterating over non-arrays
- Empty sections in the triage results panel

---

**Status**: ✅ Fixed and ready to deploy  
**Risk**: Very low - only adds parsing logic  
**Testing**: Handles all input types (string, array, null)
