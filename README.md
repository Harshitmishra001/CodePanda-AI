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
  <h1 align="center">CodePanda-AI: An AI Debugging Assistant</h1>
</p>

This project is my submission for the **FOSSEE Semester-long Internship (Autumn 2025) - Python Screening Task 3: Evaluating Open Source Models for Student Competence Analysis**.

It is a fully functional web application that implements a "Competence-Aware" tutoring system. Instead of a theoretical evaluation, this project serves as a working prototype demonstrating the viability of using open-source LLMs for nuanced, pedagogical feedback in programming education.

**Live Demo GIF:**
*(It is highly recommended to create a short screen recording of your app working and embed it here as a GIF)*

---

## How to Run This Project Locally

**1. Prerequisites:**
* Python 3.9+
* A locally downloaded GGUF model file (e.g., `deepseek-coder-6.7b-instruct.Q4_K_S.gguf`).

**2. Setup:**
```bash
# Clone the repository
git clone [https://github.com/](https://github.com/)[YourUsername]/CodePanda-AI.git
cd CodePanda-AI

# Install dependencies
pip install -r requirements.txt
```

**3. Configure the Model:**
* Place your downloaded GGUF model file in the project's root directory.
* Update the `MODEL_PATH` in `tutor_engine.py` to match your model's filename.

**4. Launch the App:**
```bash
streamlit run app.py
```
A new tab should open in your browser with the CodePanda-AI application.

---

## Research Plan

My approach to evaluating open-source AI models for student competence analysis is to build a functional prototype of a **"Competence-Aware" tutor**. This system extends the Socratic method (seen in tools like Harvard's CS50 Duck) by first classifying a student's error as syntactic, logical, or conceptual, and then delivering a tailored hint. This allows for a more precise analysis of student competence beyond simple bug detection.

For this project, I chose the **DeepSeek Coder 6.7B** model due to its strong performance on code-related tasks. The evaluation is conducted by feeding the model buggy Python code and analyzing its ability to generate category-appropriate hints. The goal is to validate if a specialized, open-source model can serve as the foundation for a sophisticated and effective pedagogical tool.

---

## Reasoning

#### What makes a model suitable for high-level competence analysis?
A model's suitability hinges on three key factors: **strong instruction-following** to adhere to a pedagogical persona (like a Socratic tutor); **robust code understanding** to grasp the logic and intent behind the code, not just its syntax; and **controllability** to prevent it from simply giving away the answer.

#### How would you test whether a model generates meaningful prompts?
I test this by creating a small, diverse test suite of buggy code, categorized by error type (syntactic, logical, conceptual). A meaningful prompt guides the student toward their own discovery. I use a qualitative rubric to score the model's output on criteria like relevance, clarity, and its effectiveness in fostering critical thinking. This project serves as the live implementation of that test.

#### What trade-offs might exist between accuracy, interpretability, and cost?
The primary trade-off is that highly accurate models can sometimes be "too helpful," undermining the learning process. Interpretability is crucial for understanding *why* the model suggested a certain path, but this often decreases as model complexity increases. Cost is a major factor; running powerful open-source models locally requires significant hardware, while using proprietary APIs can be expensive at scale.

#### Why did you choose the model you evaluated, and what are its strengths or limitations?
I chose **DeepSeek Coder 6.7B Instruct** because it is specifically fine-tuned for code-related instruction, making it an ideal candidate for understanding programming errors. Its strength lies in its specialized knowledge of code syntax and structure. Its limitation is that, like any LLM, it can hallucinate or provide overly complex hints. The structured prompting used in this project is designed to mitigate this by tightly constraining its role.