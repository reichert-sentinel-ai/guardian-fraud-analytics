# Guardian Architecture

**Date**: December 2024  
**Repository**: Guardian Fraud Detection  
**Version**: 1.0

**IMPORTANT**: This is a portfolio demonstration project using synthetic/sample datasets for demonstration purposes only.

---

## System Overview

Guardian is a real-time fraud detection system using XGBoost classification, graph analytics, and SHAP explainability. The system processes transaction streams to identify fraudulent activities with high accuracy and low latency.

---

## Architecture Principles

1. **Modularity**: Independent services with clear interfaces
2. **Scalability**: Horizontal scaling for high-throughput workloads
3. **Real-Time Processing**: Sub-second latency for demonstration use
4. **Explainability**: Model transparency with SHAP values
5. **Security**: Defense-in-depth, encrypted data at rest and in transit
6. **Open Source**: Full code availability for auditability

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      GUARDIAN SYSTEM                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐     ┌──────────────┐     ┌─────────────┐ │
│  │  Data Ingest │     │  ML Pipeline │     │  Alerting   │ │
│  │   (Loader)   │────▶│   (Models)   │────▶│  (Redis)    │ │
│  └──────────────┘     └──────────────┘     └─────────────┘ │
│         │                     │                     │        │
│         ▼                     ▼                     ▼        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │          PostgreSQL (Transaction Store)               │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Neo4j (Fraud Network Graph)              │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │       FastAPI Backend + React Frontend                │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Pipeline

### Stage 1: Data Ingestion
- Transaction data loaded from demonstration datasets (PaySim, Credit Card Fraud)
- Data validation and preprocessing
- Rate: Handles 10,000+ transactions/second (demonstration)
- Latency: <100ms to first processing

### Stage 2: Feature Engineering
- Transaction velocity calculation
- Network graph updates (Neo4j)
- Behavioral anomaly scoring
- Temporal feature extraction
- Output: 95+ engineered features

### Stage 3: Model Inference
- XGBoost ensemble (primary classifier)
- Graph Neural Network (network analysis - optional)
- SHAP value calculation for explainability
- Fraud probability score generation

### Stage 4: Alerting & Visualization
- Score threshold: 0.7 (configurable)
- Real-time alerts via Redis pub/sub
- Dashboard updates via WebSocket
- Incident creation for high-risk cases

---

## Database Schema

### PostgreSQL - Transactions

```sql
CREATE TABLE transactions (
    transaction_id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    amount DECIMAL(12,2),
    sender_id VARCHAR(100),
    receiver_id VARCHAR(100),
    transaction_type VARCHAR(50),
    is_fraud BOOLEAN,
    fraud_probability FLOAT,
    features JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_timestamp ON transactions(timestamp);
CREATE INDEX idx_sender ON transactions(sender_id);
CREATE INDEX idx_fraud ON transactions(is_fraud);
```

### Neo4j - Network Graph

```cypher
(:Transaction)-[:SENT_TO]->(:Transaction)
(:Account)-[:SENT]->(:Transaction)
(:Transaction)-[:PATTERN_SIMILAR]->(:Transaction {count: threshold})
```

---

## ML Model Architecture

### XGBoost Classifier
- **Features**: 95 engineered features
- **Ensemble**: 100 trees, max_depth=6
- **Performance**: 92%+ accuracy (demonstration results)
- **Training**: PaySim + Credit Card Fraud datasets (demonstration)
- **Class Imbalance**: Handled with SMOTE and class weighting

### Graph Neural Network (Optional Enhancement)
- **Framework**: PyTorch Geometric
- **Layers**: 3-layer GCN
- **Purpose**: Fraud ring detection
- **Performance**: 85% community detection accuracy (demonstration)

### SHAP Explainability
- **Method**: TreeExplainer for XGBoost
- **Output**: Feature importance per prediction
- **Latency**: <200ms per explanation
- **Visualization**: Waterfall plots, summary plots

---

## API Architecture

### FastAPI Backend

**Endpoints**:
```
POST   /api/v1/predict       - Real-time fraud prediction
GET    /api/v1/explain       - SHAP feature importance
GET    /api/v1/network       - Fraud network visualization
POST   /api/v1/alerts        - Create fraud alert
GET    /api/v1/metrics       - Model performance metrics
GET    /api/v1/health        - Health check
```

**Request/Response Schema**:
```python
# Prediction Request
{
    "transaction": {
        "amount": 1500.00,
        "sender_id": "C123456",
        "receiver_id": "C789012",
        "transaction_type": "TRANSFER",
        "timestamp": "2024-12-05T10:30:00Z"
    }
}

# Prediction Response
{
    "fraud_probability": 0.87,
    "is_fraud": true,
    "confidence": 0.92,
    "shap_values": {...},
    "top_features": [...]
}
```

---

## Frontend Architecture

### React Application
- **Framework**: React 18+ with TypeScript
- **State Management**: React Context API
- **Styling**: Tailwind CSS
- **Visualization**: D3.js, Recharts
- **Network Graphs**: Cytoscape.js

### Component Structure
```
src/
├── components/
│   ├── TransactionMonitor/
│   ├── FraudNetworkGraph/
│   ├── SHAPVisualization/
│   └── AlertManagement/
├── pages/
│   ├── Dashboard/
│   ├── Analytics/
│   └── Settings/
└── services/
    └── api.ts
```

---

## Deployment Architecture

### Docker Containerization

**Multi-stage Dockerfile**:
```dockerfile
# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Production stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose Setup

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://...
      - NEO4J_URL=bolt://...
      - REDIS_URL=redis://...
  
  postgres:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  neo4j:
    image: neo4j:5.0
    ports:
      - "7474:7474"
      - "7687:7687"
  
  redis:
    image: redis:7.0
```

---

## Performance Characteristics

### Latency Benchmarks (Demonstration)
- **P50 Latency**: 45ms
- **P95 Latency**: 85ms
- **P99 Latency**: 95ms

### Throughput (Demonstration)
- **Sustained TPS**: 10,000+
- **Peak TPS**: 15,000+

### Model Performance (Demonstration)
- **Accuracy**: 92%+
- **Precision**: 94%+
- **Recall**: 85%+
- **F1-Score**: 89%+
- **AUC-ROC**: 0.95+

---

## Security Considerations

### Data Security
- Encryption at rest (database)
- Encryption in transit (TLS)
- Secure API authentication
- Input validation and sanitization

### Model Security
- Model versioning and rollback
- A/B testing framework
- Adversarial attack detection
- Model drift monitoring

---

## Scalability

### Horizontal Scaling
- Stateless API design enables horizontal scaling
- Load balancer distribution
- Database connection pooling
- Redis caching layer

### Vertical Scaling
- Model inference optimization
- Feature caching
- Batch processing capabilities

---

## Monitoring & Observability

### Metrics
- Request latency (P50, P95, P99)
- Error rates
- Model prediction distribution
- Feature importance trends

### Logging
- Structured logging (JSON)
- Log levels (DEBUG, INFO, WARNING, ERROR)
- Correlation IDs for request tracing

### Health Checks
- API health endpoint
- Database connectivity
- Model availability
- External service dependencies

---

## Development & Testing

### Code Quality
- Type hints (Python 3.11+)
- Code formatting (Black)
- Linting (Flake8)
- Test coverage (>80% target)

### Testing Strategy
- Unit tests for models and utilities
- Integration tests for API endpoints
- End-to-end tests for critical flows
- Performance tests for latency validation

---

## Demonstration Project Notes

**Important**: This is a portfolio demonstration project using synthetic/sample datasets (PaySim, Credit Card Fraud) for demonstration purposes only. All performance metrics are demonstration results, not production claims.

### Demonstration Datasets
- PaySim: 6.4M transactions (synthetic mobile money data)
- Credit Card Fraud: 285K transactions (anonymized sample data)

### Demonstration Metrics
- All accuracy, latency, and throughput metrics are demonstration results
- Models trained on demonstration datasets
- Dashboards display demonstration data

---

## Technology Stack

### Backend
- Python 3.11+
- FastAPI 0.104+
- PostgreSQL 15+
- Neo4j 5.0+
- Redis 7.0+

### Machine Learning
- XGBoost 2.0+
- scikit-learn 1.3+
- PyTorch Geometric 2.3+ (optional)
- SHAP 0.43+

### Frontend
- React 18+
- TypeScript 5.0+
- Tailwind CSS 3.3+
- D3.js 7.8+
- Recharts 2.8+

### DevOps
- Docker 24.0+
- Docker Compose 2.23+
- GitHub Actions (CI/CD)
- AWS (deployment ready)

---

## References

- [Competitive Analysis](./docs/COMPETITIVE_ANALYSIS.md)
- [API Documentation](./docs/API_USAGE_GUIDE.md)
- [Database Schema](./docs/DATABASE_SCHEMA.md)
- [Deployment Guide](./docs/DOCKER_GUIDE.md)

---

*Last Updated: December 2024*  
*Portfolio Demonstration Project*

