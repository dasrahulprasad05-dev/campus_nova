"""
PlacePulse AI: UI Components & Document Processing Helpers
Module: app/components/ui_helpers.py
Author: PlacePulse AI Team
License: Approved Production Blueprint - v1.0.0
"""

import io
from typing import Optional
import pypdfium2 as pdfium


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """
    Extracts plain text from uploaded PDF resume bytes using pypdfium2.
    """
    try:
        pdf = pdfium.PdfDocument(pdf_bytes)
        text_pages = []
        for i in range(len(pdf)):
            page = pdf.get_page(i)
            textpage = page.get_textpage()
            text = textpage.get_text_range()
            if text:
                text_pages.append(text)
        return "\n".join(text_pages).strip()
    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}"


def get_custom_css() -> str:
    """Returns modern CSS for cards, badges, and metrics styling."""
    return """
    <style>
        .metric-card {
            background-color: #f8f9fa;
            border-left: 5px solid #1E88E5;
            padding: 18px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-bottom: 12px;
        }
        .metric-title {
            font-size: 13px;
            color: #6c757d;
            font-weight: 600;
            text-transform: uppercase;
        }
        .metric-val {
            font-size: 26px;
            font-weight: 700;
            color: #212529;
        }
        .badge-green {
            background-color: #e8f5e9;
            color: #2e7d32;
            padding: 4px 10px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 13px;
            display: inline-block;
            margin: 3px;
            border: 1px solid #c8e6c9;
        }
        .badge-orange {
            background-color: #fff3e0;
            color: #e65100;
            padding: 4px 10px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 13px;
            display: inline-block;
            margin: 3px;
            border: 1px solid #ffe0b2;
        }
        .risk-alert {
            background-color: #ffebee;
            color: #c62828;
            padding: 14px;
            border-radius: 8px;
            border-left: 5px solid #d32f2f;
            margin-bottom: 15px;
        }
        .success-alert {
            background-color: #e8f5e9;
            color: #1b5e20;
            padding: 14px;
            border-radius: 8px;
            border-left: 5px solid #388e3c;
            margin-bottom: 15px;
        }
    </style>
    """

