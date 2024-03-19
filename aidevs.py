from typing import Any
from requests import Session
from dotenv import load_dotenv
import os
import logging

load_dotenv()

log = logging.getLogger(__name__)


class AIDevsClient:

    def __init__(
        self, api_key: str, base_url: str = "https://tasks.aidevs.pl", session=None
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url
        if session == None:
            self.session = Session()

    def _make_url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def get_task_token(self, task: str) -> dict[str, Any]:
        token_url = self._make_url(f"/token/{task}")
        r = self.session.post(token_url, json={"apikey": self.api_key}).json()
        if "code" in r and r["code"] == 0:
            token = r.get("token")
            log.debug(f"{token=}")
            return token

        raise RuntimeError(f"Getting token failed. [{r['code']}] {r['msg']}")

    def get_task(self, task_token: str) -> dict[str, Any]:
        task_url = self._make_url(f"/task/{task_token}")
        return self.session.get(task_url).json()

    def get_hint(self, task: str) -> dict[str, Any]:
        task_url = self._make_url(f"/hint/{task}")
        return self.session.get(task_url).json()

    def send_answer(self, task_token: str, answer: Any) -> dict[str, Any]:
        answer_url = self._make_url(f"/answer/{task_token}")
        r = self.session.post(answer_url, json={"answer": answer}).json()
        if "code" in r and r["code"] == 0:
            return r

        raise RuntimeError(f"Sending answer failed. [{r['code']}] {r['msg']}")


class AIDevsTask:
    def __init__(self, aidevs: AIDevsClient, task_name: str) -> None:
        self.aidevs = aidevs
        self.task_name = task_name
        self._token = self.aidevs.get_task_token(self.task_name)
        self._input_data = self.aidevs.get_task(self._token)

    @property
    def input(self) -> Any:
        return self._input_data

    @property
    def hint(self) -> dict[str, Any]:
        return aidevs.get_hint(self.task_name)

    def answer(self, ans: Any) -> dict[str, Any]:
        return aidevs.send_answer(self._token, ans)


def header(h: str) -> None:
    print(f"\n| {h} |\n{(4+len(h))*'='}")


def pretty_print(h: str, d: dict) -> None:
    header(h)
    for k in d.keys():
        print(f"{k: <6} := {d[k]}")


aidevs = AIDevsClient(os.getenv("AIDEVS2_API_KEY"))


__all__ = ["AIDevsClient", "aidevs", "pretty_print"]
