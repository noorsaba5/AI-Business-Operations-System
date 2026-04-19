<p align="center">
  <img src="images/banner.png" alt="AI Business Operations System Banner" width="90%">
</p>


# AI Business Operations System

An AI-powered business management dashboard built for small businesses to track sales, expenses, payroll, profit/loss, smart financial alerts, and AI-generated business insights.

---

## Project Overview

The AI Business Operations System is a Streamlit-based application designed to help small businesses monitor and manage their financial operations in one place.

This system allows users to:

- record sales
- track expenses
- manage payroll
- calculate profit and loss automatically
- view financial trends through charts
- receive smart business alerts
- generate AI-powered business insights
- interact with a GPT-style business chatbot

The project combines business intelligence, automation, and AI support into one practical system.

---

## Key Features

### Financial Tracking
- Add and manage sales records
- Add and manage expense records
- Calculate total sales, total expenses, and profit/loss

### Payroll Management
- Add employee payroll details
- Calculate salary automatically
- Track total payroll cost

### Smart Business Alerts
- Detect negative profit
- Detect high expenses compared to sales
- Detect high payroll cost compared to sales
- Highlight important business risks

### AI Business Insights
- Generate automated business performance insights
- Explain financial issues in simple business language

### Business Chat Assistant
- Ask questions about profit, sales, expenses, and payroll
- Receive business advice through a chatbot interface
- Supports GPT integration with fallback local logic

### Interactive Dashboard
- Monthly filtering
- KPI summary cards
- Sales and expense trend charts
- Recent transaction tables

---

## Tech Stack

- **Python**
- **Streamlit**
- **Pandas**
- **Matplotlib**
- **OpenAI API**
- **CSV-based data storage**

---

## Project Structure

```bash
ai-business-system/
│
├── app.py
├── sales.csv
├── expenses.csv
├── payroll.csv
├── README.md
└── requirements.txt                                                                                                                                                      
## How to Run the Project
1. Clone the repository
git clone https://github.com/your-username/ai-business-system.git
cd ai-business-system
## 2. Create and activate virtual environment
python -m venv venv
On Windows
venv\Scripts\activate
## 3. Install dependencies
pip install -r requirements.txt
## 4. Run the application
streamlit run app.py
OpenAI API Setup

If you want to use GPT-powered chatbot and AI insight features, set your OpenAI API key as an environment variable.

On Windows PowerShell
$env:OPENAI_API_KEY="your_api_key_here"

Then run:

streamlit run app.py

If no API key is provided, the app still works with built-in fallback business logic.

## Example Use Cases
Small shop owners monitoring daily sales and expenses
Small businesses tracking payroll and profit
Business users who want simple AI-based financial guidance
Portfolio demonstration of AI + analytics + dashboard development
Future Improvements
Database integration with SQLite or PostgreSQL
Edit and delete transaction records
Forecast future sales and expenses
Inventory tracking
Invoice generation
User authentication
Cloud deployment
Real-time financial alerts
More advanced GPT business assistant
Why I Built This Project

I built this project to combine business operations, analytics, and AI into one practical application that solves real small business problems.

## This project demonstrates:

business problem solving
dashboard development
financial analysis logic
data handling with Python
AI integration in a real-world system

## Author

## Noor Saba
Aspiring Data Scientist | AI & Machine Learning | Python | SQL | Power BI


---
