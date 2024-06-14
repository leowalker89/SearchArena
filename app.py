import streamlit as st

# Set Streamlit to wide mode
st.set_page_config(layout="wide")

# Define the function to process the question
def ProcessQuestion(question):
    # Placeholder for the actual implementation
    # This should return answers from two models, A and B
    answer_a = "Answer from Model A"
    answer_b = "Answer from Model B"
    return answer_a, answer_b

# Initialize session state if not already done
if 'results_displayed' not in st.session_state:
    st.session_state['results_displayed'] = False
if 'answer_a' not in st.session_state:
    st.session_state['answer_a'] = ""
if 'answer_b' not in st.session_state:
    st.session_state['answer_b'] = ""
if 'selected_model' not in st.session_state:
    st.session_state['selected_model'] = ""
if 'question' not in st.session_state:
    st.session_state['question'] = ""

# Streamlit app layout
st.title("Chatbot Comparison")

# Create columns for the input and model selection
input_col, control_col = st.columns([4, 1])

with input_col:
    # Text box for user input with character limit
    question = st.text_area("Enter your question here (max 1000 characters):", max_chars=1000)

with control_col:
    # Submit button
    submit_button = st.button("Submit")

if submit_button:
    if question:
        if len(question) <= 1000:
            # Process the question and get answers
            answer_a, answer_b = ProcessQuestion(question)

            # Save answers and state to session state
            st.session_state['answer_a'] = answer_a
            st.session_state['answer_b'] = answer_b
            # st.session_state['selected_model'] = selected_model
            st.session_state['question'] = question
            st.session_state['results_displayed'] = True
        else:
            st.error("Your question exceeds the 1,000 character limit. Please shorten your question.")
    else:
        st.error("Please enter a question and select a model.")

# Display results if available in session state
if st.session_state['results_displayed']:
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"### Output A from {st.session_state['selected_model']}")
        st.write(st.session_state['answer_a'])

    with col2:
        st.write(f"### Output B from {st.session_state['selected_model']}")
        st.write(st.session_state['answer_b'])
    
    feedback_col = st.columns([1, 1, 1, 1])

    with feedback_col[0]:
        if st.button("A is better 🥇"):
            st.write("You selected: A is better")

    with feedback_col[1]:
        if st.button("B is better 🥈"):
            st.write("You selected: B is better")

    with feedback_col[2]:
        if st.button("It's a Tie 🤝"):
            st.write("You selected: It's a Tie")

    with feedback_col[3]:
        if st.button("Both are bad 👎"):
            st.write("You selected: Both are bad")
