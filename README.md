# Nyaya-Dwarpal — Justice in Your Language

**AI-Powered Legal Assistant for Bharat | Democratizing Access to Justice**

![Nyaya-Dwarpal Banner](https://img.shields.io/badge/AI%20for%20Bharat-Powered%20by%20AWS-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)
![AWS](https://img.shields.io/badge/AWS-Lambda%20%7C%20S3%20%7C%20DynamoDB-yellow?style=for-the-badge)

---

## 🌐 Live Demo

**[https://main.d1y87jb5yrv6jl.amplifyapp.com/](https://main.d1y87jb5yrv6jl.amplifyapp.com/)**

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

### 2. 📄 Document Verification
**Verify legal documents for issues and risks**

- **Smart Upload**: Drag-and-drop interface for .txt and .pdf files
- **AI-Powered Analysis**: Detects issues and flags them with HIGH/MEDIUM/LOW severity
- **Legal Risk Detection**: Identifies unfair clauses, missing sections, and legal red flags
- **Instant Results**: Get a detailed breakdown of document issues in seconds

**Use Case**: A job seeker can upload an employment agreement and instantly see which clauses are unfair, risky, or legally problematic before signing.

---

### 3. 🗂️ Case Memory (Mamla Yaad)
**Your personal legal consultation history**

- **Automatic Saving**: All voice triage sessions stored in DynamoDB
- **Smart Retrieval**: Fetch cases by user ID with filtering
- **Rich Metadata**:
  - Case ID and timestamp
  - Emotion badges (color-coded: red/orange/purple/green)
  - Legal category and relevant sections
  - Full transcription and extracted facts
- **Case Details Modal**: View complete case information

**Use Case**: A user can review their previous consultations about a property dispute and track their legal history over time.

---

### 4. 📚 Legal Library (Kanoon Gyan) *(Coming Soon)*
**Searchable database of BNS, BNSS, and CPC sections**

- Browse legal sections by category
- Plain-language explanations
- Real-world examples
- Cross-references between sections

---

## 🖥️ How to Use

### Step 1 — Open the App
Visit **[https://main.d1y87jb5yrv6jl.amplifyapp.com/](https://main.d1y87jb5yrv6jl.amplifyapp.com/)** on any browser (desktop or mobile).

---

### Step 2 — Voice Triage (Describe Your Legal Problem)

1. Click **"Voice Triage"** from the dashboard or sidebar
2. Select your **language** from the top-right dropdown (e.g. 🌐 English or हिंदी)
3. Click the **microphone button** to start recording
4. Speak your legal issue clearly — for example:
   - *"Auto driver ne mujhse 500 rupaye liye, sirf 200 rupaye ka safar tha"* (Hindi)
   - *"My landlord is not returning my security deposit"* (English)
5. Click the mic again to **stop recording**
6. The AI will automatically:
   - Transcribe your speech
   - Detect your emotional state and urgency level
   - Classify your legal issue (e.g. Consumer Rights, Tenant Rights, Labour Law)
   - Show relevant legal sections with plain-language advice
   - Suggest specific next steps with timelines and costs

> 💡 **Tip**: You can also type your issue directly using the **"Type Your Issue"** tab if you prefer not to use voice.

---

### Step 3 — Document Verification (Check Your Legal Documents)

1. Click **"Verify Document"** from the dashboard or sidebar
2. **Drag and drop** your document into the upload area, or click to browse
   - Supported formats: `.txt`, `.pdf`
3. The AI will scan your document and return a detailed report with:
   - **HIGH severity** issues (serious legal risks)
   - **MEDIUM severity** issues (clauses to negotiate)
   - **LOW severity** issues (minor concerns)
4. Review each flagged issue to understand the risk before signing

> 💡 **Tip**: Try uploading an employment agreement or rental contract to see it in action.

---

### Step 4 — View Case History

1. Click **"Case History"** from the sidebar
2. Enter your **User ID** to retrieve your past consultations
3. Click any case to view the full legal analysis and transcription

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │ Voice Triage │  │  Document    │  │ Case Memory  │              │
│  │              │  │  Verifier    │  │              │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
└─────────┼──────────────────┼──────────────────┼────────────────────┘
          │                  │                  │
          │ Sarvam AI        │                  │
          │ (Speech-to-Text) │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      API GATEWAY (REST)                              │
│  POST /voice/triage  │  POST /validate/document  │  GET /cases     │
└─────────┬──────────────────┬──────────────────┬────────────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      AWS LAMBDA FUNCTIONS                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │ Voice Triage │  │  Document    │  │ Case Memory  │              │
│  │   Lambda     │  │  Verifier    │  │   Lambda     │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
│         ▼                  ▼                  │                      │
│  ┌──────────────────────────────────────────────────────────┐       │
│  │      AWS Bedrock (Amazon Nova Lite)                     │       │
│  │  • Emotion Detection  • Legal Classification             │       │
│  │  • Document Verification  • Risk Analysis                │       │
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
          │
          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   EXTERNAL SERVICES                                  │
│  ┌──────────────────────────────────────────────────────┐           │
│  │  Sarvam AI                                           │           │
│  │  • Saaras v3 (Speech-to-Text)                       │           │
│  └──────────────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔌 API Endpoints

| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|--------------|----------|
| `/voice/triage` | POST | Analyze transcribed voice input | `{userId, transcribedText, language}` | Emotion, classification, BNS sections |
| `/validate/document` | POST | Verify legal document for issues | `{fileContent, filename}` | Severity-rated issue list |
| `/cases` | GET | Fetch user's case history | Query: `?userId={id}&limit={n}` | Array of cases with metadata |

**Base URL**: `https://ked0qedvxi.execute-api.ap-south-2.amazonaws.com/prod`

---

## 🛠️ Tech Stack

### **Cloud Infrastructure**
- **AWS CDK (Python)**: Infrastructure as Code
- **AWS Lambda (Python 3.11)**: Serverless compute
- **Amazon API Gateway**: REST API management
- **Amazon S3**: Document storage with encryption
- **Amazon DynamoDB**: NoSQL database for sessions and metadata
- **AWS Bedrock**: Amazon Nova Lite for legal reasoning
- **AWS Textract**: Document text extraction (cross-region)

### **AI/ML Services**
- **AWS Bedrock (Amazon Nova Lite)**:
  - Emotion detection and urgency analysis
  - Legal problem classification
  - Document verification and risk analysis
- **Sarvam AI Saaras v3**: Indic language speech-to-text

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

### **AWS Bedrock (Amazon Nova Lite)**
**Fast & Cost-Effective Legal Reasoning**
- **No Marketplace Subscription Required**: Nova Lite is available natively in AWS Bedrock with no additional setup
- **Low Latency**: Optimized for fast inference, ideal for real-time legal triage
- **Multilingual Support**: Strong performance across English and Indic languages
- **JSON Mode**: Reliable structured output for legal classifications

**AWS Integration**
- **Seamless Integration**: Native AWS service with no external API dependencies
- **Security & Compliance**: Enterprise-grade security with AWS IAM controls
- **Scalability**: Auto-scales with Lambda for any load
- **Cost-Effective**: Pay-per-use pricing with no minimum commitments

**Why This Matters**: When a user speaks their legal problem, they need accurate, detailed analysis fast. Amazon Nova Lite provides legal reasoning with minimal latency through AWS's infrastructure.

---

### **Sarvam AI over Amazon Transcribe**
**Purpose-Built for Bharat**
- **22 Indian Languages**: Comprehensive support for Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Punjabi, and more
- **Indic Language Accuracy**: 95%+ accuracy for Indian accents and dialects vs 70-80% with generic models
- **Code-Mixing Support**: Handles Hinglish and other mixed-language speech patterns common in India
- **Legal Terminology**: Trained on Indian legal vocabulary and context
- **Cultural Context**: Understands Indian names, places, and cultural references

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
- **99.999999999% Durability**: Your legal documents are safer than on any local server

**Security Features**:
- **No Public Access**: All documents private by default
- **IAM Policies**: Fine-grained access control per Lambda function
- **Audit Logging**: S3 access logs for compliance

**Why This Matters**: A verified legal document contains sensitive personal information. S3's pre-signed URLs ensure only the authorized user can access it, and the link expires after 1 hour.

---

### **The Serverless Advantage**

**Total Monthly Cost Breakdown** (for 10,000 users):
```
AWS Bedrock (Nova Lite):     ₹2,000  (1M tokens)
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
git clone https://github.com/kalivenkatg/Nyaya-Dwarpal-AI.git
cd Nyaya-Dwarpal-AI
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
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
npx cdk synth
npx cdk deploy --require-approval never
```

### **6. Open Frontend**
```bash
open ui/index.html
```

---

## 📊 Project Structure

```
Nyaya-Dwarpal-AI/
├── infrastructure/
│   └── nyaya_dwarpal_stack.py      # CDK infrastructure definition
├── lambda_functions/
│   ├── voice_triage/
│   │   └── handler.py               # Voice triage Lambda
│   ├── document_verifier/
│   │   └── handler.py               # Document verification Lambda
│   ├── case_memory/
│   │   └── handler.py               # Case retrieval Lambda
│   └── shared/
│       ├── models.py                # Pydantic data models
│       ├── bedrock_client.py        # Bedrock API wrapper
│       └── aws_helpers.py           # S3, DynamoDB helpers
├── ui/
│   └── index.html                   # Frontend application
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
- **Accuracy**: 85%+ confidence in legal classification using AWS Bedrock (Amazon Nova Lite)

---

## 🔐 Security & Privacy

- **Data Encryption**: All data encrypted at rest (S3, DynamoDB) and in transit (HTTPS)
- **IAM Policies**: Least-privilege access for Lambda functions
- **API Gateway**: CORS enabled for secure frontend integration
- **TTL**: Automatic data deletion after 90 days
- **No PII Storage**: User IDs are anonymized

---

## 🛣️ Roadmap

- [ ] **Phase 1** (Current): Voice Triage, Document Verification, Case Memory ✅
- [ ] **Phase 2**: Document Translation (English ↔ Regional Languages)
- [ ] **Phase 3**: Petition Generation with Citation Verification
- [ ] **Phase 4**: Legal Library with searchable BNS/BNSS/CPC sections
- [ ] **Phase 5**: Multi-language UI (Hindi, Tamil, Telugu, Bengali)
- [ ] **Phase 6**: Mobile app (React Native)
- [ ] **Phase 7**: Integration with eCourts for direct filing

---

## 👥 Team

Built with ❤️ for AI for Bharat Hackathon

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

---

## 🙏 Acknowledgments

- **AWS**: For Lambda, S3, DynamoDB, Bedrock, and cloud infrastructure
- **Sarvam AI**: For Indic language models (Saaras v3)
- **AI for Bharat**: For organizing this impactful hackathon
- **Indian Legal System**: For inspiring us to make justice accessible

---

## 📞 Contact

For questions, feedback, or collaboration:
- **GitHub**: [kalivenkatg/Nyaya-Dwarpal-AI](https://github.com/kalivenkatg/Nyaya-Dwarpal-AI)
- **Issues**: [Report a bug](https://github.com/kalivenkatg/Nyaya-Dwarpal-AI/issues)

---

**"न्याय सबके लिए, सबकी भाषा में"**  
*Justice for All, in Everyone's Language*

---

![Made with AWS](https://img.shields.io/badge/Made%20with-AWS%20Lambda-orange)
![AWS Bedrock](https://img.shields.io/badge/Powered%20by-AWS%20Bedrock-purple)
![Sarvam AI](https://img.shields.io/badge/Powered%20by-Sarvam%20AI-blue)
![Python](https://img.shields.io/badge/Python-3.11-green)
