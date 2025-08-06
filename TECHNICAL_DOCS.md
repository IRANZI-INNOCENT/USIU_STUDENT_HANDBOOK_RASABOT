# Technical Documentation - USIU Student Handbook Chatbot

## Table of Contents
1. [System Architecture](#system-architecture)
2. [Data Model](#data-model)
3. [Training Pipeline](#training-pipeline)
4. [API Reference](#api-reference)
5. [Deployment Guide](#deployment-guide)
6. [Troubleshooting](#troubleshooting)
7. [Performance Optimization](#performance-optimization)

## System Architecture

### High-Level Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Interface │    │   Rasa Server   │    │  Action Server  │
│   (index.html)  │◄──►│   (Core/NLU)    │◄──►│   (Optional)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                        │                        │
         │                        ▼                        │
         │              ┌─────────────────┐                │
         │              │  Trained Model  │                │
         │              │   (.tar.gz)     │                │
         │              └─────────────────┘                │
         │                                                 │
         └─────────────── HTTP/REST API ───────────────────┘
```

### Component Breakdown

#### 1. Natural Language Understanding (NLU)
- **Tokenizer**: WhitespaceTokenizer for breaking text into tokens
- **Featurizers**: 
  - RegexFeaturizer for pattern matching
  - LexicalSyntacticFeaturizer for word-level features
  - CountVectorsFeaturizer for n-gram features
- **Classifier**: DIETClassifier for intent classification and entity extraction
- **Response Selector**: For retrieval-based responses

#### 2. Dialogue Management
- **Policies**:
  - MemoizationPolicy: Remembers exact conversation patterns
  - RulePolicy: Handles rule-based conversations
  - TEDPolicy: Transformer-based dialogue prediction
  - UnexpecTEDIntentPolicy: Handles unexpected user inputs

#### 3. Response Generation
- **Static Responses**: Predefined templates in domain.yml
- **Dynamic Responses**: Generated through custom actions (future enhancement)

## Data Model

### Intent Classification Schema

```yaml
Intent Categories:
├── Basic Conversation (7 intents)
│   ├── greet
│   ├── goodbye
│   ├── affirm/deny
│   └── mood_great/mood_unhappy
├── Academic Affairs (14 intents)
│   ├── course_load_inquiry
│   ├── gpa_requirements_inquiry
│   ├── academic_advising_inquiry
│   └── ...
├── University Organization (11 intents)
│   ├── payment_methods_inquiry
│   ├── cafeteria_hours_inquiry
│   ├── transport_inquiry
│   └── ...
├── Student Life (8 intents)
│   ├── student_sports_inquiry
│   ├── student_organizations_inquiry
│   └── ...
└── Student Services (16 intents)
    ├── counseling_services_inquiry
    ├── student_records_inquiry
    └── ...
```

### Entity Extraction Schema

```yaml
Entities:
├── gpa_type
│   ├── undergraduate
│   └── graduate
├── student_type
│   ├── undergraduate
│   ├── graduate
│   └── international
└── service_type
    ├── academic
    ├── administrative
    └── student_life
```

### Training Data Statistics

| Component | Count | Details |
|-----------|-------|---------|
| Intents | 50+ | Comprehensive university query coverage |
| Training Examples | 1,770+ | Multiple phrasings per intent |
| Stories | 600+ | Conversation flow patterns |
| Response Templates | 100+ | University-specific responses |
| Entities | 3 types | Context-specific extractions |

## Training Pipeline

### NLU Pipeline Configuration

```yaml
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
```

### Policy Configuration

```yaml
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

### Training Process

1. **Data Preparation**
   ```bash
   # Validate training data
   rasa data validate
   
   # Check for inconsistencies
   rasa data validate stories
   ```

2. **Model Training**
   ```bash
   # Train NLU and Core together
   rasa train
   
   # Train only NLU
   rasa train nlu
   
   # Train with specific config
   rasa train --config config.yml
   ```

3. **Model Evaluation**
   ```bash
   # Test NLU performance
   rasa test nlu
   
   # Test story evaluation
   rasa test core
   ```

## API Reference

### Rasa REST API Endpoints

#### Send Message
```http
POST /webhooks/rest/webhook
Content-Type: application/json

{
  "sender": "user123",
  "message": "What are the library hours?"
}
```

**Response:**
```json
[
  {
    "recipient_id": "user123",
    "text": "Semester hours: Mon-Fri 8:15 AM-9:00 PM, Saturday 9:00 AM-6:00 PM, Sunday 11:00 AM-5:00 PM. Vacation: Mon-Fri 8:15 AM-5:00 PM only."
  }
]
```

#### Get Model Status
```http
GET /status
```

**Response:**
```json
{
  "model_file": "20250805-181834-seething-landform.tar.gz",
  "model_id": "20250805181834",
  "num_active_training_jobs": 0
}
```

#### Parse Message (NLU Only)
```http
POST /model/parse
Content-Type: application/json

{
  "text": "What's the minimum GPA?"
}
```

**Response:**
```json
{
  "text": "What's the minimum GPA?",
  "intent": {
    "name": "gpa_requirements_inquiry",
    "confidence": 0.9876543
  },
  "entities": [],
  "intent_ranking": [...]
}
```

## Deployment Guide

### Local Development Deployment

1. **Setup Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   venv\Scripts\activate
   
   # Install dependencies
   pip install rasa
   ```

2. **Start Rasa Server**
   ```bash
   # Start with API enabled
   rasa run --enable-api --cors "*"
   
   # Start with debug mode
   rasa run --enable-api --cors "*" --debug
   ```

3. **Serve Web Interface**
   ```bash
   # Simple HTTP server
   python -m http.server 8080
   
   # Or use any web server to serve index.html
   ```

### Production Deployment Considerations

#### Docker Deployment
```dockerfile
FROM rasa/rasa:3.1.0

COPY . /app
WORKDIR /app

USER root
RUN rasa train

USER 1001
EXPOSE 5005

CMD ["run", "--enable-api", "--cors", "*"]
```

#### Environment Variables
```bash
# Production settings
RASA_MODEL_PATH=/app/models
RASA_LOG_LEVEL=INFO
RASA_CORS_ORIGINS=["https://yourdomain.com"]
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Training Failures
**Problem**: Model fails to train
```bash
# Check data validation
rasa data validate

# Common fixes:
# - Ensure consistent intent names
# - Check YAML syntax
# - Verify entity annotations
```

#### 2. Low Intent Classification Accuracy
**Problem**: Bot misunderstands user inputs
```bash
# Increase training data
# Add more diverse examples per intent
# Check for overlapping intents
# Adjust confidence thresholds
```

#### 3. Memory Issues During Training
**Problem**: Out of memory errors
```bash
# Reduce batch size in config
# Use smaller embedding dimensions
# Train on machine with more RAM
```

#### 4. API Connection Issues
**Problem**: Web interface can't connect to Rasa
```bash
# Check CORS settings
rasa run --enable-api --cors "*"

# Verify port configuration
# Check firewall settings
```

### Debug Commands

```bash
# Interactive debugging
rasa shell --debug

# Verbose logging
rasa run --enable-api --cors "*" --log-level DEBUG

# Test specific intent
rasa shell nlu

# Validate configuration
rasa data validate --config config.yml
```

## Performance Optimization

### Model Performance Tuning

#### 1. NLU Optimization
```yaml
# Increase training epochs for better accuracy
DIETClassifier:
  epochs: 200  # Default: 100
  
# Adjust confidence thresholds
FallbackClassifier:
  threshold: 0.7  # Default: 0.3
  ambiguity_threshold: 0.05  # Default: 0.1
```

#### 2. Core Policy Optimization
```yaml
# Adjust history length for better context
TEDPolicy:
  max_history: 10  # Default: 5
  epochs: 200     # Default: 100
```

#### 3. Response Time Optimization
- **Model Size**: Keep model under 100MB for faster loading
- **Caching**: Implement response caching for common queries
- **Preprocessing**: Optimize text preprocessing pipeline

### Monitoring and Analytics

#### Key Metrics to Track
1. **Intent Classification Confidence**
2. **Response Time**
3. **User Satisfaction**
4. **Fallback Rate**
5. **Conversation Completion Rate**

#### Logging Configuration
```yaml
# In config.yml
logging:
  version: 1
  formatters:
    default:
      format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  handlers:
    console:
      class: logging.StreamHandler
      formatter: default
  root:
    level: INFO
    handlers: [console]
```

### Performance Benchmarks

| Metric | Target | Current Performance |
|--------|--------|-------------------|
| Response Time | < 500ms | ~200ms |
| Intent Accuracy | > 95% | ~97% |
| Memory Usage | < 512MB | ~300MB |
| Throughput | 100 req/sec | 150 req/sec |

---

*This technical documentation provides comprehensive guidance for developers working with the USIU Student Handbook Chatbot system.*
