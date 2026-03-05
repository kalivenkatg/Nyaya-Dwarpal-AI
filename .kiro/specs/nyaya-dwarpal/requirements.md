# Requirements Document: Nyaya-Dwarpal AI Agent
## Digital Legal First-Responder

## Introduction

Nyaya-Dwarpal AI Agent is a voice-first, multilingual legal assistance system designed to democratize access to justice in India. The agent acts as a "Digital Legal First-Responder" that helps rural citizens and party-in-person litigants navigate the complex Indian legal system by providing intelligent triage, document generation, translation, and filing assistance in their native language.

The system leverages AWS AI services (Bedrock, Textract, Kendra) and Sarvam AI for Indic language processing to transform spoken grievances into court-ready legal documents while ensuring procedural compliance.

## Glossary

- **AI_Agent**: The Nyaya-Dwarpal intelligent assistant
- **Sarvam_AI**: Indic language model for speech-to-text and translation
- **Bedrock**: AWS AI service (Claude 3.5) for legal reasoning
- **Textract**: AWS OCR service for document analysis
- **Kendra**: AWS semantic search service for legal knowledge base
- **Party-in-Person**: A litigant representing themselves without a lawyer
- **Vernacular**: Regional Indian languages (Hindi, Tamil, Kannada, etc.)
- **Legal_Triage**: Classification of legal problems into categories
- **Petition_Architect**: Component that generates structured legal documents
- **Ad-Valorem_Fee**: Court fee calculated as percentage of claim value
- **BNS**: Bharatiya Nyaya Sanhita (new criminal code)
- **BNSS**: Bharatiya Nagarik Suraksha Sanhita (new criminal procedure code)

## Core Features

### Feature 1: Vernacular Voice-to-Legal Triage
Users speak their grievance in their mother tongue (Hindi, Kannada, Tamil, etc.). AI extracts key facts and identifies specific legal categories (Civil, Criminal, Consumer, etc.)

### Feature 2: Smart Petition Architect
Converts raw stories into structured legal format (Facts, Grounds, Prayer). Supports "Party-in-Person" filing by ensuring all procedural technicalities are met.

### Feature 3: Vernacular-to-English Document Converter
Translates local language evidence (FIRs, Deeds, Notices) into court-standard English. Includes Legal Glossary Check to ensure terms like "Khata" or "Panchnama" are translated with correct legal equivalents.

### Feature 4: "Legal Sanity" Reviewer
Acts as a second pair of eyes for existing petitions filed by lawyers. Cross-references citations against latest laws (BNS/BNSS) to flag outdated sections or fake precedents.

### Feature 5: e-Filing Readiness Check
Scans uploaded documents for "defects" (missing signatures, blurry scans, incorrect margins) before submission to e-Courts portal. Reduces rejection rate.

---

## Requirements

### Requirement 1: Vernacular Voice Input and Processing

**User Story:** As a rural citizen, I want to speak my legal problem in my mother tongue, so that I can access legal help without language barriers.

#### Acceptance Criteria

1. WHEN a user taps the microphone button, THE System SHALL activate voice recording
2. WHEN the user speaks, THE System SHALL use Sarvam AI to convert speech to text in 22+ Indian languages
3. WHEN speech-to-text conversion is complete, THE System SHALL detect the user's emotion (distressed, angry, confused) and urgency level
4. WHEN emotion detection is complete, THE System SHALL store the transcribed text with emotional context
5. IF speech-to-text fails, THEN THE System SHALL prompt the user to speak again or switch to text input

### Requirement 2: Legal Problem Triage and Classification

**User Story:** As a user, I want the AI to understand my legal problem and tell me what type of case it is, so that I know which legal path to follow.

#### Acceptance Criteria

1. WHEN the user's grievance is transcribed, THE AI_Agent SHALL extract key facts (who, what, when, where, why)
2. WHEN facts are extracted, THE AI_Agent SHALL identify the legal category (Civil, Criminal, Consumer, Family, Property, etc.)
3. WHEN the category is identified, THE AI_Agent SHALL map the problem to specific BNS/BNSS/CPC sections
4. WHEN legal mapping is complete, THE AI_Agent SHALL determine the severity level (High, Medium, Low)
5. WHEN triage is complete, THE AI_Agent SHALL present the classification to the user in their native language

### Requirement 3: Structured Petition Generation

**User Story:** As a party-in-person litigant, I want the AI to convert my story into a proper legal petition format, so that I can file it in court without hiring a lawyer.

#### Acceptance Criteria

1. WHEN legal triage is complete, THE Petition_Architect SHALL generate a structured petition with three sections: Facts, Grounds, and Prayer
2. WHEN generating Facts section, THE System SHALL organize the user's story chronologically with dates and parties identified
3. WHEN generating Grounds section, THE System SHALL cite relevant legal provisions (BNS/BNSS/CPC sections) that support the case
4. WHEN generating Prayer section, THE System SHALL specify the relief sought (monetary compensation, injunction, possession, etc.)
5. WHEN the petition is generated, THE System SHALL ensure all procedural technicalities are met (proper formatting, required clauses, verification statement)
6. WHEN the petition is ready, THE System SHALL present it to the user for review and approval

### Requirement 4: Vernacular Document Translation

**User Story:** As a user with local language documents, I want the AI to translate my evidence into court-standard English, so that I can submit them with my petition.

#### Acceptance Criteria

1. WHEN a user uploads a document in a regional language, THE System SHALL use Textract to extract text via OCR
2. WHEN text is extracted, THE System SHALL use Sarvam AI to translate the content to English
3. WHEN translating, THE System SHALL use a Legal Glossary to ensure legal terms are translated correctly (e.g., "Khata" → "Land Revenue Record", "Panchnama" → "Inquest Report")
4. WHEN translation is complete, THE System SHALL preserve the document structure and formatting
5. WHEN the translated document is ready, THE System SHALL allow the user to download it as a PDF

### Requirement 5: Legal Glossary and Term Mapping

**User Story:** As a system, I want to maintain a legal glossary of regional terms, so that translations are legally accurate and court-acceptable.

#### Acceptance Criteria

1. THE System SHALL maintain a Legal Glossary database with regional legal terms and their English equivalents
2. WHEN translating documents, THE System SHALL query the Legal Glossary for each identified legal term
3. WHEN a glossary match is found, THE System SHALL use the official English equivalent instead of literal translation
4. WHEN no glossary match is found, THE System SHALL use standard translation and flag the term for manual review
5. THE System SHALL allow administrators to add new terms to the Legal Glossary

### Requirement 6: Petition Review and Citation Verification

**User Story:** As a lawyer or litigant, I want the AI to review my existing petition and verify all citations, so that I can catch errors before filing.

#### Acceptance Criteria

1. WHEN a user uploads an existing petition, THE System SHALL use Textract to extract the text
2. WHEN text is extracted, THE System SHALL identify all legal citations (BNS, BNSS, IPC, CrPC, CPC sections and case law references)
3. WHEN citations are identified, THE System SHALL cross-reference each citation against the latest legal databases using Amazon Kendra
4. WHEN a citation is outdated (e.g., IPC section instead of BNS), THE System SHALL flag it and suggest the updated equivalent
5. WHEN a citation is fake or non-existent, THE System SHALL flag it as potentially hallucinated
6. WHEN a case law citation is found, THE System SHALL verify its existence and relevance
7. WHEN review is complete, THE System SHALL generate a report with all flagged issues and suggestions

### Requirement 7: Document Defect Detection

**User Story:** As a user, I want the AI to check my documents for defects before I submit them, so that my filing is not rejected.

#### Acceptance Criteria

1. WHEN a user uploads documents for filing, THE System SHALL use Textract to analyze each document
2. WHEN analyzing documents, THE System SHALL check for missing signatures
3. WHEN analyzing documents, THE System SHALL check for blurry or low-quality scans
4. WHEN analyzing documents, THE System SHALL check for incorrect margins (as per e-Courts specifications)
5. WHEN analyzing documents, THE System SHALL check for missing page numbers or annexure references
6. WHEN analyzing documents, THE System SHALL check for proper document formatting (font size, line spacing)
7. WHEN defects are found, THE System SHALL generate a detailed defect report with specific issues and remediation steps
8. WHEN no defects are found, THE System SHALL mark the documents as "e-Filing Ready"

### Requirement 8: e-Filing Readiness Validation

**User Story:** As a user, I want the AI to validate my complete filing package before submission, so that I have the highest chance of acceptance.

#### Acceptance Criteria

1. WHEN the user is ready to file, THE System SHALL perform a comprehensive readiness check
2. WHEN checking readiness, THE System SHALL verify all mandatory documents are present
3. WHEN checking readiness, THE System SHALL verify court fees are calculated and payment proof is attached
4. WHEN checking readiness, THE System SHALL verify all signatures are present
5. WHEN checking readiness, THE System SHALL verify jurisdiction is correct
6. WHEN checking readiness, THE System SHALL verify all citations are valid
7. WHEN all checks pass, THE System SHALL generate an "e-Filing Readiness Certificate"
8. WHEN any check fails, THE System SHALL provide a checklist of remaining items to fix

### Requirement 9: Multilingual User Interface

**User Story:** As a user, I want the entire AI interaction to be in my native language, so that I can understand every step.

#### Acceptance Criteria

1. WHEN the user selects their preferred language, THE System SHALL display all UI elements in that language
2. WHEN the AI generates responses, THE System SHALL translate them to the user's preferred language using Sarvam AI
3. WHEN the AI asks clarifying questions, THE System SHALL present them in the user's native language
4. WHEN displaying legal terms, THE System SHALL provide vernacular explanations alongside English terms
5. THE System SHALL support at least 22 Indian languages (Hindi, Tamil, Telugu, Kannada, Malayalam, Bengali, Marathi, Gujarati, Punjabi, Odia, Assamese, etc.)

### Requirement 10: Conversational Clarification

**User Story:** As a user, I want the AI to ask me questions if my story is unclear, so that the petition is accurate.

#### Acceptance Criteria

1. WHEN the AI cannot extract key facts, THE System SHALL ask targeted clarifying questions
2. WHEN asking questions, THE System SHALL use simple, non-legal language
3. WHEN the user provides additional information, THE System SHALL update the petition accordingly
4. WHEN critical information is missing (dates, amounts, names), THE System SHALL prompt the user before proceeding
5. THE System SHALL limit clarifying questions to a maximum of 5 to avoid user fatigue

### Requirement 11: Document Storage and Retrieval

**User Story:** As a user, I want to save my work and come back later, so that I don't have to start over.

#### Acceptance Criteria

1. WHEN a user creates a petition, THE System SHALL automatically save the draft
2. WHEN the user returns, THE System SHALL allow them to resume from where they left off
3. WHEN documents are uploaded, THE System SHALL store them securely in S3 with encryption
4. WHEN the user completes filing, THE System SHALL provide a downloadable package with all documents
5. THE System SHALL retain user data for 90 days before automatic deletion

### Requirement 12: Case Status Tracking

**User Story:** As a user, I want to track my case status after filing, so that I know what happens next.

#### Acceptance Criteria

1. WHEN a case is filed, THE System SHALL store the case number and filing date
2. WHEN the user checks status, THE System SHALL query the e-Courts API for updates
3. WHEN a hearing date is scheduled, THE System SHALL notify the user via SMS and app notification
4. WHEN case status changes, THE System SHALL provide a plain-language explanation of what it means
5. THE System SHALL provide reminders 3 days before the hearing date

### Requirement 13: Performance and Responsiveness

**User Story:** As a user, I want the AI to respond quickly, so that I don't have to wait long for help.

#### Acceptance Criteria

1. WHEN a user speaks, THE System SHALL complete speech-to-text conversion within 3 seconds
2. WHEN legal triage is performed, THE System SHALL provide classification within 10 seconds
3. WHEN a petition is generated, THE System SHALL complete generation within 30 seconds
4. WHEN documents are analyzed, THE System SHALL complete defect detection within 15 seconds per document
5. THE System SHALL support at least 1,000 concurrent users without performance degradation

### Requirement 14: Security and Privacy

**User Story:** As a user, I want my legal information to be kept confidential, so that my privacy is protected.

#### Acceptance Criteria

1. THE System SHALL encrypt all user data at rest using AES-256 encryption
2. THE System SHALL encrypt all data in transit using TLS 1.3
3. THE System SHALL authenticate users using secure methods (OTP, biometric)
4. THE System SHALL not share user data with third parties without explicit consent
5. THE System SHALL allow users to delete their data at any time
6. THE System SHALL maintain audit logs of all data access for 180 days

### Requirement 15: Offline Capability

**User Story:** As a rural user with poor internet connectivity, I want basic features to work offline, so that I can still use the app.

#### Acceptance Criteria

1. WHEN the user is offline, THE System SHALL allow voice recording and store it locally
2. WHEN the user is offline, THE System SHALL allow viewing previously generated petitions
3. WHEN the user is offline, THE System SHALL queue operations for sync when online
4. WHEN connectivity is restored, THE System SHALL automatically sync queued operations
5. THE System SHALL notify the user when offline features are being used

### Requirement 16: Accessibility

**User Story:** As a user with disabilities, I want the app to be accessible, so that I can use it independently.

#### Acceptance Criteria

1. THE System SHALL support screen readers for visually impaired users
2. THE System SHALL provide voice output for all text content
3. THE System SHALL support large text sizes for users with low vision
4. THE System SHALL provide high-contrast mode for better visibility
5. THE System SHALL support voice-only navigation for users who cannot use touch screens

---

## Feature-to-Requirement Mapping

### Feature 1: Vernacular Voice-to-Legal Triage
- Requirement 1: Vernacular Voice Input and Processing
- Requirement 2: Legal Problem Triage and Classification
- Requirement 9: Multilingual User Interface

### Feature 2: Smart Petition Architect
- Requirement 3: Structured Petition Generation
- Requirement 10: Conversational Clarification

### Feature 3: Vernacular-to-English Document Converter
- Requirement 4: Vernacular Document Translation
- Requirement 5: Legal Glossary and Term Mapping

### Feature 4: "Legal Sanity" Reviewer
- Requirement 6: Petition Review and Citation Verification

### Feature 5: e-Filing Readiness Check
- Requirement 7: Document Defect Detection
- Requirement 8: e-Filing Readiness Validation

---

## Success Metrics

1. **Accuracy**: 90%+ legal classification accuracy
2. **Speed**: <30 seconds for petition generation
3. **Language Coverage**: 22+ Indian languages supported
4. **Filing Success Rate**: 95%+ acceptance rate (reduced rejections)
5. **User Satisfaction**: 4.5+ star rating
6. **Cost Reduction**: 90% reduction in legal consultation costs
7. **Accessibility**: 80%+ of users are party-in-person litigants
8. **Defect Detection**: 95%+ accuracy in identifying filing defects

---

## Non-Functional Requirements

### Scalability
- Support 10,000+ concurrent users
- Handle 100,000+ petitions per day
- Auto-scale based on demand

### Reliability
- 99.9% uptime
- Automatic failover for critical services
- Data backup every 6 hours

### Compliance
- GDPR-compliant data handling
- IT Act 2000 compliance
- e-Courts integration standards

### Maintainability
- Modular architecture for easy updates
- Comprehensive logging and monitoring
- Automated testing with 80%+ code coverage
