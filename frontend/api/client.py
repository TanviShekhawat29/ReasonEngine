import requests


class APIClient:

    def __init__(self):

        # Change this after deployment
        self.base_url = "http://127.0.0.1:8000/api/v1"

        self.timeout = 300

    # -------------------------------------------------
    # Health
    # -------------------------------------------------

    def health(self):

        response = requests.get(
            f"{self.base_url}/health",
            timeout=10,
        )

        response.raise_for_status()

        return response.json()

    # -------------------------------------------------
    # Upload PDF
    # -------------------------------------------------

    def upload_pdf(self, uploaded_file):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf",
            )
        }

        response = requests.post(
            f"{self.base_url}/upload",
            files=files,
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json()

    # -------------------------------------------------
    # Document Summary
    # -------------------------------------------------

    def get_summary(self):

        response = requests.get(
            f"{self.base_url}/document/summary",
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    # -------------------------------------------------
    # Suggested Questions
    # -------------------------------------------------

    def get_questions(self):

        response = requests.get(
            f"{self.base_url}/document/questions",
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    # -------------------------------------------------
    # Ask Question
    # -------------------------------------------------

    def ask_question(
        self,
        question,
        limit=5,
    ):

        payload = {
            "question": question,
            "limit": limit,
        }

        response = requests.post(
            f"{self.base_url}/ask",
            json=payload,
            timeout=120,
        )

        response.raise_for_status()

        return response.json()


api = APIClient()