"""
Script to build the official 30-Page B.Tech Academic Project Seminar Report PDF
for CampusNova AI (Ajay Binay Institute of Technology, BPUT, 2022-2026 Batch).
"""

import os
import re
import sys
import mistune

REPORT_MD_PATH = r"d:\campusnova\CAMPUSNOVA_30_PAGE_SEMINAR_REPORT.md"
HTML_OUTPUT_PATH = r"d:\campusnova\campusnova_report.html"
PDF_OUTPUT_PATH = r"d:\campusnova\CAMPUSNOVA_30_PAGE_SEMINAR_REPORT.pdf"

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

def format_page_content(p_num, markdown_text):
    # Custom rendering / styling tweaks per page type
    html = mistune.html(markdown_text)
    
    # Header & Footer HTML (omitted on cover page 1)
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

def generate_html(pages):
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
        padding: 16mm 20mm 16mm 22mm;
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
        height: 14mm;
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
        margin-bottom: 4mm;
    }
    .page-footer {
        height: 12mm;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-top: 1px solid #cbd5e1;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 8pt;
        color: #64748b;
        margin-top: 4mm;
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
        margin-bottom: 2.5mm;
        font-weight: 700;
    }
    h1 {
        font-size: 15pt;
        line-height: 1.25;
        text-align: center;
        letter-spacing: 0.5px;
    }
    h2 {
        font-size: 12.5pt;
        line-height: 1.3;
        border-bottom: 1px solid #e2e8f0;
        padding-bottom: 1.5mm;
        margin-top: 1mm;
    }
    h3 {
        font-size: 10.5pt;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1.5mm;
    }
    h4 {
        font-size: 9.5pt;
        font-weight: 600;
        color: #334155;
        margin-bottom: 1mm;
    }
    p {
        margin-top: 0;
        margin-bottom: 2mm;
        text-align: justify;
        line-height: 1.4;
    }
    ul, ol {
        margin-top: 0;
        margin-bottom: 2mm;
        padding-left: 5mm;
    }
    li {
        margin-bottom: 1mm;
        line-height: 1.35;
    }
    hr {
        border: none;
        border-top: 1px solid #cbd5e1;
        margin: 3mm 0;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 1.5mm;
        margin-bottom: 2.5mm;
        font-size: 8.5pt;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    th, td {
        border: 1px solid #94a3b8;
        padding: 4.5px 7px;
        text-align: left;
        line-height: 1.3;
    }
    th {
        background-color: #f1f5f9;
        color: #0f172a;
        font-weight: 700;
        text-transform: uppercase;
        font-size: 8pt;
        letter-spacing: 0.4px;
    }
    tr:nth-child(even) td {
        background-color: #fafafa;
    }
    pre {
        background-color: #ffffff;
        border: 1px solid #94a3b8;
        border-radius: 3px;
        padding: 5px 8px;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 7.5pt;
        line-height: 1.25;
        overflow: hidden;
        white-space: pre-wrap;
        word-break: break-all;
        margin-top: 1.5mm;
        margin-bottom: 2mm;
        color: #0f172a;
    }
    code {
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 8.5pt;
        background-color: #f1f5f9;
        padding: 1px 3px;
        border-radius: 2px;
        color: #0f172a;
    }
    pre code {
        background-color: transparent;
        padding: 0;
        font-size: 7.5pt;
    }
    blockquote {
        margin: 1.5mm 0;
        padding: 2mm 4mm;
        background-color: #f8fafc;
        border-left: 3px solid #2563eb;
        font-size: 9.5pt;
        font-style: italic;
    }
    .cover-page {
        justify-content: center;
        text-align: center;
        border: 2px solid #0f172a;
        margin: 5mm;
        width: 200mm;
        height: 287mm;
        padding: 15mm 18mm;
    }
    .cover-content {
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .cover-content h1 {
        font-size: 17pt;
        letter-spacing: 1px;
        margin-bottom: 2mm;
    }
    .cover-content h3 {
        font-size: 11.5pt;
        color: #334155;
    }
    .cover-content hr {
        border-top: 2px solid #0f172a;
        margin: 4mm 0;
    }
    .cover-content table {
        margin: 0 auto;
        width: 90%;
    }
    /* Compact rules for code-heavy pages (Pages 25, 26) */
    #page-25 pre, #page-26 pre {
        font-size: 6.8pt;
        line-height: 1.15;
        padding: 4px;
    }
    /* Compact rules for Table of Contents (Page 6) */
    #page-6 table {
        font-size: 8pt;
    }
    #page-6 p {
        font-size: 9pt;
        margin-bottom: 1mm;
    }
    /* Compact rules for Abstract (Page 7) */
    #page-7 p {
        font-size: 9pt;
        line-height: 1.35;
        margin-bottom: 1.8mm;
    }
    /* Compact rules for Architecture & Flowcharts (Pages 16, 18, 29) */
    #page-16 pre, #page-18 pre, #page-29 pre {
        font-size: 7pt;
        line-height: 1.15;
        border: 1px dashed #64748b;
    }
    /* References compact (Page 30) */
    #page-30 ol, #page-30 ul {
        font-size: 7.5pt;
        padding-left: 4mm;
    }
    #page-30 li {
        margin-bottom: 0.8mm;
    }
    """

    body_html = ""
    for p_num in range(1, 31):
        md_text = pages.get(p_num, f"<h1>Page {p_num}</h1>")
        body_html += format_page_content(p_num, md_text)

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
    print(f"Generated HTML report at: {HTML_OUTPUT_PATH}")

if __name__ == "__main__":
    if not os.path.exists(REPORT_MD_PATH):
        print(f"Error: {REPORT_MD_PATH} not found!")
        sys.exit(1)
    with open(REPORT_MD_PATH, "r", encoding="utf-8") as f:
        md = f.read()
    pages = extract_pages(md)
    print(f"Extracted {len(pages)} pages.")
    generate_html(pages)
