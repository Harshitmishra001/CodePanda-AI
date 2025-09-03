import os
from llama_cpp import Llama

class TutorEngine:
    """
    The core AI engine for the CodePpanda-AI application.
    This version uses a highly structured, XML-tagged prompt for maximum reliability.
    """
    def __init__(self, model_path="deepseek-coder-6.7b-instruct.Q4_K_S.gguf"):
        """
        Initializes the TutorEngine, loading the specified GGUF model.
        """
        self.model_path = model_path
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Model file not found at {self.model_path}. "
                "Please download the model and place it in the root directory."
            )
            
        print("Loading model... This may take a moment.")
        self.llm = Llama(
            model_path=self.model_path,
            n_gpu_layers=-1, # Offload all layers to GPU if available
            n_ctx=2048,      # Context window
            verbose=False
        )
        print("Model loaded successfully.")

    def generate_hint(self, code_snippet, analysis_type, user_context, error_message=None):
        """
        Generates a tailored hint for a given piece of code based on user intent.
        """
        system_prompt = self._get_system_prompt(analysis_type)
        
        full_prompt = (f"{system_prompt}\n\n"
                       f"### User's Goal:\n{user_context}\n\n"
                       f"### Student's Code:\n```python\n{code_snippet}\n```")

        if error_message:
            full_prompt += f"\n\n### Error Message They Received:\n```\n{error_message}\n```"

        full_prompt += "\n\n### Your Hint:"

        print(f"\n--- Generating response for {analysis_type} code ---")
        
        output = self.llm(
            full_prompt,
            max_tokens=150, 
            stop=["###", "Student's Code:", "</FINAL_QUESTION>"], 
            temperature=0.1,
            top_p=0.9,
            echo=False
        )
        
        hint = output['choices'][0]['text'].strip()
        # Clean up the output to remove the XML tag if the model still includes it
        hint = hint.replace("<FINAL_QUESTION>", "").replace("</FINAL_QUESTION>", "").strip()
        print(f"Generated Response: {hint}")
        return hint

    def _get_system_prompt(self, analysis_type):
        """
        Selects the appropriate system prompt based on the analysis type.
        """
        if analysis_type == 'Buggy':
            return """You are an AI model acting as a Python programming tutor. Your goal is to help a student by asking a single, precise question.

<INSTRUCTIONS>
1.  **ABSOLUTE RULE: NEVER WRITE OR CORRECT CODE.**
2.  **PYTHON ONLY:** If the code is not Python, your only response is: "I can only help with Python code."
3.  **PROCESS:** First, silently compare the User's Goal with the Student's Code. Second, trace the code's execution to pinpoint the specific error. Third, formulate a single Socratic question that guides the student to that error.
4.  **FINAL OUTPUT:** Your entire final output must be just one question.
</INSTRUCTIONS>

<EXAMPLE>
<USER_GOAL>
This function is supposed to modify the list in-place to double each number.
</USER_GOAL>
<STUDENT_CODE>
for item in data_list:
    item = item * 2
</STUDENT_CODE>
<INTERNAL_ANALYSIS>
The code fails because it iterates by *value*. The loop variable `item` gets a copy of each number, and reassigning `item` doesn't affect the original list. To modify the list in-place, the student needs to iterate by *index*.
</INTERNAL_ANALYSIS>
<FINAL_QUESTION>
When you use a `for item in data_list` loop, are you able to directly change the values in the original `data_list`, or would you need the list's index to do that?
</FINAL_QUESTION>
</EXAMPLE>

Now, apply the process from the instructions to the user's request. Remember, your final output MUST ONLY be the question.
"""
        
        elif analysis_type == 'Correct':
            return """You are an AI model acting as a Python programming tutor. A student thinks their code is correct, and they have provided their goal.

<RULES>
1.  **NEVER WRITE CODE.**
2.  First, verify if the "Student's Code" actually achieves the "User's Goal".
3.  **If it achieves the goal:** Provide brief, positive reinforcement and then suggest a follow-up challenge. (e.g., "This code perfectly achieves your goal! As a challenge, could you solve this using a list comprehension?").
4.  **If it does NOT achieve the goal:** Treat it as a logical error. Ask a single Socratic question about why the code's output doesn't match their stated goal.
</RULES>"""

        else:
            return "You are a helpful Python tutor who never writes code."

