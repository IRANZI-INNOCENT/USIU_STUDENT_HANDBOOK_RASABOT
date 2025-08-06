# Deployment Guide - USIU Student Handbook Chatbot

## Overview

This guide provides comprehensive instructions for deploying the USIU Student Handbook Chatbot in various environments, from local development to production deployment.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Production Deployment](#production-deployment)
4. [Docker Deployment](#docker-deployment)
5. [Cloud Deployment Options](#cloud-deployment-options)
6. [Configuration Management](#configuration-management)
7. [Monitoring & Maintenance](#monitoring--maintenance)
8. [Security Considerations](#security-considerations)

## Prerequisites

### System Requirements
- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.8 or higher
- **Memory**: Minimum 4GB RAM (8GB recommended for training)
- **Storage**: At least 2GB free space
- **Network**: Internet connection for dependencies

### Required Software
```bash
# Python 3.8+
python --version

# pip (usually comes with Python)
pip --version

# Git (optional, for version control)
git --version
```

## Local Development Setup

### Step 1: Project Setup
```bash
# Clone or download the project
cd /path/to/your/projects
# If using git:
git clone <repository-url> usiu-chatbot
cd usiu-chatbot

# If downloaded as zip:
# Extract to desired location and navigate to folder
```

### Step 2: Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Verify activation (should show (venv) in prompt)
```

### Step 3: Install Dependencies
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install Rasa
pip install rasa

# Verify installation
rasa --version
```

### Step 4: Train the Model
```bash
# Train the chatbot model
rasa train

# This creates a model file in the models/ directory
# Example: models/20250805-181834-seething-landform.tar.gz
```

### Step 5: Test the Installation
```bash
# Test in terminal
rasa shell

# Test the API
rasa run --enable-api --cors "*"
# Then open http://localhost:5005 in browser
```

### Step 6: Serve Web Interface
```bash
# Option 1: Python HTTP server
python -m http.server 8080
# Then open http://localhost:8080 and click index.html

# Option 2: Using any local web server
# Serve the index.html file through your preferred method
```

## Production Deployment

### Architecture Overview
```
Internet → Load Balancer → Web Server → Rasa Server → Model Files
                      ↓
                  Static Files (HTML/CSS/JS)
```

### Step 1: Prepare Production Environment
```bash
# Create production user
sudo useradd -m -s /bin/bash chatbot
sudo su - chatbot

# Setup directory structure
mkdir -p /opt/chatbot/{app,logs,config}
cd /opt/chatbot/app
```

### Step 2: Deploy Application Files
```bash
# Copy all project files to production server
scp -r * user@server:/opt/chatbot/app/

# Set proper permissions
sudo chown -R chatbot:chatbot /opt/chatbot
chmod +x /opt/chatbot/app/*.py
```

### Step 3: Production Dependencies
```bash
# Install system dependencies
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx

# Create production virtual environment
cd /opt/chatbot/app
python3 -m venv venv
source venv/bin/activate

# Install production dependencies
pip install rasa gunicorn
```

### Step 4: Configure Rasa for Production
Create `/opt/chatbot/app/production.yml`:
```yaml
# Production configuration
recipe: default.v1
assistant_id: usiu-chatbot-prod
language: en

pipeline:
  - name: WhitespaceTokenizer
  - name: RegexFeaturizer
  - name: LexicalSyntacticFeaturizer
  - name: CountVectorsFeaturizer
  - name: CountVectorsFeaturizer
    analyzer: char_wb
    min_ngram: 1
    max_ngram: 4
  - name: DIETClassifier
    epochs: 100
    constrain_similarities: true
  - name: EntitySynonymMapper
  - name: ResponseSelector
    epochs: 100
    constrain_similarities: true
  - name: FallbackClassifier
    threshold: 0.3
    ambiguity_threshold: 0.1

policies:
  - name: MemoizationPolicy
  - name: RulePolicy
  - name: UnexpecTEDIntentPolicy
    max_history: 5
    epochs: 100
  - name: TEDPolicy
    max_history: 5
    epochs: 100
    constrain_similarities: true
```

### Step 5: Create Systemd Service
Create `/etc/systemd/system/chatbot.service`:
```ini
[Unit]
Description=USIU Chatbot Rasa Server
After=network.target

[Service]
Type=simple
User=chatbot
WorkingDirectory=/opt/chatbot/app
Environment=PATH=/opt/chatbot/app/venv/bin
ExecStart=/opt/chatbot/app/venv/bin/rasa run --enable-api --cors "*" --port 5005
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Step 6: Configure Nginx
Create `/etc/nginx/sites-available/chatbot`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Serve static files
    location / {
        root /opt/chatbot/app;
        index index.html;
        try_files $uri $uri/ =404;
    }

    # Proxy API requests to Rasa
    location /webhooks/ {
        proxy_pass http://localhost:5005;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Additional API endpoints
    location /model/ {
        proxy_pass http://localhost:5005;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Step 7: Start Services
```bash
# Enable and start chatbot service
sudo systemctl enable chatbot
sudo systemctl start chatbot
sudo systemctl status chatbot

# Enable nginx
sudo ln -s /etc/nginx/sites-available/chatbot /etc/nginx/sites-enabled/
sudo systemctl reload nginx
```

## Docker Deployment

### Dockerfile
Create `Dockerfile`:
```dockerfile
FROM rasa/rasa:3.1.0

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Switch to root to install dependencies
USER root

# Train the model
RUN rasa train

# Switch back to rasa user
USER 1001

# Expose port
EXPOSE 5005

# Start command
CMD ["run", "--enable-api", "--cors", "*", "--port", "5005"]
```

### Docker Compose
Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  chatbot:
    build: .
    ports:
      - "5005:5005"
    volumes:
      - ./models:/app/models
      - ./logs:/app/logs
    environment:
      - RASA_MODEL_PATH=/app/models
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./index.html:/usr/share/nginx/html/index.html
    depends_on:
      - chatbot
    restart: unless-stopped
```

### Build and Deploy
```bash
# Build the image
docker build -t usiu-chatbot .

# Run with docker-compose
docker-compose up -d

# Check logs
docker-compose logs -f chatbot
```

## Cloud Deployment Options

### AWS Deployment

#### Using EC2
```bash
# Launch EC2 instance (Ubuntu 20.04 LTS)
# Configure security groups (ports 22, 80, 443, 5005)
# SSH into instance and follow production deployment steps
```

#### Using ECS/Fargate
```yaml
# task-definition.json
{
  "family": "usiu-chatbot",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "chatbot",
      "image": "your-account.dkr.ecr.region.amazonaws.com/usiu-chatbot:latest",
      "portMappings": [
        {
          "containerPort": 5005,
          "protocol": "tcp"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/usiu-chatbot",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### Google Cloud Platform

#### Using Cloud Run
```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/PROJECT-ID/usiu-chatbot

# Deploy to Cloud Run
gcloud run deploy --image gcr.io/PROJECT-ID/usiu-chatbot --platform managed
```

### Microsoft Azure

#### Using Container Instances
```bash
# Create resource group
az group create --name chatbot-rg --location eastus

# Deploy container
az container create \
  --resource-group chatbot-rg \
  --name usiu-chatbot \
  --image your-registry/usiu-chatbot:latest \
  --ports 5005 \
  --dns-name-label usiu-chatbot
```

## Configuration Management

### Environment Variables
```bash
# Production environment variables
export RASA_MODEL_PATH=/opt/chatbot/app/models
export RASA_LOG_LEVEL=INFO
export RASA_CORS_ORIGINS='["https://yourdomain.com"]'
export RASA_PORT=5005
```

### Configuration Files

#### Production Config (`production-config.yml`)
```yaml
# Optimized for production
recipe: default.v1
assistant_id: usiu-chatbot-production
language: en

pipeline:
  - name: WhitespaceTokenizer
  - name: RegexFeaturizer
  - name: LexicalSyntacticFeaturizer
  - name: CountVectorsFeaturizer
    analyzer: word
    min_ngram: 1
    max_ngram: 2
  - name: DIETClassifier
    epochs: 100
    constrain_similarities: true
    model_confidence: linear_norm
  - name: FallbackClassifier
    threshold: 0.7
    ambiguity_threshold: 0.1

policies:
  - name: MemoizationPolicy
    max_history: 5
  - name: RulePolicy
    core_fallback_threshold: 0.4
  - name: TEDPolicy
    max_history: 5
    epochs: 100
    constrain_similarities: true
```

#### Endpoints Configuration (`endpoints.yml`)
```yaml
action_endpoint:
  url: "http://localhost:5055/webhook"

tracker_store:
  type: InMemoryTrackerStore

event_broker:
  type: file
  path: logs/events.log
```

## Monitoring & Maintenance

### Health Checks
```bash
# Check if Rasa is running
curl http://localhost:5005/

# Check model status
curl http://localhost:5005/status

# Test conversation
curl -X POST http://localhost:5005/webhooks/rest/webhook \
  -H "Content-Type: application/json" \
  -d '{"sender": "test", "message": "hello"}'
```

### Logging Configuration
```python
# logging.conf
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/opt/chatbot/logs/chatbot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
```

### Backup Strategy
```bash
# Backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/backups/chatbot"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup models
tar -czf $BACKUP_DIR/models_$DATE.tar.gz /opt/chatbot/app/models/

# Backup configuration
tar -czf $BACKUP_DIR/config_$DATE.tar.gz /opt/chatbot/app/*.yml

# Keep only last 30 days of backups
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

### Performance Monitoring
```bash
# Monitor system resources
htop

# Monitor Rasa process
ps aux | grep rasa

# Check memory usage
free -h

# Monitor disk space
df -h
```

## Security Considerations

### Network Security
```bash
# Configure firewall
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw deny 5005  # Don't expose Rasa port directly
```

### SSL/TLS Configuration
```nginx
# nginx SSL configuration
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;

    # Rest of configuration...
}
```

### Access Control
```yaml
# Rate limiting in nginx
http {
    limit_req_zone $binary_remote_addr zone=chatbot:10m rate=10r/s;
    
    server {
        location /webhooks/ {
            limit_req zone=chatbot burst=20 nodelay;
            # proxy configuration...
        }
    }
}
```

### Data Privacy
- Ensure no sensitive data is logged
- Implement conversation data retention policies
- Regular security updates for all components
- Monitor access logs for unusual activity

## Troubleshooting

### Common Issues

#### Model Loading Errors
```bash
# Check model file exists
ls -la models/

# Verify model integrity
rasa shell --model models/your-model.tar.gz

# Retrain if corrupted
rasa train --force
```

#### Port Conflicts
```bash
# Check what's using port 5005
netstat -tulpn | grep 5005

# Kill process if needed
sudo kill -9 <PID>
```

#### Permission Issues
```bash
# Fix ownership
sudo chown -R chatbot:chatbot /opt/chatbot

# Fix permissions
chmod +x /opt/chatbot/app/venv/bin/rasa
```

### Log Analysis
```bash
# View Rasa logs
journalctl -u chatbot -f

# View nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# View application logs
tail -f /opt/chatbot/logs/chatbot.log
```

## Maintenance Tasks

### Regular Updates
```bash
# Update Rasa
pip install --upgrade rasa

# Retrain model after updates
rasa train

# Test after updates
rasa test
```

### Model Retraining
```bash
# Schedule regular retraining (crontab)
0 2 * * 0 cd /opt/chatbot/app && /opt/chatbot/app/venv/bin/rasa train

# Backup old model before retraining
cp models/*.tar.gz models/backup/
```

### Database Maintenance
```bash
# If using external databases, regular maintenance:
# - Index optimization
# - Data cleanup
# - Performance tuning
```

---

This deployment guide provides comprehensive instructions for deploying the USIU Student Handbook Chatbot in various environments. Choose the deployment method that best fits your infrastructure and requirements.
