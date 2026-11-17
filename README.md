# AI-Powered Personal Expense Tracker

## Project Overview
The AI-Powered Personal Expense Tracker is a web application that helps users manage their income and expenses. It provides a dashboard to track financial activity, visualize spending patterns, and receive AI-powered suggestions to improve spending habits.

## Features
- Add, edit, and delete income and expense transactions.
- Search and filter transactions.
- Dashboard displaying total income, expenses, and balance.
- Visual reports using Chart.js.
- Expense analysis using Pandas.
- AI-powered spending suggestions using Google Gemini.
- AI Finance Assistant to answer questions about financial data.

## Technologies Used
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **Database:** MySQL
- **Data Analysis:** Pandas
- **AI Integration:** Google Gemini API
- **Data Visualization:** Chart.js
- **Version Control:** Git and GitHub

## Project Structure

```text
AI_Expense_Tracker/
├── app.py
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
├── .env
└── .gitignore
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Nikhitha3344/AI-Powered-Personal-Expense-Tracker.git
cd AI-Powered-Personal-Expense-Tracker
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
```

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Required Libraries

```bash
pip install flask mysql-connector-python pandas python-dotenv google-genai
```

### 4. Configure MySQL

- Start MySQL using XAMPP.
- Create a database named `expense_tracker`.
- Create the `transactions` table with the required columns: `id`, `description`, `amount`, `category`, `type`, and `date`.
- Ensure the database connection settings in `app.py` match your local MySQL configuration.

### 5. Configure Gemini API

Create a `.env` file in the project root and add your Gemini API key:

```text
GEMINI_API_KEY=your_gemini_api_key
```

Keep your API key private. Do not upload the `.env` file to GitHub.

### 6. Run the Application

```bash
python app.py
```

Open the following URL in your browser:

```text
http://127.0.0.1:5000/
```

## Future Enhancements
- More detailed financial reports.
- Additional budgeting and savings features.
- Improved AI-powered financial insights.

## Author
Developed as an individual project.
