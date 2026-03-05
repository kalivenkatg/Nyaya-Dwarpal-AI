#!/usr/bin/env python3
"""
Direct Groq API test to debug category classification
"""

import json
import os

try:
    from groq import Groq
except ImportError:
    print("❌ groq package not installed. Installing...")
    import subprocess
    subprocess.check_call(["pip3", "install", "groq", "-q"])
    from groq import Groq

def test_groq_classification():
    """Test Groq API with Hindi auto driver overcharging query"""
    
    # Test query
    transcription = "Auto wale ne meter se 3 guna paisa manga"
    language = "hi"
    
    print("=" * 80)
    print("GROQ API DIRECT TEST")
    print("=" * 80)
    print(f"\nTest Query: {transcription}")
    print(f"Language: {language}")
    print("\n" + "=" * 80)
    
    # Check API key
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("\n❌ ERROR: GROQ_API_KEY environment variable not set!")
        print("Please set it with: export GROQ_API_KEY='your-api-key'")
        return
    
    print(f"\n✓ GROQ_API_KEY found (length: {len(api_key)})")
    
    # Initialize client
    client = Groq(api_key=api_key)
    
    # Build prompt (same as Lambda)
    language_instruction = f"""YOU MUST RESPOND ONLY IN {language} NATIVE SCRIPT.

For Telugu: Use ONLY తెలుగు అక్షరాలు (Telugu Unicode characters like తెలుగు).
For Hindi: Use ONLY देवनागरी अक्षर.
For Tamil: Use ONLY தமிழ் எழுத்துக்கள்.

ABSOLUTELY NO English or Roman letters in your response content. JSON keys must stay in English but ALL values must be in native script."""

    prompt = f"""{language_instruction}
You are an expert Indian lawyer with 20+ years of experience. A client has come to you with this legal issue:

CLIENT'S ISSUE (in {language}):
"{transcription}"

Your job is to provide EXTREMELY DETAILED, ACTIONABLE legal advice that the client can act on IMMEDIATELY. Do NOT give generic advice like "consult a lawyer" - that's useless. Give SPECIFIC steps they can take TODAY.

ANALYZE AND CATEGORIZE:

1. LEGAL CATEGORY (choose most specific):
   - Employment Law - Unpaid Wages: salary, wages not paid, employer owes money
   - Employment Law - Wrongful Termination: fired, terminated, dismissed without cause
   - Employment Law - Workplace Harassment: harassment, discrimination, hostile environment
   - Property Law - Tenant Rights: landlord issues, eviction, rent disputes, maintenance
   - Property Law - Property Disputes: boundary disputes, illegal construction, encroachment
   - Consumer Rights - Defective Products: faulty goods, warranty issues, refund denied
   - Consumer Rights - Service Deficiency: poor service, overcharging, fraud by seller
   - Family Law - Divorce: marriage dissolution, separation, alimony
   - Family Law - Child Custody: custody disputes, visitation rights
   - Family Law - Domestic Violence: abuse, threats, protection needed
   - Criminal Law - Theft/Fraud: stolen property, cheating, financial fraud
   - Criminal Law - Assault: physical violence, threats, intimidation
   - Contract Law - Breach: agreement violated, payment not received, contract dispute
   - Civil Disputes - Damages: compensation for injury, negligence, accident
   - Other: only if truly doesn't fit above

2. URGENCY LEVEL:
   - HIGH: Unpaid salary 2+ months, eviction notice, domestic violence, immediate threat, legal deadline within 30 days
   - MEDIUM: Defective product, contract dispute, property maintenance, delayed payment
   - LOW: General consultation, information request, minor disputes

Respond in JSON format with category, subCategory, urgency, recommendation (500+ words), nextSteps, requiredDocuments, estimatedCost, timeline, resources.

CRITICAL: Your recommendation MUST be at least 500 words with specific, actionable steps. Do NOT give generic advice. Be as detailed as a real lawyer consultation.

REMINDER: YOU MUST RESPOND ONLY IN {language} NATIVE SCRIPT. For Hindi use ONLY देवनागरी अक्षर. ABSOLUTELY NO English or Roman letters in response values.

Respond with ONLY the JSON object, no markdown formatting."""

    system_prompt = "You are an expert Indian lawyer with 20+ years of experience. You MUST provide detailed, actionable legal advice. NEVER say 'consult a lawyer' as generic advice. Always give specific steps, costs, timelines, and resources. Choose the most specific legal category - DO NOT return 'Other' unless absolutely necessary."
    
    print("\n" + "-" * 80)
    print("CALLING GROQ API")
    print("-" * 80)
    print(f"Model: llama-3.3-70b-versatile")
    print(f"Temperature: 0.7")
    print(f"Max Tokens: 3000")
    print(f"System Prompt: {system_prompt[:100]}...")
    print(f"Prompt Length: {len(prompt)} characters")
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=3000,
            temperature=0.7
        )
        
        print("\n✓ API call successful!")
        print(f"Tokens used: {response.usage.total_tokens}")
        print(f"Finish reason: {response.choices[0].finish_reason}")
        
        # Get response text
        response_text = response.choices[0].message.content.strip()
        print(f"\nResponse length: {len(response_text)} characters")
        
        # Remove markdown if present
        if response_text.startswith('```'):
            print("Removing markdown code blocks...")
            response_text = response_text.split('```')[1]
            if response_text.startswith('json'):
                response_text = response_text[4:]
            response_text = response_text.rsplit('```', 1)[0]
        
        print("\n" + "-" * 80)
        print("RAW RESPONSE (first 2000 chars)")
        print("-" * 80)
        print(response_text[:2000])
        print("...")
        
        # Parse JSON
        try:
            classification = json.loads(response_text)
            
            print("\n" + "=" * 80)
            print("CLASSIFICATION RESULTS")
            print("=" * 80)
            
            category = classification.get('category', 'MISSING')
            print(f"\n📋 Category: {category}")
            
            if category == "Other":
                print("❌ PROBLEM FOUND: Category is 'Other'!")
                print("\nThis means Groq is NOT following the prompt instructions.")
                print("The prompt explicitly says to choose a specific category.")
            elif "Consumer" in category:
                print("✓ SUCCESS: Category correctly identified as Consumer Rights!")
            else:
                print(f"⚠️  Category is '{category}'")
            
            print(f"\n📝 Sub-Category: {classification.get('subCategory', 'N/A')}")
            print(f"🚨 Urgency: {classification.get('urgency', 'N/A')}")
            
            recommendation = classification.get('recommendation', '')
            print(f"\n💡 Recommendation length: {len(recommendation)} characters")
            
            if len(recommendation) < 500:
                print(f"❌ PROBLEM: Recommendation too short ({len(recommendation)} chars)")
            
            if "consult" in recommendation.lower():
                print("❌ PROBLEM: Contains 'consult' - generic advice detected")
            
            print(f"\n📄 Next Steps: {len(classification.get('nextSteps', []))} items")
            print(f"📎 Required Documents: {len(classification.get('requiredDocuments', []))} items")
            
            # Full JSON
            print("\n" + "=" * 80)
            print("FULL JSON RESPONSE")
            print("=" * 80)
            print(json.dumps(classification, indent=2, ensure_ascii=False))
            
        except json.JSONDecodeError as e:
            print(f"\n❌ JSON PARSE ERROR: {str(e)}")
            print("\nFull response:")
            print(response_text)
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_groq_classification()
