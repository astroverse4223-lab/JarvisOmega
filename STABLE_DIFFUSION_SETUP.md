# 🎨 Stable Diffusion Setup Guide for Jarvis

## Quick Start (Windows)

### 📥 **Step 1: Download Stable Diffusion WebUI**

**Option A: One-Click Installer (Easiest)**
1. Go to: https://github.com/AUTOMATIC1111/stable-diffusion-webui
2. Download the Windows installer
3. Run the installer - it handles everything automatically

**Option B: Manual Installation**
```powershell
# 1. Install Git (if not already installed)
# Download from: https://git-scm.com/download/win

# 2. Clone the repository
cd C:\
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
cd stable-diffusion-webui

# 3. Run the installer (downloads Python, models, everything)
.\webui-user.bat
```

---

### ⚙️ **Step 2: Enable API Access**

**Edit the launch script:**

1. Open `webui-user.bat` in Notepad
2. Find this line:
   ```batch
   set COMMANDLINE_ARGS=
   ```
3. Change it to:
   ```batch
   set COMMANDLINE_ARGS=--api
   ```
4. Save the file

**Your `webui-user.bat` should look like:**
```batch
@echo off

set PYTHON=
set GIT=
set VENV_DIR=
set COMMANDLINE_ARGS=--api

call webui.bat
```

---

### 🚀 **Step 3: Start Stable Diffusion**

```powershell
# Navigate to the folder
cd C:\stable-diffusion-webui

# Run the WebUI with API enabled
.\webui-user.bat
```

**What happens:**
- First run: Downloads models (~4GB), takes 10-20 minutes
- Subsequent runs: Starts in 1-2 minutes
- You'll see: `Running on local URL: http://127.0.0.1:7860`
- **Keep this window open while using Jarvis!**

---

### ✅ **Step 4: Test It Works**

**Option 1: Web Interface**
1. Open browser: http://127.0.0.1:7860
2. Type a prompt: "a cute cat"
3. Click "Generate"
4. If image appears → Working! ✅

**Option 2: Test with Jarvis**
1. Make sure Stable Diffusion is running
2. Say to Jarvis: "Generate image of a sunset"
3. Wait 30-60 seconds
4. Image window should appear ✅

---

## 🎯 Usage with Jarvis

Once Stable Diffusion is running, use these commands:

```
"Generate image of a mountain landscape"
"Create image of a futuristic robot"
"Make me an image of a cozy cabin in snow"
"Show me an image of a dragon flying"
```

**Tips:**
- Be specific: "a red sports car on a highway at sunset"
- Add style: "oil painting of a castle, medieval style"
- Mention quality: "high quality, detailed, 4k"

---

## 🔧 Troubleshooting

### ❌ "Cannot connect to image generation API"
**Solution:**
1. Make sure `webui-user.bat` is running
2. Look for: `Running on local URL: http://127.0.0.1:7860`
3. Check the COMMANDLINE_ARGS includes `--api`

### ❌ "Out of memory" errors
**Solution:**
Add to `webui-user.bat`:
```batch
set COMMANDLINE_ARGS=--api --medvram
```
Or for very low memory:
```batch
set COMMANDLINE_ARGS=--api --lowvram
```

### ❌ Slow generation (>60 seconds)
**Solutions:**
- Use `--xformers` flag for faster generation
- Reduce image size in `image_generator.py` (default 512x512)
- Upgrade GPU if possible

### ❌ First run taking forever
**Normal!** First run downloads:
- Stable Diffusion model (~4GB)
- Python packages
- Dependencies
Can take 15-30 minutes depending on internet speed.

---

## 💡 Advanced Configuration

### Change Image Quality
Edit `scripts/image_generator.py`:

```python
# Find this section (around line 19)
json={
    'prompt': description,
    'negative_prompt': 'blurry, low quality, distorted, deformed',
    'steps': 30,        # More steps = better quality, slower (20-50)
    'width': 512,       # Image width (512, 768, 1024)
    'height': 512,      # Image height (512, 768, 1024)
    'cfg_scale': 7,     # How closely to follow prompt (7-15)
    'sampler_name': 'Euler a'  # Sampling method
}
```

### Popular Samplers
- `Euler a` - Fast, good quality (default)
- `DPM++ 2M Karras` - High quality, slower
- `DDIM` - Fast, lower quality

### Install Better Models
1. Download models from: https://civitai.com
2. Place `.safetensors` files in: `stable-diffusion-webui\models\Stable-diffusion\`
3. Restart WebUI
4. Select model in web interface

---

## 📊 System Requirements

**Minimum:**
- GPU: NVIDIA GTX 1060 6GB or AMD equivalent
- RAM: 8GB
- Storage: 10GB free
- OS: Windows 10/11

**Recommended:**
- GPU: NVIDIA RTX 3060 12GB or better
- RAM: 16GB
- Storage: 20GB+ free (for multiple models)
- OS: Windows 11

**Without GPU:**
Use `--use-cpu` flag (very slow, 5-10 minutes per image)

---

## 🎨 Example Prompts

**Landscapes:**
```
"mountain landscape at sunset, realistic, 4k"
"tropical beach with palm trees, crystal clear water"
"forest path in autumn, golden hour lighting"
```

**Characters:**
```
"portrait of a wizard with long beard, fantasy art"
"cyberpunk girl with neon lights, digital art"
"friendly robot character, pixar style"
```

**Objects:**
```
"vintage car, 1960s style, detailed"
"modern kitchen interior, minimalist design"
"fantasy sword with glowing runes"
```

**Styles:**
```
"oil painting of a castle, medieval style"
"watercolor illustration of flowers"
"anime style character with blue hair"
```

---

## 🔄 Daily Workflow

**1. Start your day:**
```powershell
cd C:\stable-diffusion-webui
.\webui-user.bat
```

**2. Use Jarvis normally**
- Stable Diffusion runs in background
- Say image generation commands
- Images appear in windows

**3. End of day:**
- Close the WebUI window
- Or leave running if generating many images

---

## 📚 Additional Resources

- **Official Docs:** https://github.com/AUTOMATIC1111/stable-diffusion-webui
- **Model Library:** https://civitai.com
- **Discord Community:** https://discord.gg/stablediffusion
- **Tutorial Videos:** Search "Automatic1111 tutorial" on YouTube

---

## 🎉 Quick Command Reference

**Start WebUI:**
```powershell
cd C:\stable-diffusion-webui
.\webui-user.bat
```

**With custom settings:**
```powershell
# Low memory GPU
set COMMANDLINE_ARGS=--api --medvram
.\webui-user.bat

# Very low memory
set COMMANDLINE_ARGS=--api --lowvram
.\webui-user.bat

# Fast generation (requires xformers)
set COMMANDLINE_ARGS=--api --xformers
.\webui-user.bat
```

**Update to latest version:**
```powershell
cd C:\stable-diffusion-webui
git pull
```

---

## ✅ Checklist

- [ ] Downloaded Stable Diffusion WebUI
- [ ] Ran first time setup (downloaded models)
- [ ] Added `--api` flag to `webui-user.bat`
- [ ] Started WebUI and saw "Running on local URL"
- [ ] Tested in web browser (http://127.0.0.1:7860)
- [ ] Tested with Jarvis image generation command
- [ ] Images saving to Desktop/JarvisImages folder

---

**Once setup is complete, just say:**
```
"Generate image of anything you imagine"
```

**And Jarvis will create it for you!** 🎨✨

---

**Installation Time:** 20-30 minutes first time  
**Daily Startup Time:** 1-2 minutes  
**Generation Time:** 10-60 seconds per image  

**Questions?** Check the troubleshooting section above!
