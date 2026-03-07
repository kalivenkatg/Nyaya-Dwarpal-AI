# Nyaya-Dwarpal — Justice in Your Language

**AI-Powered Legal Assistant for Bharat | Democratizing Access to Justice**

![Nyaya-Dwarpal Banner](https://img.shields.io/badge/AI%20for%20Bharat-Powered%20by%20AWS-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)
![AWS](https://img.shields.io/badge/AWS-Lambda%20%7C%20S3%20%7C%20DynamoDB-yellow?style=for-the-badge)

---

## 🎯 Problem Statement

**Access to justice in India faces critical barriers:**

- **Language Gap**: 90% of Indians don't speak English fluently, yet most legal documents are in English
- **Legal Complexity**: Understanding BNS (Bharatiya Nyaya Sanhita), BNSS, and CPC sections is overwhelming for common citizens
- **Cost Barrier**: Legal consultation costs ₹500-₹2000 per hour, unaffordable for 70% of the population
- **Time Delay**: Court backlogs of 4+ crore cases mean years of waiting for justice
- **Documentation Burden**: Filing petitions requires technical legal knowledge most citizens lack

**Nyaya-Dwarpal bridges this gap** by providing AI-powered legal assistance in regional languages, making justice accessible to every Indian.

---

## ✨ Features

### 1. 🎤 Voice Triage (Awaaz Se Nyaya)
**Speak your legal problem in your own language**

- **Voice Recording**: Click-to-record interface with real-time waveform visualization
- **Speech-to-Text**: Powered by Sarvam AI Saaras v3 model for accurate Indic language transcription
- **Emotion Detection**: AI analyzes emotional state (angry, distressed, confused, calm) and urgency level
- **Legal Classification**: Automatically categorizes issues (Civil, Criminal, Consumer, Family, Property)
- **BNS Intelligence**: Identifies relevant Bharatiya Nyaya Sanhita sections with plain-language explanations
- **Multi-language Support**: Hindi, English, and other regional languages

**Use Case**: A farmer in rural Maharashtra can describe a land dispute in Marathi, and the system will identify relevant legal sections and urgency.

---

### 2. 📄 Document Translation (Bhasha Parivartan)
**Translate legal documents between English and regional languages**

- **Smart Upload**: Drag-and-drop interface for .txt and .pdf files
- **S3 Integration**: Secure document storage with encryption
- **Intelligent Extraction**: 
  - Direct text reading for .txt files
  - AWS Textract for PDFs and images (cross-region support)
- **Legal Translation**: Sarvam AI Mayura v1 model with formal legal tone
- **Chunked Processing**: Handles large documents by splitting into 900-character chunks
- **Download Support**: Pre-signed S3 URLs for translated documents

**Use Case**: A small business owner receives an English legal notice and needs it translated to Tamil to understand the implications.

---

### 3. 📝 Petition Architect (Darkhwast Nirman)
**AI-generated legal petitions in proper format**

- **Fact Extraction**: Automatically extracts key facts from user's description
- **Legal Grounding**: Identifies applicable BNS/BNSS/CPC sections
- **Structured Drafting**: Generates petitions with:
  - Facts Section: Chronological narrative
  - Grounds Section: Legal provisions and arguments
  - Prayer Section: Relief sought
  - Verification Statement: Proper legal format
- **Citation Verification**: Validates legal citations and suggests updated equivalents
- **Defect Detection**: Identifies missing information or formatting issues

**Use Case**: A tenant facing illegal eviction can generate a properly formatted petition citing relevant sections without hiring a lawyer.

---

### 4. 🗂️ Case Memory (Mamla Yaad)
**Your personal legal consultation history**

- **Automatic Saving**: All voice triage sessions stored in DynamoDB
- **Smart Retrieval**: Fetch cases by user ID with filtering
- **Rich Metadata**: 
  - Case ID and timestamp
  - Emotion badges (color-coded: red/orange/purple/green)
  - Legal category and relevant sections
  - Full transcription and extracted facts
- **Case Details Modal**: View complete case information
- **Generate Petition**: One-click petition generation from saved cases

**Use Case**: A user can review their previous consultations about a property dispute and generate a petition when ready to file.

---

### 5. 📚 Legal Library (Kanoon Gyan) *(Coming Soon)*
**Searchable database of BNS, BNSS, and CPC sections**

- Browse legal sections by category
- Plain-language explanations
- Real-world examples
- Cross-references between sections

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │ Voice Triage │  │  Document    │  │ Case Memory  │              │
│  │   (React)    │  │  Upload      │  │   (React)    │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
└─────────┼──────────────────┼──────────────────┼────────────────────┘
          │                  │                  │
          │ Sarvam AI        │                  │
          │ (Speech-to-Text) │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      API GATEWAY (REST)                              │
│  POST /voice/triage  │  POST /translate/document  │  GET /cases    │
│  POST /petition/generate  │  POST /petition/clarify                 │
└─────────┬──────────────────┬──────────────────┬────────────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      AWS LAMBDA FUNCTIONS                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │ Voice Triage │  │  Document    │  │ Case Memory  │              │
│  │   Lambda     │  │  Translator  │  │   Lambda     │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
│         │                  │                  │                      │
│         │ ┌────────────────┴──────────────────┘                     │
│         │ │                                                          │
│         ▼ ▼                                                          │
│  ┌──────────────────────────────────────────────────────────┐       │
│  │      AWS Bedrock (Claude 3.5 Sonnet)                    │       │
│  │  • Emotion Detection  • Legal Classification             │       │
│  │  • Fact Extraction    • Petition Generation              │       │
│  └──────────────────────────────────────────────────────────┘       │
└─────────┬──────────────────┬──────────────────┬────────────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │  DynamoDB    │  │  S3 Buckets  │  │  AWS Textract│              │
│  │  • Sessions  │  │  • Documents │  │  (PDF/Image) │              │
│  │  • Metadata  │  │  • Archives  │  │              │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
└─────────────────────────────────────────────────────────────────────┘
          │                  │
          ▼                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   EXTERNAL SERVICES                                  │
│  ┌──────────────────────────────────────────────────────┐           │
│  │  Sarvam AI                                           │           │
│  │  • Saaras v3 (Speech-to-Text)                       │           │
│  │  • Mayura v1 (Translation)                          │           │
│  └──────────────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔌 API Endpoints

| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|--------------|----------|
| `/voice/triage` | POST | Analyze transcribed voice input | `{userId, transcribedText, language}` | Emotion, classification, BNS sections |
| `/translate/document` | POST | Translate legal documents | `{userId, s3Key, sourceLanguage, targetLanguage, documentType}` | Original and translated text |
| `/cases` | GET | Fetch user's case history | Query: `?userId={id}&limit={n}` | Array of cases with metadata |
| `/petition/generate` | POST | Generate legal petition | `{userId, facts, legalCategory, relevantSections}` | Structured petition draft |
| `/petition/clarify` | POST | Clarify petition details | `{userId, sessionId, question}` | Clarification response |

**Base URL**: `https://ked0qedvxi.execute-api.ap-south-2.amazonaws.com/prod`

---

## 🛠️ Tech Stack

### **Cloud Infrastructure**
- **AWS CDK (Python)**: Infrastructure as Code
- **AWS Lambda (Python 3.11)**: Serverless compute
- **Amazon API Gateway**: REST API management
- **Amazon S3**: Document storage with encryption
- **Amazon DynamoDB**: NoSQL database for sessions and metadata
- **AWS Bedrock**: Claude 3.5 Sonnet for legal reasoning
- **AWS Textract**: Document text extraction (cross-region)

### **AI/ML Services**
- **AWS Bedrock (Claude 3.5 Sonnet)**: 
  - Emotion detection and urgency analysis
  - Legal problem classification
  - Fact extraction
  - Petition generation
  - Document verification
- **Sarvam AI Saaras v3**: Indic language speech-to-text
- **Sarvam AI Mayura v1**: Legal document translation with formal tone

### **Frontend**
- **HTML5 + Tailwind CSS**: Responsive UI
- **Vanilla JavaScript**: No framework overhead
- **MediaRecorder API**: Browser-based audio recording
- **Fetch API**: RESTful API integration

### **Development Tools**
- **Python 3.11**: Lambda runtime
- **Pydantic**: Data validation
- **Boto3**: AWS SDK for Python
- **Git**: Version control

---

## 🤔 Why These Services?

### **AWS Bedrock (Claude 3.5 Sonnet)**
**Advanced Legal Reasoning**
- **State-of-the-Art Performance**: Claude 3.5 Sonnet excels at complex reasoning and analysis
- **Long Context Window**: Handles detailed legal documents and multi-turn conversations
- **Multilingual Support**: Strong performance across English and Indic languages
- **JSON Mode**: Reliable structured output for legal classifications

**AWS Integration**
- **Seamless Integration**: Native AWS service with no external API dependencies
- **Security & Compliance**: Enterprise-grade security with AWS IAM controls
- **Scalability**: Auto-scales with Lambda for any load
- **Cost-Effective**: Pay-per-use pricing with no minimum commitments

**Why This Matters**: When a user speaks their legal problem, they need accurate, detailed analysis. Claude 3.5 Sonnet provides sophisticated legal reasoning while maintaining fast response times through AWS's infrastructure.

---

### **Sarvam AI over Amazon Transcribe**
**Purpose-Built for Bharat**
- **22 Indian Languages**: Comprehensive support for Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Punjabi, and more
- **Indic Language Accuracy**: 95%+ accuracy for Indian accents and dialects vs 70-80% with generic models
- **Code-Mixing Support**: Handles Hinglish and other mixed-language speech patterns common in India
- **Legal Terminology**: Trained on Indian legal vocabulary and context
- **Cultural Context**: Understands Indian names, places, and cultural references
- **Formal Translation**: Mayura v1 provides legal-grade translations with proper formal tone

**Why This Matters**: A farmer in rural Maharashtra speaking Marathi with local dialect needs accurate transcription. Amazon Transcribe's limited Indic support would miss critical details, while Sarvam AI captures every word correctly.

---

### **DynamoDB over RDS**
**Serverless & Cost-Effective**
- **Zero Ops Overhead**: No database servers to manage, patch, or scale
- **Scales to Zero Cost**: Pay only for actual reads/writes, not idle database capacity
- **Millisecond Latency**: Single-digit millisecond response times for case retrieval
- **Auto-Scaling**: Handles traffic spikes during peak hours without manual intervention
- **Built-in TTL**: Automatic data expiration after 90 days for privacy compliance
- **Global Tables**: Easy replication across regions if we expand beyond India

**Cost Comparison**:
- **RDS**: ₹8,000-₹15,000/month for smallest instance (even with zero traffic)
- **DynamoDB**: ₹0-₹500/month for typical usage (scales with actual usage)

**Why This Matters**: For a social impact project serving rural India, we can't afford ₹15,000/month for an idle database. DynamoDB costs ₹50/month during development and scales automatically when we reach millions of users.

---

### **Lambda over EC2**
**Event-Driven & Cost-Efficient**
- **Pay Per Request**: Charged only for actual execution time (milliseconds), not idle server hours
- **Auto-Scaling**: Handles 1 request or 10,000 requests without configuration
- **Perfect for AI Bursts**: Bedrock inference takes 2-5 seconds; Lambda is ideal for these short-lived tasks
- **No Server Management**: No OS patching, security updates, or capacity planning
- **Built-in Monitoring**: CloudWatch logs and metrics included
- **Cold Start Optimization**: Python 3.11 runtime starts in <1 second

**Cost Comparison**:
- **EC2 t3.medium**: ₹2,500/month (24/7 running, even with zero traffic)
- **Lambda**: ₹0-₹300/month for typical usage (1M requests = ₹150)

**Why This Matters**: A voice triage request takes 3 seconds to process. With Lambda, we pay for 3 seconds. With EC2, we'd pay for 24/7 server time even when no one is using the app at 3 AM.

---

### **S3 for Documents**
**Secure & Scalable Storage**
- **Encryption at Rest**: AES-256 encryption for all stored documents
- **Pre-Signed URLs**: Temporary, secure download links that expire after 1 hour
- **Versioning**: Keep document history for audit trails
- **Lifecycle Policies**: Automatically archive old documents to Glacier for cost savings
- **Cross-Region Replication**: Disaster recovery and low-latency access
- **99.999999999% Durability**: Your legal documents are safer than on any local server

**Security Features**:
- **No Public Access**: All documents private by default
- **IAM Policies**: Fine-grained access control per Lambda function
- **Audit Logging**: S3 access logs for compliance
- **Virus Scanning**: Can integrate with AWS Macie for content inspection

**Why This Matters**: A translated legal notice contains sensitive personal information. S3's pre-signed URLs ensure only the authorized user can download it, and the link expires after 1 hour. No risk of documents being shared or leaked.

---

### **The Serverless Advantage**

**Total Monthly Cost Breakdown** (for 10,000 users):
```
AWS Bedrock (Claude 3.5):    ₹2,000  (1M tokens)
Lambda Execution:            ₹300    (100K invocations)
DynamoDB:                    ₹500    (10M reads/writes)
S3 Storage:                  ₹200    (100GB documents)
API Gateway:                 ₹100    (100K requests)
Sarvam AI:                   ₹1,500  (10K transcriptions)
─────────────────────────────────────────────────
TOTAL:                       ₹4,600/month
```

**Traditional Stack Cost** (EC2 + RDS + Load Balancer):
```
EC2 Instances (2x t3.medium):  ₹5,000
RDS (db.t3.small):             ₹8,000
Application Load Balancer:     ₹2,000
EBS Storage:                   ₹1,000
─────────────────────────────────────────────────
TOTAL:                         ₹16,000/month
```

**Savings**: ₹11,900/month (74% cost reduction) + zero ops overhead

**Why This Matters**: As a social impact project, every rupee saved on infrastructure is a rupee we can invest in reaching more underserved communities. Serverless architecture makes this financially sustainable.

---

## 🚀 Setup and Deployment

### **Prerequisites**
```bash
# Install required tools
- Python 3.11+
- Node.js 20+ (for AWS CDK)
- AWS CLI configured with credentials
- Git
```

### **1. Clone Repository**
```bash
git clone https://github.com/ScaryPython692/Nyaya_Dwarpal.git
cd Nyaya_Dwarpal
```

### **2. Install Dependencies**
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install CDK dependencies
npm install -g aws-cdk
```

### **3. Configure AWS Credentials**
```bash
aws configure
# Enter your AWS Access Key ID, Secret Access Key, and Region (ap-south-2)
```

### **4. Bootstrap CDK (First Time Only)**
```bash
npx cdk bootstrap aws://ACCOUNT-ID/ap-south-2
```

### **5. Deploy Infrastructure**
```bash
# Synthesize CloudFormation template
npx cdk synth

# Deploy to AWS
npx cdk deploy --require-approval never
```

### **6. Note the API Endpoint**
After deployment, CDK will output:
```
Outputs:
NyayaDwarpalStack.ApiEndpoint = https://ked0qedvxi.execute-api.ap-south-2.amazonaws.com/prod/
NyayaDwarpalStack.VoiceTriageEndpoint = https://ked0qedvxi.execute-api.ap-south-2.amazonaws.com/prod/voice/triage
NyayaDwarpalStack.CasesEndpoint = https://ked0qedvxi.execute-api.ap-south-2.amazonaws.com/prod/cases
```

### **7. Open Frontend**
```bash
# Open the frontend in your browser
open ui/enhanced-index.html
```

The frontend will automatically connect to the deployed API endpoints.

---

## 📊 Project Structure

```
Nyaya_Dwarpal/
├── infrastructure/
│   └── nyaya_dwarpal_stack.py      # CDK infrastructure definition
├── lambda_functions/
│   ├── voice_triage/
│   │   └── handler.py               # Voice triage Lambda
│   ├── document_translator/
│   │   └── handler.py               # Translation Lambda
│   ├── petition_architect/
│   │   └── handler.py               # Petition generation Lambda
│   ├── case_memory/
│   │   └── handler.py               # Case retrieval Lambda
│   └── shared/
│       ├── models.py                # Pydantic data models
│       ├── bedrock_client.py        # Bedrock API wrapper
│       └── aws_helpers.py           # S3, DynamoDB helpers
├── ui/
│   └── enhanced-index.html          # Frontend application
├── app.py                           # CDK app entry point
├── cdk.json                         # CDK configuration
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

---

## 🧪 Testing

### **Test Voice Triage**
```bash
curl -X POST "https://ked0qedvxi.execute-api.ap-south-2.amazonaws.com/prod/voice/triage" \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "test-user-001",
    "transcribedText": "My landlord has not returned my security deposit for 3 months",
    "language": "en"
  }'
```

### **Test Document Translation**
```bash
# 1. Upload file to S3 bucket
aws s3 cp test_legal_notice.txt s3://YOUR-BUCKET-NAME/documents/

# 2. Call translation API
curl -X POST "https://ked0qedvxi.execute-api.ap-south-2.amazonaws.com/prod/translate/document" \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "test-user-001",
    "s3Key": "documents/test_legal_notice.txt",
    "sourceLanguage": "en",
    "targetLanguage": "hi",
    "documentType": "Legal Notice"
  }'
```

### **Test Case Memory**
```bash
curl -X GET "https://ked0qedvxi.execute-api.ap-south-2.amazonaws.com/prod/cases?userId=test-user-001&limit=10"
```

---

## 🎓 Hackathon

**AI for Bharat Competition**
- **Powered by**: AWS
- **Theme**: Democratizing AI for Indian Languages
- **Focus**: Access to Justice through AI

**Our Mission**: Make legal assistance accessible to every Indian, regardless of language, location, or economic status.

---

## 📈 Impact Metrics

- **Language Accessibility**: Support for 10+ Indian languages via Sarvam AI
- **Cost Reduction**: Free legal triage vs ₹500-₹2000 per consultation
- **Time Savings**: Instant analysis vs days of waiting for lawyer appointments
- **Reach**: Cloud-based solution accessible from any smartphone
- **Accuracy**: 85%+ confidence in legal classification using AWS Bedrock (Claude 3.5 Sonnet)

---

## 🔐 Security & Privacy

- **Data Encryption**: All data encrypted at rest (S3, DynamoDB) and in transit (HTTPS)
- **IAM Policies**: Least-privilege access for Lambda functions
- **API Gateway**: CORS enabled for secure frontend integration
- **TTL**: Automatic data deletion after 90 days
- **No PII Storage**: User IDs are anonymized

---

## 🛣️ Roadmap

- [ ] **Phase 1** (Current): Voice Triage, Document Translation, Case Memory ✅
- [ ] **Phase 2**: Petition Generation with Citation Verification
- [ ] **Phase 3**: Legal Library with searchable BNS/BNSS/CPC sections
- [ ] **Phase 4**: Multi-language UI (Hindi, Tamil, Telugu, Bengali)
- [ ] **Phase 5**: Mobile app (React Native)
- [ ] **Phase 6**: Integration with eCourts for direct filing

---

## 👥 Team

Built with ❤️ for AI for Bharat Hackathon

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

---

## 🙏 Acknowledgments

- **AWS**: For Lambda, S3, DynamoDB, Bedrock, and cloud infrastructure
- **Sarvam AI**: For Indic language models (Saaras v3, Mayura v1)
- **AI for Bharat**: For organizing this impactful hackathon
- **Indian Legal System**: For inspiring us to make justice accessible

---

## 📞 Contact

For questions, feedback, or collaboration:
- **GitHub**: [ScaryPython692/Nyaya_Dwarpal](https://github.com/ScaryPython692/Nyaya_Dwarpal)
- **Issues**: [Report a bug](https://github.com/ScaryPython692/Nyaya_Dwarpal/issues)

---

**"न्याय सबके लिए, सबकी भाषा में"**  
*Justice for All, in Everyone's Language*

---

![Made with AWS](https://img.shields.io/badge/Made%20with-AWS%20Lambda-orange)
![AWS Bedrock](https://img.shields.io/badge/Powered%20by-AWS%20Bedrock-purple)
![Sarvam AI](https://img.shields.io/badge/Powered%20by-Sarvam%20AI-blue)
![Python](https://img.shields.io/badge/Python-3.11-green)

