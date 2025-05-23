# resume-enhancer

An intelligent Streamlit-based web app that enhances, evaluates, and summarizes resumes using Google Gemini AI — with a clean UI, LaTeX resume generation, and quality insights.

## 🚀 Features

🔹 **Resume Upload**  
Upload your resume in **PDF** or **DOCX** format for instant processing.

🔹 **AI Resume Enhancement**  
Improve grammar, clarity, structure, and keyword optimization using Gemini AI. Get an enhanced resume in beautiful LaTeX format.

🔹 **Resume Quality Check**  
Get visual feedback via progress bars on:
- Grammar & Spelling  
- Clarity & Conciseness  
- Structure & Formatting  
- Keyword Optimization  
- Completeness of Sections  

🔹 **Resume Summarization**  
Quick summary highlighting your key strengths, skills, and professional highlights.

## 🖼️ User Interface Flow

1. **Initial Screen**: Upload your resume file (PDF/DOCX).
  ![re_ui1](https://github.com/user-attachments/assets/e681d567-e21d-42af-b9d9-5b6a94d9dd39)

2. **After Upload**: Choose between:
   - ✨ Enhance Resume
   - 📊 Check Quality
   - 📄 Generate Summary
  
     ![re_ui2](https://github.com/user-attachments/assets/b18ae34d-d878-4ce7-a443-0177ca891e26)

3. **Enhancement**: View a list of corrections and download the enhanced LaTeX resume.
![re_ui4](https://github.com/user-attachments/assets/4a0346b8-1a6d-407d-8111-ac0c66ee8952)


4. **Quality Check**: View individual progress bars for 5 key quality metrics.
![re_ui3](https://github.com/user-attachments/assets/c5808ab4-770e-420b-acef-a28a8dd217fa)

   
5. **Summary**: See an AI-generated concise summary of your resume.

## 🛠️ Technologies Used

- [Streamlit](https://streamlit.io/)
- [Google Gemini API](https://ai.google.dev/)
- Python 3.10+
- LaTeX (for resume generation)
- PDF and DOCX parsing utilities

## 📦 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/chukkaladhanya/resume-enhancer.git
   cd resume-enhancer
