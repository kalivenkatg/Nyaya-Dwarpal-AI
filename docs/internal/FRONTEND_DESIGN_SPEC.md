# Nyaya-Dwarpal Frontend Design Specification

**Project**: Justice Guardian - Legal-Tech Dashboard  
**Target**: Indian citizens navigating the Bharatiya Nyaya Sanhita (BNS) system  
**Tech Stack**: React + Tailwind CSS + AWS Amplify

---

## 1. Visual Identity

### Color Palette
```css
/* Primary Colors */
--nyaya-blue: #1A237E;        /* Deep Navy - Primary brand color */
--evidence-white: #FFFFFF;     /* Pure white - Background */
--justice-gold: #C5A059;       /* Gold - Highlights and accents */

/* Secondary Colors */
--nyaya-blue-light: #3949AB;   /* Lighter blue for hover states */
--nyaya-blue-dark: #0D1642;    /* Darker blue for headers */
--gray-50: #F9FAFB;            /* Light gray backgrounds */
--gray-100: #F3F4F6;           /* Card backgrounds */
--gray-200: #E5E7EB;           /* Borders */
--gray-600: #4B5563;           /* Secondary text */
--gray-900: #111827;           /* Primary text */

/* Status Colors */
--success-green: #10B981;      /* Success states */
--warning-amber: #F59E0B;      /* Warning states */
--error-red: #EF4444;          /* Error states */
--info-blue: #3B82F6;          /* Info states */

/* Emotion Colors */
--emotion-angry: #DC2626;      /* Angry emotion indicator */
--emotion-distressed: #F97316; /* Distressed emotion indicator */
--emotion-confused: #8B5CF6;   /* Confused emotion indicator */
--emotion-calm: #059669;       /* Calm emotion indicator */
```

### Typography
```css
/* Font Family */
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

/* Font Sizes */
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */

/* Font Weights */
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

---

## 2. Layout Structure

### Global Navigation (Sidebar)
**Width**: 280px (desktop), Full-width drawer (mobile)  
**Position**: Fixed left  
**Background**: Nyaya Blue (#1A237E)

**Navigation Items**:
1. 🏠 Dashboard
2. ✍️ New Petition
3. 🎤 Voice Triage
4. 📁 Case Memory
5. 📚 Legal Library
6. ⚙️ Settings

### Main Content Area
**Layout**: Flex container with responsive padding  
**Max Width**: 1440px  
**Padding**: 24px (mobile), 32px (tablet), 48px (desktop)

### Header Bar
**Height**: 64px  
**Background**: Evidence White with shadow  
**Contents**: 
- Page title (left)
- Language toggle (center-right)
- Accessibility toggle (right)
- User profile (far right)

---

## 3. Core Components

### 3.1 Voice Triage Interface

#### Microphone Button (Idle State)
```
Size: 120px × 120px
Shape: Circle
Background: Gradient (Nyaya Blue → Nyaya Blue Light)
Icon: Microphone (48px)
Animation: Subtle pulse (scale 1.0 → 1.05, 2s loop)
Shadow: 0 10px 40px rgba(26, 35, 126, 0.3)
```

#### Microphone Button (Active State)
```
Size: Expands to 300px × 200px
Shape: Rounded rectangle
Background: Nyaya Blue with waveform overlay
Animation: Audio waveform visualization
Text: "Listening..." (below waveform)
Action: Click to stop recording
```

#### Triage Results Card
```
Layout: Grid (2 columns on desktop, 1 on mobile)
Sections:
  - Emotion Badge (top-left)
  - Urgency Indicator (top-right)
  - Legal Category (center)
  - Relevant Sections (bottom, scrollable)
  - Extracted Facts (expandable accordion)
```

### 3.2 Petition Architect Workspace

#### Split-Screen Layout
```
Desktop: 50/50 split
Tablet: 60/40 split
Mobile: Stacked (upload top, draft bottom)
```

#### Left Panel: File Upload Zone
```
Height: 400px (min)
Border: 2px dashed Gray-200
Background: Gray-50
Hover: Border → Justice Gold, Background → Gray-100
States:
  - Empty: "Drag & drop or click to upload"
  - Uploading: Progress bar with percentage
  - Uploaded: File preview with remove button
Accepted: .txt, .pdf (max 10MB)
```

#### Right Panel: Drafting Area
```
Background: Evidence White
Border: 1px solid Gray-200
Padding: 24px
Font: Monospace for legal text
Features:
  - Real-time text streaming
  - Copy to clipboard button
  - Download as PDF button
  - Edit mode toggle
```

### 3.3 BNS Intelligence Sidebar

#### Slide-out Panel
```
Width: 400px
Position: Fixed right
Background: Evidence White
Shadow: -4px 0 24px rgba(0, 0, 0, 0.1)
Animation: Slide in from right (300ms ease-out)
```

#### Legal Section Card
```
Layout: Vertical stack
Components:
  - Section number badge (Justice Gold)
  - Section title (Bold, Nyaya Blue)
  - Plain-language explanation (Gray-600)
  - "Learn More" link
  - Relevance score (0-100%)
```

### 3.4 Case Memory Grid

#### Card Layout
```
Grid: 3 columns (desktop), 2 (tablet), 1 (mobile)
Gap: 24px
Card Height: 280px
```

#### Case Card Structure
```
Header:
  - User ID badge (top-left)
  - Date (top-right)
Body:
  - Emotion indicator (colored dot + label)
  - Case summary (2 lines, truncated)
  - Legal category badge
Footer:
  - "View Draft" button (primary)
  - "Continue" button (secondary)
```

---

## 4. Interactive Elements

### 4.1 Buttons

#### Primary Button
```css
background: var(--nyaya-blue);
color: var(--evidence-white);
padding: 12px 24px;
border-radius: 8px;
font-weight: 600;
transition: all 200ms;
hover: background: var(--nyaya-blue-light);
active: transform: scale(0.98);
```

#### Secondary Button
```css
background: transparent;
color: var(--nyaya-blue);
border: 2px solid var(--nyaya-blue);
padding: 12px 24px;
border-radius: 8px;
font-weight: 600;
hover: background: var(--nyaya-blue), color: white;
```

#### Icon Button
```css
size: 40px × 40px;
border-radius: 50%;
background: var(--gray-100);
hover: background: var(--gray-200);
```

### 4.2 Form Inputs

#### Text Input
```css
height: 48px;
padding: 12px 16px;
border: 2px solid var(--gray-200);
border-radius: 8px;
focus: border-color: var(--nyaya-blue), outline: none;
```

#### Textarea
```css
min-height: 120px;
padding: 12px 16px;
border: 2px solid var(--gray-200);
border-radius: 8px;
resize: vertical;
```

### 4.3 Loading States

#### Skeleton Loader
```css
background: linear-gradient(90deg, #F3F4F6 25%, #E5E7EB 50%, #F3F4F6 75%);
animation: shimmer 1.5s infinite;
border-radius: 8px;
```

#### Spinner
```css
size: 24px × 24px;
border: 3px solid var(--gray-200);
border-top-color: var(--nyaya-blue);
border-radius: 50%;
animation: spin 1s linear infinite;
```

---

## 5. Accessibility Features

### High Contrast Mode
```
Toggle in header
Increases contrast ratios to WCAG AAA standards
Changes:
  - Text: Gray-600 → Gray-900
  - Borders: Gray-200 → Gray-400
  - Backgrounds: Enhanced contrast
```

### Multi-Language Support
```
Languages: English, Hindi (हिंदी)
Toggle: Dropdown in header
Persists: localStorage
Affects: All UI text, not legal content
```

### Keyboard Navigation
```
Tab order: Logical flow
Focus indicators: 2px solid Justice Gold outline
Skip links: "Skip to main content"
ARIA labels: All interactive elements
```

### Screen Reader Support
```
Semantic HTML: <nav>, <main>, <article>, <aside>
ARIA roles: Proper role attributes
Live regions: For dynamic content updates
Alt text: All images and icons
```

---

## 6. Responsive Breakpoints

```css
/* Mobile First Approach */
--mobile: 0px;        /* 0-639px */
--tablet: 640px;      /* 640-1023px */
--desktop: 1024px;    /* 1024-1279px */
--wide: 1280px;       /* 1280px+ */

/* Usage */
@media (min-width: 640px) { /* Tablet */ }
@media (min-width: 1024px) { /* Desktop */ }
@media (min-width: 1280px) { /* Wide */ }
```

---

## 7. Animation Guidelines

### Timing Functions
```css
--ease-in: cubic-bezier(0.4, 0, 1, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
```

### Duration Standards
```css
--duration-fast: 150ms;    /* Micro-interactions */
--duration-base: 200ms;    /* Standard transitions */
--duration-slow: 300ms;    /* Complex animations */
--duration-slower: 500ms;  /* Page transitions */
```

### Common Animations
```css
/* Fade In */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Slide Up */
@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

/* Pulse */
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}
```

---

## 8. Component States

### Loading States
```
- Skeleton loaders for content
- Spinners for actions
- Progress bars for uploads
- Disabled state for buttons
```

### Empty States
```
- Illustration + message
- Call-to-action button
- Helpful tips or guidance
```

### Error States
```
- Error icon (red)
- Error message (clear, actionable)
- Retry button
- Support link
```

### Success States
```
- Success icon (green)
- Success message
- Next action button
- Confetti animation (optional)
```

---

## 9. API Integration Points

### Voice Triage
```
POST /voice/triage
Loading: Show waveform animation
Success: Display triage results card
Error: Show error message with retry
```

### Petition Generation
```
POST /petition/generate
Loading: Show "Drafting..." with progress
Success: Stream text to drafting area
Error: Show error with "Try Again"
```

### File Upload (S3)
```
Upload to S3 bucket
Loading: Progress bar (0-100%)
Success: Show file preview
Error: Show upload failed message
```

### Case History (DynamoDB)
```
GET from DynamoDB
Loading: Skeleton cards
Success: Populate case grid
Error: Show "Unable to load cases"
```

---

## 10. Mobile Considerations

### Touch Targets
```
Minimum size: 44px × 44px
Spacing: 8px between targets
```

### Mobile Navigation
```
Hamburger menu (top-left)
Bottom navigation bar (optional)
Swipe gestures for panels
```

### Mobile Voice Recording
```
Larger microphone button (160px)
Full-screen recording interface
Haptic feedback on start/stop
```

### Mobile Petition Drafting
```
Stacked layout (not split-screen)
Sticky action buttons at bottom
Collapsible sections
```

---

## 11. Performance Targets

```
First Contentful Paint: < 1.5s
Time to Interactive: < 3.5s
Largest Contentful Paint: < 2.5s
Cumulative Layout Shift: < 0.1
First Input Delay: < 100ms
```

---

## 12. Browser Support

```
Chrome: Last 2 versions
Firefox: Last 2 versions
Safari: Last 2 versions
Edge: Last 2 versions
Mobile Safari: iOS 13+
Chrome Mobile: Android 8+
```
