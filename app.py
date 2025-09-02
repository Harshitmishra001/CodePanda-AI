import streamlit as st
from tutor_engine import TutorEngine

# --- Page Configuration ---
st.set_page_config(
    page_title="CodePanda-AI",
    page_icon="🐼",
    layout="wide"
)

# --- State Management & Model Loading ---
@st.cache_resource
def load_tutor_engine():
    """Loads the TutorEngine and caches it."""
    try:
        return TutorEngine(model_path="deepseek-coder-6.7b-instruct.Q4_K_S.gguf")
    except FileNotFoundError:
        return None

# Load the engine and handle potential errors
if 'engine' not in st.session_state:
    st.session_state.engine = load_tutor_engine()

# --- UI Layout ---
st.title("🐼 CodePanda-AI")
st.markdown("A lazy but brilliant AI tutor to help you with your Python code.")

# --- Sidebar for Instructions and Controls ---
with st.sidebar:
    st.header("How to Use")
    st.info(
        "1. Tell CodePanda if your code has a bug or if you think it's correct.\n"
        "2. Paste your Python code into the main text area.\n"
        "3. (Optional) If you have a bug, paste the error message you received.\n"
        "4. Click the button to get a hint!"
    )
    st.header("Step 1: What's the status of your code?")
    analysis_choice = st.selectbox(
        "Choose an option:",
        options=["My code has a bug", "I think my code is correct"],
        key='analysis_type_select'
    )
    # Map the user-friendly choice to the key the engine expects
    analysis_key = 'Buggy' if analysis_choice == "My code has a bug" else 'Correct'

    # Display an error if the model couldn't be loaded
    if st.session_state.engine is None:
        st.error("Model not found! Please ensure the GGUF model file is in the root directory.")

# --- Main Interaction Area ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Step 2: Enter Your Code")
    code_input = st.text_area(
        "Paste your Python code here:",
        height=300,
        key='code_input_area',
        placeholder="def my_function():\n    # your code here"
    )

    error_message_input = None
    if analysis_key == 'Buggy':
        st.subheader("Step 3 (Optional): Paste Error Message")
        error_message_input = st.text_area(
            "If you got an error, paste it here:",
            height=100,
            key='error_input_area',
            placeholder="e.g., SyntaxError: invalid syntax"
        )

if st.button("Ask CodePanda for a Hint!", type="primary", use_container_width=True):
    if st.session_state.engine:
        if code_input:
            with col2:
                st.subheader("💡 CodePanda's Hint")
                with st.spinner("Ugh... thinking... one moment..."):
                    hint = st.session_state.engine.generate_hint(
                        code_snippet=code_input,
                        analysis_type=analysis_key,
                        error_message=error_message_input
                    )
                    st.info(hint)
        else:
            st.warning("You forgot to paste your code. I'm going back to sleep.")
    else:
        st.error("The AI engine isn't loaded. Can't help you. Nap time.")

