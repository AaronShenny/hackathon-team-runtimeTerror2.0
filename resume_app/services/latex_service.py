import os
import subprocess
from django.conf import settings

def generate_latex(data):
    """
    Generates LaTeX code from resume data.
    """
    name = data.get("name", "John Doe")
    email = data.get("email", "john@example.com")
    phone = data.get("phone", "123-456-7890")
    summary = data.get("summary", "")
    experience = data.get("experience", [])
    education = data.get("education", [])
    skills = data.get("skills", [])

    full_name = data.get("name", "John Doe") or "John Doe"
    name_parts = full_name.split()
    first_name = name_parts[0] if name_parts else "John"
    last_name = name_parts[1] if len(name_parts) > 1 else ""
    
    email = data.get("email", "john@example.com")
    phone = data.get("phone", "123-456-7890")
    
    latex = r"""\documentclass[11pt,a4paper,sans]{moderncv}
\moderncvstyle{classic}
\moderncvcolor{blue}
\usepackage[utf8]{inputenc}
\usepackage[scale=0.75]{geometry}

\name{""" + first_name + "}{" + last_name + r"""}
\email{""" + email + r"""}
\phone{""" + phone + r"""}


\begin{document}
\makecvtitle

\section{Summary}
""" + summary + r"""

\section{Experience}
"""
    for exp in experience:
        latex += r"\cventry{" + exp.get("dates", "") + "}{" + exp.get("title", "") + "}{" + exp.get("company", "") + "}{}{}{" + exp.get("description", "") + "}\n"

    latex += r"""
\section{Education}
"""
    for edu in education:
        latex += r"\cventry{" + edu.get("dates", "") + "}{" + edu.get("degree", "") + "}{" + edu.get("school", "") + "}{}{}{}\n"

    latex += r"""
\section{Skills}
\cvitem{}{""" + ", ".join(skills) + r"""}

\end{document}
"""
    return latex

def compile_latex(latex_content, output_name="optimized_resume"):
    """
    Attempts to compile LaTeX to PDF.
    Returns the path to the PDF if successful, else None.
    """
    tex_path = os.path.join(settings.MEDIA_ROOT, f"{output_name}.tex")
    pdf_path = os.path.join(settings.MEDIA_ROOT, f"{output_name}.pdf")
    
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(latex_content)
        
    try:
        # Requires pdflatex to be installed on the system
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory", settings.MEDIA_ROOT, tex_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return pdf_path
    except Exception as e:
        print(f"LaTeX compilation failed: {e}")
        return None
