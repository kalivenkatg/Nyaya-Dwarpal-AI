# How to Open the Nyaya-Dwarpal UI

## ✅ Method 1: Open Directly in Browser (Easiest!)

### On macOS:
```bash
open ui/enhanced-index.html
```

### On Windows:
```bash
start ui/enhanced-index.html
```

### On Linux:
```bash
xdg-open ui/enhanced-index.html
```

### Or Simply:
1. Navigate to your project folder in Finder/File Explorer
2. Go to the `ui` folder
3. Double-click `enhanced-index.html`
4. It will open in your default browser!

---

## ✅ Method 2: Using Python HTTP Server (Recommended for Testing)

This method is better because it serves the file over HTTP (some browser features work better this way):

```bash
# Navigate to the ui directory
cd ui

# Start a simple HTTP server (Python 3)
python3 -m http.server 8000

# Or if you have Python 2
python -m SimpleHTTPServer 8000
```

Then open your browser and go to:
```
http://localhost:8000/enhanced-index.html
```

Press `Ctrl+C` to stop the server when done.

---

## ✅ Method 3: Using VS Code Live Server

If you're using VS Code:

1. Install the "Live Server" extension by Ritwick Dey
2. Right-click on `ui/enhanced-index.html`
3. Select "Open with Live Server"
4. Your browser will open automatically!

---

## 🎨 What You'll See

When the UI opens, you'll see:

### **Nyaya-Dwarpal Interface**
- **Sidebar** (left): Navigation menu with:
  - Dashboard
  - New Petition
  - Voice Triage (active by default)
  - Case Memory
  - Legal Library

- **Main Area** (center): Voice Triage page with:
  - Large microphone button with pulsing gold ring
  - Document upload section below
  - Loading spinner when processing

- **BNS Intelligence Panel** (right): 
  - Slides in after voice analysis
  - Shows emotion, urgency, legal category
  - Displays relevant BNS sections

### **Color Scheme**
- **Nyaya Blue**: #1A237E (primary)
- **Justice Gold**: #C5A059 (accents)
- **Evidence White**: #FFFFFF (background)

---

## 🧪 Testing the Features

### 1. Test Voice Triage
1. Click the microphone button
2. Allow microphone access when prompted
3. Speak your legal issue (or it will use a demo fallback)
4. Watch the waveform animation
5. See results in the BNS Intelligence panel

### 2. Test Document Upload
1. Scroll down to "Or Upload Documents"
2. Drag and drop a .txt or .pdf file
3. Watch the upload progress bar
4. See translated text in the modal

### 3. Test Case Memory
1. Click "Case Memory" in the sidebar
2. See your saved cases with emotion badges
3. Click "View Details" on any case
4. See full transcription and legal sections

---

## 🔧 Troubleshooting

### Issue: Microphone doesn't work
**Solution**: 
- Make sure you're using HTTPS or localhost
- Grant microphone permissions in browser
- Check browser console for errors

### Issue: API calls fail
**Solution**:
- Check that your API Gateway is deployed
- Verify the API endpoint URL in the HTML file
- Check browser console for CORS errors

### Issue: Page looks broken
**Solution**:
- Make sure you're opening `enhanced-index.html` (not `index.html`)
- Check that Tailwind CSS CDN is loading
- Try hard refresh: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows)

### Issue: "File not found" error
**Solution**:
- Make sure you're in the project root directory
- Check that `ui/enhanced-index.html` exists
- Try the full path: `/Users/abhinavkumar/Desktop/nyaya-dwarpal/ui/enhanced-index.html`

---

## 📱 Mobile Testing

To test on mobile:

1. Start Python HTTP server (Method 2 above)
2. Find your computer's IP address:
   ```bash
   # On Mac/Linux
   ifconfig | grep "inet "
   
   # On Windows
   ipconfig
   ```
3. On your phone, open browser and go to:
   ```
   http://YOUR_IP_ADDRESS:8000/enhanced-index.html
   ```
   Example: `http://192.168.1.100:8000/enhanced-index.html`

---

## 🚀 Quick Start Command

Copy and paste this into your terminal:

```bash
cd /Users/abhinavkumar/Desktop/nyaya-dwarpal && open ui/enhanced-index.html
```

Or for HTTP server:

```bash
cd /Users/abhinavkumar/Desktop/nyaya-dwarpal/ui && python3 -m http.server 8000
```

Then open: http://localhost:8000/enhanced-index.html

---

## 🎥 Demo Flow for Judges

1. **Open UI** → Shows professional legal assistant interface
2. **Click Microphone** → Pulsing gold ring, waveform animation
3. **Speak Issue** → "My landlord hasn't returned my deposit"
4. **See Analysis** → BNS panel slides in with emotion, urgency, sections
5. **Upload Document** → Drag .txt file, see translation progress
6. **View Cases** → Click Case Memory, see color-coded emotion badges
7. **View Details** → Click any case, see full modal with all info

---

**Ready to impress the judges! 🎯**

**"न्याय सबके लिए, सबकी भाषा में"**  
*Justice for All, in Everyone's Language*
