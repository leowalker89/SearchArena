import streamlit as st
import random
from helpers import query_you_com, query_tavily, query_perplexity, query_brave
import time

# Set Streamlit to wide mode
st.set_page_config(layout="wide")

# Define the function to process the question
def ProcessQuestion(question):
    # Randomly select two out of the four functions
    functions = [query_you_com, query_tavily, query_perplexity, query_brave]
    selected_functions = random.sample(functions, 2)

    # Get answers from the selected functions
    answer_a = selected_functions[0](question)
    answer_b = selected_functions[1](question)

    return answer_a, answer_b, selected_functions

# Initialize session state if not already done
if "results_displayed" not in st.session_state:
    st.session_state["results_displayed"] = False
if "answer_a" not in st.session_state:
    st.session_state["answer_a"] = ""
if "answer_b" not in st.session_state:
    st.session_state["answer_b"] = ""
if "question" not in st.session_state:
    st.session_state["question"] = ""
if "source_a" not in st.session_state:
    st.session_state["source_a"] = ""
if "source_b" not in st.session_state:
    st.session_state["source_b"] = ""
if "winner" not in st.session_state:
    st.session_state["winner"] = ""

# Streamlit app layout
st.title("Search Engine Agent Comparison")

# Text box for user input with character limit
question = st.text_area(
    "Enter your question here (max 1000 characters):", max_chars=1000
)

# Submit button
submit_button = st.button("Submit")

if submit_button:
    if question:
        if len(question) <= 1000:
            # Process the question and get answers
            answer_a, answer_b, selected_functions = ProcessQuestion(question)

            # Save answers and state to session state
            st.session_state["answer_a"] = answer_a
            st.session_state["answer_b"] = answer_b
            st.session_state["question"] = question
            st.session_state["source_a"] = selected_functions[0].__name__
            st.session_state["source_b"] = selected_functions[1].__name__
            st.session_state["results_displayed"] = True
            st.session_state["winner"] = ""
        else:
            st.error(
                "Your question exceeds the 1,000 character limit. Please shorten your question."
            )
    else:
        st.error("Please enter a question.")

# Display results if available in session state
if st.session_state["results_displayed"]:
    button_col1, button_col2, button_col3, button_col4 = st.columns(4)

    def display_feedback(message):
        st.markdown(
            f'<div style="position: fixed; bottom: 10px; left: 10px; background-color: #f0f0f0; padding: 10px; border-radius: 5px;">{message}</div>',
            unsafe_allow_html=True,
        )

    with button_col1:
        if st.button("It's a Tie 🤝"):
            st.session_state["winner"] = "Tie"
            display_feedback("You selected: It's a Tie")
        
    with button_col2:
        if st.button("A is better 💪"):
            st.session_state["winner"] = "A"
            display_feedback("You selected: A is better")
    with button_col3:
        if st.button("B is better 🥇"):
            st.session_state["winner"] = "B"
            display_feedback("You selected: B is better")
    with button_col4:
        if st.button("Both are bad 👎"):
            st.session_state["winner"] = "Both are bad"
            display_feedback("You selected: Both are bad")

    col1, col2 = st.columns(2)
    with col1:
        if st.session_state["winner"]:
            if st.session_state["winner"] == "A":
                st.write(f"### ⭐ {st.session_state['source_a'].replace('query_', '').capitalize()} 🥇")
                
            elif st.session_state["winner"] == "B":
                st.write(f"### {st.session_state['source_a'].replace('query_', '').capitalize()} 🥈")
        else:
            st.write("### Result A")
        st.write(st.session_state["answer_a"])

    with col2:
        if st.session_state["winner"]:
            if st.session_state["winner"] == "B":
                st.write(f"### ⭐ {st.session_state['source_b'].replace('query_', '').capitalize()} 🥇")

            elif st.session_state["winner"] == "A":
                st.write(f"### {st.session_state['source_b'].replace('query_', '').capitalize()} 🥈")
        else:
            st.write("### Result B")
        st.write(st.session_state["answer_b"])

    # Add information about human feedback
    st.write("### Importance of Human Feedback")
    st.write("""
        Comparing search results from different engines is crucial for improving search technologies.
        Your feedback helps us understand which search engines provide the most relevant results.
        This approach is similar to LMSys Chatbot Arena where they compare the outputs of different open-source chatbots.
    """)