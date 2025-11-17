---
author: "Regan William DUFF"
company: "AXIOM INTELLIGENCE LIMITED"
company_number: "9287393"
date: "October 26, 2025"
cryptographic_signature: "7d5e48fa871a0264f87aaac5313b80babe01dcbe286ee9e2c9925515b5c87e5e"
constitutional_compliance: "Satya, Asteya, Ahimsa"
provenance_hash: "ffcbf39be82677fad09c7183c4f1fe44098807c9f3c88f9fda87c953a4787ea2"
---

# GATEKEEPER - Deployment Guide

Complete step-by-step guide for deploying GATEKEEPER to production.

**Deployment Options:**
1. Railway.app (Recommended - Easiest)
2. Render.com (Alternative)
3. Fly.io (Advanced)
4. AWS/GCP/Azure (Enterprise)

---

## 🚂 Option 1: Railway.app (Recommended)

**Why Railway?**
- ✅ One-click deploy
- ✅ Free tier available
- ✅ Automatic HTTPS
- ✅ Built-in monitoring
- ✅ Easy environment variables

### Step 1: Prepare Repository

```bash
# Create railway.json
cat > railway.json << 'EOF'
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python -m axiom.apps.gatekeeper.cli deploy --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
EOF

# Create Procfile
echo "web: python -m axiom.apps.gatekeeper.cli deploy --host 0.0.0.0 --port \$PORT" > Procfile

# Create requirements.txt
pip freeze > requirements.txt
```

### Step 2: Deploy to Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Create project
railway init

# Add environment variables
railway variables set OPENAI_API_KEY=sk-...
railway variables set NOTIFICATION_EMAIL=you@example.com
railway variables set SMTP_SERVER=smtp.gmail.com
railway variables set SMTP_PORT=587
railway variables set SMTP_USERNAME=your-email@gmail.com
railway variables set SMTP_PASSWORD=your-app-password

# Deploy
railway up

# Get URL
railway domain
```

**Your app is now live at:** `https://your-app.railway.app`

### Step 3: Configure Custom Domain (Optional)

```bash
# Add custom domain
railway domain add gatekeeper.yourdomain.com

# Update DNS (in your domain registrar):
# Type: CNAME
# Name: gatekeeper
# Value: your-app.railway.app
```

---

## 🎨 Option 2: Render.com

**Why Render?**
- ✅ Free tier (with limitations)
- ✅ Automatic deployments from Git
- ✅ Built-in databases
- ✅ Easy scaling

### Step 1: Create render.yaml

```yaml
services:
  - type: web
    name: gatekeeper
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python -m axiom.apps.gatekeeper.cli deploy --host 0.0.0.0 --port $PORT
    envVars:
      - key: OPENAI_API_KEY
        sync: false
      - key: NOTIFICATION_EMAIL
        sync: false
      - key: SMTP_SERVER
        value: smtp.gmail.com
      - key: SMTP_PORT
        value: 587
      - key: SMTP_USERNAME
        sync: false
      - key: SMTP_PASSWORD
        sync: false
    healthCheckPath: /health
```

### Step 2: Deploy

1. Push code to GitHub/GitLab
2. Go to https://dashboard.render.com/
3. Click "New +" → "Web Service"
4. Connect your repository
5. Render auto-detects `render.yaml`
6. Click "Create Web Service"
7. Add environment variables in Render dashboard

**Your app is live at:** `https://gatekeeper.onrender.com`

---

## ✈️ Option 3: Fly.io

**Why Fly.io?**
- ✅ Global edge deployment
- ✅ Low latency worldwide
- ✅ Free tier available
- ✅ Excellent for WebSocket apps

### Step 1: Install Fly CLI

```bash
# Windows
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"

# macOS/Linux
curl -L https://fly.io/install.sh | sh

# Login
fly auth login
```

### Step 2: Create fly.toml

```toml
app = "gatekeeper"
primary_region = "sea"  # Seattle (change to nearest region)

[build]
  [build.args]
    PYTHON_VERSION = "3.11"

[env]
  PORT = "8080"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0
  
  [[http_service.checks]]
    interval = "10s"
    timeout = "2s"
    grace_period = "5s"
    method = "GET"
    path = "/health"

[[services]]
  protocol = "tcp"
  internal_port = 8080

  [[services.ports]]
    port = 80
    handlers = ["http"]

  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]

[[services.tcp_checks]]
  interval = "15s"
  timeout = "2s"
  grace_period = "1s"
```

### Step 3: Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8080

# Run
CMD ["python", "-m", "axiom.apps.gatekeeper.cli", "deploy", "--host", "0.0.0.0", "--port", "8080"]
```

### Step 4: Deploy

```bash
# Initialize app
fly launch

# Set secrets
fly secrets set OPENAI_API_KEY=sk-...
fly secrets set NOTIFICATION_EMAIL=you@example.com
fly secrets set SMTP_SERVER=smtp.gmail.com
fly secrets set SMTP_PORT=587
fly secrets set SMTP_USERNAME=your-email@gmail.com
fly secrets set SMTP_PASSWORD=your-app-password

# Deploy
fly deploy

# Get URL
fly status
```

**Your app is live at:** `https://gatekeeper.fly.dev`

---

## ☁️ Option 4: AWS/GCP/Azure (Enterprise)

### AWS Deployment (EC2 + Application Load Balancer)

**Prerequisites:**
- AWS Account
- AWS CLI configured
- EC2 key pair created

**Step 1: Launch EC2 Instance**

```bash
# Create security group
aws ec2 create-security-group \
    --group-name gatekeeper-sg \
    --description "GATEKEEPER security group"

# Allow SSH (port 22)
aws ec2 authorize-security-group-ingress \
    --group-name gatekeeper-sg \
    --protocol tcp --port 22 --cidr 0.0.0.0/0

# Allow HTTP (port 80)
aws ec2 authorize-security-group-ingress \
    --group-name gatekeeper-sg \
    --protocol tcp --port 80 --cidr 0.0.0.0/0

# Allow HTTPS (port 443)
aws ec2 authorize-security-group-ingress \
    --group-name gatekeeper-sg \
    --protocol tcp --port 443 --cidr 0.0.0.0/0

# Launch instance
aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1f0 \
    --instance-type t3.small \
    --key-name your-key-pair \
    --security-groups gatekeeper-sg \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=gatekeeper}]'
```

**Step 2: SSH and Install**

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@<instance-public-ip>

# Install dependencies
sudo apt update
sudo apt install -y python3-pip nginx

# Clone repository
git clone https://github.com/yourorg/axiom-x.git
cd axiom-x

# Install Python dependencies
pip3 install -r requirements.txt

# Create systemd service
sudo cat > /etc/systemd/system/gatekeeper.service << 'EOF'
[Unit]
Description=GATEKEEPER AI Sales Agent
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/axiom-x
Environment="OPENAI_API_KEY=sk-..."
Environment="NOTIFICATION_EMAIL=you@example.com"
ExecStart=/usr/bin/python3 -m axiom.apps.gatekeeper.cli deploy --host 127.0.0.1 --port 8765
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Start service
sudo systemctl daemon-reload
sudo systemctl enable gatekeeper
sudo systemctl start gatekeeper
```

**Step 3: Configure Nginx Reverse Proxy**

```nginx
# /etc/nginx/sites-available/gatekeeper
server {
    listen 80;
    server_name gatekeeper.yourdomain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8765;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/gatekeeper /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Install SSL certificate (Let's Encrypt)
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d gatekeeper.yourdomain.com
```

---

## 🔧 Post-Deployment Configuration

### 1. Test Deployment

```bash
# Health check
curl https://your-app.com/health

# Expected response:
# {"status":"healthy","version":"1.0.0"}

# Test conversation
curl -X POST https://your-app.com/api/conversations/new

# Test message
curl -X POST https://your-app.com/api/conversations/message \
  -H "Content-Type: application/json" \
  -d '{"conversation_id":"...","message":"Tell me about SENTINEL"}'
```

### 2. Set Up Monitoring

**Railway:**
```bash
# View logs
railway logs

# View metrics
railway status
```

**Render:**
- Dashboard → Your Service → Logs
- Dashboard → Your Service → Metrics

**Fly.io:**
```bash
# View logs
fly logs

# View metrics
fly dashboard
```

**AWS CloudWatch:**
```bash
# Install CloudWatch agent on EC2
sudo apt install -y amazon-cloudwatch-agent

# Configure monitoring
aws cloudwatch put-metric-alarm \
    --alarm-name gatekeeper-high-cpu \
    --alarm-description "Alert when CPU > 80%" \
    --metric-name CPUUtilization \
    --namespace AWS/EC2 \
    --statistic Average \
    --period 300 \
    --threshold 80 \
    --comparison-operator GreaterThanThreshold
```

### 3. Set Up Alerts

**Email Alerts:**
```python
# In notifier.py, add alert for system errors
def send_error_alert(error_message: str):
    send_email(
        to=os.getenv("ADMIN_EMAIL"),
        subject="🚨 GATEKEEPER Error",
        body=f"Error occurred:\n\n{error_message}"
    )
```

**Slack/Discord Webhooks:**
```python
import requests

def send_slack_alert(message: str):
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    requests.post(webhook_url, json={"text": message})
```

### 4. Enable HTTPS (if not automatic)

**Let's Encrypt (Certbot):**
```bash
# Install certbot
sudo apt install -y certbot

# Get certificate
sudo certbot certonly --standalone -d gatekeeper.yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 0 * * * certbot renew --quiet
```

### 5. Set Up Backups

**Conversation Data:**
```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf /backups/gatekeeper_${DATE}.tar.gz \
    conversations/ \
    receipts/ \
    analytics.db
EOF

chmod +x backup.sh

# Schedule daily backups
crontab -e
# Add: 0 2 * * * /path/to/backup.sh
```

---

## 🔒 Security Hardening

### 1. Environment Variables

**Never commit:**
```bash
# Add to .gitignore
echo ".env" >> .gitignore
echo "*.key" >> .gitignore
echo "*.pem" >> .gitignore
```

**Use secrets management:**
```bash
# Railway
railway variables set SECRET_KEY=...

# AWS Secrets Manager
aws secretsmanager create-secret \
    --name gatekeeper/openai-key \
    --secret-string "sk-..."
```

### 2. Rate Limiting

**Add to web.py:**
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/conversations/message")
@limiter.limit("10/minute")  # 10 requests per minute per IP
async def send_message(request: Request, msg: MessageRequest):
    # ...
```

### 3. CORS Configuration

**Production CORS:**
```python
# In web.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific domain only
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Specific methods only
    allow_headers=["Content-Type", "Authorization"],
)
```

### 4. DDoS Protection

**CloudFlare (Recommended):**
1. Sign up at https://cloudflare.com
2. Add your domain
3. Update nameservers
4. Enable "Under Attack" mode if needed

**AWS WAF:**
```bash
# Create WAF rules
aws wafv2 create-web-acl \
    --name gatekeeper-waf \
    --scope REGIONAL \
    --default-action Allow={} \
    --rules file://waf-rules.json
```

---

## 📊 Performance Optimization

### 1. Caching

**Redis caching:**
```python
import redis

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=6379,
    decode_responses=True
)

# Cache receipts (they don't change)
def get_cached_receipt(system: str):
    cached = redis_client.get(f"receipt:{system}")
    if cached:
        return json.loads(cached)
    
    receipt = generate_receipt(system)
    redis_client.setex(f"receipt:{system}", 3600, json.dumps(receipt))
    return receipt
```

### 2. CDN for Static Assets

**CloudFlare CDN:**
- Automatically enabled with CloudFlare
- Caches static files globally

**AWS CloudFront:**
```bash
# Create CloudFront distribution
aws cloudfront create-distribution \
    --origin-domain-name your-app.com \
    --default-root-object index.html
```

### 3. Database Optimization

**If using PostgreSQL:**
```sql
-- Add indexes for common queries
CREATE INDEX idx_conversations_status ON conversations(status);
CREATE INDEX idx_conversations_timestamp ON conversations(created_at DESC);
CREATE INDEX idx_messages_conversation ON messages(conversation_id);
```

---

## 🧪 Testing in Production

### 1. Smoke Tests

```bash
# Run automated tests against production
python -m pytest tests/test_production.py --url https://your-app.com
```

### 2. Load Testing

```bash
# Install locust
pip install locust

# Create locustfile.py
cat > locustfile.py << 'EOF'
from locust import HttpUser, task, between

class GatekeeperUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def create_conversation(self):
        self.client.post("/api/conversations/new")
    
    @task(3)
    def send_message(self):
        response = self.client.post("/api/conversations/new")
        conv_id = response.json()["conversation_id"]
        
        self.client.post("/api/conversations/message", json={
            "conversation_id": conv_id,
            "message": "Tell me about SENTINEL"
        })
EOF

# Run load test
locust -f locustfile.py --host https://your-app.com
```

### 3. Red Team Testing

```bash
# Run against production
python -m axiom.apps.gatekeeper.red_team_swarm --url https://your-app.com
```

---

## 🚨 Rollback Procedure

### Railway
```bash
# List deployments
railway deployments

# Rollback to previous
railway deployment rollback <deployment-id>
```

### Render
- Dashboard → Deployments → Click "Rollback" on previous deployment

### Fly.io
```bash
# List versions
fly releases

# Rollback
fly releases rollback <version>
```

### AWS/Manual
```bash
# Stop service
sudo systemctl stop gatekeeper

# Restore previous version
git checkout <previous-commit>
pip install -r requirements.txt

# Restart
sudo systemctl start gatekeeper
```

---

## 📈 Scaling

### Horizontal Scaling

**Railway/Render:**
- Dashboard → Settings → Instances → Increase count

**Fly.io:**
```bash
# Scale to 3 instances
fly scale count 3

# Auto-scale based on load
fly autoscale set min=1 max=10
```

**AWS:**
```bash
# Create Auto Scaling Group
aws autoscaling create-auto-scaling-group \
    --auto-scaling-group-name gatekeeper-asg \
    --launch-configuration-name gatekeeper-lc \
    --min-size 1 \
    --max-size 10 \
    --desired-capacity 2 \
    --target-group-arns <alb-target-group-arn>
```

### Vertical Scaling

**Increase instance size:**
- Railway: Change plan in dashboard
- Render: Upgrade instance type
- Fly.io: `fly scale vm shared-cpu-2x`
- AWS: Change instance type

---

## ✅ Post-Deployment Checklist

- [ ] Health endpoint returns 200
- [ ] HTTPS enabled and certificate valid
- [ ] Environment variables set correctly
- [ ] SMTP email sending works
- [ ] Analytics tracking conversations
- [ ] Qualification notifications arrive
- [ ] WebSocket connections working
- [ ] Receipt generation functional
- [ ] Privacy guard blocking attacks (100% rate)
- [ ] Rate limiting enabled
- [ ] Monitoring/logging configured
- [ ] Backups scheduled
- [ ] DNS configured (if custom domain)
- [ ] Load testing passed (>100 concurrent users)
- [ ] Red team testing passed (100% defense rate)

---

## 🆘 Emergency Contacts

**Production Issues:**
- Email: ops@axiomintelligence.co.nz
- Slack: #gatekeeper-alerts
- Phone: +64 XXX XXXX (24/7)

**Incident Response:**
1. Check health endpoint
2. Review logs for errors
3. Check monitoring dashboard
4. Rollback if needed
5. Report incident

---

**Deployment completed? Mark your status:**
```bash
echo "✅ GATEKEEPER DEPLOYED TO PRODUCTION" > DEPLOYMENT_STATUS.txt
date >> DEPLOYMENT_STATUS.txt
```

**Next:** Drive traffic and get your first qualified lead! 🎯
