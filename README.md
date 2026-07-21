# StudyMate AI Tutor 📚

An AI study assistant built with Python, Pandas, Google Gemini, and Streamlit.

StudyMate helps students understand difficult concepts, generate quizzes, create flashcards, request hints, build study plans, and track their study activity through a Pandas-powered dashboard.

## Live Demo

- **Application:** https://studymate-ai-kf8mhcbqdtwnltfzbdprc2.streamlit.app/
- **Source Code:** 

## Quick Start

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd studymate-ai
```

### 2. Install the dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your Gemini API key

Create a file named:

```text
.streamlit/secrets.toml
```

Add:

```toml
GEMINI_API_KEY = "your_api_key_here"
```

Do not upload this file or your real API key to GitHub.

### 4. Start the application

```bash
streamlit run app.py
```

Open the local address shown by Streamlit, usually:

```text
http://localhost:8501
```

## Features

- AI-generated explanations adapted to the student's level
- Multi-turn conversational context
- Practice quizzes and questions
- Flashcard generation
- Step-by-step hints
- Topic summaries
- Personalized study plans
- Study-history tracking
- Pandas-powered learning statistics
- Downloadable CSV reports
- Interactive Streamlit chat interface
- Secure API-key management

## Example Prompts

```text
Explain photosynthesis to a middle-school student.
```

```text
Quiz me on Python classes with five multiple-choice questions.
```

```text
Create flashcards about the parts of a cell.
```

```text
Give me a hint for solving 3x + 7 = 22.
```

```text
Create a seven-day study plan for my biology exam.
```

## Architecture

```text
studymate-ai/
├── app.py
│   ├── StudyMateBot
│   │   ├── Connects to the Gemini API
│   │   ├── Sends tutoring instructions
│   │   ├── Maintains conversation context
│   │   └── Returns AI-generated responses
│   │
│   ├── StudyHistory
│   │   ├── Stores questions and answers
│   │   ├── Manages a Pandas DataFrame
│   │   ├── Calculates study statistics
│   │   └── Exports history to CSV
│   │
│   └── Streamlit Interface
│       ├── Chat interface
│       ├── Study dashboard
│       ├── Recent-question table
│       └── CSV download button
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Application Flow

```text
Student enters a question
        ↓
Streamlit receives the prompt
        ↓
StudyMateBot sends the request to Gemini
        ↓
Gemini generates a tutoring response
        ↓
StudyHistory stores the interaction
        ↓
Pandas updates the statistics
        ↓
Streamlit displays the response and dashboard
```

## Object-Oriented Design

### `StudyMateBot`

Responsible for:

- Creating the Gemini client
- Sending questions to Gemini
- Applying the tutor instructions
- Maintaining conversation context
- Passing completed interactions to the history object

### `StudyHistory`

Responsible for:

- Storing timestamps, questions, and answers
- Managing the Pandas DataFrame
- Calculating learning statistics
- Displaying recent questions
- Exporting study history as CSV

### Composition

The `StudyMateBot` class uses a `StudyHistory` object:

```python
self.history = history
```

This separates AI functionality from data-management functionality, making the application easier to maintain and expand.

## Pandas Data Model

Study activity is stored in a DataFrame with the following columns:

```text
timestamp | question | answer
```

Pandas is used to:

- Create and update the study-history table
- Count the total number of questions
- Calculate average question length
- Calculate average answer length
- Display recent questions
- Export study activity to CSV

## Technology Stack

```text
Python          Application logic
OOP             Bot and history class design
Pandas          Study data and analytics
Gemini API      AI-generated tutoring responses
Streamlit       Interactive web interface
GitHub          Source control and portfolio hosting
```

## Security

The Gemini API key is stored using Streamlit Secrets.

The real API key should never be placed inside:

```text
app.py
README.md
requirements.txt
GitHub commits
screenshots
```

The following files are excluded through `.gitignore`:

```text
.env
.streamlit/secrets.toml
```

## Current Limitations

- Study history is stored in the active Streamlit session.
- Refreshing or restarting the application may reset the history.
- Gemini responses may occasionally contain inaccurate information.
- The application does not currently include user accounts.
- Gemini usage may be subject to API limits.

## Future Improvements

- Persistent database storage
- User accounts and study profiles
- Quiz scoring
- Topic-based performance tracking
- Study-progress charts
- Document and note uploads
- Spaced-repetition flashcards
- Automated testing

## Resume Summary

> Built and deployed an object-oriented AI study assistant using Python, Pandas, the Gemini API, and Streamlit. Implemented multi-turn conversational context, personalized tutoring instructions, study-history analytics, an interactive dashboard, and downloadable CSV reports.

## Author

**Your Name**

- GitHub: Add your GitHub profile link
- LinkedIn: Add your LinkedIn profile link
- Portfolio: Add your portfolio link
