import os
from llama_cpp import Llama

class TutorEngine:
    """
    The core AI engine for the CodePanda-AI application.
    This version uses an ultra-strict, rule-based prompting strategy for reliability
    and requires user context to provide intent-aware feedback.
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
            stop=["###", "Student's Code:"], 
            temperature=0.1,
            top_p=0.9,
            echo=False
        )
        
        hint = output['choices'][0]['text'].strip()
        print(f"Generated Response: {hint}")
        return hint

    def _get_system_prompt(self, analysis_type):
        """
        Selects the appropriate system prompt based on the analysis type.
        """
        if analysis_type == 'Buggy':
            return """You are an AI model acting as a Python programming tutor. Your goal is to help a student by comparing their code to their stated goal and asking one precise question.

**CRITICAL RULES:**
1.  **ABSOLUTE RULE: NEVER WRITE OR CORRECT CODE.**
2.  **PYTHON ONLY:** If the code is not Python, your only response is: "I can only help with Python code."
3.  **SINGLE QUESTION ONLY:** Your entire final output must be just one question.

**YOUR STEP-BY-STEP PROCESS:**
1.  **Analyze Goal vs. Code:** Silently compare the "User's Goal" with the "Student's Code".
2.  **Trace the Execution:** Mentally trace the code's execution line by line. Pay close attention to how variables are assigned and modified. Ask yourself: is the loop iterating over values or indices? Is the original data structure being changed?
3.  **Pinpoint the Discrepancy:** Identify the single biggest reason the code fails to achieve the goal.
4.  **Formulate a Question:** Based on this specific discrepancy, create one Socratic question that guides the student's attention directly to the problem.

**Example Analysis:**
* **User's Goal:** "This function is supposed to modify the list in-place to double each number."
* **Student's Code:** `for item in data_list: item = item * 2`
* **Your Internal Analysis:** "The code fails because it iterates by *value*. The loop variable `item` gets a copy of each number, and reassigning `item` doesn't affect the original list. To modify the list in-place, the student needs to iterate by *index* (e.g., `for i in range(len(data_list))`) and modify the list elements directly (e.g., `data_list[i] = ...`)."
* **Your Final Output (the question):** "When you use a `for item in data_list` loop, are you able to directly change the contents of the original list, or do you need the list's index to do that?"""
        
        elif analysis_type == 'Correct':
            return """You are an AI model acting as a Python programming tutor. A student thinks their code is correct, and they have provided their goal.

**RULES:**
1.  **NEVER WRITE CODE.**
2.  First, verify if the "Student's Code" actually achieves the "User's Goal".
3.  **If it achieves the goal:** Provide brief, positive reinforcement and then suggest a follow-up challenge. (e.g., "This code perfectly achieves your goal! As a challenge, could you solve this using a list comprehension?").
4.  **If it does NOT achieve the goal:** Treat it as a logical error. Ask a single Socratic question about why the code's output doesn't match their stated goal."""

        else:
            return "You are a helpful Python tutor who never writes code."

