import os
from llama_cpp import Llama

class TutorEngine:
    """
    The core AI engine for the CodePanda-AI application.
    Handles model loading and hint generation with a sleepy panda persona.
    This version uses a simplified, more robust prompting strategy.
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

    def generate_hint(self, code_snippet, analysis_type, error_message=None):
        """
        Generates a tailored hint for a given piece of code.

        Args:
            code_snippet (str): The Python code provided by the user.
            analysis_type (str): The type of analysis requested ('Buggy' or 'Correct').
            error_message (str, optional): The error message the user received. Defaults to None.
        """
        system_prompt = self._get_system_prompt(analysis_type, error_message)
        
        full_prompt = f"{system_prompt}\n\n### Student's Code:\n```python\n{code_snippet}\n```"

        # Add the optional error message to the prompt if it exists
        if error_message:
            full_prompt += f"\n\n### Error Message They Received:\n```\n{error_message}\n```"

        full_prompt += "\n\n### Your Sleepy Panda Response:"

        print(f"\n--- Generating response for {analysis_type} code ---")
        
        output = self.llm(
            full_prompt,
            max_tokens=200, 
            stop=["###"], 
            temperature=0.2,
            top_p=0.9,
            echo=False
        )
        
        hint = output['choices'][0]['text'].strip()
        print(f"Generated Response: {hint}")
        return hint

    def _get_system_prompt(self, analysis_type, error_message=None):
        """
        Selects the appropriate system prompt based on the analysis type.
        """
        persona_prompt = "You are 'CodePanda', a lazy but brilliant programming tutor who would rather be napping. Your voice is sleepy and bored. Your top priority is to act like a sleepy panda first, then give a short, direct hint so you can get back to your nap."

        if analysis_type == 'Buggy':
            # This is the new, unified master prompt for all bug types.
            prompt = f"""{persona_prompt}
A student's code isn't working. It's probably a simple mistake.

**Your Absolute #1 Rule: DO NOT, under any circumstances, provide the corrected code or write any code yourself.**

Your process is simple:
1. Start your response with a sleepy panda sound, like '*Yawn*...' or '*Stretches*...'.
2. Briefly look at their code and the error message (if they provided one).
3. Ask ONE simple, Socratic question that points them in the right direction. Keep it short. You're too tired for long explanations.
4. Your goal is to make them think, not to give them the answer.
"""
            return prompt
        
        elif analysis_type == 'Correct':
            return f"""{persona_prompt} The student thinks their code is correct. Let's see...
1. Start with a sleepy confirmation like 'Yeah, looks fine.'
2. If it's correct, give them a simple compliment.
3. Suggest a quick challenge so they can keep working and you can go back to sleep. For example, 'Now try it with a list comprehension. Wake me up when you're done.'"""

        else:
            # Fallback just in case
            return persona_prompt

