import streamlit as st
import random
from helpers import query_you_com, query_tavily, query_perplexity, query_brave
from provider_info import search_providers
# from mongod_db import MongoDBHandler
# from swarms.utils.loguru_logger import logger
import time

# mongo = MongoDBHandler()

# Set Streamlit to wide mode
st.set_page_config(layout="wide", page_title="SearchArena")

# Add information to sidebar
# st.sidebar.title("About the App")
# st.sidebar.write("""
# This app allows you to compare responses from different search engines.
# Submit a question, and you'll receive answers from two randomly selected search engines.
# You can then vote on which response you prefer.
# """)
# st.sidebar.write("""
# **[GitHub](https://github.com/leowalker89/SearchArena)**""")

# Header section
st.title("⚔️ Search Arena: Evaluating and Comparing Search Providers")

# Subheader with introduction
st.header("Welcome to Search Arena")
st.write("""
Welcome to Search Arena, an open platform for evaluating and comparing search providers through crowdsourced human preferences. Inspired by the groundbreaking work of LMSYS's Chatbot Arena in benchmarking large language models (LLMs), Search Arena aims to bring a similar approach to the world of search.

Our platform allows you to input a query and receive results from two anonymous search providers. After reviewing the results, you can vote for the provider that delivered the most relevant and helpful information. The search providers' identities are kept hidden during the voting process to ensure unbiased evaluation. You can continue refining your query and interacting with the search results until you are satisfied with the outcome.

Currently, Search Arena compares results from four leading search providers: Tavily, Brave Search, Perplexity, and You.com. By collecting votes from a wide user base, we aim to establish a robust leaderboard that reflects the real-world performance and user preferences of these search engines.

Join us in our mission to advance search technology through open collaboration and data-driven insights. Your participation will contribute to a growing dataset that will be made available to the research community, fostering innovation and improvement in the field of information retrieval.
""")

# Define the function to process the question
def ProcessQuestion(question):
    # Randomly select two out of the four functions
    functions = [query_you_com, query_tavily, query_perplexity, query_brave]
    selected_functions = random.sample(functions, 2)

    # Get answers from the selected functions
    answer_a = selected_functions[0](question)
    answer_b = selected_functions[1](question)
    
    # Log into mongodb
    # try: 
    #     logger.info(f"Logging question: {question}")
    #     mongo.add(
    #         {
    #             "question": question,
    #             "answer_a": answer_a,
    #             "answer_b": answer_b,
    #             "selected_functions": [f.__name__ for f in selected_functions],
    #             "query_time": time.time(),
    #         }
    #     )
    #     logger.info("Successfully logged into mongodb")
    # except Exception as e:
    #     logger.error(f"Error logging into mongodb: {e}")

    return answer_a, answer_b, selected_functions


# Initialize session state if not already done
default_values = {
    "state": "arena_ready",
    "question": "",
    "answer_a": "",
    "answer_b": "",
    "source_a": "",
    "source_b": "",
    "winner": "",
    "selected_button": ""
}

for key, value in default_values.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Streamlit app layout
st.title("Search Engine Agent Comparison")

def on_submit():
    question = st.session_state["question_input"]
    if question:
        answer_a, answer_b, selected_functions = ProcessQuestion(question)
        st.session_state["question"] = question
        st.session_state["answer_a"] = answer_a
        st.session_state["answer_b"] = answer_b
        st.session_state["source_a"] = selected_functions[0].__name__
        st.session_state["source_b"] = selected_functions[1].__name__
        st.session_state["state"] = "arena_review"

def handle_vote(vote):
    st.session_state["winner"] = vote
    st.session_state["state"] = "arena_results"

def get_provider_info(provider_function_name):
    provider_name_map = {
        'query_you_com': 'You.com',
        'query_tavily': 'Tavily',
        'query_perplexity': 'Perplexity AI',
        'query_brave': 'Brave Search'
    }
    provider_name = provider_name_map.get(provider_function_name)
    return next((provider for provider in search_providers if provider['company_name'] == provider_name), {})

def render_ready_state():
    st.text_area("Enter your question here (max 1000 characters):", 
                 max_chars=1000, 
                 key="question_input", 
                 on_change=on_submit)
    st.button("Submit", on_click=on_submit)

def render_review_state():
    st.write("## Results")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### Answer A")
        st.write(st.session_state["answer_a"])
    with col2:
        st.write("### Answer B")
        st.write(st.session_state["answer_b"])
    st.write("### Vote for the Best Answer")
    col1, col2, col3, col4 = st.columns(4)
    if col1.button("It's a Tie 🤝"):
        handle_vote("Tie")
    if col2.button("A is better 💪"):
        handle_vote("A")
    if col3.button("B is better 🥇"):
        handle_vote("B")
    if col4.button("Both are bad 👎"):
        handle_vote("Both are bad")

def render_results_state():
    st.write("## Results")
    st.write(f"### Question: {st.session_state['question']}")
    
    provider_info_a = get_provider_info(st.session_state["source_a"])
    provider_info_b = get_provider_info(st.session_state["source_b"])
    
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state["winner"] == "A":
            st.write(f"### ⭐ {provider_info_a['company_name']} 🥇")
        elif st.session_state["winner"] == "Tie":
            st.write(f"### 🤝 {provider_info_a['company_name']} 🤝")
        elif st.session_state["winner"] == "Both are bad":
            st.write(f"### 👎 {provider_info_a['company_name']} 👎")
        else:
            st.write(f"### {provider_info_a['company_name']} 🥈")
        st.write("**Response:**")
        st.markdown(f"<div style='padding: 10px; border: 1px solid #ddd;'>{st.session_state['answer_a']}</div>", unsafe_allow_html=True)

    with col2:
        if st.session_state["winner"] == "B":
            st.write(f"### ⭐ {provider_info_b['company_name']} 🥇")
        elif st.session_state["winner"] == "Tie":
            st.write(f"### 🤝 {provider_info_b['company_name']} 🤝")
        elif st.session_state["winner"] == "Both are bad":
            st.write(f"### 👎 {provider_info_b['company_name']} 👎")
        else:
            st.write(f"### {provider_info_b['company_name']} 🥈")
        st.write("**Response:**")
        st.markdown(f"<div style='padding: 10px; border: 1px solid #ddd;'>{st.session_state['answer_b']}</div>", unsafe_allow_html=True)
    
    st.write("### Feedback")
    st.text_area("Please provide feedback on why you chose the winner:", key="feedback")
    st.write("### About the search providers:")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Website:** [{provider_info_a['website']}]({provider_info_a['website']})")
        st.write(f"**Overview:** {provider_info_a['overview']}")
    with col2:
        st.write(f"**Website:** [{provider_info_b['website']}]({provider_info_b['website']})")
        st.write(f"**Overview:** {provider_info_b['overview']}")

if st.session_state["state"] == "arena_ready":
    render_ready_state()
elif st.session_state["state"] == "arena_review":
    render_review_state()
elif st.session_state["state"] == "arena_results":
    render_results_state()

# Apply custom CSS to highlight the selected button
selected_button = st.session_state.get("selected_button", "")

if selected_button:
    st.markdown(
        f"""
        <style>
        button[kind="primary"]{{
            background-color: #4CAF50 !important;
            color: white !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )