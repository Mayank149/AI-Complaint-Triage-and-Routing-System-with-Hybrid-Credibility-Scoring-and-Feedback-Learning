# AI Complaint Triage & Routing System

An intelligent complaint management system that automatically classifies complaints by department and urgency level, while assessing their credibility using a hybrid scoring approach combining rule-based analysis and machine learning confidence metrics.

**Author:** Mayank Bansal

---

## Features

- **Automated Classification**: ML-powered prediction of department and urgency level
- **Hybrid Credibility Scoring**: Combines rule-based heuristics with ML confidence scores
- **Follow-up Question Generation**: Automatically suggests additional information for low-credibility complaints
- **Feedback System**: Allows users to correct predictions for continuous improvement
- **Admin Panel**: Password-protected database viewer to monitor all complaints and feedback
- **Modern UI**: Clean, responsive interface with smooth animations

---

## Hybrid Credibility Score

The system uses a **hybrid credibility scoring mechanism** that combines two approaches:

### Formula
```
Credibility Score = (0.7 × Rule Score) + (0.3 × ML Score)
```

### Components

#### 1. Rule-Based Score (70% weight)
Analyzes complaint text for specific quality indicators:

**Positive Signals (+20 points each):**
- ✅ Length ≥ 50 characters (+20)
- ✅ Time reference (dates, times, relative time)
- ✅ Location reference (room, hostel, block, floor, etc.)
- ✅ Identifiers (roll no, ID, ticket number)
- ✅ Evidence mention (screenshot, photo, attachment)

**Negative Signals:**
- ❌ Length < 20 characters (-40)
- ❌ Vague/emotional language (-20)
  - Examples: "please help", "asap", "very bad", "worst", "angry"

**Range:** 0-100 (clamped)

#### 2. ML Confidence Score (30% weight)
Average of department and urgency prediction confidence scores from the trained models:
```
ML Score = ((Department Confidence + Urgency Confidence) / 2) × 100
```

### Credibility Threshold
- **Score ≥ 60**: Complaint accepted as-is
- **Score < 60**: Follow-up questions generated to gather missing details

---

## Architecture

### Backend (Flask)
- **`app.py`**: Main Flask application with API endpoints
- **`db.py`**: SQLite database operations (complaints & feedback tables)
- **`inference.py`**: ML model loading and prediction logic
- **`credibility.py`**: Hybrid credibility scoring implementation
- **`questions.py`**: Follow-up question generation

### Frontend
- **`index.html`**: Main application interface
- **`style.css`**: Modern, responsive styling
- **`script.js`**: Client-side logic and API integration

### Machine Learning Models
- **Department Classifier**: Predicts appropriate department (IT Support, Hostels, Academics, etc.)
- **Urgency Classifier**: Predicts urgency level (Low, Medium, High)
- Both models use scikit-learn pipelines with TF-IDF vectorization

---

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "AI Complaint Triage and Routing System"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database**
   ```bash
   python db.py
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your browser and navigate to `http://127.0.0.1:5000`
   - Open `index.html` in your browser

---

## 📊 Database Schema

### Complaints Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| text | TEXT | Complaint description |
| predicted_department | TEXT | ML-predicted department |
| department_confidence | REAL | Confidence score (0-1) |
| predicted_urgency | TEXT | ML-predicted urgency |
| urgency_confidence | REAL | Confidence score (0-1) |
| credibility_score | INTEGER | Hybrid credibility score (0-100) |
| timestamp | TEXT | ISO format timestamp (IST) |

### Feedback Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| complaint_id | INTEGER | Reference to complaint |
| predicted_department | TEXT | System's prediction |
| correct_department | TEXT | User's correction |
| predicted_urgency | TEXT | System's prediction |
| correct_urgency | TEXT | User's correction |
| timestamp | TEXT | ISO format timestamp (IST) |

---

## 🔐 Admin Panel

Access the admin panel to view all complaints and feedback:

1. Click the 🔐 button in the top-right corner
2. Enter password: `admin123`
3. View both database tables with filtering and sorting

**Note:** For production deployment, change the password using environment variables.

---

## 🛠️ API Endpoints

### POST `/analyze-complaint`
Analyzes a complaint and returns predictions.

**Request:**
```json
{
  "text": "Internet not working in hostel room 204"
}
```

**Response:**
```json
{
  "department": "IT Support",
  "department_confidence": 0.95,
  "urgency": "Medium",
  "urgency_confidence": 0.87,
  "credibility_score": 78,
  "followup_questions": [],
  "complaint_id": 1
}
```

### POST `/feedback`
Submits user feedback for predictions.

### POST `/admin/authenticate`
Authenticates admin access.

### GET `/admin/database`
Returns all complaints and feedback (admin only).

---

## Dependencies

- **Flask**: Web framework
- **Flask-CORS**: Cross-origin resource sharing
- **scikit-learn**: Machine learning models
- **joblib**: Model serialization
- **numpy**: Numerical operations

---

## UI Features

- **Responsive Design**: Works on desktop and mobile
- **Real-time Validation**: Character count and input validation
- **Smooth Animations**: Fade-in effects and transitions
- **Color-coded Results**: Visual indicators for credibility levels
- **Modal Dialogs**: Clean admin authentication and data viewing

---

## License

This project is a solo work by Mayank Bansal.

---

## Future Enhancements

- [ ] Deploy to production (Render/Heroku)
- [ ] Add email notifications for high-urgency complaints
- [ ] Implement model retraining pipeline using feedback data
- [ ] Add complaint status tracking (Open/In Progress/Resolved)
- [ ] Multi-language support
- [ ] Analytics dashboard for complaint trends

---

## Contact

**Mayank Bansal**  
For questions or suggestions, please open an issue in the repository.
