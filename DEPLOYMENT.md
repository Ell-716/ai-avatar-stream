# Deployment Guide

## Local Development

### Without Docker

**Backend:**
```bash
uvicorn backend.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm run dev
```

Access at:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### With Docker

```bash
docker-compose up --build
```

Access at:
- Frontend: http://localhost
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Production Deployment

### Prerequisites

- Docker & Docker Compose installed
- API keys (Groq, ElevenLabs)
- Domain name (optional)

### Steps

#### 1. Clone repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-avatar-stream.git
cd ai-avatar-stream
```

#### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with production API keys
```

Required environment variables:
```env
GROQ_API_KEY=your_groq_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
VOICE_ID_ELENA=21m00Tcm4TlvDq8ikWAM
VOICE_ID_MARCUS=29vD33N1CtxCmqQRPOHJ
```

#### 3. Build and deploy

```bash
docker-compose up -d
```

#### 4. Verify deployment

```bash
# Check running containers
docker-compose ps

# View logs
docker-compose logs -f

# Test health endpoints
curl http://localhost:8000/health
curl http://localhost/
```

---

## Monitoring

### View Logs

```bash
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend
```

### Check Health

```bash
# Backend health
curl http://localhost:8000/health

# Frontend health
curl http://localhost/

# Check container status
docker-compose ps
```

### Restart Services

```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart backend
docker-compose restart frontend
```

---

## Scaling

### Cloud Deployment Options

#### AWS (Amazon Web Services)

1. **Push images to ECR**
   ```bash
   aws ecr create-repository --repository-name ai-stream-backend
   aws ecr create-repository --repository-name ai-stream-frontend
   docker tag ai-stream-backend:latest <account-id>.dkr.ecr.<region>.amazonaws.com/ai-stream-backend:latest
   docker push <account-id>.dkr.ecr.<region>.amazonaws.com/ai-stream-backend:latest
   ```

2. **Deploy with ECS**
   - Create ECS cluster
   - Create task definitions for backend and frontend
   - Create services
   - Configure Application Load Balancer

#### GCP (Google Cloud Platform)

1. **Push images to GCR**
   ```bash
   gcloud builds submit --tag gcr.io/<project-id>/ai-stream-backend
   gcloud builds submit --tag gcr.io/<project-id>/ai-stream-frontend
   ```

2. **Deploy with Cloud Run**
   ```bash
   gcloud run deploy ai-stream-backend \
     --image gcr.io/<project-id>/ai-stream-backend \
     --platform managed
   ```

#### Azure

1. **Push images to ACR**
   ```bash
   az acr create --resource-group myResourceGroup --name myregistry --sku Basic
   docker tag ai-stream-backend myregistry.azurecr.io/ai-stream-backend
   docker push myregistry.azurecr.io/ai-stream-backend
   ```

2. **Deploy with AKS or Container Instances**

---

## SSL/TLS Setup

### Using Let's Encrypt with Nginx

1. **Install Certbot**
   ```bash
   sudo apt-get install certbot python3-certbot-nginx
   ```

2. **Obtain certificate**
   ```bash
   sudo certbot --nginx -d yourdomain.com
   ```

3. **Update nginx.conf** to use SSL
   ```nginx
   server {
       listen 443 ssl;
       ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
       # ... rest of config
   }
   ```

---

## Troubleshooting

### Backend won't start

```bash
# Check logs
docker-compose logs backend

# Common issues:
# - Missing API keys in .env
# - Port 8000 already in use
# - Invalid Python dependencies
```

### Frontend won't build

```bash
# Check logs
docker-compose logs frontend

# Common issues:
# - Node modules not installed
# - TypeScript errors
# - Missing environment variables
```

### WebSocket connection fails

- Ensure backend is running
- Check CORS settings in backend/main.py
- Verify nginx proxy configuration for /ws

### Health checks failing

```bash
# Backend
docker exec ai-stream-backend python -c "import requests; requests.get('http://localhost:8000/health')"

# Frontend
docker exec ai-stream-frontend wget -O- http://localhost/
```

---

## Maintenance

### Update images

```bash
git pull origin main
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Clear volumes

```bash
docker-compose down -v
```

### Cleanup unused images

```bash
docker system prune -af
```

---

## Performance Tuning

### Backend

- Increase Uvicorn workers: `CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--workers", "4"]`
- Configure Gunicorn for production workloads
- Enable Redis for caching (future enhancement)

### Frontend

- Nginx already includes gzip compression
- Static assets cached for 1 year
- Consider CDN for global distribution

---

## Security

### Best Practices

1. **Never commit .env file**
2. **Use secrets management** (AWS Secrets Manager, GCP Secret Manager)
3. **Enable HTTPS** in production
4. **Restrict CORS** to specific domains
5. **Update dependencies** regularly

### Security Scan

```bash
# Scan Docker images
docker scan ai-stream-backend:latest
docker scan ai-stream-frontend:latest
```

---

## Support

For issues and questions:
- GitHub Issues: https://github.com/YOUR_USERNAME/ai-avatar-stream/issues
- Documentation: README.md
