# Nyaya-Dwarpal Frontend Implementation Guide

## Created Components

### ✅ Layout Components
1. **Sidebar.jsx** - Fixed sidebar navigation with logo and menu items
2. **Header.jsx** - Top header with menu toggle, language/contrast toggles, and user profile
3. **MainLayout.jsx** - Wrapper component combining sidebar and header

### ✅ Voice Triage Components
1. **MicrophoneButton.jsx** - Animated microphone button with pulse effect
2. **WaveformVisualizer.jsx** - Canvas-based audio waveform visualization
3. **TriageResultsCard.jsx** - Comprehensive results display with emotion, classification, and legal sections

### ✅ Styling
1. **tailwind.config.js** - Custom theme with Nyaya-Dwarpal colors and animations
2. **globals.css** - Base styles, custom scrollbar, skeleton loaders, and utilities

---

## Remaining Components to Implement

### Petition Components
```jsx
// frontend/src/components/petition/FileUploadZone.jsx
- Drag-and-drop file upload
- Progress bar for S3 uploads
- File preview with remove button
- Accepted formats: .txt, .pdf (max 10MB)

// frontend/src/components/petition/DraftingArea.jsx
- Real-time text streaming display
- Copy to clipboard button
- Download as PDF button
- Edit mode toggle

// frontend/src/components/petition/PetitionWorkspace.jsx
- Split-screen layout (50/50 on desktop)
- Combines FileUploadZone and DraftingArea
- Responsive stacking on mobile
```

### Legal Components
```jsx
// frontend/src/components/legal/BNSSidebar.jsx
- Slide-out panel from right
- Displays detected legal sections
- Animated entrance (300ms)

// frontend/src/components/legal/LegalSectionCard.jsx
- Section number badge (Justice Gold)
- Section title (Bold, Nyaya Blue)
- Plain-language explanation
- Relevance score indicator

// frontend/src/components/legal/SectionBadge.jsx
- Reusable badge for section numbers
- Color-coded by act type (BNS, CPC, IPC)
```

### Case Memory Components
```jsx
// frontend/src/components/case/CaseMemoryGrid.jsx
- Responsive grid (3 cols desktop, 2 tablet, 1 mobile)
- Skeleton loaders while fetching
- Empty state when no cases

// frontend/src/components/case/CaseCard.jsx
- User ID badge
- Date display
- Emotion indicator
- Case summary (2 lines truncated)
- Legal category badge
- "View Draft" and "Continue" buttons

// frontend/src/components/case/EmotionIndicator.jsx
- Colored dot based on emotion
- Emotion label
- Confidence percentage
```

### Common Components
```jsx
// frontend/src/components/common/Button.jsx
- Primary, secondary, and icon variants
- Loading state with spinner
- Disabled state
- Size variants (sm, md, lg)

// frontend/src/components/common/Input.jsx
- Text input with label
- Error state with message
- Helper text
- Icon support

// frontend/src/components/common/Card.jsx
- Reusable card container
- Variants: default, elevated, bordered
- Padding options

// frontend/src/components/common/Badge.jsx
- Color variants: primary, success, warning, error, info
- Size variants: sm, md, lg
- Rounded or pill shape

// frontend/src/components/common/Spinner.jsx
- Loading spinner
- Size variants
- Color customization

// frontend/src/components/common/SkeletonLoader.jsx
- Shimmer animation
- Various shapes (text, circle, rectangle)
- Customizable dimensions

// frontend/src/components/common/EmptyState.jsx
- Illustration or icon
- Message text
- Call-to-action button
- Helpful tips
```

### Accessibility Components
```jsx
// frontend/src/components/accessibility/LanguageToggle.jsx
- Dropdown with English and Hindi options
- Persists to localStorage
- Updates UI text (not legal content)

// frontend/src/components/accessibility/ContrastToggle.jsx
- Toggle button for high contrast mode
- Adds 'high-contrast' class to body
- Persists to localStorage
- Icon changes based on state
```

---

## Pages to Implement

### Dashboard Page
```jsx
// frontend/src/pages/Dashboard.jsx
- Welcome message
- Quick stats (total cases, pending petitions)
- Recent activity feed
- Quick action buttons (New Petition, Voice Triage)
```

### Voice Triage Page
```jsx
// frontend/src/pages/VoiceTriage.jsx
- Centered MicrophoneButton
- TriageResultsCard (shown after recording)
- Instructions panel
- Language selector
```

### New Petition Page
```jsx
// frontend/src/pages/NewPetition.jsx
- PetitionWorkspace component
- BNSSidebar (slide-out)
- Progress indicator
- Save draft functionality
```

### Case Memory Page
```jsx
// frontend/src/pages/CaseMemory.jsx
- CaseMemoryGrid component
- Search and filter controls
- Sort options (date, emotion, category)
- Pagination
```

### Legal Library Page
```jsx
// frontend/src/pages/LegalLibrary.jsx
- Searchable database of BNS sections
- Category filters
- Plain-language explanations
- Related sections
```

---

## Custom Hooks

### useVoiceRecording
```javascript
// frontend/src/hooks/useVoiceRecording.js
import { useState, useRef } from 'react';

export default function useVoiceRecording() {
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const mediaRecorderRef = useRef(null);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;

      const chunks = [];
      mediaRecorder.ondataavailable = (e) => chunks.push(e.data);
      mediaRecorder.onstop = () => {
        const blob = new Blob(chunks, { type: 'audio/webm' });
        setAudioBlob(blob);
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (error) {
      console.error('Error accessing microphone:', error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
      setIsRecording(false);
    }
  };

  return { isRecording, audioBlob, startRecording, stopRecording };
}
```

### useFileUpload
```javascript
// frontend/src/hooks/useFileUpload.js
import { useState } from 'react';
import { uploadToS3 } from '../services/s3Upload';

export default function useFileUpload() {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState(null);

  const upload = async (file) => {
    setUploading(true);
    setError(null);
    setProgress(0);

    try {
      const result = await uploadToS3(file, (progressEvent) => {
        const percentCompleted = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        );
        setProgress(percentCompleted);
      });

      setUploading(false);
      return result;
    } catch (err) {
      setError(err.message);
      setUploading(false);
      throw err;
    }
  };

  return { upload, uploading, progress, error };
}
```

### useAPI
```javascript
// frontend/src/hooks/useAPI.js
import { useState, useCallback } from 'react';
import api from '../services/api';

export default function useAPI() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const request = useCallback(async (endpoint, options = {}) => {
    setLoading(true);
    setError(null);

    try {
      const response = await api(endpoint, options);
      setLoading(false);
      return response;
    } catch (err) {
      setError(err.message);
      setLoading(false);
      throw err;
    }
  }, []);

  return { request, loading, error };
}
```

### useLanguage
```javascript
// frontend/src/hooks/useLanguage.js
import { useState, useEffect } from 'react';

const translations = {
  en: {
    dashboard: 'Dashboard',
    newPetition: 'New Petition',
    voiceTriage: 'Voice Triage',
    caseMemory: 'Case Memory',
    legalLibrary: 'Legal Library',
    // ... more translations
  },
  hi: {
    dashboard: 'डैशबोर्ड',
    newPetition: 'नई याचिका',
    voiceTriage: 'वॉयस ट्राइएज',
    caseMemory: 'केस मेमोरी',
    legalLibrary: 'कानूनी पुस्तकालय',
    // ... more translations
  },
};

export default function useLanguage() {
  const [language, setLanguage] = useState(
    localStorage.getItem('language') || 'en'
  );

  useEffect(() => {
    localStorage.setItem('language', language);
  }, [language]);

  const t = (key) => translations[language][key] || key;

  return { language, setLanguage, t };
}
```

---

## Services

### API Service
```javascript
// frontend/src/services/api.js
const API_BASE_URL = process.env.REACT_APP_API_ENDPOINT;

export default async function api(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const config = {
    method: options.method || 'GET',
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  if (options.body) {
    config.body = JSON.stringify(options.body);
  }

  const response = await fetch(url, config);
  
  if (!response.ok) {
    throw new Error(`API Error: ${response.statusText}`);
  }

  return response.json();
}

// Specific API calls
export const voiceTriage = (data) =>
  api('/voice/triage', { method: 'POST', body: data });

export const generatePetition = (data) =>
  api('/petition/generate', { method: 'POST', body: data });

export const clarifyPetition = (data) =>
  api('/petition/clarify', { method: 'POST', body: data });
```

### S3 Upload Service
```javascript
// frontend/src/services/s3Upload.js
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';

const s3Client = new S3Client({
  region: process.env.REACT_APP_AWS_REGION,
  credentials: {
    // Use AWS Amplify or Cognito for credentials
  },
});

export async function uploadToS3(file, onProgress) {
  const key = `uploads/${Date.now()}-${file.name}`;
  
  const command = new PutObjectCommand({
    Bucket: process.env.REACT_APP_S3_BUCKET,
    Key: key,
    Body: file,
    ContentType: file.type,
  });

  try {
    await s3Client.send(command);
    return { key, bucket: process.env.REACT_APP_S3_BUCKET };
  } catch (error) {
    console.error('S3 upload error:', error);
    throw error;
  }
}
```

---

## Installation & Setup

### 1. Create React App
```bash
npx create-react-app nyaya-dwarpal-frontend
cd nyaya-dwarpal-frontend
```

### 2. Install Dependencies
```bash
npm install \
  react-router-dom \
  @heroicons/react \
  @aws-sdk/client-s3 \
  tailwindcss \
  postcss \
  autoprefixer
```

### 3. Initialize Tailwind
```bash
npx tailwindcss init -p
```

### 4. Environment Variables
Create `.env`:
```
REACT_APP_API_ENDPOINT=https://ked0qedvxi.execute-api.ap-south-2.amazonaws.com/prod
REACT_APP_S3_BUCKET=nyayadwarpalstack-nyayadocbucketv24eb39526-yskr4fmijdf4
REACT_APP_AWS_REGION=ap-south-2
```

### 5. Copy Component Files
Copy all created component files to their respective directories in `src/`.

### 6. Run Development Server
```bash
npm start
```

---

## Deployment with AWS Amplify

### 1. Initialize Amplify
```bash
npm install -g @aws-amplify/cli
amplify init
```

### 2. Add Hosting
```bash
amplify add hosting
# Select: Hosting with Amplify Console
```

### 3. Deploy
```bash
amplify publish
```

---

## Testing Checklist

- [ ] Voice recording works on desktop and mobile
- [ ] File upload shows progress bar
- [ ] Triage results display correctly
- [ ] Sidebar navigation works
- [ ] Language toggle switches UI text
- [ ] High contrast mode increases contrast
- [ ] Responsive on mobile, tablet, desktop
- [ ] Keyboard navigation works
- [ ] Screen reader announces content
- [ ] Loading states show during API calls
- [ ] Error states display helpful messages
- [ ] Empty states show when no data

---

## Performance Optimization

1. **Code Splitting**: Use React.lazy() for route-based splitting
2. **Image Optimization**: Use WebP format with fallbacks
3. **Caching**: Implement service worker for offline support
4. **Bundle Size**: Analyze with webpack-bundle-analyzer
5. **Lazy Loading**: Load components only when needed

---

## Accessibility Compliance

- WCAG 2.1 Level AA compliance
- Keyboard navigation support
- Screen reader compatibility
- High contrast mode
- Focus indicators
- ARIA labels and roles
- Semantic HTML

---

## Next Steps

1. Implement remaining components (petition, legal, case memory)
2. Add authentication with AWS Cognito
3. Implement real-time updates with WebSockets
4. Add offline support with service workers
5. Create comprehensive test suite
6. Set up CI/CD pipeline
7. Performance monitoring with AWS CloudWatch RUM
8. User analytics with AWS Pinpoint
