# AI Tutor  
### AI-Driven Learning Analytics and Personalized Study Assistant

AI Tutor is an intelligent learning analytics system that analyzes student performance, identifies weak topics, and provides personalized insights to improve learning outcomes.  
The system uses machine learning and NLP techniques to evaluate attempts, track progress, and support data-driven academic improvement through an interactive dashboard.

---

## ⚠️ Disclaimer
This application is intended **for educational and demonstration purposes only**.  
It is not a replacement for professional academic guidance or certified assessment systems.

---

## 🔑 Key Highlights
- AI-based student performance analysis
- Weak-topic identification using ML
- Personalized learning insights
- Student and admin dashboards
- Data-driven progress visualization
- Suitable for academic projects and demos

---

## ✨ Features
- Student authentication and secure login
- AI-driven weak-topic prediction
- Performance analytics (accuracy, attempts, response time)
- Personalized feedback and insights
- Interactive student dashboard
- Admin panel for managing students and attempts
- Real-time data updates
- Clean and user-friendly UI
- Scalable and modular architecture
- Supports multiple students
- Designed for learning analytics research

---

## 🛠️ Tech Stack
- **Backend:** Python, FastAPI  
- **Frontend:** Streamlit  
- **AI / ML:** Machine Learning, NLP  
- **Database:** SQLite / PostgreSQL (configurable)  
- **Environment:** Python Virtual Environment  

---
## ▶️ Run from Terminal

Follow the steps below to set up and run the application locally.

### 1️⃣ Start  The Backend

python -m venv venv
venv\Scripts\activate
uvicorn backend.main:app --reload

### Start The Frontend
streamlit run frontend/dashboard.py




## 📂 Project Structure
```text
AI-Tutor/
├── backend/
│   ├── main.py
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── database.py
├── frontend/
│   └── dashboard.py
├── requirements.txt
└── README.md
