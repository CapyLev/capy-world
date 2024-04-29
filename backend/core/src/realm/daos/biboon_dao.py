import enum
import logging

import requests
from requests import Response

from config.settings import application_consts


class BiboonDAO:
    class BiboonDAOError(Exception):
        pass

    class BiboonUrl(enum.StrEnum):
        PING = "/api/core/ping"
        SEND_WELCOME_MSG = "/api/real/send_welcome_msg"

    class Method(enum.StrEnum):
        GET = "GET"
        POST = "POST"

    def _send(
        self,
        url: str,
        method: Method,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> Response:
        try:
            response = requests.request(
                method=method,
                url=url,
                data=data,
                headers=headers or {"Content-type": "application/json"},
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as exc:
            logging.error(f"Biboon server throw exception: {exc}. Endpoint: {url}")
            raise self.BiboonDAOError from exc

        return response

    def ping(self) -> bool:
        url = f"{application_consts.biboon_server.SERVICE_URL}{self.BiboonUrl.PING}"
        method = self.Method.GET
        try:
            _ = self._send(
                url=url,
                method=method,
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
        url = f"{application_consts.biboon_server.SERVICE_URL}{self.BiboonUrl.SEND_WELCOME_MSG}"
        method = self.Method.POST
        data = {
            "server_id": server_id,
            "user_id": user_id,
        }

        _ = self._send(
            url=url,
            method=method,
            data=data,
        )
