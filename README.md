# 🏏 AI Cricket Analyst

An AI-powered **IPL Cricket Analytics Dashboard** that combines **data-driven insights** with **Large Language Models (LLMs)** to deliver professional cricket analysis — similar to Cricinfo-style commentary.

This project is built using **Python, Gradio, Plotly, and Groq LLM** and is deployed on **Hugging Face Spaces**.

---


I am deeply passionate about cricket and analytics. This project reflects my interest in combining **sports analytics** with **artificial intelligence** to extract meaningful insights from real IPL data.

---

## 🌐 Live Demo

👉 **Hugging Face Space:**  
https://huggingface.co/spaces/sujal05/ai-cricket-analyst

---

## 🚀 Features

- 🤖 AI-generated IPL-only cricket insights  
- 📊 Top run scorers & wicket takers analysis  
- 📈 Season-wise player performance trends  
- ⚔️ Player vs Player comparison  
- 🎨 Modern interactive dashboard UI  
- 🔐 Secure API handling using environment variables  

---

## 🧠 How the System Works (Step-by-Step)

1. IPL match and ball-by-ball data is loaded using **Pandas**
2. Statistical insights are computed (runs, wickets, strike rate, trends)
3. Key numerical facts are passed to the **Groq LLM**
4. The LLM generates **crisp, professional IPL-only analysis**
5. Results are displayed using **Gradio UI** and **Plotly charts**

---

## 🛠️ Tech Stack

- **Programming Language:** Python  
- **Frontend:** Gradio  
- **Visualization:** Plotly  
- **LLM:** Groq (LLaMA 3.1)  
- **Data Processing:** Pandas  
- **Deployment:** Hugging Face Spaces  

---

## 📁 Project Structure

AI-Cricket-Analyst/
│
├── app.py # Main application
├── matches.csv # IPL match data
├── deliveries.csv # Ball-by-ball IPL data
├── requirements.txt # Dependencies
├── .gitignore 
└── README.md


## 🔐 Environment Variables

This project uses **secure API handling**.

Set the following variable:

GROQ_API_KEY=your_api_key_here


### On Hugging Face:
- Go to **Settings → Secrets**
- Add `GROQ_API_KEY`

---

## ▶️ Run Locally

```bash
git clone https://github.com/Sujal0507/AI-Cricket-Analyst.git
cd AI-Cricket-Analyst
pip install -r requirements.txt
python app.py


## 👤 About the Author
Sujal Patel
📧 Email: sujalpatel788@gmail.com
🔗 GitHub: https://github.com/Sujal0507


**Sujal Patel**  
🎓 MSc Big Data Analytics Student  
🏏 Cricket Enthusiast & Data Science Aspirant  

