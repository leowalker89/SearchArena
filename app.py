import streamlit as st
import random
from helpers import query_you_com, query_tavily, query_perplexity
from mongod_db import MongoDBHandler
from swarms.utils.loguru_logger import logger
import time

mongo = MongoDBHandler()

# Set Streamlit to wide mode
st.set_page_config(layout="wide")


# Define the function to process the question
def ProcessQuestion(question):
    # Randomly select two out of the three functions
    functions = [query_you_com, query_tavily, query_perplexity]
    selected_functions = random.sample(functions, 2)

    # Get answers from the selected functions
    answer_a = selected_functions[0](question)
    answer_b = selected_functions[1](question)
    
    # Log into mongodb
    try: 
        logger.info(f"Logging question: {question}")
        mongo.add(
            {
                "question": question,
                "answer_a": answer_a,
                "answer_b": answer_b,
                "selected_functions": [f.__name__ for f in selected_functions],
                "query_time": time.time(),
            }
        )
        logger.info("Successfully logged into mongodb")
    except Exception as e:
        logger.error(f"Error logging into mongodb: {e}")

    return answer_a, answer_b


# Initialize session state if not already done
if "results_displayed" not in st.session_state:
    st.session_state["results_displayed"] = False
if "answer_a" not in st.session_state:
    st.session_state["answer_a"] = ""
if "answer_b" not in st.session_state:
    st.session_state["answer_b"] = ""
if "question" not in st.session_state:
    st.session_state["question"] = ""

# Streamlit app layout
st.title("Search Engine Agent Comparison")

# Create columns for the input and model selection
input_col, control_col = st.columns([4, 1])

with input_col:
    # Text box for user input with character limit
    question = st.text_area(
        "Enter your question here (max 1000 characters):", max_chars=1000
    )

with control_col:
    # Submit button
    submit_button = st.button("Submit")

if submit_button:
    if question:
        if len(question) <= 1000:
            # Process the question and get answers
            answer_a, answer_b = ProcessQuestion(question)

            # Save answers and state to session state
            st.session_state["answer_a"] = answer_a
            st.session_state["answer_b"] = answer_b
            st.session_state["question"] = question
            st.session_state["results_displayed"] = True
        else:
            st.error(
                "Your question exceeds the 1,000 character limit. Please shorten your question."
            )
    else:
        st.error("Please enter a question.")

# Display results if available in session state
if st.session_state["results_displayed"]:
    col1, col2 = st.columns(2)
    with col1:
        st.write("### Output A")
        st.write(st.session_state["answer_a"])
        a_feedback_grid = st.columns(1)
    with col2:
        st.write("### Output B")
        st.write(st.session_state["answer_b"])
        b_feedback_grid = st.columns(2)

    # Create a placeholder for the feedback div
    feedback_placeholder = st.empty()

    def display_feedback(message):
        feedback_placeholder.markdown(
            f'<div style="position: fixed; bottom: 10px; left: 10px; background-color: #f0f0f0; padding: 10px; border-radius: 5px;">{message}</div>',
            unsafe_allow_html=True,
        )

    with a_feedback_grid[0]:
        if st.button("A is better 🥇"):
            display_feedback("You selected: A is better")
    with b_feedback_grid[0]:
        if st.button("B is better 💪"):
            display_feedback("You selected: B is better")
    with a_feedback_grid[0]:
        if st.button("It's a Tie 🤝"):
            display_feedback("You selected: It's a Tie")
    with b_feedback_grid[0]:
        if st.button("Both are bad 👎"):
            display_feedback("You selected: Both are bad")
