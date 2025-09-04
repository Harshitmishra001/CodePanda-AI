<p align="center">
  <svg width="150" height="150" viewBox="0 0 1024 1024" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M512 1024C795.836 1024 1024 795.836 1024 512C1024 228.164 795.836 0 512 0C228.164 0 0 228.164 0 512C0 795.836 228.164 1024 512 1024Z" fill="#FFFFFF"/>
    <path d="M512 962.758C765.348 962.758 962.758 765.348 962.758 512C962.758 258.652 765.348 61.2418 512 61.2418C258.652 61.2418 61.2418 258.652 61.2418 512C61.2418 765.348 258.652 962.758 512 962.758Z" fill="#FFFFFF" stroke="#1F2328" stroke-width="60"/>
    <path d="M380.082 458.077C380.082 458.077 425.438 412.721 445.148 412.721C464.858 412.721 480.959 445.148 480.959 445.148L495.255 316.326C495.255 316.326 480.959 285.704 445.148 285.704C409.336 285.704 380.082 322.449 380.082 322.449L380.082 458.077Z" fill="#1F2328"/>
    <path d="M643.918 458.077C643.918 458.077 598.562 412.721 578.852 412.721C559.142 412.721 543.041 445.148 543.041 445.148L528.745 316.326C528.745 316.326 543.041 285.704 578.852 285.704C614.664 285.704 643.918 322.449 643.918 322.449L643.918 458.077Z" fill="#1F2328"/>
    <path d="M666.611 635.83C666.611 701.373 607.729 746.729 512 746.729C416.271 746.729 357.389 701.373 357.389 635.83C357.389 570.286 422.394 543.041 512 543.041C601.606 543.041 666.611 570.286 666.611 635.83Z" fill="#1F2328"/>
    <ellipse cx="383.144" cy="557.337" rx="90.5408" ry="87.4786" fill="#1F2328"/>
    <ellipse cx="640.856" cy="557.337" rx="90.5408" ry="87.4786" fill="#1F2328"/>
  </svg>
  <h1 align="center">CodePanda-AI: An Intent-Aware Debugging Tutor</h1>
</p>

This project is my submission for the **FOSSEE Semester-long Internship (Autumn 2025) – Python Screening Task 3: Evaluating Open Source Models for Student Competence Analysis**.

It is a functional prototype of an **intent-aware AI tutor**. Instead of directly fixing code, CodePanda-AI analyzes the student’s programming goal and buggy Python code, then generates **Socratic hints** that guide the learner toward their own discovery.

> 🔎 **Why this matters**: General-purpose AI tools can short-circuit learning by giving full solutions. CodePanda-AI keeps the student in the driver’s seat by prompting reasoning rather than replacing it.

---

## 📽️ Image 

<img width="1920" height="1080" alt="Code1" src="https://github.com/user-attachments/assets/3ff9ab70-7141-4416-959e-8d4d4b579ec7" />

---

## 🚀 How to Run Locally

### 1) Prerequisites
- Python **3.9+**
- A locally downloaded **GGUF** model (e.g., `deepseek-coder-6.7b-instruct.Q4_K_S.gguf`)

### 2) Setup
```bash
# Clone the repository
git clone https://github.com/Harshitmishra001/CodePanda-AI.git
cd CodePanda-AI

# (Optional) Create and activate a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3) Configure the Model
- Place your downloaded **GGUF** model file in the project root (or a `models/` folder).
- Open `tutor_engine.py` and set:
```python
MODEL_PATH = "deepseek-coder-6.7b-instruct.Q4_K_S.gguf"  # update to your filename
```

### 4) Launch the App
```bash
streamlit run app.py
```
A browser tab will open with the CodePanda-AI interface.

---

## 📑 Research Plan

My research plan was to evaluate the suitability of the **DeepSeek Coder 6.7B** model for providing Socratic hints. I chose a practical methodology: build a functional prototype. This allowed me to test the model's capabilities in a real-world scenario, focusing on its ability to understand user intent and follow complex, restrictive instructions.

The inspiration came from *Rubber Duck Debugging*, where explaining code often reveals solutions. CodePanda-AI extends this idea by asking the student a single, well-targeted question, accelerating self-discovery.

Validation was iterative: I created test cases with common Python bugs and evaluated responses. Failures (e.g., giving away answers or copying instructions) were treated as bugs in the system. Through a **structured XML-like prompt**, the model consistently produced meaningful, pedagogically useful hints.

---

## 🧠 Reasoning

### What makes a model suitable for high-level competence analysis?
Through my experience building CodePanda-AI, I found that a model's suitability for this kind of teaching task isn't just about its size, but about three specific qualities. First, it needs to be excellent at instruction-following. My early tests showed that a model will default to giving away the answer unless it can precisely follow complex rules, especially "negative" rules like "do not write code." Second, it needs the ability to reason about user intent, which is why I made the user's goal a required input. The model had to be capable of comparing a plain English sentence to a Python script and identifying where they logically diverged. Finally, and most importantly, it must be highly controllable. I learned that this control wasn't a default feature, but something I had to build myself through a very structured and rigid prompt design.
### How would you test whether a model generates meaningful prompts?
My method for testing was a practical, hands-on feedback loop. I started by defining "meaningful" as a prompt that was Socratic (it had to be a question) and that guided the student to the root cause of their error without giving them the solution. I then developed a small suite of test cases with different kinds of common bugs—syntax errors, logical errors, and deeper conceptual mistakes. I fed these to the model and evaluated its output against my definition. When a hint was not meaningful (like when it asked a generic question or gave away the answer), I treated it as a bug in my own system. I would analyze why the AI failed and then refine my instructions to it, making them stricter and clearer. This process of testing, analyzing the failure, and improving the prompt was how I systematically increased the quality and reliability of the hints.
### What trade-offs might exist between accuracy, interpretability, and cost?
I encountered a few key trade-offs during this project. The most interesting one was between giving the AI a creative "persona" and its accuracy in following rules. My initial attempts to make the AI act like a cute panda resulted in unreliable and often incorrect responses. A more direct, rule-based prompt was far more reliable, so I had to trade the creative persona for accuracy and control. There was also a clear cost trade-off. By choosing to run a model locally, I made a conscious trade-off: I accepted the one-time hardware requirement for running the model on my machine in exchange for zero ongoing API costs. This also provided the huge benefits of privacy and the ability for the app to work completely offline, which is critical for an accessible educational tool.
### Why did you choose the model you evaluated, and what are its strengths or limitations?
My choice of DeepSeek Coder 6.7B Instruct was strategic and based on three main factors that made it perfect for a FOSSEE-aligned educational project.
  1. It's Lightweight and Accessible: As a 6.7B parameter model in a GGUF quantized format, it is lightweight enough to run effectively on consumer-grade hardware. This was a non-negotiable requirement for me, as it ensures the final application is accessible to students without needing powerful, expensive machines.
  2. It's Specialized for Code: The model is pre-trained on a massive amount of source code, giving it a strong, built-in understanding of programming logic and syntax.
  3. It's an "Instruct" Model: It is specifically fine-tuned to follow complex commands, which was the entire foundation of my prompt engineering strategy.
  4. Its main limitation, which I discovered during testing, was its susceptibility to "prompt leakage," where it would literally copy parts of the examples from my instructions instead of learning the process. However, this limitation became an opportunity. By redesigning my prompt to use a more rigid, XML-like structure, I was able to successfully overcome this issue, which in itself was a valuable engineering lesson in

---

## 🧩 Features
- Intent-aware analysis of **goal + code**  
- Generates exactly **one Socratic hint** per turn  
- Local, offline-first workflow (privacy-friendly)  
- Prompt templates designed for **controllability**  
- Extensible architecture for new hint strategies  

---

## 🔧 Configuration Tips
- Prefer **Q4_K_S** or **Q5_K_M** quantizations for a balance of memory and quality.  
- If running on CPU only, reduce **context_length** and **n_threads** for stability.  
- For GPUs with limited VRAM (e.g., 6GB), use a lower-precision GGUF and smaller **n_ctx**.

---

## 🛣️ Roadmap
- [ ] Maintain chat history for iterative guidance  
- [ ] Automatic bug-type classification (syntax / logic / conceptual)  
- [ ] VS Code plugin for in-editor tutoring  
- [ ] Export hint sessions as study notes

---

## 🤝 Acknowledgements & References
- [DeepSeek Coder 6.7B Instruct](https://huggingface.co/deepseek-ai)  
- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)  
- [Streamlit](https://streamlit.io)  

---

## 📝 License
MIT 
