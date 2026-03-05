# AWS Amplify Deployment Guide for Nyaya-Dwarpal Frontend

## Option 1: Deploy via AWS Amplify Console (Recommended - Easiest)

### Step 1: Access AWS Amplify Console
1. Go to: https://console.aws.amazon.com/amplify/
2. Click **"New app"** → **"Host web app"**

### Step 2: Connect GitHub Repository
1. Select **"GitHub"** as the source
2. Authorize AWS Amplify to access your GitHub account
3. Select repository: **ScaryPython692/Nyaya_Dwarpal**
4. Select branch: **main**

### Step 3: Configure Build Settings
1. App name: `Nyaya-Dwarpal`
2. Build settings (use this configuration):

```yaml
version: 1
frontend:
  phases:
    build:
      commands:
        - cp ui/enhanced-index.html index.html
  artifacts:
    baseDirectory: /
    files:
      - index.html
```

3. Click **"Next"**

### Step 4: Review and Deploy
1. Review all settings
2. Click **"Save and deploy"**
3. Wait 2-3 minutes for deployment to complete

### Step 5: Get Your Live URL
After deployment completes, you'll see:
- **Live URL**: `https://main.xxxxxx.amplifyapp.com`
- This URL is publicly accessible and ready for judges!

---

## Option 2: Manual S3 Static Website Hosting (Alternative)

If you prefer S3 static hosting:

### Step 1: Create S3 Bucket
```bash
aws s3 mb s3://nyaya-dwarpal-frontend --region ap-south-2
```

### Step 2: Configure for Static Website
```bash
aws s3 website s3://nyaya-dwarpal-frontend --index-document index.html
```

### Step 3: Upload Frontend
```bash
cp ui/enhanced-index.html index.html
aws s3 cp index.html s3://nyaya-dwarpal-frontend/ --acl public-read
```

### Step 4: Set Bucket Policy
```bash
aws s3api put-bucket-policy --bucket nyaya-dwarpal-frontend --policy '{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "PublicReadGetObject",
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::nyaya-dwarpal-frontend/*"
  }]
}'
```

### Step 5: Access Your Site
Your site will be available at:
```
http://nyaya-dwarpal-frontend.s3-website.ap-south-2.amazonaws.com
```

---

## Option 3: Quick Deploy via AWS Console (No CLI Required)

### For S3 Static Website:

1. **Create S3 Bucket**:
   - Go to S3 Console: https://s3.console.aws.amazon.com/s3/
   - Click "Create bucket"
   - Name: `nyaya-dwarpal-frontend`
   - Region: `ap-south-2`
   - Uncheck "Block all public access"
   - Click "Create bucket"

2. **Upload File**:
   - Open the bucket
   - Click "Upload"
   - Rename `ui/enhanced-index.html` to `index.html`
   - Upload the file
   - Click "Upload"

3. **Enable Static Website Hosting**:
   - Go to bucket "Properties" tab
   - Scroll to "Static website hosting"
   - Click "Edit"
   - Enable "Static website hosting"
   - Index document: `index.html`
   - Click "Save changes"

4. **Set Permissions**:
   - Go to "Permissions" tab
   - Click "Bucket Policy"
   - Paste this policy:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Sid": "PublicReadGetObject",
         "Effect": "Allow",
         "Principal": "*",
         "Action": "s3:GetObject",
         "Resource": "arn:aws:s3:::nyaya-dwarpal-frontend/*"
       }
     ]
   }
   ```
   - Click "Save changes"

5. **Get Your URL**:
   - Go back to "Properties" tab
   - Scroll to "Static website hosting"
   - Copy the "Bucket website endpoint"
   - Example: `http://nyaya-dwarpal-frontend.s3-website.ap-south-2.amazonaws.com`

---

## Recommended: Use AWS Amplify Console

**Why Amplify?**
- ✅ Automatic HTTPS (SSL certificate)
- ✅ Global CDN (CloudFront)
- ✅ Custom domain support
- ✅ Continuous deployment from GitHub
- ✅ Free tier: 1000 build minutes/month, 15 GB served/month
- ✅ Professional URL: `https://main.xxxxxx.amplifyapp.com`

**Why not S3 alone?**
- ❌ No HTTPS by default (only HTTP)
- ❌ No CDN (slower for global users)
- ❌ Less professional URL

---

## After Deployment

### Update README.md with Live URL

Add this section to your README.md:

```markdown
## 🌐 Live Demo

**Frontend Application**: [https://main.xxxxxx.amplifyapp.com](https://main.xxxxxx.amplifyapp.com)

Try the live demo:
1. Click the microphone button to record your legal issue
2. Upload a document for translation
3. View your case history in Case Memory
4. Generate legal petitions with AI assistance

**API Endpoint**: https://ked0qedvxi.execute-api.ap-south-2.amazonaws.com/prod
```

---

## Troubleshooting

### Issue: Amplify build fails
**Solution**: Make sure the `amplify.yml` build spec is correct:
```yaml
version: 1
frontend:
  phases:
    build:
      commands:
        - cp ui/enhanced-index.html index.html
  artifacts:
    baseDirectory: /
    files:
      - index.html
```

### Issue: S3 website shows 403 Forbidden
**Solution**: 
1. Check bucket policy allows public read
2. Verify "Block public access" is disabled
3. Ensure file is named `index.html`

### Issue: API calls fail from frontend
**Solution**: 
1. Check CORS is enabled on API Gateway
2. Verify API endpoint URL in `enhanced-index.html`
3. Check browser console for errors

---

## Cost Estimate

### AWS Amplify Hosting
- **Free Tier**: 1000 build minutes/month, 15 GB served/month
- **After Free Tier**: $0.01 per build minute, $0.15 per GB served
- **Estimated Cost**: $0-5/month for hackathon demo

### S3 Static Website
- **Storage**: $0.023 per GB/month
- **Requests**: $0.0004 per 1000 GET requests
- **Data Transfer**: $0.09 per GB (first 10 TB)
- **Estimated Cost**: $0-2/month for hackathon demo

---

## Next Steps

1. ✅ Deploy frontend using Option 1 (Amplify Console)
2. ✅ Get live URL
3. ✅ Update README.md with live URL
4. ✅ Test all features (Voice Triage, Document Upload, Case Memory)
5. ✅ Share URL with judges!

---

**Need Help?**
- AWS Amplify Docs: https://docs.aws.amazon.com/amplify/
- S3 Static Website Docs: https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html

---

**"न्याय सबके लिए, सबकी भाषा में"**  
*Justice for All, in Everyone's Language*
