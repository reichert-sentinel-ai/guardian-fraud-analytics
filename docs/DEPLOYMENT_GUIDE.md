# Live Demo Deployment Guide

**Repository**: All Sentinel Analytics Repos (Guardian, Foresight, Cipher)  
**Date**: December 2024  
**Status**: Complete

---

## Overview

This guide provides step-by-step instructions for deploying live demos of Guardian, Foresight, and Cipher to various hosting platforms. Each repository can be deployed independently or as part of a unified Sentinel Analytics platform.

---

## Deployment Options

### Option 1: Streamlit Cloud (Recommended for Dashboards)

**Best for**: Quick dashboard deployment, free tier available  
**Requirements**: GitHub repository, Streamlit Cloud account  
**Cost**: Free (with limitations), Paid plans available

#### Steps for Guardian

1. **Prepare Repository**
   ```bash
   cd project/repo-guardian
   # Ensure requirements.txt includes streamlit
   # Ensure streamlit_app.py exists in root
   ```

2. **Deploy to Streamlit Cloud**
   - Go to https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Select repository: `reichert-sentinel-ai/guardian-fraud-analytics`
   - Main file: `streamlit_app.py`
   - Branch: `main`
   - Click "Deploy"

3. **Configure Environment Variables**
   - Add required environment variables in Streamlit Cloud settings
   - API keys, database URLs, etc.

4. **Access Demo**
   - URL: `https://guardian-fraud-analytics.streamlit.app`
   - Share URL with stakeholders

#### Steps for Foresight

1. **Prepare Repository**
   ```bash
   cd project/repo-foresight
   # Ensure requirements.txt includes streamlit
   # Ensure streamlit_app.py exists in root
   ```

2. **Deploy to Streamlit Cloud**
   - Follow same steps as Guardian
   - Repository: `reichert-sentinel-ai/foresight-crime-prediction`
   - URL: `https://foresight-crime-prediction.streamlit.app`

#### Steps for Cipher

1. **Prepare Repository**
   ```bash
   cd project/repo-cipher
   # Ensure requirements.txt includes streamlit
   # Ensure streamlit_app.py exists in root
   ```

2. **Deploy to Streamlit Cloud**
   - Follow same steps as Guardian
   - Repository: `reichert-sentinel-ai/cipher-threat-tracker`
   - URL: `https://cipher-threat-tracker.streamlit.app`

---

### Option 2: Docker + AWS/Azure/GCP

**Best for**: Production deployments, full control  
**Requirements**: Docker, cloud account, domain name  
**Cost**: Pay-as-you-go (typically $20-100/month)

#### Steps for All Repos

1. **Build Docker Image**
   ```bash
   cd project/repo-guardian  # or repo-foresight, repo-cipher
   docker build -t guardian:latest .
   ```

2. **Push to Container Registry**
   ```bash
   # AWS ECR
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
   docker tag guardian:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/guardian:latest
   docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/guardian:latest
   ```

3. **Deploy to Cloud**
   - **AWS ECS**: Create ECS service with Docker image
   - **Azure Container Instances**: Deploy container instance
   - **Google Cloud Run**: Deploy container to Cloud Run

4. **Configure Load Balancer**
   - Set up application load balancer
   - Configure HTTPS with SSL certificate
   - Point domain to load balancer

---

### Option 3: Vercel/Netlify (For Frontend + API)

**Best for**: React frontends, static sites with API routes  
**Requirements**: GitHub repository, Vercel/Netlify account  
**Cost**: Free tier available, paid plans for production

#### Steps for Guardian (React Frontend)

1. **Prepare Repository**
   ```bash
   cd project/repo-guardian
   # Ensure React app is in frontend/ directory
   # Ensure API routes are configured
   ```

2. **Deploy to Vercel**
   ```bash
   npm install -g vercel
   vercel login
   vercel --prod
   ```

3. **Configure Environment Variables**
   - Add environment variables in Vercel dashboard
   - API endpoints, database URLs, etc.

4. **Access Demo**
   - URL: `https://guardian-fraud-analytics.vercel.app`

---

### Option 4: Hugging Face Spaces (Free Alternative)

**Best for**: ML model demos, free hosting  
**Requirements**: Hugging Face account, GitHub repository  
**Cost**: Free

#### Steps for All Repos

1. **Create Space**
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Select "Streamlit" SDK
   - Name: `guardian-fraud-analytics`

2. **Configure Repository**
   - Connect GitHub repository
   - Set SDK to Streamlit
   - Configure environment variables

3. **Deploy**
   - Space builds automatically
   - URL: `https://huggingface.co/spaces/<username>/guardian-fraud-analytics`

---

## Environment Setup

### Required Environment Variables

#### Guardian
```bash
# Database
GUARDIAN_DB_URL=postgresql://user:pass@localhost:5432/guardian
GUARDIAN_REDIS_URL=redis://localhost:6379

# API Keys
GUARDIAN_API_KEY=your_api_key_here

# Model Paths
GUARDIAN_MODEL_PATH=/app/models/xgboost_model.pkl
```

#### Foresight
```bash
# Database
FORESIGHT_DB_URL=postgresql://user:pass@localhost:5432/foresight
FORESIGHT_REDIS_URL=redis://localhost:6379

# Mapbox
MAPBOX_ACCESS_TOKEN=your_mapbox_token_here

# Data Sources
CHICAGO_DATA_URL=https://data.cityofchicago.org/...
```

#### Cipher
```bash
# Elasticsearch
CIPHER_ES_URL=http://localhost:9200

# Neo4j
CIPHER_NEO4J_URL=bolt://localhost:7687
CIPHER_NEO4J_USER=neo4j
CIPHER_NEO4J_PASS=password

# IOC Sources
OTX_API_KEY=your_otx_key_here
ABUSE_CH_API_KEY=your_abuse_ch_key_here
```

---

## Pre-Deployment Checklist

### For Each Repository

- [ ] `requirements.txt` is up to date
- [ ] `Dockerfile` exists and is tested
- [ ] `docker-compose.yml` configured (if needed)
- [ ] Environment variables documented
- [ ] Database migrations run (if applicable)
- [ ] Sample data loaded (for demo)
- [ ] API endpoints tested
- [ ] Frontend builds successfully
- [ ] Tests pass
- [ ] Documentation updated

---

## Post-Deployment Steps

### 1. Verify Deployment

```bash
# Check API health
curl https://your-demo-url.com/api/health

# Check dashboard loads
open https://your-demo-url.com
```

### 2. Monitor Performance

- Set up monitoring (e.g., Sentry, DataDog)
- Configure alerts for errors
- Monitor resource usage

### 3. Update Documentation

- Update README with live demo URL
- Add deployment status badges
- Document any deployment-specific notes

---

## Demo URLs Template

Add to each repository's README:

```markdown
## 🚀 Live Demo

**Guardian**: [https://guardian-fraud-analytics.streamlit.app](https://guardian-fraud-analytics.streamlit.app)  
**Foresight**: [https://foresight-crime-prediction.streamlit.app](https://foresight-crime-prediction.streamlit.app)  
**Cipher**: [https://cipher-threat-tracker.streamlit.app](https://cipher-threat-tracker.streamlit.app)
```

---

## Troubleshooting

### Common Issues

1. **Streamlit Cloud Build Fails**
   - Check `requirements.txt` for conflicts
   - Verify Python version compatibility
   - Check logs in Streamlit Cloud dashboard

2. **Docker Build Fails**
   - Verify Dockerfile syntax
   - Check base image availability
   - Review build logs for errors

3. **Environment Variables Not Loading**
   - Verify variable names match exactly
   - Check platform-specific variable formats
   - Restart deployment after adding variables

4. **Database Connection Issues**
   - Verify database URL format
   - Check network connectivity
   - Verify credentials

---

## Security Considerations

### For Production Deployments

- [ ] Use HTTPS (SSL certificates)
- [ ] Secure API keys and secrets
- [ ] Enable authentication/authorization
- [ ] Configure CORS properly
- [ ] Set up rate limiting
- [ ] Enable logging and monitoring
- [ ] Regular security updates

---

## Cost Estimation

### Free Tier Options

- **Streamlit Cloud**: Free (public repos), $20/month (private)
- **Hugging Face Spaces**: Free
- **Vercel**: Free (with limitations)
- **Netlify**: Free (with limitations)

### Paid Options

- **AWS ECS**: ~$20-50/month (small deployments)
- **Azure Container Instances**: ~$15-40/month
- **Google Cloud Run**: Pay-per-use (~$10-30/month)

---

## Quick Deploy Scripts

### Streamlit Cloud (One-Click)

```bash
# Create deployment script
cat > deploy-streamlit.sh << 'EOF'
#!/bin/bash
REPO=$1
APP_NAME=$2

echo "Deploying $APP_NAME to Streamlit Cloud..."
echo "1. Go to https://share.streamlit.io"
echo "2. Select repository: $REPO"
echo "3. Main file: streamlit_app.py"
echo "4. Click Deploy"
EOF

chmod +x deploy-streamlit.sh
```

### Docker Quick Deploy

```bash
# Create quick deploy script
cat > deploy-docker.sh << 'EOF'
#!/bin/bash
REPO=$1
IMAGE_NAME=$2

cd project/$REPO
docker build -t $IMAGE_NAME:latest .
docker tag $IMAGE_NAME:latest your-registry/$IMAGE_NAME:latest
docker push your-registry/$IMAGE_NAME:latest
echo "Deployed $IMAGE_NAME to container registry"
EOF

chmod +x deploy-docker.sh
```

---

## Next Steps

After deployment:

1. ✅ Add demo URLs to README files
2. ✅ Update portfolio website with live links
3. ✅ Create demo walkthrough videos
4. ✅ Share with stakeholders/recruiters
5. ✅ Monitor performance and usage

---

*Last Updated: December 2024*  
*Supporting Homeland Security Through Advanced Data Science* 🇺🇸

