# CV Processor - Automated Resume Parser

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![IMAP](https://img.shields.io/badge/IMAP-Email-orange)
![Google Sheets](https://img.shields.io/badge/Google%20Sheets-API-green)

Automated system for parsing candidate resumes from emails and saving structured data to Google Sheets. Supports PDF, DOCX, and image attachments with OCR.

## Features

- 📧 **Email Processing**  
  - IMAP integration with Gmail  
  - Filters emails with "CV" or "резюме" in subject  
  - Extracts: Name, Email, Phone (Moldovan formats), Date  

- 📑 **Resume Parsing**  
  - **PDF/DOCX**: Education, Work Experience, Skills  
  - **Images (JPG/PNG)**: OCR via Tesseract  
  - Multilingual support (auto-translation to Russian)  

- 📊 **Google Sheets Integration**  
  - Automatic table creation  
  - Structured columns:  
    ```
    Date | First Name | Last Name | Email | Phone | Education | Experience | Skills
    ```

## Setup

1. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/cv-processor.git
   cd cv-processor