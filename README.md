# 🛍️ AI Product Recommendation Studio

A state-of-the-art AI-powered product recommendation system built with Streamlit and powered by Google Gemini AI.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

- **🤖 AI-Powered Recommendations**: Natural language product search using Google Gemini 1.5 Flash model
- **⚡ Smart Fallback Engine**: Deterministic recommendation system when AI is unavailable
- **🎨 Modern UI**: Premium dark theme with animations, glassmorphism, and responsive design
- **📦 Rich Product Catalog**: 18+ products across 6 categories (Phones, Laptops, Headphones, Smartwatches, Tablets, Accessories)
- **🔒 Secure**: API keys managed via environment variables, never exposed in code
- **☁️ Cloud-Ready**: Deployable on Streamlit Community Cloud

## 🖥️ Screenshots

The application features:
- Animated hero section with gradient backgrounds
- Interactive example query chips
- Product cards with hover effects
- Recommendation cards with match scores and progress bars
- Category filtering and budget controls

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Local Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "Recommendation system"
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API key** (optional - fallback engine works without it)
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   # Edit .streamlit/secrets.toml with your Gemini API key from https://makersuite.google.com/app/apikey
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open in browser**
   Navigate to `http://localhost:8501`

## 🔑 API Configuration

### Option 1: Streamlit Secrets (Recommended)

Create `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "your-gemini-api-key"
```

Get your free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Option 2: Environment Variable

```bash
export GEMINI_API_KEY="your-gemini-api-key"
```

### Without API Key

The application works without an API key using the smart fallback recommendation engine.

## ☁️ Streamlit Community Cloud Deployment

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub repository
   - Set main file path to `app.py`

3. **Configure Secrets**
   - In the Streamlit Cloud dashboard, go to your app settings
   - Navigate to "Secrets"
   - Add:
     ```toml
     GEMINI_API_KEY = "your-gemini-api-key"
     ```

## 📁 Project Structure

```
Recommendation system/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .gitignore                  # Git ignore rules
└── .streamlit/
    ├── config.toml             # Streamlit theme configuration
    └── secrets.toml.example    # Example secrets file
```

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Backend | Python 3.9+ |
| AI API | Google Gemini 1.5 Flash |
| SDK | google-generativeai |
| Styling | Custom CSS with animations |

## 🔌 Google Gemini API Integration

### SDK Usage
```python
import google.generativeai as genai

genai.configure(api_key="your-api-key")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(prompt)
```

### Model
- **gemini-1.5-flash**: Fast, efficient model for production use (free tier available)

### Response Schema
```json
{
  "recommendations": [
    {
      "product_id": "string",
      "match_score": 0-100,
      "reason": "string"
    }
  ],
  "summary": "string"
}
```

## 📊 Evaluation Criteria Mapping

| Criterion | Implementation |
|-----------|----------------|
| AI API Integration | Google Gemini API with gemini-1.5-flash model |
| Product Display | Rich product cards with specs, ratings, categories |
| User Input | Natural language text input with optional filters |
| Recommendations | AI-powered with structured JSON output |
| Error Handling | Graceful fallback, timeout handling, validation |
| UI/UX | Modern dark theme, animations, responsive design |
| Code Quality | Functions, type hints, clean structure |
| Security | Secrets management, no hardcoded keys |
| Deployment | Streamlit Cloud ready |

## ⚡ Fallback Recommendation Engine

When the AI API is unavailable, the system uses a deterministic fallback engine that:

1. **Parses budget** from natural language (e.g., "under $500")
2. **Extracts categories** from keywords (e.g., "laptop", "phone")
3. **Matches tags and specs** against user query
4. **Calculates relevance scores** based on:
   - Name matching
   - Description matching
   - Tag matching
   - Best-for matching
   - Budget fit bonus
   - Rating bonus
5. **Returns top 3 products** with generated reasons

## 🎨 UI Features

- **Hero Section**: Animated gradient background with floating blobs
- **Product Cards**: Hover effects, gradient borders, specs display
- **Recommendation Cards**: Match score progress bars, reason boxes
- **Example Chips**: Clickable preset queries
- **Tabs**: AI Recommender, Product Catalog, How It Works, API Status
- **Dark Theme**: Premium purple/blue color scheme

## 📝 Example Queries

Try these natural language queries:
- "I want a phone under $500"
- "Recommend a lightweight laptop for students"
- "I need headphones with good battery life"
- "Show me budget products for gaming"
- "Best smartwatch for fitness tracking"
- "Tablet for kids under $200"

## ⚠️ Known Limitations

1. **API Availability**: Requires valid Gemini API key for AI recommendations (free tier available)
2. **Static Catalog**: Product data is built-in, not from external database
3. **No Persistence**: User preferences are not saved between sessions
4. **Rate Limits**: Free tier has request limits

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io) for the amazing framework
- [Google Gemini](https://ai.google.dev/) for the AI API
- Built for demonstration and evaluation purposes
