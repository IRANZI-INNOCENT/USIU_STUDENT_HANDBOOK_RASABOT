# USIU Student Handbook Chatbot 🤖

## Project Overview

The USIU Student Handbook Chatbot is an intelligent conversational AI system designed to assist students at the United States International University (USIU) with quick access to essential university information. Built using the Rasa framework, this chatbot provides instant responses to common student queries about academic affairs, university services, student life, and administrative procedures.

## 🎯 Purpose & Objectives

- **Instant Information Access**: Provide 24/7 access to university policies and procedures
- **Improved Student Experience**: Reduce wait times for getting answers to common questions
- **Administrative Efficiency**: Decrease workload on university staff by automating responses to frequently asked questions
- **User-Friendly Interface**: Offer an intuitive web-based chat interface for easy interaction

## 🏗️ System Architecture

### Technology Stack
- **Framework**: Rasa 3.1 (Open Source Conversational AI)
- **Language**: Python 3.8+
- **NLU Pipeline**: Default Rasa pipeline with DIET classifier
- **Frontend**: HTML5, CSS3, JavaScript, Tailwind CSS
- **Deployment**: Local development environment

### Core Components

1. **Natural Language Understanding (NLU)**
   - Intent classification for 50+ different student queries
   - Entity extraction for specific information (GPA types, student classifications)
   - Support for multiple ways of asking the same question

2. **Dialogue Management**
   - Rule-based responses for specific queries
   - Story-driven conversation flows
   - Context-aware conversations

3. **Response Generation**
   - Pre-defined responses for university policies
   - Dynamic content based on user context
   - Multi-turn conversation support

## 📋 Features & Capabilities

### Academic Information
- **Course Load Requirements**: Minimum units for undergraduate and graduate students
- **GPA Requirements**: Academic standing policies and probation procedures
- **Academic Advising**: Contact information and services provided
- **Attendance Policies**: Class attendance requirements and medical absence procedures
- **Registration**: Course registration and transfer credit information
- **Graduation Requirements**: Degree completion criteria

### University Services
- **Library Services**: Hours, borrowing policies, fines, study spaces, and resources
- **Payment Methods**: Accepted payment options and deferred payment plans
- **Transportation**: University transport services
- **Cafeteria**: Operating hours and rules
- **ICT Services**: Technology support and regulations

### Student Life
- **Student Organizations**: Clubs and societies information
- **Sports & Recreation**: Athletic programs and facilities
- **Leadership Opportunities**: Student government and leadership roles
- **Campus Life**: General student life information
- **International Students**: Services for international student community

### Administrative Services
- **Student Records**: Academic records and transcript services
- **Student Conduct**: Disciplinary policies and procedures
- **Housing**: Student hostel information
- **Emergency Services**: Fire safety and emergency procedures

## 📊 Technical Implementation

### Intent Recognition
The system recognizes 50+ different intents categorized into:
- **Basic Conversation** (7 intents): Greetings, goodbyes, affirmations
- **Academic Affairs** (14 intents): Course-related queries
- **University Organization** (11 intents): Administrative services
- **Student Life** (8 intents): Campus life and activities
- **Student Services** (16 intents): Support services

### Training Data
- **1,770+ training examples** across all intents
- **664 conversation stories** for dialogue flow training
- **Multiple phrasings** for each intent to improve recognition accuracy

### Response System
- **100+ predefined responses** covering all major university topics
- **Context-aware responses** that adapt based on conversation flow
- **Fallback mechanisms** for unrecognized queries

## 🚀 Getting Started

### Prerequisites
```bash
Python 3.8+
pip (Python package manager)
```

### Installation
1. **Clone the repository**
   ```bash
   git clone [repository-url]
   cd rasahandbook
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install rasa
   ```

4. **Train the model**
   ```bash
   rasa train
   ```

5. **Run the chatbot**
   ```bash
   # Terminal interface
   rasa shell
   
   # Web interface
   rasa run --enable-api --cors "*"
   # Then open index.html in a web browser
   ```

## 💻 Usage Examples

### Sample Conversations

**Academic Query:**
```
User: What's the minimum GPA required?
Bot: Undergraduate students need minimum 2.0 GPA; graduate students need 3.0 GPA. Poor performance leads to Warning → Probation → Dismissal. Students can appeal dismissal within 10 working days.
```

**Library Information:**
```
User: What are the library hours?
Bot: Semester hours: Mon-Fri 8:15 AM-9:00 PM, Saturday 9:00 AM-6:00 PM, Sunday 11:00 AM-5:00 PM. Vacation: Mon-Fri 8:15 AM-5:00 PM only.
```

**Course Load Query:**
```
User: How many courses should I take?
Bot: Undergraduate students need minimum 9 units (full-time is 12 units/4 courses). Graduate students need minimum 6 units (full-time is 9 units).
```

## 📁 Project Structure

```
rasahandbook/
├── actions/                 # Custom action files
│   ├── __init__.py
│   └── actions.py          # Custom Python actions
├── data/                   # Training data
│   ├── nlu.yml            # Intent examples and entities
│   ├── rules.yml          # Conversation rules
│   └── stories.yml        # Training stories
├── models/                # Trained models
├── tests/                 # Test stories
├── config.yml             # Rasa configuration
├── domain.yml             # Domain definition
├── endpoints.yml          # API endpoints
├── credentials.yml        # Channel credentials
├── index.html             # Web interface
└── README.md             # This documentation
```

## 🔧 Configuration

### Rasa Configuration (`config.yml`)
- **Language**: English
- **Pipeline**: Default Rasa pipeline with DIET classifier
- **Policies**: Memoization, Rule, and TED policies for dialogue management

### Domain Configuration (`domain.yml`)
- **Intents**: 50+ categorized intents
- **Entities**: GPA types, student classifications, service types
- **Slots**: Context variables for conversation state
- **Responses**: 100+ predefined university responses

## 🎨 User Interface

The web interface features:
- **Modern Design**: Clean, responsive layout using Tailwind CSS
- **USIU Branding**: University colors (Navy Blue #002855, Gold #FFC72C)
- **Chat Interface**: Familiar messaging-style interaction
- **Mobile-Friendly**: Responsive design for all devices
- **Accessibility**: Clear typography and color contrast

## 📈 Performance & Metrics

### Model Performance
- **Intent Classification Accuracy**: Optimized through extensive training data
- **Response Relevance**: High accuracy for university-specific queries
- **Coverage**: Comprehensive coverage of student handbook topics

### System Capabilities
- **Response Time**: Near-instantaneous responses
- **Availability**: 24/7 operational capability
- **Scalability**: Can handle multiple concurrent users
- **Maintainability**: Easy to update with new university policies

## 🔮 Future Enhancements

### Planned Features
1. **Database Integration**: Connect to live university databases for real-time information
2. **Multilingual Support**: Add support for multiple languages
3. **Advanced NLU**: Implement more sophisticated natural language understanding
4. **Analytics Dashboard**: Track usage patterns and popular queries
5. **Mobile App**: Develop native mobile applications
6. **Voice Interface**: Add speech-to-text and text-to-speech capabilities

### Potential Integrations
- **Student Information System**: Direct access to student records
- **Course Management System**: Real-time course availability
- **Event Calendar**: University events and deadlines
- **Directory Services**: Staff and faculty contact information

## 🤝 Contributing

### Development Guidelines
1. Follow Rasa best practices for conversation design
2. Maintain consistent response formatting
3. Test all new intents thoroughly
4. Update documentation for any changes
5. Ensure responses reflect current university policies

### Adding New Features
1. Update `nlu.yml` with new intent examples
2. Add corresponding responses in `domain.yml`
3. Create training stories in `stories.yml`
4. Test and retrain the model
5. Update documentation

## 📞 Support & Contact

For technical support or questions about the chatbot:
- **Project Developer**: [Your Name]
- **Course**: [Course Name/Number]
- **Institution**: United States International University (USIU)
- **Date**: Summer 2025

## 📄 License

This project is developed for educational purposes as part of coursework at USIU. All university-specific information is sourced from official USIU documentation and policies.

## 🙏 Acknowledgments

- **Rasa Community**: For providing excellent documentation and support
- **USIU Administration**: For access to university policies and procedures
- **Course Instructors**: For guidance and project requirements
- **Beta Testers**: Students who provided feedback during development

---

*This chatbot represents a comprehensive solution for improving student access to university information while demonstrating advanced conversational AI capabilities using the Rasa framework.*
