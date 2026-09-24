# Finz AI-Native Financial Review Challenge
Finz --- AI Financial Review Platform

An AI-native financial review application built for the FINZ Software
Engineering Internship Challenge.

Live Application

Frontend: https://finz-financial-review.vercel.app/

Backend: Deployed on Render.

Core Workflow

Raw Transaction File
        ↓
     Ingestion
        ↓
   Categorization
        ↓
 Review / Correction
        ↓
 Deterministic P&L
        ↓
 Variance Analysis
        ↓
 AI Financial Analyst
        ↓
 Transaction-Level Evidence

The application separates deterministic financial computation from
LLM-based reasoning:

Financial totals and calculations are performed by backend code.

Transaction classification uses deterministic rules with confidence
scores and review flags.

The LLM is used for natural-language financial analysis and
explanation.

AI responses are grounded in application data and transaction
evidence.

Features

Transaction Ingestion

Users can upload a raw bank transaction Excel file. The system validates
the required columns, parses the data, and stores transactions in
PostgreSQL.

Expected columns:

Transaction ID
Date
Description
Counterparty
Amount
Method

A newly uploaded dataset replaces the currently loaded dataset.

Transaction Categorization

Transactions are classified into categories such as:

Revenue

Food

Beverage

Payroll

Rent

Utilities

Marketing

Insurance

Cleaning

Delivery Commission

Refunds & Discounts

Office/Admin Supplies

Repairs & Maintenance

POS/Software Subscription

Accounting/Bookkeeping

To-go Packaging & Disposables

Equipment

Loan Repayment

Owner Distribution

Sales Tax

Gift Card Liability

Each transaction stores its category, confidence, review status, and
accounting treatment.

Human Review & Correction

Lower-confidence classifications are placed into a review queue. Users
can change the category and accounting treatment. After correction, the
transaction is marked as reviewed and its confidence is set to 1.0.

Accounting Treatment

Transactions can be assigned:

P&L
Balance Sheet
Equity

Examples:

Equipment purchases → Balance Sheet

Loan principal repayment → Balance Sheet

Sales tax → Balance Sheet

Gift card liability → Balance Sheet

Owner distributions → Equity

This prevents non-operating transactions from being included in
operating P&L.

Deterministic Monthly P&L

Monthly P&L is calculated entirely by backend code:

Revenue
- COGS
= Gross Profit

Gross Profit
- Operating Expenses
= Operating Profit

COGS currently includes Food and Beverage. Operating expenses include
Payroll, Rent, Utilities, Marketing, Insurance, Cleaning, Delivery
Commission, Office/Admin Supplies, Repairs & Maintenance, POS/Software
Subscription, Accounting/Bookkeeping, and To-go Packaging & Disposables.

The LLM does not calculate or invent financial totals.

Variance Analysis

The application compares two months and calculates:

Previous operating profit

Current operating profit

Operating profit change

Operating profit change percentage

Category-level changes

Major variance drivers

Underlying transaction evidence

AI Financial Analyst

Users can ask natural-language questions such as:

Which month had the highest operating profit?
Why did operating profit change?
What are the major cost drivers?
Which transactions need attention?

The analyst is instructed to:

Never invent financial numbers.

Never invent transaction IDs.

Use supplied financial context as authoritative.

Keep answers relevant and concise.

Identify transaction evidence when relevant.

Avoid unsupported accounting reclassification.

State when the available data is insufficient.

Architecture

                 ┌─────────────────────┐
                 │      Next.js        │
                 │      Frontend       │
                 └──────────┬──────────┘
                            │ REST API
                            ▼
                 ┌─────────────────────┐
                 │       FastAPI       │
                 │       Backend       │
                 └──────────┬──────────┘
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
       PostgreSQL      Financial Logic   AI Analyst
             │              │              │
             │         P&L / Variance      │
             │                             ▼
             │                           Groq
             ▼
        Transactions

Project Structure

backend/
├── app/
│   ├── main.py
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── api/
├── alembic/
├── tests/
├── requirements.txt
└── alembic.ini

frontend/
├── app/
├── components/
├── lib/
└── package.json

Technology Stack

Backend

Python

FastAPI

SQLAlchemy

PostgreSQL

Alembic

Pandas

OpenPyXL

Pydantic

psycopg

AI

LangChain Groq

Groq

openai/gpt-oss-120b

Frontend

Next.js

React

TypeScript

React Markdown

GitHub Flavored Markdown

Deployment

Vercel --- frontend

Render --- backend

PostgreSQL --- production database

Important Technical Decisions

Deterministic financial calculations

Financial numbers are calculated by backend services rather than asking
an LLM to perform accounting calculations. This keeps calculations
reproducible.

Human-in-the-loop classification

Lower-confidence classifications are surfaced for human review instead
of being blindly accepted.

Explicit accounting treatment

Category and accounting treatment are stored separately. This allows the
system to exclude items such as equipment purchases, loan principal
repayments, taxes, and owner distributions from operating P&L.

AI for reasoning, not arithmetic

The AI analyst handles natural-language interpretation while financial
totals remain deterministic.

Evidence-driven AI responses

The analyst receives application-generated financial context and
transaction data and is instructed not to invent financial numbers or
transaction identifiers.

API Endpoints

Ingestion

POST /api/ingestion/transactions

Classification

POST /api/classification/run

Review Queue

GET /api/transactions/review

Correct Classification

PUT /api/transactions/{transaction_id}/classification

P&L

GET /api/financial/pnl

Variance

GET /api/financial/variance?previous_month=YYYY-MM&current_month=YYYY-MM

AI Analyst

POST /api/analyst/ask

Local Setup

Clone

git clone https://github.com/Karankaush/finz-financial-review.git
cd finz-financial-review

Backend

cd backend
python -m venv venv

Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Create backend/.env:

DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/finz_db
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b

Run migrations:

alembic upgrade head

Start backend:

uvicorn app.main:app --reload

Frontend

cd frontend
npm install

Create frontend/.env.local:

NEXT_PUBLIC_API_URL=http://127.0.0.1:8000

Run:

npm run dev

Frontend runs on http://localhost:3000.

Example Workflow

Upload the transaction Excel file.

Run classification.

Open the review queue.

Correct an uncertain transaction.

Generate monthly P&L.

Compare two months using variance analysis.

Inspect the largest variance drivers.

Trace drivers back to transactions.

Ask the AI financial analyst a question.

Financial Logic

Revenue

Transactions classified as Revenue contribute to revenue.

Contra-Revenue

Refunds & Discounts are treated as contra-revenue.

COGS

Food
Beverage

are treated as COGS.

Operating Profit

Operating Profit =
Revenue
- COGS
- Operating Expenses

Transactions classified as Balance Sheet or Equity items are excluded
from operating P&L.

Testing

Run:

pytest

The deployed workflow was also tested for transaction ingestion,
classification, review queue, P&L calculation, variance analysis, and AI
analyst requests.

Deployment

Frontend

The Next.js application is deployed on Vercel and uses:

NEXT_PUBLIC_API_URL=<Render backend URL>

Backend

The FastAPI application is deployed on Render.

Start command:

uvicorn app.main:app --host 0.0.0.0 --port $PORT

Database migrations are executed during the Render build:

pip install -r requirements.txt && alembic upgrade head

Design Philosophy

The application follows an AI-native workflow rather than treating AI as
a chatbot added to a conventional dashboard.

Ingest
  ↓
Understand
  ↓
Review
  ↓
Calculate
  ↓
Explain
  ↓
Investigate

Deterministic systems handle financial accuracy, while AI handles
natural-language reasoning and interpretation.

Author

Karan Kaushik

Software Engineering / Python Backend / GenAI
