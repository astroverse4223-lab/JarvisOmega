# 🌐 Quick Start: Deploy Your Jarvis Website

## 🚀 Deploy in 3 Steps

### Step 1: Install Vercel CLI
```powershell
npm install -g vercel
```

### Step 2: Login to Vercel
```powershell
vercel login
```
(Opens browser - sign in with GitHub)

### Step 3: Deploy!
```powershell
.\deploy-vercel.ps1
```

**Done!** Your website is live! 🎉

---

## 📦 Including Your Jarvis Executable

### Option A: Build & Auto-Deploy
```powershell
# Build the executable
python build.py

# Deploy (automatically includes Jarvis.exe)
.\deploy-vercel.ps1
```

The script finds `dist/Jarvis.exe` and adds it to your deployment!

### Option B: Manual Copy
```powershell
# Copy to downloads folder
copy dist\Jarvis.exe website\downloads\Jarvis-Omega.exe

# Deploy
vercel --prod
```

---

## 🔗 Your URLs After Deployment

- **Website:** `https://jarvis-omega.vercel.app`
- **Download:** `https://jarvis-omega.vercel.app/downloads/Jarvis-Omega.exe`
- **Download Page:** `https://jarvis-omega.vercel.app/download.html`

*(Your actual URL will be shown after deployment)*

---

## ⚙️ What Was Created

### New Files:
✅ `vercel.json` - Vercel configuration
✅ `deploy-vercel.ps1` - Auto-deployment script (Windows)
✅ `deploy-vercel.sh` - Auto-deployment script (Linux/Mac)
✅ `website/download.html` - Download page
✅ `website/downloads/` - Folder for executables
✅ `VERCEL_DEPLOYMENT_GUIDE.md` - Full deployment docs

### Updated Files:
✅ `website/index.html` - Links now point to download page
✅ `.gitignore` - Excludes large files from Git

---

## 🎯 What Changed on Your Website

**Before:**
- Download button → GitHub

**After:**
- Download button → Your own download page
- Download page → Your hosted Jarvis.exe
- Professional download experience!

---

## 🔄 Updating Your Site

Made changes? Deploy again:
```powershell
.\deploy-vercel.ps1
```

Live in ~30 seconds!

---

## 💡 Pro Tips

### 1. Custom Domain
```bash
vercel domains add yourjarvis.com
```

### 2. GitHub Auto-Deploy
Connect your repo on Vercel dashboard for automatic deploys on every push!

### 3. Large Files?
If your executable > 100MB, use GitHub Releases instead:
1. Create release on GitHub
2. Upload executable
3. Update download.html with release URL

---

## 🆘 Quick Troubleshooting

**Can't find vercel command?**
```powershell
npm install -g vercel
```

**Download button shows error?**
- Make sure `Jarvis.exe` is built: `python build.py`
- Check file is < 100MB
- Use GitHub Releases for larger files

**Want to use GitHub for downloads?**
Edit `website/download.html` line ~175, change:
```javascript
const downloadUrl = 'https://github.com/yourusername/jarvis/releases/latest/download/Jarvis.exe';
```

---

## 📚 Full Documentation

See `VERCEL_DEPLOYMENT_GUIDE.md` for:
- Custom domains
- Environment variables
- CI/CD setup
- Advanced configuration

---

## ✨ You're Ready!

Your Jarvis Omega website is deployment-ready!

**Next steps:**
1. Run: `.\deploy-vercel.ps1`
2. Get your live URL
3. Share with the world! 🌍

Questions? Check `VERCEL_DEPLOYMENT_GUIDE.md`
