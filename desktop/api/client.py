"""
API client for the Chemical Equipment Visualizer backend.
Uses Token authentication for the desktop app.
"""
import os
import requests


class APIClient:
    """Client for the REST API. Uses Token auth for desktop."""
    BASE_URL = 'http://127.0.0.1:8000/api'

    def __init__(self):
        self.token = None

    def _headers(self):
        """Headers including auth token when available."""
        h = {'Content-Type': 'application/json'}
        if self.token:
            h['Authorization'] = f'Token {self.token}'
        return h

    def register(self, username: str, password: str) -> dict:
        """
        POST to /api/auth/register/, create user.
        Returns response JSON. Raises requests.HTTPError on error.
        """
        r = requests.post(
            f'{self.BASE_URL}/auth/register/',
            json={'username': username, 'password': password},
        )
        if r.status_code >= 400:
            error_msg = 'Registration failed'
            try:
                error_data = r.json()
                error_msg = error_data.get('error', error_data.get('detail', error_msg))
            except:
                error_msg = r.text or error_msg
            raise requests.HTTPError(error_msg, response=r)
        return r.json()

    def login(self, username: str, password: str) -> dict:
        """
        POST to /api/auth/login/, store token.
        Returns response JSON. Raises requests.HTTPError on error.
        """
        r = requests.post(
            f'{self.BASE_URL}/auth/login/',
            json={'username': username, 'password': password},
        )
        if r.status_code >= 400:
            error_msg = 'Login failed'
            try:
                error_data = r.json()
                error_msg = error_data.get('error', error_data.get('detail', error_msg))
            except:
                error_msg = r.text or error_msg
            raise requests.HTTPError(error_msg, response=r)
        data = r.json()
        self.token = data.get('token')
        return data

    def logout(self) -> None:
        """POST to /api/auth/logout/ with token header."""
        try:
            requests.post(
                f'{self.BASE_URL}/auth/logout/',
                headers=self._headers(),
            )
        except Exception:
            pass
        self.token = None

    def upload(self, filepath: str) -> dict:
        """
        POST file to /api/upload/ with Authorization: Token <token>.
        Returns response JSON.
        """
        with open(filepath, 'rb') as f:
            files = {'file': (os.path.basename(filepath), f, 'text/csv')}
            headers = {}
            if self.token:
                headers['Authorization'] = f'Token {self.token}'
            r = requests.post(
                f'{self.BASE_URL}/upload/',
                files=files,
                headers=headers,
            )
        r.raise_for_status()
        return r.json()

    def get_datasets(self) -> list:
        """GET /api/datasets/ with token. Returns list."""
        r = requests.get(f'{self.BASE_URL}/datasets/', headers=self._headers())
        r.raise_for_status()
        return r.json()

    def get_dataset(self, dataset_id: int) -> dict:
        """GET /api/datasets/<id>/ with token. Returns dict."""
        r = requests.get(
            f'{self.BASE_URL}/datasets/{dataset_id}/',
            headers=self._headers(),
        )
        r.raise_for_status()
        return r.json()

    def get_summary(self, dataset_id: int) -> dict:
        """GET /api/summary/<id>/ with token. Returns dict."""
        r = requests.get(
            f'{self.BASE_URL}/summary/{dataset_id}/',
            headers=self._headers(),
        )
        r.raise_for_status()
        return r.json()

    def download_pdf(self, dataset_id: int, save_path: str) -> None:
        """GET /api/pdf/<id>/ with token, write content to save_path."""
        r = requests.get(
            f'{self.BASE_URL}/pdf/{dataset_id}/',
            headers=self._headers(),
            stream=True,
        )
        r.raise_for_status()
        with open(save_path, 'wb') as f:
            f.write(r.content)
