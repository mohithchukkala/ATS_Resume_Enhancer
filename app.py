import streamlit as st
from resume_utilis import extract_text_from_pdf, extract_text_from_docx
import google.generativeai as genai
import re

genai.configure(api_key="AIzaSyCU6AUNuasUZiiwT6PAjLbnflrnfYfNjWM")

st.set_page_config(page_title="Smart Resume Enhancer", page_icon="📄", layout="centered")

st.title("📄 Smart Resume Enhancer")

# --- Helpers ---
def convert_bold_markdown_to_latex(text):
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'\\textbf{\1}', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', text)
    return text

def lines_to_latex_items(text):
    lines = text.split('\n')
    latex_lines = []
    for line in lines:
        line = line.strip()
        if line.startswith('* ') or line.startswith('- '):
            latex_lines.append(r'  \item ' + line[2:].strip())
        elif line:
            latex_lines.append(r'  \item ' + line.strip())
    return '\n'.join(latex_lines)

def escape_latex(text):
    replacements = {
        '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_',
        '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}',
        '^': r'\^{}'
    }
    for key, val in replacements.items():
        text = text.replace(key, val)
    return text

def process_section_content(text, use_list=False):
    text = convert_bold_markdown_to_latex(text)
    text = escape_latex(text)
    if use_list:
        return lines_to_latex_items(text)
    return text

def section_block(title, content, use_list=False):
    body = process_section_content(content, use_list)
    if use_list:
        return f"\\section*{{{title}}}\n\\begin{{itemize}}\n{body}\n\\end{{itemize}}\n"
    else:
        return f"\\section*{{{title}}}\n{body}\n"

def parse_sections(text):
    sections = {
        "Objective": "No relevant data found",
        "Education": "No relevant data found",
        "Experience": "No relevant data found",
        "Skills": "No relevant data found",
        "Projects": "No relevant data found",
        "Certifications": "No relevant data found",
        "Extracurricular Activities": "No relevant data found",
        "Declaration": "No relevant data found"
    }
    current_section = None
    collected = []

    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
        if any(heading.lower() in line.lower() for heading in sections):
            if current_section and collected:
                sections[current_section] = '\n'.join(collected)
                collected = []
            for key in sections:
                if key.lower() in line.lower():
                    current_section = key
                    break
        elif current_section:
            collected.append(line)

    if current_section and collected:
        sections[current_section] = '\n'.join(collected)

    return sections

def get_quality_scores(text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = (
        "Evaluate the following resume based on these 5 criteria. Return a score (0 to 100) for each in this format:\n\n"
        "Grammar & Spelling: [score]\n"
        "Clarity & Conciseness: [score]\n"
        "Structure & Formatting: [score]\n"
        "Keyword Optimization: [score]\n"
        "Completeness of Sections: [score]\n\n"
        "Resume:\n" + text
    )
    response = model.generate_content(prompt).text

    scores = {}
    for line in response.splitlines():
        parts = line.split(":")
        if len(parts) == 2:
            label = parts[0].strip()
            try:
                score = int(parts[1].strip().replace('%', ''))
                scores[label] = max(0, min(score, 100))  # Clamp between 0–100
            except:
                pass
    return scores

def parse_corrections(text):
    lines = text.split('\n')
    corrections = []
    capture = False
    for line in lines:
        if "corrections" in line.lower():
            capture = True
            continue
        if capture:
            if line.startswith("-") or line.startswith("*"):
                corrections.append(line.lstrip("-* ").strip())
            elif line == "":
                break
            else:
                corrections.append(line)
    return corrections if corrections else [text]

def get_resume_summary(text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = (
        "Summarize the following resume in a concise paragraph highlighting key skills, experience, and education:\n\n"
        + text
    )
    response = model.generate_content(prompt).text
    return response.strip()

# --- UI Logic ---

uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    ext = uploaded_file.name.split('.')[-1].lower()
    resume_text = extract_text_from_pdf(uploaded_file) if ext == "pdf" else extract_text_from_docx(uploaded_file)

    st.markdown("---")
    st.info("Select an action below:")

    col1, col2, col3 = st.columns(3)
    with col1:
        btn_enhance = st.button("🚀 Improve & Download")
    with col2:
        btn_quality = st.button("📊 Quality Insights")
    with col3:
        btn_summary = st.button("📝 Quick Summary")

    if btn_enhance:
        with st.spinner("Enhancing resume and generating corrections..."):
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = (
                "You're a resume enhancer bot. Given the following resume text, improve it by fixing grammar, "
                "phrasing, and structure. Return in this format:\n\n"
                "Improved Resume:\n"
                "[Improved resume organized into sections like Objective, Education, Experience, Skills, Projects, Certifications, Extracurricular Activities, Declaration]\n\n"
                "Corrections:\n"
                "- Correction 1\n- Correction 2\n..."
            )
            response = model.generate_content(prompt + "\n\n" + resume_text)
            response_text = response.text

            if "Corrections:" in response_text:
                improved_resume = response_text.split("Corrections:")[0].replace("Improved Resume:", "").strip()
                corrections_text = response_text.split("Corrections:")[1].strip()
            else:
                improved_resume = response_text.strip()
                corrections_text = ""

            sections = parse_sections(improved_resume)
            corrections = parse_corrections(corrections_text)

            latex_code = (
                "\\documentclass[11pt]{article}\n"
                "\\usepackage[margin=1in]{geometry}\n"
                "\\usepackage[utf8]{inputenc}\n"
                "\\usepackage{enumitem}\n"
                "\\usepackage{titlesec}\n"
                "\\titleformat{\\section}{\\large\\bfseries}{}{0em}{}\n\n"
                "\\title{Enhanced Resume}\n"
                "\\date{}\n\n"
                "\\begin{document}\n"
                "\\maketitle\n\n"
                + section_block("Objective", sections["Objective"], use_list=False)
                + section_block("Education", sections["Education"], use_list=True)
                + section_block("Experience", sections["Experience"], use_list=True)
                + section_block("Skills", sections["Skills"], use_list=True)
                + section_block("Projects", sections["Projects"], use_list=True)
                + section_block("Certifications", sections["Certifications"], use_list=True)
                + section_block("Extracurricular Activities", sections["Extracurricular Activities"], use_list=True)
                + section_block("Declaration", sections["Declaration"], use_list=False)
                + "\\end{document}"
            )

        st.success("✅ Resume enhanced successfully!")
        st.subheader("🛠️ Corrections Made")
        for idx, correction in enumerate(corrections, 1):
            st.markdown(f"**{idx}.** {correction}")

        st.download_button("📥 Download Enhanced LaTeX Resume", latex_code, file_name="enhanced_resume.tex")

    if btn_quality:
        with st.spinner("Analyzing resume quality..."):
            quality_scores = get_quality_scores(resume_text)
        st.subheader("📊 Resume Quality Evaluation")
        for criterion, score in quality_scores.items():
            st.markdown(f"**{criterion} — {score}%**")
            st.progress(score / 100)

    if btn_summary:
        with st.spinner("Generating resume summary..."):
            summary = get_resume_summary(resume_text)
        st.subheader("📝 Resume Summary")
        st.write(summary)

else:
    st.info("Please upload a resume to get started.")


