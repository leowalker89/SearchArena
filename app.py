import streamlit as st
import random
from helpers import query_you_com, query_tavily, query_perplexity, query_brave
from provider_info import search_providers
from mongod_db import MongoDBHandler
from bson.objectid import ObjectId
# from swarms.utils.loguru_logger import logger
import time
import uuid

# mongo = MongoDBHandler()

# Set Streamlit to wide mode
st.set_page_config(layout="wide", page_title="SearchArena")

# Add information to sidebar
st.sidebar.title("About the App")
st.sidebar.write("""
Welcome to Search Arena, an open platform for evaluating and comparing search providers.

**How it works:**
1. Enter a single question in the text area.
2. Receive answers from two anonymous search providers.
3. Review the answers and vote for the one that you prefer.
4. After voting, the identities of the search providers will be revealed.
5. You can also provide feedback on your choice.

**Search Providers:**
- [Tavily](https://tavily.com/)
- [Brave Search](https://brave.com/search/api)
- [Perplexity AI](https://docs.perplexity.ai/)
- [You.com](https://api.you.com/)

Each search provider has its unique features and capabilities. After voting, you can learn more about the providers and their offerings.

**[GitHub](https://github.com/leowalker89/SearchArena)**

**[LinkedIn](https://www.linkedin.com/in/leowalker89/)**

**[X/Twitter](https://twitter.com/leowalker9)**
""")

# Header section
st.title("⚔️ Search Arena: Comparing Search Providers")

# Display the image
st.image("images/arena.png", use_column_width=True)

# Define the function to process the question
def ProcessQuestion(question):
    document_id = None
    # Randomly select two out of the four functions
    functions = [query_you_com, query_tavily, query_perplexity, query_brave]
    selected_functions = random.sample(functions, 2)

    # Get answers from the selected functions
    answer_a = selected_functions[0](question)
    answer_b = selected_functions[1](question)
    
    # Log into mongodb
    mongo = MongoDBHandler()
    
    try: 
        # logger.info(f"Logging question: {question}")
        document_id = mongo.add(
            {
                "question": question,
                "answer_a": answer_a,
                "answer_b": answer_b,
                "selected_functions": [f.__name__ for f in selected_functions],
                "query_time": time.time(),
                "session_id": st.session_state.session_id,
            }
        )
        # logger.info("Successfully logged into mongodb")
    except Exception as e:
        # logger.error(f"Error logging into mongodb: {e}")
        print(f"Error logging into mongodb: {e}")

    return answer_a, answer_b, selected_functions, document_id

def UpdateVote(session_id, vote):
    mongo = MongoDBHandler()
    try:
        mongo.update(
            {"session_id": session_id},
            {"$set": {"vote": vote}}
        )
    except Exception as e:
        print(f"Error updating vote in mongodb: {e}")

def UpdateFeedback(session_id, feedback):
    mongo = MongoDBHandler()
    try:
        mongo.update(
            {"session_id": session_id},
            {"$set": {"feedback": feedback}}
        )
    except Exception as e:
        print(f"Error updating feedback in mongodb: {e}")

def on_submit():
    question = st.session_state["question_input"]
    if question:
        answer_a, answer_b, selected_functions, document_id = ProcessQuestion(question)
        st.session_state["question"] = question
        st.session_state["answer_a"] = answer_a
        st.session_state["answer_b"] = answer_b
        st.session_state["source_a"] = selected_functions[0].__name__
        st.session_state["source_b"] = selected_functions[1].__name__
        st.session_state["state"] = "arena_review"
        st.session_state["document_id"] = document_id

def handle_vote(vote):
    st.session_state["winner"] = vote
    st.session_state["state"] = "arena_results"
    UpdateVote(st.session_state["session_id"], vote)

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
    feedback = st.text_area("Please provide feedback on why you chose the winner:")
    if feedback:
        UpdateFeedback(st.session_state["session_id"], feedback)
        st.write("Thank you for your feedback!")
    
    st.write("### About the search providers:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Website:** [{provider_info_a['website']}]({provider_info_a['website']})")
        st.write(f"**Overview:** {provider_info_a['overview']}")
    with col2:
        st.write(f"**Website:** [{provider_info_b['website']}]({provider_info_b['website']})")
        st.write(f"**Overview:** {provider_info_b['overview']}")


# Initialize session state if not already done
default_values = {
    "state": "arena_ready",
    "question": "",
    "answer_a": "",
    "answer_b": "",
    "source_a": "",
    "source_b": "",
    "winner": "",
    "selected_button": "",
    "document_id": "",
    "feedback": "",
    "session_id": str(uuid.uuid4())
}

for key, value in default_values.items():
    if key not in st.session_state:
        st.session_state[key] = value

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