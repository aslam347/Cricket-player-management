# 🏏 Cricket Player Management System (AI + Data Analytics Focused)
<br>
<br>

---
<br>

An **AI-driven cricket analytics and player management system** built using **Streamlit (frontend)**, **FastAPI (backend)** and **MySQL (database)**, designed to demonstrate **real-world Data Science, AI/ML, and backend engineering skills**.
<br>
<br>

---
<br>

This project is ideal for showcasing expertise in:
✅ Data Engineering  
✅ Sports Analytics  
✅ Machine Learning-ready architecture  
✅ API development (FastAPI)  
✅ Full-Stack Data Applications  
✅ Business Intelligence & Performance Analysis  

---
<br>

This application helps you:

- Manage and structure large-scale cricket player data  
- Automatically track and analyze player performance  
- Generate data-driven insights for selection decisions  
- Build and optimize **Best XI squads using analytics**  
- Compare players using **statistical and AI-based metrics**  
- Demonstrate real-world use cases for **Data Science & AI/ML Engineering roles**

> 🎯 **Built specifically to stand out for AI/ML Engineer, Data Scientist and Sports Analytics job roles**

---
<br>

## 🚀 Features

✅ Add, update and delete players  
✅ Role-based selection (Batsman / Bowler / All-rounder)  
✅ Smart stat validation (prevents invalid data)  
✅ Top Batsman & Top Bowler analytics dashboard  
✅ **AI-style Best XI team generator (data-driven)**  
✅ Advanced role-based charts & statistical analysis  
✅ Compact performance graphs (Matplotlib + Pandas)  
✅ AI-powered insights & summary report  
✅ Secure admin authentication  
✅ Activity logs (Data Engineering concept)  
✅ CSV export for Machine Learning model training  
✅ Modular & scalable architecture (for future ML models)

---
<br>

## 🛠 Tech Stack

| Layer        | Tool          |
|-------------|---------------|
| Frontend    | Streamlit     |
| Backend     | FastAPI       |
| Database    | MySQL         |
| ORM         | SQLAlchemy    |
| Visualization | Pandas, Matplotlib |
| Version Control | Git, GitHub |
| Logging     | Python Logging |

---
<br>

## 📁 Folder Structure

```text
Cricket-player-management/
│
├── Fast_api_learning/
│   ├── app.py              # Streamlit frontend
│   ├── backend.py          # FastAPI backend
│   ├── database_model.py   # DB schema
│   ├── basemodel.py        # Pydantic models
│   ├── db_connection.py    # MySQL connection
│   ├── activity.log        # System logs
│   └── README.md
│
├── requirements.txt
├── .gitignore
└── README.md




```

---

##  Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/aslam347/Cricket-player-management.git
cd Cricket-player-management
```

### 2. Create Virtual Environment & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate     # For Linux/Mac
venv\Scripts\activate        # For Windows

pip install -r requirements.txt
```

### 3. Setup MySQL Database

- Create a database named `cricket_db` (or your choice).
- Create the `cricket_db` table:

```sql
CREATE TABLE players (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  age INT,
  role VARCHAR(50),
  matches INT,
  runs INT,
  wickets INT,
  strike_rate FLOAT,
  economy FLOAT
);

```
- Update your MySQL credentials based on your requirements

---

##  Running the Project

### 1. Start FastAPI Backend

```bash
cd Fast_api_learning
uvicorn backend:app --reload

```

### 2. Start Streamlit Frontend

```bash
cd Fast_api_learning
streamlit run app.py

```

---

##  Dashboard Preview

📊 Dashboard Preview

📈 Best Batsman & Best Bowler analytics

📊 Role-based performance comparison

📉 Graphs using Matplotlib + Pandas

🤖 Data-driven Best XI generator

📁 CSV export (for ML training)

🔐 Secure Admin Panel

🧠 AI-style insights & summary report

---

##  TODO / Future Improvements

🔮 Future Improvements (For AI/ML Path)

- Add Machine Learning model to predict player performance

- Add LLM-based cricket match insights

- Add Power BI / Tableau dashboard

- Deploy on AWS / Azure

- Add Player Recommendation System

- Add Fantasy Cricket Team Generator
---

##  Author

**Mohamed Aslam**  
 [LinkedIn](www.linkedin.com/in/mohamed-aslam-1b99b8212)  
 [GitHub](https://github.com/aslam347)

---

##  License

MIT License

Copyright (c) 2025 Mohamed Aslam M

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND...
