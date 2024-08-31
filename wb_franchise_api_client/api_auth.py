import aiohttp
from typing import Optional, Dict, Any
from .api_config import APIConfig, HTTPException
from .models import TokenResponse, RequestCodeResponse


class ApiAuth:
    """Auth client for wb franchise"""

    def __init__(self, api_config: APIConfig):
        self.api_config = api_config
        self.headers = {
            "Accept": "application/json",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Referer": "https://franchise.wildberries.ru/",
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {self.api_config.get_basic_token()}",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"
        }

    async def _request(self,
                       method: str,
                       path: str,
                       params: Optional[Dict[str, Any]] = None,
                       data: Optional[Dict[str, Any]] = None,
                       return_status: bool = False) -> Dict[str, Any] | int:
        """Common request method

        :param method: HTTP method
        :param path: API path
        :param params: Optional parameters
        :param data: Optional data
        :param return_status: Return HTTP status code
        :return: Response
        """
        url = self.api_config.auth_base_path + path
        async with aiohttp.ClientSession() as session:
            async with session.request(
                    method,
                    url,
                    params=params,
                    data=data,
                    headers=self.headers,
            ) as response:
                if return_status:
                    return response.status
                try:
                    response_data = await response.json()
                except aiohttp.ContentTypeError:
                    response_text = await response.text()
                    raise HTTPException(response.status, f"Invalid response from server: {response_text}")
                if response.status in {400, 401, 403, 429, 500}:
                    raise HTTPException(response.status, f"{response_data}")
                return response_data

    async def request_code(self, phone: str) -> RequestCodeResponse:
        """Request code for auth

        :param phone: phone number
        :return RequestCodeResponse
        """
        path = "/request_code"
        params = {"phone": phone}
        response_data = await self._request("GET", path, params=params)
        if isinstance(response_data, dict):
            return RequestCodeResponse(**response_data)
        else:
            raise HTTPException(response_data, "Unexpected response format")

    async def connect_code(self, username: str, password: str = None, refresh_token: str = None) -> TokenResponse:
        """Connect with code and get access token or use refresh token

        :param username: username (phone number)
        :param password: password (code from lk)
        :param refresh_token: current refresh token
        :return TokenResponse
        """
        path = "/connect/token"
        data = {"grant_type": "", "username": username}
        if password:
            data.update({
                "grant_type": "password",
                "password": password
            })
        elif refresh_token:
            data.update({
                "grant_type": "refresh_token",
                "refresh_token": refresh_token
            })
        else:
            raise ValueError("Either password or refresh_token must be provided")

        response_data = await self._request("POST", path, data=data)
        if isinstance(response_data, dict):
            return TokenResponse(**response_data)
        else:
            raise HTTPException(response_data, "Unexpected response format")


async def main():
    api_config = APIConfig(auth_base_path="https://auth-orr.wildberries.ru", basic_token="ZnJhbmNoaXNlOjJoVjlPMnVzSk0yRUg1RjU=")
    api_auth = ApiAuth(api_config)
    await api_auth.request_code("79282951709")
    code = input("Enter code: ")
    response_connect = await api_auth.connect_code(username="79282951709", password=code)
    print(response_connect)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())



