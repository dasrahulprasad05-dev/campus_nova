"""
Script to build the official 12-Slide B.Tech Academic Seminar Presentation (PPT) PDF
for CampusNova AI (Ajay Binay Institute of Technology, BPUT, 2022-2026 Batch).
"""

import os
import re
import sys
import mistune

PPT_MD_PATH = r"d:\campusnova\CAMPUSNOVA_12_SLIDE_SEMINAR_PPT.md"
HTML_OUTPUT_PATH = r"d:\campusnova\campusnova_presentation.html"
PDF_OUTPUT_PATH = r"d:\campusnova\CAMPUSNOVA_12_SLIDE_SEMINAR_PPT.pdf"

def extract_slides(md_content):
    pattern = r'={20,}\s*\n\s*SLIDE\s+(\d+)\s*\n\s*={20,}\s*\n(?:```)?'
    matches = list(re.finditer(pattern, md_content))
    slides = {}
    for i in range(len(matches)):
        s_num = int(matches[i].group(1))
        start = matches[i].end()
        end = matches[i+1].start() if i+1 < len(matches) else len(md_content)
        chunk = md_content[start:end].strip()
        if chunk.startswith("```"):
            chunk = chunk[3:].lstrip()
        if chunk.endswith("```"):
            chunk = chunk[:-3].rstrip()
        slides[s_num] = chunk
    return slides

def format_slide_content(s_num, markdown_text):
    html = mistune.html(markdown_text)
    
    header_html = f"""
    <div class="slide-header">
        <span class="hdr-inst">AJAY BINAY INSTITUTE OF TECHNOLOGY, KATAKA | CSE (2022–2026)</span>
        <span class="hdr-num">SLIDE {s_num:02d} / 12</span>
    </div>
    """
    
    footer_html = f"""
    <div class="slide-footer">
        <span class="ftr-title">CampusNova AI: B.Tech Placement Predictive Intelligence Platform</span>
        <span class="ftr-meta">Rahul Prasad Das (2301206094) & Team | Guide: Prof. Rajesh Kumar Sahoo</span>
    </div>
    """
    
    if s_num == 1:
        return f"""
        <div class="slide slide-title" id="slide-{s_num}">
            <div class="slide-inner">
                {html}
            </div>
            {footer_html}
        </div>
        """
        
    return f"""
    <div class="slide" id="slide-{s_num}">
        {header_html}
        <div class="slide-inner">
            {html}
        </div>
        {footer_html}
    </div>
    """

def generate_html(slides):
    css_styles = """
    @page {
        size: A4 landscape;
        margin: 0;
    }
    *, *::before, *::after {
        box-sizing: border-box;
    }
    body {
        margin: 0;
        padding: 0;
        background-color: #ffffff;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #0f172a;
        -webkit-font-smoothing: antialiased;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }
    .slide {
        width: 297mm;
        height: 210mm;
        padding: 10mm 15mm 10mm 15mm;
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
    .slide:last-child {
        page-break-after: avoid;
    }
    .slide-header {
        height: 8mm;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1.5px solid #2563eb;
        font-size: 8pt;
        font-weight: 700;
        color: #1e3a8a;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 3mm;
    }
    .hdr-num {
        background-color: #dbeafe;
        color: #1d4ed8;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: 800;
    }
    .slide-footer {
        height: 7mm;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-top: 1px solid #cbd5e1;
        font-size: 7.5pt;
        color: #64748b;
        margin-top: 2mm;
    }
    .ftr-meta {
        font-weight: 600;
        color: #334155;
    }
    .slide-inner {
        flex: 1;
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }
    h1 {
        font-size: 15pt;
        font-weight: 800;
        color: #0f172a;
        margin: 0 0 1.5mm 0;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }
    h2 {
        font-size: 12pt;
        font-weight: 700;
        color: #1e40af;
        margin: 0 0 1.5mm 0;
    }
    h3 {
        font-size: 9.5pt;
        font-weight: 700;
        color: #2563eb;
        margin: 1mm 0 1.5mm 0;
    }
    h4 {
        font-size: 8.5pt;
        font-weight: 700;
        color: #334155;
        margin: 1mm 0 1mm 0;
    }
    p {
        margin: 0 0 1.5mm 0;
        font-size: 8.5pt;
        line-height: 1.35;
        color: #334155;
    }
    ul, ol {
        margin: 0 0 1.5mm 0;
        padding-left: 5mm;
        font-size: 8.5pt;
    }
    li {
        margin-bottom: 0.8mm;
        line-height: 1.3;
    }
    hr {
        border: none;
        border-top: 1px solid #e2e8f0;
        margin: 2mm 0;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 1mm 0 2mm 0;
        font-size: 7.5pt;
    }
    th, td {
        border: 1px solid #94a3b8;
        padding: 3.5px 6px;
        text-align: left;
        line-height: 1.25;
    }
    th {
        background-color: #f1f5f9;
        color: #0f172a;
        font-weight: 700;
        text-transform: uppercase;
    }
    tr:nth-child(even) td {
        background-color: #f8fafc;
    }
    pre {
        background-color: #ffffff;
        border: 1px solid #94a3b8;
        border-radius: 4px;
        padding: 4px 6px;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 6.8pt;
        line-height: 1.15;
        overflow: hidden;
        white-space: pre-wrap;
        margin: 1mm 0 1.5mm 0;
        color: #0f172a;
    }
    code {
        font-family: 'Consolas', monospace;
        font-size: 7.5pt;
        background-color: #f1f5f9;
        padding: 1px 3px;
        border-radius: 2px;
    }
    blockquote {
        margin: 1mm 0;
        padding: 1.5mm 3mm;
        background-color: #f8fafc;
        border-left: 3px solid #10b981;
        font-size: 7.8pt;
        line-height: 1.3;
        color: #1e293b;
    }
    /* Title slide custom */
    .slide-title .slide-inner {
        text-align: center;
        justify-content: center;
    }
    .slide-title h1 {
        font-size: 18pt;
        color: #1e3a8a;
    }
    .slide-title h3 {
        font-size: 11pt;
        color: #475569;
    }
    .slide-title table {
        width: 80%;
        margin: 3mm auto;
    }
    """

    body_html = ""
    for s_num in range(1, 13):
        md_text = slides.get(s_num, f"<h1>Slide {s_num}</h1>")
        body_html += format_slide_content(s_num, md_text)

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>CampusNova AI - 12-Slide Seminar Presentation Deck</title>
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
    print(f"Generated Presentation HTML at: {HTML_OUTPUT_PATH}")

if __name__ == "__main__":
    if not os.path.exists(PPT_MD_PATH):
        print(f"Error: {PPT_MD_PATH} not found!")
        sys.exit(1)
    with open(PPT_MD_PATH, "r", encoding="utf-8") as f:
        md = f.read()
    slides = extract_slides(md)
    print(f"Extracted {len(slides)} slides.")
    generate_html(slides)

