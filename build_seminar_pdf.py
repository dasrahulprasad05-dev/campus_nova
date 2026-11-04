"""
Script to build the official 30-Page B.Tech Academic Project Seminar Report PDF
for CampusNova AI (Ajay Binay Institute of Technology, BPUT, 2022-2026 Batch).
Featuring 8 authentic website screenshots across Pages 28 & 29 with pure white backgrounds.
"""

import os
import re
import sys
import base64
import mistune

REPORT_MD_PATH = r"d:\campusnova\CAMPUSNOVA_30_PAGE_SEMINAR_REPORT.md"
SCREENSHOTS_DIR = r"d:\campusnova\screenshots"
HTML_OUTPUT_PATH = r"d:\campusnova\campusnova_report.html"
PDF_OUTPUT_PATH = r"d:\campusnova\CAMPUSNOVA_30_PAGE_SEMINAR_REPORT.pdf"

def get_base64_images():
    b64_dict = {}
    for i in range(1, 9):
        for f in os.listdir(SCREENSHOTS_DIR):
            if f.startswith(f"screen_{i}_") and f.endswith(".png"):
                full_path = os.path.join(SCREENSHOTS_DIR, f)
                with open(full_path, "rb") as img_f:
                    data = base64.b64encode(img_f.read()).decode("utf-8")
                    b64_dict[i] = data
                break
    return b64_dict

def extract_pages(md_content):
    pattern = r'={20,}\s*\n\s*PAGE\s+(\d+)\s*\n\s*={20,}\s*\n(?:```)?'
    matches = list(re.finditer(pattern, md_content))
    pages = {}
    for i in range(len(matches)):
        p_num = int(matches[i].group(1))
        start = matches[i].end()
        end = matches[i+1].start() if i+1 < len(matches) else len(md_content)
        chunk = md_content[start:end].strip()
        if chunk.startswith("```"):
            chunk = chunk[3:].lstrip()
        if chunk.endswith("```"):
            chunk = chunk[:-3].rstrip()
        pages[p_num] = chunk
    return pages

def format_page_28(images_b64):
    """Page 28: Chapter 10 UI Showcase Part I (Screens 1 to 4)"""
    return f"""
    <div class="page" id="page-28">
        <div class="page-header">
            <span class="hdr-left">AJAY BINAY INSTITUTE OF TECHNOLOGY, KATAKA</span>
            <span class="hdr-right">B.Tech Project Seminar (CSE 2022–2026)</span>
        </div>
        <div class="page-body">
            <h2 class="showcase-main-h2">CHAPTER 10: DEPLOYED APPLICATION SHOWCASE (PART I)</h2>
            <div class="showcase-subhead">Core Predictive Intelligence, Package Estimation & Early-Warning Explainability (White Theme)</div>
            
            <div class="showcase-grid-2x2">
                <!-- Screen 1 -->
                <div class="showcase-card">
                    <div class="sc-title">
                        <span class="sc-fig">Fig 10.1</span> Executive Analytics Dashboard & Model Telemetry
                    </div>
                    <div class="sc-img-wrap">
                        <img src="data:image/png;base64,{images_b64.get(1, '')}" class="sc-img" alt="Screen 1: Dashboard">
                    </div>
                    <div class="sc-meta">
                        <p><strong>Core Functionality:</strong> Central T&P cockpit aggregating global ML metrics, branch-wise placement percentages, and active ASGI microservice health telemetry.</p>
                        <p><strong>Live Output:</strong> 95.31% Decision Tree Accuracy, ±0.21 LPA Ridge Regressor MAE, 2,907 Dataset records, 11 tech roles, and 100% Pytest pass badge.</p>
                    </div>
                </div>
                
                <!-- Screen 2 -->
                <div class="showcase-card">
                    <div class="sc-title">
                        <span class="sc-fig">Fig 10.2</span> Placement Probability Predictor & Radial Gauge
                    </div>
                    <div class="sc-img-wrap">
                        <img src="data:image/png;base64,{images_b64.get(2, '')}" class="sc-img" alt="Screen 2: Placement Predictor">
                    </div>
                    <div class="sc-meta">
                        <p><strong>Core Functionality:</strong> Ingests student CGPA, internships, backlogs, and stream to execute real-time Scikit-Learn pipeline inference with zero data leakage.</p>
                        <p><strong>Live Output:</strong> Radial probability gauge displaying <strong>95.3% Likelihood</strong>, status <strong>HIGH PROBABILITY - JOB READY</strong>, with 1.24 ms latency.</p>
                    </div>
                </div>
                
                <!-- Screen 3 -->
                <div class="showcase-card">
                    <div class="sc-title">
                        <span class="sc-fig">Fig 10.3</span> Expected CTC Salary Regressor & Tiers
                    </div>
                    <div class="sc-img-wrap">
                        <img src="data:image/png;base64,{images_b64.get(3, '')}" class="sc-img" alt="Screen 3: CTC Regressor">
                    </div>
                    <div class="sc-meta">
                        <p><strong>Core Functionality:</strong> Ridge regression estimating realistic compensation brackets based on academic marks, aptitude, and non-linear internship interaction terms.</p>
                        <p><strong>Live Output:</strong> Projected Offer: <strong>₹ 8.45 LPA</strong> (Bracket: ₹ 7.50 – ₹ 9.40 LPA), corporate category <strong>Tier-2 Specialist / Product</strong> with itemized drivers.</p>
                    </div>
                </div>
                
                <!-- Screen 4 -->
                <div class="showcase-card">
                    <div class="sc-title">
                        <span class="sc-fig">Fig 10.4</span> Early-Warning At-Risk Explainability (XAI)
                    </div>
                    <div class="sc-img-wrap">
                        <img src="data:image/png;base64,{images_b64.get(4, '')}" class="sc-img" alt="Screen 4: At-Risk Explainer">
                    </div>
                    <div class="sc-meta">
                        <p><strong>Core Functionality:</strong> Prescriptive XAI diagnostic engine identifying vulnerable student profiles (P &lt; 0.40) to deliver immediate corrective roadmaps before placement drives.</p>
                        <p><strong>Live Output:</strong> High-risk case (28.4% prob), feature detractor penalties (-35% for backlogs, -25% for 0 internships), and 3 prioritized prescriptive remediation actions.</p>
                    </div>
                </div>
            </div>
        </div>
        <div class="page-footer">
            <span class="ftr-left">CampusNova AI: Placement Intelligence & Data Science Platform</span>
            <span class="ftr-right">Page 28 of 30</span>
        </div>
    </div>
    """

def format_page_29(images_b64):
    """Page 29: Chapter 10 UI Showcase Part II (Screens 5 to 8)"""
    return f"""
    <div class="page" id="page-29">
        <div class="page-header">
            <span class="hdr-left">AJAY BINAY INSTITUTE OF TECHNOLOGY, KATAKA</span>
            <span class="hdr-right">B.Tech Project Seminar (CSE 2022–2026)</span>
        </div>
        <div class="page-body">
            <h2 class="showcase-main-h2">CHAPTER 10: DEPLOYED APPLICATION SHOWCASE (PART II)</h2>
            <div class="showcase-subhead">Technical Resume NLP, Skill Taxonomy, Hybrid RAG Mentor & Telemetry Ledger</div>
            
            <div class="showcase-grid-2x2">
                <!-- Screen 5 -->
                <div class="showcase-card">
                    <div class="sc-title">
                        <span class="sc-fig">Fig 10.5</span> Technical Resume NLP Screener & Classifier
                    </div>
                    <div class="sc-img-wrap">
                        <img src="data:image/png;base64,{images_b64.get(5, '')}" class="sc-img" alt="Screen 5: Resume Screener">
                    </div>
                    <div class="sc-meta">
                        <p><strong>Core Functionality:</strong> Sublinear TF-IDF vectorizer (2,500 features) + LinearSVC pipeline mapping unstructured candidate resumes to 11 tech domain roles.</p>
                        <p><strong>Live Output:</strong> Identified Domain: <strong>Full-Stack Web Developer</strong> with <strong>98.5% Accuracy</strong>, extracting 7 verified technical tokens (React, SQL, FastAPI).</p>
                    </div>
                </div>
                
                <!-- Screen 6 -->
                <div class="showcase-card">
                    <div class="sc-title">
                        <span class="sc-fig">Fig 10.6</span> Skill-Gap Taxonomy & Corporate Benchmark
                    </div>
                    <div class="sc-img-wrap">
                        <img src="data:image/png;base64,{images_b64.get(6, '')}" class="sc-img" alt="Screen 6: Skill Gap">
                    </div>
                    <div class="sc-meta">
                        <p><strong>Core Functionality:</strong> Differential competency analysis comparing student technical profile against corporate job descriptions to isolate high-impact missing skills.</p>
                        <p><strong>Live Output:</strong> 5 Matched Competencies (React, Node.js, Git, SQL, Python), 3 Critical Missing Gaps (Docker, Redis, Automated Testing), and target action plan.</p>
                    </div>
                </div>
                
                <!-- Screen 7 -->
                <div class="showcase-card">
                    <div class="sc-title">
                        <span class="sc-fig">Fig 10.7</span> Hybrid RAG AI Placement Mentor in Action
                    </div>
                    <div class="sc-img-wrap">
                        <img src="data:image/png;base64,{images_b64.get(7, '')}" class="sc-img" alt="Screen 7: RAG Mentor">
                    </div>
                    <div class="sc-meta">
                        <p><strong>Core Functionality:</strong> Dual-tier conversational interview mentor using local BM25 over 70+ FAANG questions with automatic fallback to Google Gemini Flash API.</p>
                        <p><strong>Live Output:</strong> Technical interview answer on the <strong>CAP Theorem</strong> with structured Consistency, Availability, and Partition Tolerance proofs and follow-up Q&A cards.</p>
                    </div>
                </div>
                
                <!-- Screen 8 -->
                <div class="showcase-card">
                    <div class="sc-title">
                        <span class="sc-fig">Fig 10.8</span> Prediction Audit Ledger & Relational Store
                    </div>
                    <div class="sc-img-wrap">
                        <img src="data:image/png;base64,{images_b64.get(8, '')}" class="sc-img" alt="Screen 8: Audit History">
                    </div>
                    <div class="sc-meta">
                        <p><strong>Core Functionality:</strong> Relational telemetry database (SQLite3 WAL mode) auditing student predictions with candidate search, stream filters, and CSV export controls.</p>
                        <p><strong>Live Output:</strong> Relational table tracking 124 logged student inferences (Rahul Das: 95.3%, Purnachandra Swain: 92.1%, Rohit Thakur: 84.6%), with <code>[📥 Export CSV]</code>.</p>
                    </div>
                </div>
            </div>
        </div>
        <div class="page-footer">
            <span class="ftr-left">CampusNova AI: Placement Intelligence & Data Science Platform</span>
            <span class="ftr-right">Page 29 of 30</span>
        </div>
    </div>
    """

def format_page_content(p_num, markdown_text, images_b64):
    if p_num == 28:
        return format_page_28(images_b64)
    if p_num == 29:
        return format_page_29(images_b64)
        
    html = mistune.html(markdown_text)
    
    header_html = ""
    footer_html = ""
    if p_num > 1:
        header_html = f"""
        <div class="page-header">
            <span class="hdr-left">AJAY BINAY INSTITUTE OF TECHNOLOGY, KATAKA</span>
            <span class="hdr-right">B.Tech Project Seminar (CSE 2022–2026)</span>
        </div>
        """
        footer_html = f"""
        <div class="page-footer">
            <span class="ftr-left">CampusNova AI: Placement Intelligence & Data Science Platform</span>
            <span class="ftr-right">Page {p_num} of 30</span>
        </div>
        """
    
    # Custom styling for cover page (Page 1)
    if p_num == 1:
        return f"""
        <div class="page cover-page" id="page-{p_num}">
            <div class="cover-content">
                {html}
            </div>
        </div>
        """
    
    return f"""
    <div class="page" id="page-{p_num}">
        {header_html}
        <div class="page-body">
            {html}
        </div>
        {footer_html}
    </div>
    """

def generate_html(pages, images_b64):
    css_styles = """
    @page {
        size: A4 portrait;
        margin: 0;
    }
    *, *::before, *::after {
        box-sizing: border-box;
    }
    body {
        margin: 0;
        padding: 0;
        background-color: #ffffff;
        font-family: 'Times New Roman', Times, serif;
        font-size: 10.5pt;
        line-height: 1.45;
        color: #0f172a;
        -webkit-font-smoothing: antialiased;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }
    .page {
        width: 210mm;
        height: 297mm;
        padding: 13mm 18mm 13mm 20mm;
        margin: 0 auto;
        position: relative;
        page-break-after: always;
        page-break-inside: avoid;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        background-color: #ffffff;
        overflow: hidden;
    }
    .page:last-child {
        page-break-after: avoid;
    }
    .page-header {
        height: 12mm;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1.5px solid #0f172a;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 8pt;
        font-weight: 600;
        color: #334155;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 3mm;
    }
    .page-footer {
        height: 10mm;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-top: 1px solid #cbd5e1;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 8pt;
        color: #64748b;
        margin-top: 3mm;
    }
    .ftr-right {
        font-weight: 700;
        color: #0f172a;
    }
    .page-body {
        flex: 1;
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }
    h1, h2, h3, h4 {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #0f172a;
        margin-top: 0;
        margin-bottom: 2mm;
        font-weight: 700;
    }
    h1 {
        font-size: 15pt;
        line-height: 1.25;
        text-align: center;
        letter-spacing: 0.5px;
    }
    h2 {
        font-size: 12pt;
        line-height: 1.3;
        border-bottom: 1px solid #e2e8f0;
        padding-bottom: 1.5mm;
        margin-top: 1mm;
    }
    h3 {
        font-size: 10pt;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1.5mm;
    }
    h4 {
        font-size: 9pt;
        font-weight: 600;
        color: #334155;
        margin-bottom: 1mm;
    }
    p {
        margin-top: 0;
        margin-bottom: 1.8mm;
        text-align: justify;
        line-height: 1.38;
    }
    ul, ol {
        margin-top: 0;
        margin-bottom: 1.8mm;
        padding-left: 5mm;
    }
    li {
        margin-bottom: 0.8mm;
        line-height: 1.32;
    }
    hr {
        border: none;
        border-top: 1px solid #cbd5e1;
        margin: 2.5mm 0;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 1.5mm;
        margin-bottom: 2mm;
        font-size: 8pt;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    th, td {
        border: 1px solid #94a3b8;
        padding: 4px 6px;
        text-align: left;
        line-height: 1.25;
    }
    th {
        background-color: #f1f5f9;
        color: #0f172a;
        font-weight: 700;
        text-transform: uppercase;
        font-size: 7.5pt;
        letter-spacing: 0.4px;
    }
    tr:nth-child(even) td {
        background-color: #fafafa;
    }
    pre {
        background-color: #ffffff;
        border: 1px solid #94a3b8;
        border-radius: 3px;
        padding: 4px 7px;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 7pt;
        line-height: 1.2;
        overflow: hidden;
        white-space: pre-wrap;
        word-break: break-all;
        margin-top: 1.5mm;
        margin-bottom: 1.8mm;
        color: #0f172a;
    }
    code {
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 8pt;
        background-color: #f1f5f9;
        padding: 1px 3px;
        border-radius: 2px;
        color: #0f172a;
    }
    pre code {
        background-color: transparent;
        padding: 0;
        font-size: 7pt;
    }
    blockquote {
        margin: 1.5mm 0;
        padding: 2mm 4mm;
        background-color: #f8fafc;
        border-left: 3px solid #2563eb;
        font-size: 9pt;
        font-style: italic;
    }
    .cover-page {
        justify-content: center;
        text-align: center;
        border: 2px solid #0f172a;
        margin: 4mm;
        width: 202mm;
        height: 289mm;
        padding: 14mm 16mm;
    }
    .cover-content {
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .cover-content h1 {
        font-size: 16pt;
        letter-spacing: 1px;
        margin-bottom: 2mm;
    }
    .cover-content h3 {
        font-size: 11pt;
        color: #334155;
    }
    .cover-content hr {
        border-top: 2px solid #0f172a;
        margin: 3mm 0;
    }
    .cover-content table {
        margin: 0 auto;
        width: 90%;
    }
    
    /* Dedicated Showcase Styles for Pages 28 & 29 */
    .showcase-main-h2 {
        font-size: 11pt;
        font-weight: 800;
        color: #1e3a8a;
        text-transform: uppercase;
        margin-bottom: 0.8mm;
        border-bottom: 1.5px solid #1e3a8a;
        padding-bottom: 0.8mm;
    }
    .showcase-subhead {
        font-size: 8pt;
        color: #475569;
        font-style: italic;
        margin-bottom: 2mm;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    .showcase-grid-2x2 {
        display: grid;
        grid-template-columns: 1fr 1fr;
        grid-template-rows: 1fr 1fr;
        gap: 2mm;
        flex: 1;
        overflow: hidden;
    }
    .showcase-card {
        background-color: #ffffff;
        border: 1px solid #94a3b8;
        border-radius: 4px;
        padding: 2mm 2.5mm;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        overflow: hidden;
    }
    .sc-title {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 8pt;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 1mm;
        display: flex;
        align-items: center;
        gap: 4px;
    }
    .sc-fig {
        background-color: #eff6ff;
        color: #1d4ed8;
        border: 1px solid #bfdbfe;
        font-size: 7pt;
        font-weight: 800;
        padding: 1px 3px;
        border-radius: 3px;
    }
    .sc-img-wrap {
        width: 100%;
        height: 58mm;
        border: 1px solid #cbd5e1;
        border-radius: 3px;
        overflow: hidden;
        margin-bottom: 1mm;
        background-color: #ffffff;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .sc-img {
        width: 100%;
        height: 100%;
        object-fit: contain;
    }
    .sc-meta {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 7.2pt;
        line-height: 1.22;
        color: #334155;
    }
    .sc-meta p {
        margin: 0 0 0.8mm 0;
        text-align: left;
    }
    .sc-meta strong {
        color: #0f172a;
    }

    /* Page-specific compact adjustments */
    #page-25 pre, #page-26 pre {
        font-size: 6.8pt;
        line-height: 1.15;
        padding: 3px 5px;
    }
    #page-27 table {
        font-size: 7.5pt;
    }
    #page-27 pre {
        font-size: 6.5pt;
        line-height: 1.15;
        margin: 1mm 0;
    }
    #page-27 p, #page-27 li {
        font-size: 8.5pt;
        line-height: 1.28;
    }
    #page-6 table {
        font-size: 7.8pt;
    }
    #page-6 p {
        font-size: 8.5pt;
        margin-bottom: 1mm;
    }
    #page-7 p {
        font-size: 8.8pt;
        line-height: 1.32;
        margin-bottom: 1.5mm;
    }
    #page-16 pre, #page-18 pre {
        font-size: 6.8pt;
        line-height: 1.15;
        border: 1px dashed #64748b;
    }
    #page-30 ol, #page-30 ul {
        font-size: 7.2pt;
        padding-left: 4mm;
    }
    #page-30 li {
        margin-bottom: 0.6mm;
    }
    """

    body_html = ""
    for p_num in range(1, 31):
        md_text = pages.get(p_num, f"<h1>Page {p_num}</h1>")
        body_html += format_page_content(p_num, md_text, images_b64)

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>CampusNova AI - B.Tech Project Seminar Report (30 Pages)</title>
    <style>
        {css_styles}
    </style>
</head>
<body>
    {body_html}
</body>
</html>
"""
    with open(HTML_OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Generated HTML report with 8 embedded UI screenshots at: {HTML_OUTPUT_PATH}")

if __name__ == "__main__":
    if not os.path.exists(REPORT_MD_PATH):
        print(f"Error: {REPORT_MD_PATH} not found!")
        sys.exit(1)
    with open(REPORT_MD_PATH, "r", encoding="utf-8") as f:
        md = f.read()
    pages = extract_pages(md)
    print(f"Extracted {len(pages)} pages.")
    images_b64 = get_base64_images()
    print(f"Loaded {len(images_b64)} website screenshots into memory.")
    generate_html(pages, images_b64)
