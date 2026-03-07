"""
Groq API Integration Utility

This module provides a wrapper for Groq API calls with error handling,
retry logic, and rate limiting for the Nyaya-Dwarpal AI Agent.
"""

import json
import time
import os
from typing import Dict, Any, Optional
from groq import Groq


class BedrockClient:
    """
    Wrapper for Groq API with Llama 3.3 70B model
    
    Features:
    - Automatic retry with exponential backoff
    - Token bucket rate limiting
    - Error handling for throttling
    - Prompt template management
    """
    
    # Groq model ID
    MODEL_ID = "llama-3.3-70b-versatile"
    
    # Rate limiting configuration
    MAX_TOKENS_PER_MINUTE = 10000
    TOKEN_BUCKET_SIZE = 10000
    TOKEN_REFILL_RATE = 166.67  # tokens per second (10000/60)
    
    def __init__(self, region: str = "us-east-1"):
        """
        Initialize Groq client
        
        Args:
            region: Unused parameter (kept for backward compatibility)
        """
        # Don't initialize Groq client here - do it lazily in invoke_model
        self.client = None
        
        # Token bucket for rate limiting
        self.token_bucket = self.TOKEN_BUCKET_SIZE
        self.last_refill_time = time.time()
    
    def _ensure_client(self):
        """Lazily initialize Groq client when needed"""
        if self.client is None:
            print(f"Environment keys available: {list(os.environ.keys())}")
            api_key = os.environ.get("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY not set")
            self.client = Groq(api_key=api_key)
    
    def _refill_token_bucket(self):
        """Refill token bucket based on elapsed time"""
        current_time = time.time()
        elapsed = current_time - self.last_refill_time
        tokens_to_add = elapsed * self.TOKEN_REFILL_RATE
        
        self.token_bucket = min(
            self.TOKEN_BUCKET_SIZE,
            self.token_bucket + tokens_to_add
        )
        self.last_refill_time = current_time
    
    def _wait_for_tokens(self, estimated_tokens: int):
        """
        Wait if necessary to respect rate limits
        
        Args:
            estimated_tokens: Estimated tokens for the request
        """
        self._refill_token_bucket()
        
        if self.token_bucket < estimated_tokens:
            wait_time = (estimated_tokens - self.token_bucket) / self.TOKEN_REFILL_RATE
            time.sleep(wait_time)
            self._refill_token_bucket()
        
        self.token_bucket -= estimated_tokens
    
    def invoke_model(
        self,
        prompt: str,
        max_tokens: int = 2048,
        temperature: float = 0.1,
        system_prompt: Optional[str] = None,
        retry_attempts: int = 3,
    ) -> Dict[str, Any]:
        """
        Invoke Groq Llama 3.3 70B model with retry logic
        
        Args:
            prompt: User prompt for the model
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0.0 to 1.0) - default 0.7 for detailed responses
            system_prompt: Optional system prompt for context
            retry_attempts: Number of retry attempts on failure
            
        Returns:
            Dict containing model response and metadata
            
        Raises:
            Exception: If all retry attempts fail
        """
        # Ensure Groq client is initialized (lazy initialization)
        self._ensure_client()
        
        print(f"[Groq] Invoking model with temperature={temperature}, max_tokens={max_tokens}")
        
        # Estimate tokens for rate limiting (rough approximation)
        estimated_tokens = len(prompt.split()) * 1.3 + max_tokens
        self._wait_for_tokens(int(estimated_tokens))
        
        # Prepare messages
        messages = []
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
            print(f"[Groq] System prompt: {system_prompt[:200]}...")
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        print(f"[Groq] Sending request to {self.MODEL_ID}...")
        
        # Retry logic with exponential backoff
        for attempt in range(retry_attempts):
            try:
                response = self.client.chat.completions.create(
                    model=self.MODEL_ID,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                
                print(f"[Groq] Response received. Tokens: {response.usage.total_tokens}")
                
                return {
                    "text": response.choices[0].message.content,
                    "stop_reason": response.choices[0].finish_reason,
                    "usage": {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens
                    },
                    "model_id": self.MODEL_ID,
                }
                
            except Exception as e:
                error_message = str(e)
                print(f"[Groq] Error on attempt {attempt + 1}: {error_message}")
                
                # Handle rate limiting with exponential backoff
                if "rate_limit" in error_message.lower() and attempt < retry_attempts - 1:
                    wait_time = (2 ** attempt) * 1.0  # 1s, 2s, 4s
                    print(f"[Groq] Rate limited. Waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                
                # Handle temporary errors with retry
                if attempt < retry_attempts - 1:
                    print(f"[Groq] Retrying in 2s...")
                    time.sleep(2.0)  # Wait 2 seconds before retry
                    continue
                
                # Re-raise if last attempt
                raise
        
        raise Exception("All retry attempts failed")
    
    def build_legal_triage_prompt(
        self,
        transcribed_text: str,
        language: str,
        use_native_script: bool = True,
    ) -> str:
        """
        Build prompt for legal problem triage and classification

        Args:
            transcribed_text: User's grievance in their native language
            language: Language code (e.g., 'en' for English, 'hi' for Hindi, 'ta' for Tamil)
            use_native_script: If True, use native script; if False, use romanized text

        Returns:
            Formatted prompt for Groq
        """
        # Language name mapping
        language_map = {
            'en': {'name': 'English', 'script': 'Latin script'},
            'hi': {'name': 'Hindi', 'script': 'Devanagari script (देवनागरी अक्षर)'},
            'te': {'name': 'Telugu', 'script': 'Telugu script (తెలుగు అక్షరాలు)'},
            'ta': {'name': 'Tamil', 'script': 'Tamil script (தமிழ் எழுத்துக்கள்)'},
            'bn': {'name': 'Bengali', 'script': 'Bengali script (বাংলা লিপি)'},
            'mr': {'name': 'Marathi', 'script': 'Devanagari script (देवनागरी अक्षर)'},
            'gu': {'name': 'Gujarati', 'script': 'Gujarati script (ગુજરાતી લિપિ)'},
            'kn': {'name': 'Kannada', 'script': 'Kannada script (ಕನ್ನಡ ಲಿಪಿ)'},
            'ml': {'name': 'Malayalam', 'script': 'Malayalam script (മലയാളം ലിപി)'},
            'pa': {'name': 'Punjabi', 'script': 'Gurmukhi script (ਗੁਰਮੁਖੀ ਲਿਪੀ)'},
        }

        lang_info = language_map.get(language, {'name': language, 'script': 'native script'})
        language_name = lang_info['name']
        script_name = lang_info['script']

        # Build language instruction based on language and script preference
        if language == 'en':
            # English - no native script confusion
            language_instruction = """Respond in clear, professional English.

    JSON keys must be in English. All content values must be in English."""
            language_reminder = ""
        elif use_native_script:
            # Non-English with native script
            language_instruction = f"""YOU MUST RESPOND ONLY IN {language_name.upper()} USING {script_name.upper()}.

    For {language_name}: Use ONLY {script_name}.

    ABSOLUTELY NO English or Roman letters in your response content. JSON keys must stay in English but ALL values must be in {script_name}."""
            language_reminder = f"""

    REMINDER: YOU MUST RESPOND ONLY IN {language_name.upper()} USING {script_name.upper()}. ABSOLUTELY NO English or Roman letters in response values."""
        else:
            # Non-English with romanized text
            language_instruction = f"""Respond in {language_name} using English/Roman letters (romanized/transliterated text).

    JSON keys must be in English. All content values must be in romanized {language_name}."""
            language_reminder = ""

        return f"""{language_instruction}

    You are an expert Indian lawyer with 20+ years of experience. A client has come to you with this legal issue:

    CLIENT'S ISSUE (in {language_name}):
    "{transcribed_text}"

    Your job is to provide EXTREMELY DETAILED, ACTIONABLE legal advice that the client can act on IMMEDIATELY. Do NOT give generic advice like "consult a lawyer" - that's useless. Give SPECIFIC steps they can take TODAY.

    ANALYZE AND CATEGORIZE:

    1. LEGAL CATEGORY (choose most specific - DO NOT use "Other" unless absolutely necessary):
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
       - Other: ONLY if truly doesn't fit any category above

    2. URGENCY LEVEL:
       - HIGH: Unpaid salary 2+ months, eviction notice, domestic violence, immediate threat, legal deadline within 30 days
       - MEDIUM: Defective product, contract dispute, property maintenance, delayed payment
       - LOW: General consultation, information request, minor disputes

    3. PROVIDE EXTREMELY DETAILED ADVICE:

    Your response MUST include:

    A. IMMEDIATE ACTIONS (What to do in next 24-48 hours):
       - Specific documents to gather (with examples)
       - Evidence to collect (photos, recordings, witnesses)
       - People to contact (with phone numbers/websites if possible)

    B. STEP-BY-STEP LEGAL PROCESS (Timeline-based):
       - DAY 1-3: First actions
       - WEEK 1: Legal notice/complaint filing
       - WEEK 2-4: Follow-up actions
       - MONTH 2+: Court proceedings if needed

    C. WHERE TO FILE COMPLAINTS:
       - Exact office names (Labour Commissioner, Consumer Forum, Police Station, etc.)
       - Online portals (with URLs like shramsuvidha.gov.in, consumerhelpline.gov.in)
       - Physical addresses if known
       - Free vs paid options

    D. COST BREAKDOWN:
       - Legal notice: ₹2,000-5,000
       - Court filing fees: ₹500-2,000
       - Lawyer fees: ₹10,000-50,000 (range based on complexity)
       - FREE options: Legal aid, government helplines, online complaints

    E. TIMELINE:
       - Best case: X days/weeks
       - Average case: X months
       - Worst case: X months/years

    F. LEGAL RIGHTS & LAWS:
       - Specific Act names (Payment of Wages Act 1936, Consumer Protection Act 2019, etc.)
       - Section numbers (Section 5, Section 35, etc.)
       - What the law says in simple language
       - Penalties for violator

    G. COMPENSATION/REMEDY:
       - What client can claim (money, possession, injunction, etc.)
       - How much (specific amounts or formulas)
       - Interest rates (typically 9-15% per annum)

    H. FREE RESOURCES:
       - State Legal Services Authority (free lawyers)
       - Government helplines (with numbers)
       - Online complaint portals
       - NGOs that can help

    I. WARNINGS/CAUTIONS:
       - Time limits (statute of limitations)
       - Documents NOT to sign
       - Common mistakes to avoid
       - When to definitely hire a lawyer

    CRITICAL INSTRUCTIONS:
    - Your recommendation MUST be at least 500 words with specific, actionable steps
    - DO NOT give generic advice
    - Be as detailed as a real lawyer consultation
    - Choose the MOST SPECIFIC category - avoid "Other"
    - Return ONLY valid JSON - NO markdown backticks, NO preamble, NO extra text

    Respond in JSON format with these EXACT keys:
    {{
      "category": "Employment Law - Unpaid Wages",
      "subCategory": "Salary not paid for 3 months",
      "urgency": "high",
      "urgencyReason": "Detailed explanation of why this is urgent with legal basis",
      "emotionalState": "distressed",
      "facts": {{
    "who": "employer and employee",
    "what": "unpaid salary",
    "when": "3 months",
    "where": "workplace location if mentioned",
    "amount": "monetary value if mentioned"
      }},
      "legalSections": [
    {{
      "act": "Payment of Wages Act, 1936",
      "section": "Section 5",
      "description": "Wages must be paid within 7 days for monthly employees",
      "penalty": "Fine up to ₹3,750 + compensation to employee",
      "remedy": "Can claim full wages + interest + compensation"
    }}
      ],
      "recommendation": "EXTREMELY DETAILED multi-paragraph advice with specific steps, timelines, costs, and resources. Include:\\n\\n1. IMMEDIATE ACTIONS (Next 24-48 hours):\\n- Gather X, Y, Z documents\\n- Contact A, B, C people\\n- Preserve evidence by doing X\\n\\n2. LEGAL PROCESS (Week by week):\\n- Week 1: Send legal notice via lawyer (₹2,000-5,000)\\n- Week 2: File complaint at Labour Commissioner (FREE)\\n- Week 3-4: Attend hearing\\n- Month 2+: Labour Court if needed\\n\\n3. WHERE TO GO:\\n- Labour Commissioner Office: [address/website]\\n- Online complaint: shramsuvidha.gov.in\\n- Free legal aid: State Legal Services Authority\\n\\n4. YOUR RIGHTS:\\n- Under Section X of Act Y, you are entitled to Z\\n- Employer faces penalty of A if found guilty\\n- You can claim B + C + D\\n\\n5. COSTS:\\n- Legal notice: ₹X\\n- Filing fees: ₹Y (or FREE at Labour Commissioner)\\n- Lawyer: ₹Z (or FREE via legal aid)\\n\\n6. TIMELINE:\\n- Labour Commissioner: 1-3 months\\n- Labour Court: 6-12 months\\n- High Court appeal: 1-2 years\\n\\n7. FREE RESOURCES:\\n- [Resource 1]: [How to access]\\n- [Resource 2]: [Contact details]\\n\\n8. WARNINGS:\\n- File within X days or you lose right to claim\\n- Don't sign any settlement without lawyer review\\n- Keep all original documents safe",
      "nextSteps": [
    "TODAY: Collect employment contract, salary slips, bank statements showing no deposits",
    "DAY 2: Visit State Legal Services Authority for free lawyer consultation",
    "DAY 3: Lawyer sends legal notice to employer demanding payment within 7 days",
    "DAY 10: If no response, file written complaint at Labour Commissioner office (FREE)",
    "DAY 30: Attend Labour Commissioner hearing with all documents",
    "DAY 60: If unresolved, file case in Labour Court with lawyer"
      ],
      "requiredDocuments": [
    "Employment contract or appointment letter",
    "Salary slips for last 6 months",
    "Bank statements showing salary deposits (or lack thereof)",
    "Email/WhatsApp correspondence with employer about salary",
    "Any written warnings or termination letters",
    "Identity proof (Aadhaar, PAN card)"
      ],
      "estimatedCost": "Legal notice: ₹2,000-5,000, Labour Commissioner: FREE, Labour Court filing: ₹500-1,000, Lawyer fees: ₹10,000-25,000 (or FREE via legal aid for cases under ₹5 lakhs)",
      "timeline": "1-3 months via Labour Commissioner (fastest route), 6-12 months if case goes to Labour Court, 1-2 years if appeals to High Court",
      "severity": "high",
      "resources": [
    {{
      "name": "Labour Commissioner Office",
      "action": "File free complaint at nearest office. Find location: https://labour.gov.in/",
      "cost": "Completely FREE - no fees for filing or hearings",
      "timeline": "Complaint resolved in 1-3 months typically"
    }},
    {{
      "name": "State Legal Services Authority",
      "action": "Get free lawyer for cases under ₹5 lakhs. Visit district legal aid office or call 15100",
      "cost": "Completely FREE legal representation",
      "timeline": "Lawyer assigned within 7-15 days"
    }},
    {{
      "name": "Shram Suvidha Portal",
      "action": "File online complaint: https://shramsuvidha.gov.in/",
      "cost": "FREE online complaint system",
      "timeline": "Response within 30 days"
    }}
      ],
      "legalDisclaimer": "This advice is AI-generated for informational purposes only. Please consult a qualified legal professional before taking any action. Laws may vary by state."
    }}
    {language_reminder}"""

    
    def build_petition_generation_prompt(
        self,
        facts: Dict[str, Any],
        legal_category: str,
        relevant_sections: list,
    ) -> str:
        """
        Build prompt for structured petition generation
        
        Args:
            facts: Extracted facts from triage
            legal_category: Legal category (Civil, Criminal, etc.)
            relevant_sections: List of relevant legal sections
            
        Returns:
            Formatted prompt for Bedrock
        """
        return f"""You are a legal document drafting assistant for Indian courts. Generate a structured legal petition.

Facts: {json.dumps(facts, indent=2, ensure_ascii=False)}
Legal Category: {legal_category}
Relevant Sections: {', '.join(relevant_sections)}

Generate a petition with three sections:

1. FACTS: Organize the story chronologically with dates and parties clearly identified
2. GROUNDS: Cite relevant legal provisions (BNS/BNSS/CPC sections) that support the case
3. PRAYER: Specify the relief sought (monetary compensation, injunction, possession, etc.)

Ensure all procedural technicalities are met:
- Proper formatting with numbered paragraphs
- Required clauses and legal language
- Verification statement at the end

Format your response as JSON with keys: facts_section, grounds_section, prayer_section."""
    
    def build_citation_verification_prompt(
        self,
        petition_text: str,
        citations: list,
    ) -> str:
        """
        Build prompt for citation verification and relevance assessment
        
        Args:
            petition_text: Full petition text
            citations: List of extracted citations
            
        Returns:
            Formatted prompt for Bedrock
        """
        return f"""You are a legal citation verification assistant for Indian law. Review the following citations.

Petition excerpt:
{petition_text[:1000]}...

Citations to verify:
{json.dumps(citations, indent=2, ensure_ascii=False)}

For each citation:
1. Check if it's outdated (e.g., IPC instead of BNS, CrPC instead of BNSS)
2. Assess relevance to the legal argument
3. Suggest updated equivalents if outdated

Format your response as JSON array with objects containing: citation, is_outdated, suggested_replacement, relevance_score (0-1), relevance_explanation."""
    
    def build_clarification_prompt(
        self,
        petition_draft: str,
        missing_info: list,
    ) -> str:
        """
        Build prompt for generating clarifying questions
        
        Args:
            petition_draft: Current petition draft
            missing_info: List of missing information items
            
        Returns:
            Formatted prompt for Bedrock
        """
        return f"""You are a helpful legal assistant. The petition draft is missing some information.

Current draft:
{petition_draft[:500]}...

Missing information:
{json.dumps(missing_info, indent=2, ensure_ascii=False)}

Generate up to 5 targeted clarifying questions in simple, non-legal language. Focus on critical information like dates, amounts, and names.

Format your response as JSON array of strings (questions)."""
