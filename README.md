# Workforce Readiness AI Platform

![Python](https://img.shields.io/badge/Language-Python_3.9+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![Scikit-Learn](https://img.shields.io/badge/ML-Scikit_Learn-F7931E?style=for-the-badge&logo=scikit-learn)

An enterprise-grade **AI-powered Workforce Analytics Platform** that uses **Random Forest classifiers** to predict employee performance trajectories and recommend optimal career paths. Built with a premium **Glassmorphism UI**, the platform provides HR managers with deep talent intelligence and gives interns a personalized AI Virtual Mentor.

## 🌟 Key Features

### For HR Managers
- **Strategic Talent Overview**: Real-time KPI dashboard tracking workforce size, engagement scores, attrition risk rates, and task efficiency.
- **AI Performance Prediction**: Train a Random Forest model on 5,000+ synthetic employee records to predict whether an employee's performance trend is **Improving**, **Stable**, or **Declining**.
- **Career Path Predictor**: A secondary ML model analyzes technical assessment scores to recommend the best-fit department for each intern post-internship.
- **Automated PDF Reports**: Generate premium, color-coded performance reports with AI-highlighted risk indicators, downloadable as professional PDF documents.
- **Employee CRUD Operations**: Full lifecycle management — Add, View, Compare (multi-select skill matrix), and Remove employees.

### For Interns
- **AI Virtual Mentor**: Personalized coaching based on real-time metrics. If performance is declining, the AI generates a specific weekly action plan targeting stress, productivity, engagement, and upskilling.
- **Performance Rings**: Plotly gauge charts benchmarking the intern's Task Completion, Attendance, and Engagement against their department average.
- **Skill Matrix Comparison**: Side-by-side grouped bar charts comparing the intern's scores against the department mean across 6 core metrics.
- **4-Week Trajectory**: Seeded trend line visualization showing performance evolution over the last 4 weeks.

## 🧠 System Architecture

```text
┌─────────────────────────────────────────────┐
│              Streamlit Frontend              │
│         (Glassmorphism Dark Theme)           │
├──────────┬──────────────┬───────────────────┤
│  Auth    │  HR Portal   │  Intern Portal    │
│  Module  │  (CRUD + AI) │  (Mentor + Rings) │
├──────────┴──────────────┴───────────────────┤
│           Random Forest Classifier           │
│     (Performance Trend + Career Path)        │
├─────────────────────────────────────────────┤
│              CSV Data Layer                  │
│     (Workforce Dataset + User Auth DB)       │
└─────────────────────────────────────────────┘
```

## 🛠️ Technology Stack

- **Frontend**: Streamlit with custom CSS (Glassmorphism, Lottie Animations)
- **Machine Learning**: Scikit-Learn (Random Forest Classifier, Label Encoding, Train/Test Split)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly (Gauge Charts, Line Charts, Grouped Bar Charts)
- **Report Generation**: FPDF (Premium formatted PDF exports)
- **Authentication**: SHA-256 password hashing, SMTP OTP verification

## 🚀 Quick Start

### Prerequisites
- Python 3.9+

### Installation

1. Clone the repository
```bash
git clone https://github.com/Shiva-keerth/Workforce-Readiness-AI.git
cd Workforce-Readiness-AI
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the Application
```bash
streamlit run app.py
```

## 📁 Project Structure

```
Workforce-Readiness-AI/
├── app.py                  # Main entry point & routing logic
├── config.py               # Theme, CSS, constants, helper functions
├── helpers.py              # Data persistence, auth utilities, OTP
├── auth.py                 # Login/Register with OTP verification
├── hr_portal.py            # HR Dashboard, AI Models, PDF Reports
├── intern_portal.py        # Intern Dashboard, AI Mentor, Charts
├── intern dataset.csv      # Workforce analytics dataset (5000+ records)
├── requirements.txt        # Python dependencies
└── .gitignore
```

## 📊 AI Models

| Model | Algorithm | Purpose | Accuracy |
|-------|-----------|---------|----------|
| Performance Predictor | Random Forest (150 trees) | Predict Improving/Stable/Declining trends | ~92% |
| Career Path Recommender | Random Forest (100 trees) | Recommend best-fit department | ~88% |

## 📈 Scalability

While this prototype uses CSV-based storage, the modular architecture is designed to scale by replacing the CSV layer with PostgreSQL and deploying the Streamlit app on a cloud platform like AWS EC2 or Streamlit Community Cloud.

## 👤 Author

**Shiva Keerth G** — [LinkedIn](https://www.linkedin.com/in/shiva-keerth-9574b92a6/) | [GitHub](https://github.com/Shiva-keerth)
