# Deployment Instructions - Groq to Bedrock Migration

## ✅ CONFIRMED: Repository Configuration

### Git Remote
```bash
git remote -v
# origin  https://github.com/kalivenkatg/Nyaya-Dwarpal-AI.git (fetch)
# origin  https://github.com/kalivenkatg/Nyaya-Dwarpal-AI.git (push)
```

**Status**: ✅ Correctly connected to https://github.com/kalivenkatg/Nyaya-Dwarpal-AI.git

### Amplify Configuration
```yaml
# amplify.yml
version: 1
frontend:
  artifacts:
    baseDirectory: ui
    files:
      - '**/*'
```

**Status**: ✅ Correctly configured to serve from `ui/` directory
**Live URL**: https://main.d1y87jb5yrv6jl.amplifyapp.com/

## 🚨 BLOCKER: GitHub Account Suspended

**Error**:
```
remote: Your account is suspended. Please visit https://support.github.com for more information.
fatal: unable to access 'https://github.com/kalivenkatg/Nyaya-Dwarpal-AI.git/': The requested URL returned error: 403
```

**Action Required**: Visit https://support.github.com to resolve account suspension

## 📦 Ready to Deploy (4 Commits)

```bash
git log --oneline origin/main..HEAD
# 663be06 docs: Add Groq to Bedrock migration documentation
# 4c71f49 Replace Groq AI with AWS Bedrock Claude 3.5 Sonnet for legal classification
# db08eb6 Fix: Strip markdown backticks from Groq JSON response
```

### Key Changes in These Commits

#### Backend (Already Deployed via CDK ✅)
- Replaced Groq API with AWS Bedrock
- Updated `bedrock_client.py` to use Claude 3.5 Sonnet
- Removed GROQ_API_KEY dependency
- Lambda functions working correctly

#### Frontend (Pending Amplify Deployment ⚠️)
- **File**: `ui/index.html`
- **Line**: 157
- **Change**: "Groq AI" → "AWS Bedrock"

#### Documentation
- Updated README.md with new architecture
- Added migration documentation
- Updated cost estimates

## 🚀 Deployment Steps (Once GitHub Access Restored)

### Step 1: Push to GitHub
```bash
git push origin main
```

**Expected Output**:
```
Enumerating objects: X, done.
Counting objects: 100% (X/X), done.
Delta compression using up to Y threads
Compressing objects: 100% (X/X), done.
Writing objects: 100% (X/X), Z KiB | Z MiB/s, done.
Total X (delta Y), reused Z (delta W), pack-reused 0
To https://github.com/kalivenkatg/Nyaya-Dwarpal-AI.git
   bda64cc..663be06  main -> main
```

### Step 2: Verify Push Success
```bash
git log --oneline origin/main..HEAD
# (should be empty - all commits pushed)
```

### Step 3: Monitor Amplify Build
1. Go to AWS Amplify Console
2. Navigate to app: Nyaya-Dwarpal
3. Check "Build history" tab
4. Latest build should show:
   - Branch: main
   - Commit: 663be06
   - Status: In Progress → Success

**Build Duration**: ~2-3 minutes

### Step 4: Verify Deployment
```bash
# Check if new content is live
curl https://main.d1y87jb5yrv6jl.amplifyapp.com/ | grep "AWS Bedrock"
```

**Expected**: Should find "AWS Bedrock" in the response

### Step 5: Test Navigation
Visit https://main.d1y87jb5yrv6jl.amplifyapp.com/ and test:
- ✅ Home page loads
- ✅ Sidebar navigation works
- ✅ Voice Triage page accessible
- ✅ Document Upload page accessible
- ✅ Case Memory page accessible
- ✅ Footer shows "AWS Bedrock" (not "Groq AI")

### Step 6: Test Voice Triage Feature
1. Click "Voice Triage" in sidebar
2. Click microphone button
3. Speak a test query (English or Hindi)
4. Verify:
   - ✅ Transcription appears
   - ✅ Legal classification works
   - ✅ No GROQ_API_KEY errors
   - ✅ Results display correctly

### Step 7: Check CloudWatch Logs
```bash
# In AWS Console → CloudWatch → Log Groups
# Find: /aws/lambda/NyayaDwarpalStack-VoiceTriageLambda...
# Look for recent logs showing:
[Bedrock] Invoking model with temperature=0.7, max_tokens=3000
[Bedrock] Response received. Stop reason: end_turn
[BEDROCK RAW RESPONSE] First 500 chars: {...
```

**Expected**: Should see `[Bedrock]` messages, NOT `[Groq]`

## 🔄 Alternative Deployment Methods

### Option A: Manual Amplify Deployment (If GitHub Push Fails)

1. **Via AWS Console**:
   - Go to AWS Amplify Console
   - Select app: Nyaya-Dwarpal
   - Click "Deploy without Git provider"
   - Upload `ui/` directory as ZIP file

2. **Via AWS CLI**:
   ```bash
   cd ui
   zip -r ../ui-deployment.zip .
   aws amplify create-deployment \
     --app-id <app-id> \
     --branch-name main \
     --file-map ui-deployment.zip
   ```

### Option B: Direct File Edit on GitHub (If Web Access Works)

1. Go to https://github.com/kalivenkatg/Nyaya-Dwarpal-AI/blob/main/ui/index.html
2. Click "Edit this file" (pencil icon)
3. Find line 157
4. Change: `Groq AI` → `AWS Bedrock`
5. Commit changes
6. Amplify will auto-deploy

### Option C: Use SSH Authentication (If Configured)

```bash
# Check if SSH key exists
ls -la ~/.ssh/id_*.pub

# If exists, change remote URL
git remote set-url origin git@github.com:kalivenkatg/Nyaya-Dwarpal-AI.git

# Push
git push origin main
```

### Option D: Use Personal Access Token (If Available)

```bash
# Create PAT at: https://github.com/settings/tokens
# Then:
git remote set-url origin https://<PAT>@github.com/kalivenkatg/Nyaya-Dwarpal-AI.git
git push origin main
```

## 📊 Current Status Summary

| Component | Status | Details |
|-----------|--------|---------|
| Git Remote | ✅ Correct | Connected to kalivenkatg/Nyaya-Dwarpal-AI.git |
| Amplify Config | ✅ Correct | Serving from ui/ directory |
| Backend Lambda | ✅ Deployed | Using AWS Bedrock (no Groq) |
| Frontend Code | ✅ Ready | Changes committed locally |
| GitHub Push | ⚠️ Blocked | Account suspended |
| Amplify Deploy | ⚠️ Pending | Waiting for GitHub push |
| Live Site | ⚠️ Old Version | Still shows "Groq AI" |

## 🎯 What Happens After Push

### Automatic Amplify Build Process

1. **GitHub Webhook** triggers Amplify
2. **Amplify clones** latest code from main branch
3. **Amplify runs** preBuild commands (echo statement)
4. **Amplify runs** build commands (echo statement)
5. **Amplify packages** artifacts from `ui/` directory
6. **Amplify deploys** to CloudFront CDN
7. **Live site updates** at https://main.d1y87jb5yrv6jl.amplifyapp.com/

**Total Time**: ~2-3 minutes from push to live

### Expected Changes on Live Site

**Before** (Current):
```html
<p>...using AWS Lambda, Sarvam AI, and Groq AI.</p>
```

**After** (Post-deployment):
```html
<p>...using AWS Lambda, Sarvam AI, and AWS Bedrock.</p>
```

## 🔍 Verification Checklist

After deployment completes:

- [ ] GitHub push successful (no errors)
- [ ] Amplify build shows "Success" status
- [ ] Live site loads at https://main.d1y87jb5yrv6jl.amplifyapp.com/
- [ ] Footer text shows "AWS Bedrock" (not "Groq AI")
- [ ] Navigation works (all sidebar links)
- [ ] Voice Triage feature works
- [ ] No GROQ_API_KEY errors in CloudWatch
- [ ] CloudWatch logs show `[Bedrock]` messages
- [ ] Legal classification returns specific categories

## 📝 Rollback Plan (If Issues Arise)

### Rollback Frontend Only
```bash
# Revert the UI change
git revert 4c71f49 --no-commit
git commit -m "Rollback: Revert to Groq AI in UI"
git push origin main
```

### Rollback Backend Only
```bash
# Revert bedrock_client.py changes
git revert 4c71f49
npx cdk deploy --require-approval never
```

### Full Rollback
```bash
# Revert all changes
git revert 663be06 4c71f49 db08eb6
git push origin main
npx cdk deploy --require-approval never
```

## 🆘 Troubleshooting

### Issue: Amplify Build Fails
**Check**: Build logs in Amplify Console
**Common Causes**:
- Missing files in `ui/` directory
- Syntax errors in HTML/JS
- amplify.yml misconfiguration

**Solution**: Review build logs, fix errors, push again

### Issue: Site Shows Old Content After Deploy
**Cause**: CloudFront cache
**Solution**: 
1. Clear browser cache (Cmd+Shift+R on Mac)
2. Or wait 5-10 minutes for CDN cache to expire
3. Or invalidate CloudFront cache in AWS Console

### Issue: Voice Triage Still Shows GROQ_API_KEY Error
**Cause**: Backend not deployed or Lambda using old code
**Solution**:
```bash
npx cdk deploy --require-approval never
```

### Issue: Navigation Broken
**Cause**: JavaScript errors or missing files
**Solution**: Check browser console for errors, verify all files in `ui/` directory

## 📞 Support

If issues persist after following these instructions:
1. Check AWS Amplify build logs
2. Check AWS Lambda CloudWatch logs
3. Check browser console for JavaScript errors
4. Review commit history: `git log --oneline -10`

## ✅ Success Criteria

Deployment is successful when:
1. ✅ GitHub push completes without errors
2. ✅ Amplify build shows "Success" status
3. ✅ Live site shows "AWS Bedrock" in footer
4. ✅ Voice Triage works without GROQ_API_KEY errors
5. ✅ All navigation links work
6. ✅ CloudWatch logs show `[Bedrock]` messages

---

**Created**: March 7, 2026
**Status**: Ready to deploy (pending GitHub access)
**Blocker**: GitHub account suspension
**Next Action**: Resolve GitHub suspension, then run `git push origin main`
