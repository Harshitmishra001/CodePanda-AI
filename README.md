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


---

## 🚀 How to Run Locally

### 1) Prerequisites
- Python **3.9+**
- A locally downloaded **GGUF** model (e.g., `deepseek-coder-6.7b-instruct.Q4_K_S.gguf`)

### 2) Setup
```bash
# Clone the repository
git clone https://github.com/YourUsername/CodePanda-AI.git
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
1. **Instruction-following precision** — especially for negative rules like *“do not write code.”*  
2. **Ability to reason over user intent** — comparing plain-English goals with code.  
3. **Controllability** — shaping the model’s behavior reliably through prompt engineering.  

### How would you test whether a model generates meaningful prompts?
Define “meaningful” as a **Socratic, guiding, non-solution-revealing** question. Test across diverse bugs (syntax, logic, recursion). Treat any poor hint as a system bug and refine prompts iteratively.

### What trade-offs exist between accuracy, interpretability, and cost?
- **Accuracy vs. Creativity:** A playful *panda persona* reduced reliability, so strict prompts were used.  
- **Cost vs. Accessibility:** Local execution needs modest hardware but avoids API fees and preserves privacy.  

### Why choose DeepSeek Coder 6.7B?
- **Lightweight & accessible** (runs on consumer hardware).  
- **Specialized for code** (pre-trained extensively on source code).  
- **Fine-tuned for instructions**, which is critical for a Socratic tutor.  
- **Limitation:** Susceptible to prompt leakage — mitigated via rigid, XML-style prompts.  

---

## 🧩 Features
- Intent-aware analysis of **goal + code**  
- Generates exactly **one Socratic hint** per turn  
- Local, offline-first workflow (privacy-friendly)  
- Prompt templates designed for **controllability**  
- Extensible architecture for new hint strategies  

---

## 🗂️ Suggested Repository Structure
```
CodePanda-AI/
├─ app.py
├─ tutor_engine.py
├─ prompts/
│  └─ socratic_prompt.xml
├─ models/
│  └─ deepseek-coder-6.7b-instruct.Q4_K_S.gguf   # (user-provided)
├─ requirements.txt
└─ README.md
```

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
