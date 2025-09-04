# Deploy Cushion Order Verifier UI on Render

This guide will help you deploy your Cushion Order Verifier UI application on Render, a modern cloud platform that makes deployment simple and automatic.

## Prerequisites

- A Render account (free tier available)
- Your OpenAI API key
- Your application code in a Git repository (GitHub, GitLab, or Bitbucket)

## Step 1: Prepare Your Repository

### 1.1 Ensure Your Code is in Git
Make sure your project is in a Git repository and pushed to GitHub, GitLab, or Bitbucket.

### 1.2 Verify Required Files
Your repository should contain:
- `main.py` (your FastAPI application)
- `requirements.txt` (Python dependencies)
- `render.yaml` (Render configuration - already created)
- `templates/` directory with `index.html`
- `static/` directory (if you have static files)

## Step 2: Create a Render Account

1. Go to [render.com](https://render.com)
2. Sign up for a free account
3. Connect your GitHub/GitLab/Bitbucket account

## Step 3: Deploy Your Application

### 3.1 Create a New Web Service

1. **Log into Render Dashboard**
   - Go to your Render dashboard
   - Click **"New +"** button
   - Select **"Web Service"**

2. **Connect Your Repository**
   - Choose your Git provider (GitHub, GitLab, or Bitbucket)
   - Select your repository: `Cushion_Order_Verifier_UI`
   - Click **"Connect"**

3. **Configure Your Service**
   - **Name**: `cushion-order-verifier` (or your preferred name)
   - **Environment**: `Python 3`
   - **Region**: Choose the closest to your users
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: Leave empty (uses root)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`

### 3.2 Set Environment Variables

In the **Environment Variables** section, add:

| Key | Value | Description |
|-----|-------|-------------|
| `OPENAI_API_KEY` | `your-openai-api-key` | Your OpenAI API key (required) |
| `USE_CUSTOM_GPT` | `false` | Set to true if using custom GPT assistant |
| `CUSTOM_ASSISTANT_ID` | `your-assistant-id` | Only if USE_CUSTOM_GPT=true |

**Important**: 
- Click **"Add Environment Variable"** for each one
- Mark `OPENAI_API_KEY` as **"Secret"** for security
- Mark `CUSTOM_ASSISTANT_ID` as **"Secret"** if using custom GPT

### 3.3 Advanced Settings (Optional)

- **Auto-Deploy**: Keep enabled for automatic deployments
- **Health Check Path**: `/` (your app's root endpoint)
- **Plan**: Start with **Free** plan

### 3.4 Deploy

1. Click **"Create Web Service"**
2. Render will automatically:
   - Clone your repository
   - Install dependencies from `requirements.txt`
   - Start your application
   - Provide you with a public URL

## Step 4: Monitor Your Deployment

### 4.1 Check Build Logs
- Go to your service dashboard
- Click **"Logs"** tab
- Monitor the build process
- Look for any errors

### 4.2 Test Your Application
- Once deployed, you'll get a URL like: `https://cushion-order-verifier.onrender.com`
- Visit the URL to test your application
- Try the Shopify integration with a test order number

## Step 5: Configure Custom Domain (Optional)

### 5.1 Add Custom Domain
1. Go to your service settings
2. Click **"Custom Domains"**
3. Add your domain name
4. Follow DNS configuration instructions

### 5.2 SSL Certificate
- Render automatically provides SSL certificates
- Your app will be accessible via HTTPS

## Troubleshooting

### Common Issues

1. **Build Fails**
   - Check `requirements.txt` for correct dependencies
   - Ensure all required files are in the repository
   - Check build logs for specific error messages

2. **Application Won't Start**
   - Verify the start command: `python main.py`
   - Check that `main.py` is in the root directory
   - Review application logs for startup errors

3. **Environment Variables Not Working**
   - Ensure variables are marked as "Secret" if they contain sensitive data
   - Check variable names match exactly (case-sensitive)
   - Redeploy after adding new environment variables

4. **Static Files Not Loading**
   - Verify `static/` directory is in your repository
   - Check that static files are properly referenced in templates

5. **OpenAI API Errors**
   - Verify your API key is correct and has sufficient credits
   - Check that the key is properly set in environment variables
   - Ensure your OpenAI account is active

### Performance Optimization

1. **Upgrade Plan**
   - Free tier has limitations (sleeps after inactivity)
   - Consider upgrading to Starter plan ($7/month) for better performance

2. **Optimize Dependencies**
   - Remove unused packages from `requirements.txt`
   - Use specific version numbers for better reproducibility

3. **Monitor Usage**
   - Check Render dashboard for resource usage
   - Monitor API usage and costs

## Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `OPENAI_API_KEY` | Yes | Your OpenAI API key | `sk-...` |
| `USE_CUSTOM_GPT` | No | Use custom GPT assistant | `false` |
| `CUSTOM_ASSISTANT_ID` | No | Custom assistant ID | `asst_...` |

## Render Configuration File

The `render.yaml` file in your repository contains the deployment configuration:

```yaml
services:
  - type: web
    name: cushion-order-verifier
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python main.py
    envVars:
      - key: OPENAI_API_KEY
        sync: false
      - key: USE_CUSTOM_GPT
        value: false
      - key: CUSTOM_ASSISTANT_ID
        sync: false
```

## Security Best Practices

1. **Environment Variables**
   - Never commit API keys to your repository
   - Use Render's environment variable system
   - Mark sensitive variables as "Secret"

2. **HTTPS**
   - Render provides automatic SSL certificates
   - Always use HTTPS in production

3. **API Keys**
   - Rotate API keys regularly
   - Monitor API usage and costs
   - Use least-privilege access

## Cost Considerations

### Free Tier Limitations
- **Sleep**: App sleeps after 15 minutes of inactivity
- **Build Time**: 90 minutes per month
- **Bandwidth**: 100 GB per month
- **CPU**: 0.1 CPU, 512 MB RAM

### Paid Plans
- **Starter**: $7/month - No sleep, better performance
- **Standard**: $25/month - More resources, better scaling

## Support and Resources

- **Render Documentation**: https://render.com/docs
- **Render Community**: https://community.render.com
- **FastAPI Documentation**: https://fastapi.tiangolo.com
- **OpenAI API Documentation**: https://platform.openai.com/docs

## Next Steps After Deployment

1. **Test All Features**
   - Shopify integration
   - Audio file uploads
   - GPT processing
   - Error handling

2. **Set Up Monitoring**
   - Monitor application logs
   - Set up alerts for errors
   - Track API usage

3. **Optimize Performance**
   - Monitor response times
   - Optimize database queries (if applicable)
   - Consider caching strategies

4. **Backup and Recovery**
   - Regular backups of your code
   - Document your deployment process
   - Test recovery procedures

Your Cushion Order Verifier UI is now ready for production use on Render!
