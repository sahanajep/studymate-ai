import os
from datetime import datetime

import pandas as pd
import streamlit as st
from google import genai


class StudyHistory:
    """Stores and analyzes study activity using Pandas."""

    COLUMNS = ["timestamp", "question", "answer"]

    def __init__(self, data=None):
        if data is None:
            self.data = pd.DataFrame(columns=self.COLUMNS)
        else:
            self.data = data.copy()

    def add_entry(self, question, answer):
        new_entry = pd.DataFrame(
            [
                {
                    "timestamp": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "question": question,
                    "answer": answer,
                }
            ]
        )

        self.data = pd.concat(
            [self.data, new_entry],
            ignore_index=True,
        )

    def statistics(self):
        if self.data.empty:
            return {
                "questions": 0,
                "average_question_length": 0,
                "average_answer_length": 0,
            }

        return {
            "questions": len(self.data),
            "average_question_length": round(
                self.data["question"]
                .astype(str)
                .str.len()
                .mean(),
                1,
            ),
            "average_answer_length": round(
                self.data["answer"]
                .astype(str)
                .str.len()
                .mean(),
                1,
            ),
        }

    def recent(self, number=5):
        return self.data.tail(number)

    def to_csv(self):
        return self.data.to_csv(index=False).encode("utf-8")


class StudyMateBot:
    """Gemini-powered study assistant."""

    SYSTEM_INSTRUCTION = """
You are StudyMate, a patient and encouraging AI study tutor.

Follow these rules:
- Explain concepts clearly and step by step.
- Adjust explanations to the student's level.
- Use examples and analogies.
- Explain methods instead of only providing answers.
- Create quizzes, flashcards, summaries, and study plans.
- Give hints when requested.
- Ask a brief check-for-understanding question.
- Admit uncertainty rather than inventing information.
- Encourage learning and academic integrity.
"""

    def __init__(
        self,
        api_key,
        history,
        previous_interaction_id=None,
        model="gemini-3.6-flash",
    ):
        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.history = history
        self.previous_interaction_id = previous_interaction_id

    def ask(self, question):
        request = {
            "model": self.model,
            "input": question,
            "system_instruction": self.SYSTEM_INSTRUCTION,
        }

        if self.previous_interaction_id:
            request["previous_interaction_id"] = (
                self.previous_interaction_id
            )

        interaction = self.client.interactions.create(**request)

        answer = (
            interaction.output_text
            or "StudyMate did not return a text response."
        )

        self.previous_interaction_id = interaction.id
        self.history.add_entry(question, answer)

        return answer


def get_api_key():
    """Read the API key from Streamlit Secrets or the environment."""
    api_key = os.getenv("GEMINI_API_KEY")

    try:
        api_key = st.secrets.get("GEMINI_API_KEY", api_key)
    except Exception:
        pass

    return api_key


st.set_page_config(
    page_title="StudyMate AI Tutor",
    page_icon="📚",
    layout="wide",
)

st.title("📚 StudyMate AI Tutor")
st.caption(
    "An object-oriented study assistant built with "
    "Python, Pandas, Gemini, and Streamlit."
)

api_key = get_api_key()

if not api_key:
    st.error(
        "GEMINI_API_KEY is missing. Add it through "
        "Streamlit Secrets."
    )
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "history_data" not in st.session_state:
    st.session_state.history_data = pd.DataFrame(
        columns=StudyHistory.COLUMNS
    )

if "previous_interaction_id" not in st.session_state:
    st.session_state.previous_interaction_id = None

history = StudyHistory(st.session_state.history_data)

with st.sidebar:
    st.header("Study Dashboard")

    statistics = history.statistics()

    st.metric(
        "Questions asked",
        statistics["questions"],
    )

    st.metric(
        "Average question length",
        statistics["average_question_length"],
    )

    st.metric(
        "Average answer length",
        statistics["average_answer_length"],
    )

    if st.button("Start new conversation"):
        st.session_state.messages = []
        st.session_state.previous_interaction_id = None
        st.rerun()

    if st.button("Clear study history"):
        st.session_state.history_data = pd.DataFrame(
            columns=StudyHistory.COLUMNS
        )
        st.rerun()

    st.download_button(
        label="Download study history",
        data=history.to_csv(),
        file_name="study_history.csv",
        mime="text/csv",
        disabled=history.data.empty,
    )

    if not history.data.empty:
        st.subheader("Recent questions")
        st.dataframe(
            history.recent()[["timestamp", "question"]],
            hide_index=True,
            use_container_width=True,
        )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input(
    "Ask for an explanation, quiz, summary, or study plan..."
)

if prompt:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    history = StudyHistory(st.session_state.history_data)

    bot = StudyMateBot(
        api_key=api_key,
        history=history,
        previous_interaction_id=(
            st.session_state.previous_interaction_id
        ),
    )

    try:
        with st.spinner("StudyMate is thinking..."):
            answer = bot.ask(prompt)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

        st.session_state.previous_interaction_id = (
            bot.previous_interaction_id
        )

        st.session_state.history_data = bot.history.data

    except Exception as error:
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": f"An error occurred: {error}",
            }
        )

    st.rerun()
