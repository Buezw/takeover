# Calendar Takeover

![Calendar Interface](https://via.placeholder.com/800x400?text=Calendar+Takeover+Interface)

An AI-powered intelligent calendar management system, using FastAPI backend and HTML/JS frontend, integrated with DeepSeek AI for natural language event creation.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Configuration Details](#configuration-details)
- [API Documentation](#api-documentation)
- [Usage Examples](#usage-examples)
- [Troubleshooting](#troubleshooting)
- [Development Guide](#development-guide)

## 📝 Project Overview

Calendar Takeover is an intelligent calendar system that allows users to interact with an AI assistant to add and manage events using natural language. The system provides an intuitive dark theme interface, responsive design, and powerful natural language processing capabilities.

This project aims to simplify the calendar management experience, enabling users to create complex schedules through conversational interactions without cumbersome forms or complex time pickers.

## ✨ Features

- **🗓️ Dark Theme Calendar**: Aesthetic dark UI supporting month and day views
- **🤖 AI Assistant**: Add and modify events using natural language
- **📊 Event Visualization**: Display events visually on the calendar with detailed information
- **🔄 Flexible Navigation**: Easily switch between months and jump to today
- **📱 Responsive Design**: Adaptable to devices of different screen sizes
- **🚀 High Performance**: Frontend-backend separation architecture for smooth experience
- **🧩 Extensibility**: Modular design for easy addition of new features

## 🏗️ System Architecture

The project adopts a microservice architecture with frontend and backend separation:

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│             │       │             │       │             │
│  Frontend   │◄─────►│  Main API   │◄─────►│  DeepSeek   │
│ HTML/JS/CSS │       │   FastAPI   │       │     API     │
│             │       │             │       │             │
└─────────────┘       └──────┬──────┘       └─────────────┘
                             │
                      ┌──────▼──────┐
                      │             │
                      │  AI Chat    │
                      │  Microservice │
                      │             │
                      └─────────────┘
```

1. **Frontend**: Single-page application implemented with HTML/CSS/JavaScript
   - Renders the calendar interface
   - Manages user interactions
   - Communicates with the backend via API

2. **Main Backend**: FastAPI service handling calendar events and basic functionalities
   - CRUD operations for events
   - Data storage and management
   - Communication with the frontend

3. **AI Chat Microservice**: FastAPI service dedicated to natural language processing
   - Receives chat messages
   - Calls DeepSeek API to parse user intent
   - Returns structured event data to the main service

4. **DeepSeek AI**: Provides powerful natural language processing capabilities
   - Converts user natural language into structured data
   - Supports various time expressions and event descriptions

## 🛠️ Tech Stack

- **Frontend**:
  - HTML5, CSS3, JavaScript
  - Pure native implementation, no external dependencies
  - Responsive grid layout

- **Backend**:
  - Python 3.8+
  - FastAPI framework
  - Uvicorn ASGI server
  - HTTPX asynchronous HTTP client

- **AI Service**:
  - DeepSeek API
  - Custom prompt engineering

- **Storage**:
  - Current version: In-memory storage
  - Extensible: Supports database storage

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- DeepSeek API Key

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/takeover.git
   cd takeover
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv takeover_env
   # Windows
   takeover_env\Scripts\activate
   # Linux/macOS
   source takeover_env/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install fastapi uvicorn httpx requests
   ```

4. **Configure API Key**
   Set your DeepSeek API key in `config.py`:
   ```python
   DEEPSEEK_API_KEY = "your-api-key-here"
   ```

5. **Start Services**
   ```bash
   # Use run.py to start all services
   python run.py
   ```

6. **Access the Application**
   Open the `calender.html` file in your browser.

## ⚙️ Configuration Details

### Configuration File

The main configuration is in the `config.py` file:

```python
# DeepSeek API Configuration
DEEPSEEK_API_KEY = "your-api-key-here"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# Error Messages Configuration
ERROR_MESSAGES = {
    "parse_error": "Sorry, I couldn't understand your input...",
    "api_error": "Sorry, the AI service is temporarily unavailable...",
    "validation_error": "Please ensure the event date and title are provided..."
}

# AI Prompt Template
EVENT_PROMPT = '''
You are a calendar assistant. Please convert user input into structured event data...
'''
```

### Server Port Configuration

- **Main Service**: Default port `8079`
- **AI Chat Service**: Default port `8181`

You can modify these via command-line arguments:

```bash
uvicorn server:app --host 127.0.0.1 --port <custom-port>
```

### Frontend Configuration

Frontend API endpoint configuration is in `calender.html`:

```javascript
// API Endpoint Configuration
const API_BASE = ''; // Default is relative path
// To modify to an absolute path, for example:
// const API_BASE = 'http://127.0.0.1:8079';
```

## 📚 API Documentation

### Main Service API (Port 8079)

#### Get Events

- **GET** `/api/events`
  - Retrieve all events
  - Returns: Array of events

- **GET** `/api/events?date=YYYY-MM-DD`
  - Retrieve events for a specific date
  - Parameters: `date` - ISO format date string
  - Returns: Array of events

- **GET** `/api/events?year=YYYY&month=MM`
  - Retrieve events for a specific month
  - Parameters: `year` - Year, `month` - Month (1-12)
  - Returns: Array of events

#### Debug Endpoint

- **GET** `/debug`
  - Retrieve service status information
  - Returns: Debug information object

### AI Chat Service API (Port 8181)

#### Chat Interface

- **POST** `/chat`
  - Process user chat messages
  - Request Body: `{ "message": "User message" }`
  - Returns:
    ```json
    {
      "response": "AI reply message",
      "event": { 
        "title": "Event title",
        "date": "2024-01-01",
        "time_start": "15:00",
        "time_end": "16:00",
        "description": "Event description"
      }
    }
    ```
  - Note: When unable to parse events, the `event` field is `null`.

### Event Data Structure

```json
{
  "title": "Event title",
  "date": "YYYY-MM-DD",
  "time_start": "HH:MM",
  "time_end": "HH:MM",
  "description": "Event description"
}
```

## 🎯 Usage Examples

### 1. Add Events via AI Assistant

![Add Event](https://via.placeholder.com/800x400?text=Add+Event)

1. Enter in the left chat box:
   ```
   Add a team meeting tomorrow at 3 PM
   ```
2. The AI assistant will parse your intent and extract key information.
3. The system automatically creates the event and displays it on the calendar.

### 2. View Date Details

![Date Details](https://via.placeholder.com/800x400?text=Date+Details)

1. Click on any date in the calendar.
2. The right sidebar will display all events for that date.
3. View detailed information about events, including time and description.

### 3. Month Navigation

![Month Navigation](https://via.placeholder.com/800x400?text=Month+Navigation)

1. Use the top arrow buttons to switch between months.
2. Click the "Today" button to quickly jump to the current day.

## 🔍 Troubleshooting

### Common Issues

1. **AI Service Connection Failure**
   - Check if the DeepSeek API key is correct.
   - Verify network connection status.
   - Check AI service logs.

2. **Events Not Displayed on Calendar**
   - Ensure server port configuration is correct.
   - Check browser console for errors.
   - Validate event format.

3. **Natural Language Parsing Inaccuracy**
   - Try using more explicit language to describe events.
   - Check if the EVENT_PROMPT template is configured correctly.
   - Consider adjusting API parameters to lower the temperature value.

### Error Debugging

The project includes two test scripts:

- `test_api.py`: Comprehensive testing of DeepSeek API connection.
- `simple_test.py`: Simplified end-to-end testing.

Run these scripts to verify the working status of system components:

```bash
python test_api.py
python simple_test.py
```

### Logging

Both main services include detailed logging:

```bash
# View main service logs
uvicorn server:app --log-level debug

# View AI service logs
uvicorn chat_service:app --log-level debug
```

## 👨‍💻 Development Guide

### Project Structure

```
e:\OneDrive\Gits\takeover\
│
├── calender.html        # Frontend interface
├── server.py            # Main backend service
├── chat_service.py      # AI chat microservice
├── config.py            # Configuration file
├── test_api.py          # API test script
└── simple_test.py       # Simplified test script
```

### Extend Event Storage

The current version uses in-memory storage for events, which can be extended to use a database:

```python
# Add database support in server.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./calendar.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Create event model
class EventModel(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    date = Column(String)
    time_start = Column(String, nullable=True)
    time_end = Column(String, nullable=True)
    description = Column(String, nullable=True)
```

### Add New Features

Extend AI chat functionality to support more operations:

```python
# Add more intent handling in chat_service.py
async def chat_with_ai(message: ChatMessage):
    user_message = message.message.lower()
    
    if any(keyword in user_message for keyword in ["add", "create", "schedule"]):
        # Handle logic for adding events
        return await handle_create_event(user_message)
    
    elif any(keyword in user_message for keyword in ["find", "search", "show"]):
        # Handle logic for finding events
        return await handle_search_event(user_message)
    
    elif any(keyword in user_message for keyword in ["cancel", "delete", "remove"]):
        # Handle logic for deleting events
        return await handle_delete_event(user_message)
        
    else:
        # Handle general conversation
        return {"response": "I am your calendar assistant..."}
```

## 📜 License

This project is for learning and research purposes only.

---

For any questions or suggestions, feel free to submit an Issue or Pull Request. 