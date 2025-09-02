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
        # NOTE: Make sure your model file name matches this path
        return TutorEngine(model_path="deepseek-coder-6.7b-instruct.Q4_K_S.gguf")
    except FileNotFoundError:
        return None

# Load the engine and store it in the session state
if 'engine' not in st.session_state:
    st.session_state.engine = load_tutor_engine()

# --- UI Layout ---
st.title("🐼 CodePanda-AI")
st.markdown("An AI tutor that understands your goals to give you better hints.")

# --- Sidebar for Instructions and Controls ---
with st.sidebar:
    st.header("How to Use")
    st.info(
        "1. Select the status of your code (buggy or correct).\n"
        "2. **Crucially, describe what you want your code to do.**\n"
        "3. Paste your Python code.\n"
        "4. (Optional) If you have a bug, paste the error message.\n"
        "5. Click the button to get a hint!"
    )
    st.header("Step 1: Code Status")
    analysis_choice = st.selectbox(
        "Choose an option:",
        options=["My code has a bug", "I think my code is correct"],
        key='analysis_type_select',
        label_visibility="collapsed"
    )
    # Map the user-friendly choice to the key the engine expects
    analysis_key = 'Buggy' if analysis_choice == "My code has a bug" else 'Correct'

    # Display an error if the model couldn't be loaded
    if st.session_state.engine is None:
        st.error("Model not found! Please ensure the GGUF model file is in the root directory.")

# --- Main Interaction Area ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Step 2: Describe Your Goal")
    user_context = st.text_area(
        "What are you trying to achieve with this code? (This is required)",
        height=100,
        key='user_context_area',
        placeholder="e.g., 'I want a function that takes a list of numbers and returns a new list with only the even ones.'"
    )

    st.subheader("Step 3: Enter Your Code")
    code_input = st.text_area(
        "Paste your Python code here:",
        height=250,
        key='code_input_area',
        placeholder="def get_evens(numbers):\n    # your code here"
    )

    error_message_input = None
    if analysis_key == 'Buggy':
        st.subheader("Step 4 (Optional): Paste Error Message")
        error_message_input = st.text_area(
            "If you got an error, paste it here:",
            height=100,
            key='error_input_area',
            placeholder="e.g., SyntaxError: invalid syntax"
        )

# --- Button and Hint Generation Logic ---
if st.button("Ask CodePanda for a Hint!", type="primary", use_container_width=True):
    if st.session_state.engine:
        # Check if the compulsory context field and code field are filled
        if user_context and code_input:
            with col2:
                st.subheader("💡 CodePanda's Hint")
                with st.spinner("Analyzing your goal and code..."):
                    hint = st.session_state.engine.generate_hint(
                        code_snippet=code_input,
                        analysis_type=analysis_key,
                        user_context=user_context,
                        error_message=error_message_input
                    )
                    st.info(hint)
        elif not user_context:
            st.warning("Please describe your goal in Step 2. I need to know what you're trying to do!")
        else:
            st.warning("Please enter some code for me to analyze.")
    else:
        st.error("The AI engine isn't loaded. Cannot provide a hint.")

