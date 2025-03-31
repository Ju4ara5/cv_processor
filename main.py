
from .config import Config
from .email.client import EmailClient
from .email.parser import EmailParser
from .resume.pdf_parser import PdfResumeParser
from .resume.docx_parser import DocxResumeParser
from .resume.ocr import ImageResumeParser
from .storage.google_sheets import GoogleSheetsClient
from googletrans import Translator
from typing import Dict, Optional


class CVProcessor:
    """Основной класс обработки резюме"""

    def __init__(self):
        self.config = Config()
        self.translator = Translator() if self.config.TRANSLATE_TO_RUSSIAN else None
        self.sheets_client = GoogleSheetsClient(
            "credentials.json",
            self.config.SPREADSHEET_URL
        )
        self.sheets_client.ensure_headers()

    def process_emails(self):
        """Основной метод обработки писем"""
        email_client = EmailClient(self.config.EMAIL, self.config.PASSWORD)

        try:
            for mail_id in email_client.fetch_unread_emails():
                try:
                    email_data = email_client.get_email_data(mail_id)
                    parsed_email = EmailParser.parse(email_data["raw"])

                    # Обработка вложений
                    resume_data = self._process_attachments(
                        parsed_email["attachments"]
                    )

                    # Подготовка данных
                    row_data = self._prepare_row_data(parsed_email, resume_data)

                    # Добавление в таблицу
                    self.sheets_client.add_candidate(row_data)

                    # Пометка письма как прочитанного
                    email_client.mark_as_read(mail_id)

                except Exception as e:
                    print(f"Ошибка обработки письма: {e}")
                    continue

        finally:
            email_client.close()

    def _process_attachments(self, attachments: list) -> Dict:
        """Обработка вложений (резюме)"""
        resume_data = {}

        for attachment in attachments:
            try:
                filename = attachment["filename"].lower()
                content = attachment["content"]

                # Выбор парсера по типу файла
                if filename.endswith(".pdf"):
                    parser = PdfResumeParser()
                elif filename.endswith((".doc", ".docx")):
                    parser = DocxResumeParser()
                elif filename.endswith((".jpg", ".jpeg", ".png")):
                    parser = ImageResumeParser()
                else:
                    continue

                # Парсинг резюме
                parsed = parser.parse(content)

                # Перевод на русский при необходимости
                if self.translator:
                    for field in ["education", "experience", "skills"]:
                        if parsed[field]:
                            try:
                                translated = self.translator.translate(
                                    parsed[field],
                                    dest='ru'
                                ).text
                                parsed[field] = translated
                            except:
                                pass

                # Объединение данных
                for key, value in parsed.items():
                    if value and not resume_data.get(key):
                        resume_data[key] = value

            except Exception as e:
                print(f"Ошибка обработки вложения: {e}")
                continue

        return resume_data

    def _prepare_row_data(self, email_data: Dict, resume_data: Dict) -> list:
        """Подготовка данных для строки таблицы"""
        # Приоритет: данные из письма, затем из резюме
        phone = email_data.get("phone") or resume_data.get("phone", "")

        return [
            email_data["date"],
            email_data["first_name"],
            email_data["last_name"],
            email_data["email"],
            phone,
            resume_data.get("education", ""),
            resume_data.get("experience", ""),
            resume_data.get("skills", ""),
            ""  # Можно добавить ссылку на резюме
        ]


if __name__ == "__main__":
    processor = CVProcessor()
    processor.process_emails()