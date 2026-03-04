import json, logging, os, yaml
from logging.handlers import RotatingFileHandler
import requests
from requests.exceptions import HTTPError, Timeout, RequestException

def setup_logging(config: dict) -> logging.Logger:
    log = logging.getLogger("client_http")
    log.setLevel(getattr(logging, config["level"].upper()))
    formatter = logging.Formatter(
        '{"time":"%(asctime)s","level":"%(levelname)s","message":"%(message)s"}'
    )

    if config["console"]:
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        log.addHandler(ch)

    fh = RotatingFileHandler(
        config["file"],
        maxBytes=config["max_bytes"],
        backupCount=config["backup_count"]
    )
    fh.setFormatter(formatter)
    log.addHandler(fh)
    return log

def load_config(path="config.yaml") -> dict:
    with open(path, encoding="utf8") as fh:
        cfg = yaml.safe_load(fh)
    cfg["api"]["base_url"] = os.getenv("API_BASE_URL") or cfg["api"]["base_url"]
    cfg["logging"]["level"] = os.getenv("LOG_LEVEL") or cfg["logging"]["level"]
    return cfg

class APIClient:
    def __init__(self, base_url: str, timeout: int, logger: logging.Logger):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.log = logger
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "lab2-client/1.0"})

    def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        self.log.info("%s %s", method.upper(), url)
        try:
            resp = self.session.request(method, url, timeout=self.timeout, **kwargs)
            resp.raise_for_status()
            return resp.json() if "json" in resp.headers.get("Content-Type", "") else {"text": resp.text}
        except HTTPError as e:
            self.log.error("HTTP error %s - %s", e.response.status_code, e.response.text)
            raise
        except Timeout:
            self.log.error("Timeout after %ss", self.timeout)
            raise
        except RequestException as e:
            self.log.error("Request failed: %s", e)
            raise
        except json.JSONDecodeError:
            self.log.error("Invalid JSON response")
            raise

    def get(self, endpoint: str, params=None) -> dict:
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint: str, data: dict) -> dict:
        return self._request("POST", endpoint, json=data)