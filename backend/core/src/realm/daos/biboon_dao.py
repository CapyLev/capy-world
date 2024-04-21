import enum
import logging

import requests

from config.settings import application_consts


class BiboonDAO:
    class BiboonDAOError(Exception):
        pass

    class Method(enum.Enum):
        GET = "GET"
        POST = "POST"

    def _send(
        self,
        url: str,
        method: Method,
        data: dict | None = None,
    ) -> dict:
        try:
            response = requests.request(method=method.value, url=url, data=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as exc:
            logging.error(f"Biboon server throw exception: {exc}. Endpoint: {url}")
            raise self.BiboonDAOError from exc

        return response.json()

    def ping(self) -> bool:
        try:
            _ = self._send(
                url=f"{application_consts.biboon_server.SERVICE_URL}/api/core/ping",
                method=self.Method.GET,
            )
        except self.BiboonDAOError as exc:
            logging.error(f"Cannot ping biboon server: {exc}")
            return False

        return True

    def send_welcome_message(
        self,
        server_id: int,
        user_id: int,
    ) -> None:
        pass
