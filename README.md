# Vibe-Coded AI Resume Builder

A vibe-coded web app that helps users turn raw resume content into polished, job-ready output using AI-assisted editing, scoring, and formatting.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [What Stands Out](#what-stands-out)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Notes](#notes)

## Overview
This project is a Django-based AI Resume Builder with a chat-style interface. Users can upload a resume, ask for improvements, and get AI-generated refinements and structured output.

## Features
- Chat-style resume refinement workflow.
- AI-assisted writing improvements.
- Resume file upload support.
- Resume scoring utilities.
- LaTeX-based resume generation/compilation pipeline.

## How It Works
1. Start a chat session in the app.
2. Upload your existing resume (optional).
3. Provide your goals, target role, and experience details.
4. The AI agent analyzes the input and returns improved resume content.
5. You iterate in chat, then export/use the final version.

## What Stands Out
- **Vibe-coded user experience:** lightweight, fast iteration loop.
- **Agent + tools architecture:** combines conversation with scoring and formatting helpers.
- **Practical output focus:** designed for directly usable resume improvements.
- **End-to-end flow:** from rough inputs to cleaner, stronger resume content.

## Installation
### 1) Prerequisites
- Python 3.11+ (recommended)
- pip
- (Optional) A LaTeX distribution if you want PDF compilation from `.tex` (e.g., TeX Live)

### 2) Clone and enter the project
```bash
git clone <your-repo-url>
cd hackathon-team-runtimeTerror2.0
```

### 3) Create and activate a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```

### 4) Install dependencies
If you have a requirements file, use it:
```bash
pip install -r requirements.txt
```

If not, install the core packages directly:
```bash
pip install django google-adk google-genai google-generativeai pypdf python-docx scikit-learn numpy
```

### 5) Configure environment variables
Set your Google API key before running the app:
```bash
export GOOGLE_API_KEY="your_api_key_here"
```

### 6) Run migrations and start the server
```bash
python manage.py migrate
python manage.py runserver
```

Then open: `http://127.0.0.1:8000/`

## Usage
- Open the home/chat page.
- Start a new session.
- Upload your resume and/or paste your current content.
- Ask for targeted improvements (ATS optimization, stronger bullets, concise summary, etc.).
- Iterate until the resume is finalized.

## Project Structure
- `ai_resume_builder/` – Django project settings and app wiring.
- `resume_app/` – Core resume/chat app logic, agent, tools, and services.
- `templates/` – HTML templates.
- `static/` – CSS/assets.
- `media/` – Uploaded and generated files.

## Tech Stack
- Django
- Google ADK + Google GenAI
- Python NLP/data tooling (`scikit-learn`, `numpy`)
- Document processing (`pypdf`, `python-docx`)

## Notes
- This project appears to be in prototype/hackathon form.
- For production usage, consider adding:
  - pinned dependency management (`requirements.txt`),
  - secure secret handling,
  - robust file validation and error handling,
  - production-ready deployment settings.
