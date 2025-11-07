# Demo GIF Creation Guide

## Overview
Create a professional demo GIF showing the Guardian fraud detection system in action.

## Tools Required

### Option 1: OBS Studio (Recommended - Free)
1. Download: https://obsproject.com/
2. Free, open-source screen recorder
3. Export as MP4, convert to GIF with online tools

### Option 2: ScreenToGif (Windows - Free)
1. Download: https://www.screentogif.com/
2. Directly records and exports as GIF
3. Simple interface, perfect for demo creation

### Option 3: LICEcap (Cross-platform - Free)
1. Download: https://www.cockos.com/licecap/
2. Lightweight, records directly to GIF
3. Good for quick demos

## Demo Script (2-3 minute recording)

### Scene 1: Overview (10 seconds)
- Show README with badges
- Highlight "Quick Start" section
- Show model performance metrics

### Scene 2: Data Generation (15 seconds)
```bash
python scripts/create_demo_data.py
```
- Show synthetic data generation
- Highlight 100K transactions created
- Show training/test split

### Scene 3: Model Training (20 seconds)
```bash
python scripts/train_quick_model.py
```
- Show training progress with AUC scores
- Highlight fast training time (5-15 min)
- Show final metrics output

### Scene 4: Model Evaluation (15 seconds)
- Show metrics.json with performance scores
- Highlight accuracy, precision, recall, F1, AUC-ROC
- Show model file saved

### Scene 5: API Demo (30 seconds)
```bash
python scripts/run_api.py
# Or: uvicorn src.api.main:app --reload
```
- Show FastAPI docs (http://localhost:8000/docs)
- Demonstrate prediction endpoint
- Show SHAP explanation endpoint

### Scene 6: Code Walkthrough (30 seconds)
- Show project structure
- Highlight key files:
  - `src/data/generate_synthetic_fraud_data.py`
  - `src/models/trainer.py`
  - `src/api/routers/predict.py`
- Show clean, well-documented code

### Scene 7: Results Summary (10 seconds)
- Show dashboard/visualization (if available)
- Highlight key features
- Return to README with badges

## GIF Specifications

### Dimensions
- **Width:** 1280px (recommended) or 1920px
- **Aspect Ratio:** 16:9 (for GitHub README)
- **Frame Rate:** 10-15 FPS (keeps file size reasonable)

### File Size
- **Target:** < 10MB (GitHub recommendation)
- **Max:** 25MB (GitHub limit)
- Use compression if needed:
  - https://ezgif.com/optimize
  - https://squoosh.app/

### Duration
- **Total:** 2-3 minutes (can speed up in editing)
- **Loop:** Enable infinite loop for GitHub

## Post-Production Tips

### Editing
1. **Remove pauses** - Speed up idle time
2. **Add captions** - Explain what's happening
3. **Smooth transitions** - Fade between scenes
4. **Add highlights** - Use cursor highlighting or zoom

### Optimization
1. **Reduce colors** - Limit to 256 colors
2. **Lower frame rate** - 10 FPS is usually enough
3. **Crop unnecessary areas** - Focus on important parts
4. **Resize if needed** - Smaller = faster loading

## Adding to README

Once created, add to README.md:

```markdown
## Demo

![Demo GIF](docs/demo.gif)

Watch the system in action: [Full Video](https://youtube.com/your-video-link)
```

Or embed directly:

```markdown
## Quick Demo

![Guardian Fraud Detection Demo](https://github.com/reichert-sentinel-ai/guardian/blob/main/docs/demo.gif)
```

## Alternative: YouTube Video

If GIF is too large:
1. Upload to YouTube as "Unlisted"
2. Create thumbnail image
3. Link in README:
```markdown
[![Demo Video](docs/demo-thumbnail.png)](https://youtube.com/watch?v=YOUR_VIDEO_ID)
```

## Quick Start Commands

```bash
# 1. Generate demo data
python scripts/create_demo_data.py

# 2. Train model
python scripts/train_quick_model.py

# 3. Start API
python scripts/run_api.py

# 4. Open in browser
# http://localhost:8000/docs
```

## Checklist

- [ ] Record all 7 scenes
- [ ] Edit and optimize GIF
- [ ] Test file size (< 10MB)
- [ ] Add to README
- [ ] Test loading on GitHub
- [ ] Create thumbnail (optional)
- [ ] Upload to YouTube (optional)

## Resources

- **OBS Studio:** https://obsproject.com/
- **ScreenToGif:** https://www.screentogif.com/
- **GIF Optimizer:** https://ezgif.com/optimize
- **Compression:** https://squoosh.app/

---

**Tip:** Record in high quality first, then optimize. It's easier to compress than to enhance later!

