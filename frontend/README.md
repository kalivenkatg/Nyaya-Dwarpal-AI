# Nyaya-Dwarpal Frontend

React + Tailwind CSS implementation for the Justice Guardian legal-tech dashboard.

## Project Structure

```
frontend/
├── public/
│   ├── index.html
│   └── assets/
│       ├── icons/
│       └── images/
├── src/
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Sidebar.jsx
│   │   │   ├── Header.jsx
│   │   │   └── MainLayout.jsx
│   │   ├── voice/
│   │   │   ├── MicrophoneButton.jsx
│   │   │   ├── WaveformVisualizer.jsx
│   │   │   └── TriageResultsCard.jsx
│   │   ├── petition/
│   │   │   ├── FileUploadZone.jsx
│   │   │   ├── DraftingArea.jsx
│   │   │   └── PetitionWorkspace.jsx
│   │   ├── legal/
│   │   │   ├── BNSSidebar.jsx
│   │   │   ├── LegalSectionCard.jsx
│   │   │   └── SectionBadge.jsx
│   │   ├── case/
│   │   │   ├── CaseMemoryGrid.jsx
│   │   │   ├── CaseCard.jsx
│   │   │   └── EmotionIndicator.jsx
│   │   ├── common/
│   │   │   ├── Button.jsx
│   │   │   ├── Input.jsx
│   │   │   ├── Card.jsx
│   │   │   ├── Badge.jsx
│   │   │   ├── Spinner.jsx
│   │   │   ├── SkeletonLoader.jsx
│   │   │   └── EmptyState.jsx
│   │   └── accessibility/
│   │       ├── LanguageToggle.jsx
│   │       └── ContrastToggle.jsx
│   ├── pages/
│   │   ├── Dashboard.jsx
│   │   ├── VoiceTriage.jsx
│   │   ├── NewPetition.jsx
│   │   ├── CaseMemory.jsx
│   │   └── LegalLibrary.jsx
│   ├── hooks/
│   │   ├── useVoiceRecording.js
│   │   ├── useFileUpload.js
│   │   ├── useAPI.js
│   │   └── useLanguage.js
│   ├── services/
│   │   ├── api.js
│   │   ├── s3Upload.js
│   │   └── dynamodb.js
│   ├── utils/
│   │   ├── constants.js
│   │   ├── helpers.js
│   │   └── validators.js
│   ├── styles/
│   │   ├── globals.css
│   │   └── tailwind.config.js
│   ├── App.jsx
│   └── index.js
├── package.json
└── README.md
```

## Installation

```bash
npm install
```

## Development

```bash
npm run dev
```

## Build

```bash
npm run build
```

## Environment Variables

Create a `.env` file:

```
REACT_APP_API_ENDPOINT=https://ked0qedvxi.execute-api.ap-south-2.amazonaws.com/prod
REACT_APP_S3_BUCKET=nyayadwarpalstack-nyayadocbucketv24eb39526-yskr4fmijdf4
REACT_APP_AWS_REGION=ap-south-2
```
