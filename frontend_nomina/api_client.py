import requests
import time
from django.conf import settings

class APIClient:
    @staticmethod
    def get_headers(request=None):
        headers = {"Content-Type": "application/json"}
        if request and request.session.get('access_token'):
            token = request.session.get('access_token')
            headers["Authorization"] = f"Bearer {token}"
        return headers

    @classmethod
    def get(cls, endpoint, request=None, params=None):
        url = f"{settings.API_BASE_URL}{endpoint}"
        t0 = time.time()
        print(f"[FRONTEND -> BACKEND] GET -> {url}", flush=True)
        try:
            response = requests.get(url, headers=cls.get_headers(request), params=params, timeout=10)
            elapsed = round((time.time() - t0) * 1000, 2)
            print(f"[FRONTEND -> BACKEND SUCCESS] GET {endpoint} | Status: {response.status_code} | Tiempo: {elapsed}ms", flush=True)
            return response
        except Exception as e:
            elapsed = round((time.time() - t0) * 1000, 2)
            print(f"[FRONTEND -> BACKEND ERROR] GET {url} | Error: {e} | Tiempo: {elapsed}ms", flush=True)
            return None

    @classmethod
    def post(cls, endpoint, request=None, data=None, json_data=None):
        url = f"{settings.API_BASE_URL}{endpoint}"
        t0 = time.time()
        print(f"[FRONTEND -> BACKEND] POST -> {url}", flush=True)
        try:
            if json_data is not None:
                response = requests.post(url, headers=cls.get_headers(request), json=json_data, timeout=10)
            else:
                headers = cls.get_headers(request)
                if data and isinstance(data, dict):
                    headers.pop("Content-Type", None)
                    response = requests.post(url, headers=headers, data=data, timeout=10)
                else:
                    response = requests.post(url, headers=headers, json=data, timeout=10)
            elapsed = round((time.time() - t0) * 1000, 2)
            print(f"[FRONTEND -> BACKEND SUCCESS] POST {endpoint} | Status: {response.status_code} | Tiempo: {elapsed}ms", flush=True)
            return response
        except Exception as e:
            elapsed = round((time.time() - t0) * 1000, 2)
            print(f"[FRONTEND -> BACKEND ERROR] POST {url} | Error: {e} | Tiempo: {elapsed}ms", flush=True)
            return None

    @classmethod
    def put(cls, endpoint, request=None, json_data=None):
        url = f"{settings.API_BASE_URL}{endpoint}"
        t0 = time.time()
        print(f"[FRONTEND -> BACKEND] PUT -> {url}", flush=True)
        try:
            response = requests.put(url, headers=cls.get_headers(request), json=json_data, timeout=10)
            elapsed = round((time.time() - t0) * 1000, 2)
            print(f"[FRONTEND -> BACKEND SUCCESS] PUT {endpoint} | Status: {response.status_code} | Tiempo: {elapsed}ms", flush=True)
            return response
        except Exception as e:
            elapsed = round((time.time() - t0) * 1000, 2)
            print(f"[FRONTEND -> BACKEND ERROR] PUT {url} | Error: {e} | Tiempo: {elapsed}ms", flush=True)
            return None

    @classmethod
    def delete(cls, endpoint, request=None):
        url = f"{settings.API_BASE_URL}{endpoint}"
        t0 = time.time()
        print(f"[FRONTEND -> BACKEND] DELETE -> {url}", flush=True)
        try:
            response = requests.delete(url, headers=cls.get_headers(request), timeout=10)
            elapsed = round((time.time() - t0) * 1000, 2)
            print(f"[FRONTEND -> BACKEND SUCCESS] DELETE {endpoint} | Status: {response.status_code} | Tiempo: {elapsed}ms", flush=True)
            return response
        except Exception as e:
            elapsed = round((time.time() - t0) * 1000, 2)
            print(f"[FRONTEND -> BACKEND ERROR] DELETE {url} | Error: {e} | Tiempo: {elapsed}ms", flush=True)
            return None
