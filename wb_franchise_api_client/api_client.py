import aiohttp
from typing import Optional, Dict, Any
from models import *
import json

from .api_config import APIConfig, HTTPException


class ApiClient:
    """API Client for API Franchise

    :param access_token: access token for requests
    :param api_config: APIConfig instance
    """

    def __init__(self, access_token: str, api_config: APIConfig) -> None:
        self.api_config = api_config
        self.headers = {
            "Accept": "application/json.txt, text/plain, */*",
            "Referer": "https://franchise.wildberries.ru/",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "sec-ch-ua-platform": "Windows",
            "Authorization": f"Bearer {access_token}",
        }

    async def _get_response_data_wb(self,
                                    *,
                                    method: str,
                                    path: str,
                                    params: Optional[Dict[str, Any]] = None,
                                    data: Optional[Dict[str, Any]] = None,
                                    return_status: bool = False, prefix: str) -> Dict[str, Any] | int:
        """Common method to get response from API

        :param method: HTTP method
        :param path: API path
        :param params: API params
        :param data: API data
        :param return_status: Return status code or not
        :param prefix: API prefix to determine where was an error
        :return Response
        """
        ERROR_STATUS = {
            "account": "Ошибка получения данных аккаунта",
            "sales": "Ошибка получения данных по продажам",
            "reward": "Ошибка получения данных по вознаграждениям",
            "shortages": "Ошибка получения данных по недостачам",
            "history_shortage": "Ошибка получения данных по истории недостачи",
            "shks": "Ошибка получения данных по ШК в недостаче",
            "office_rates": "Ошибка получения данных по рейтингам офисов",
            "office_speed": "Ошибка получения данных по скорости офисов",
            "office_workload": "Ошибка получения данных по загрузке офисов",
            "operations": f"Ошибка получения данных по операциям",
            "employees": f"Ошибка получения данных по сотрудникам",
            "employees_operations": f"Ошибка получения данных по операциям сотрудников",
        }
        url = self.api_config.base_path + path
        async with aiohttp.ClientSession() as session:
            async with session.request(
                    method,
                    url,
                    params=params,
                    json=data,
                    headers=self.headers,
            ) as response:
                if return_status:
                    return response.status
                try:
                    response_data = await response.json()
                except aiohttp.ContentTypeError:
                    response_text = await response.text()
                    content_type = response.headers.get('Content-Type', '')
                    if content_type.startswith('text/plain'):
                        try:
                            response_data = json.loads(response_text)
                        except json.JSONDecodeError:
                            raise HTTPException(response.status,
                                                f"{ERROR_STATUS.get(prefix, 'Ошибка')} (Invalid response from server): {response_text} (Content-Type: {content_type})")
                    else:
                        raise HTTPException(response.status,
                                            f"{ERROR_STATUS.get(prefix, 'Ошибка')} (Invalid response from server): {response_text} (Content-Type: {content_type})")

                if response.status in {400, 401, 403, 429, 500}:
                    raise HTTPException(response.status, f"{ERROR_STATUS.get(prefix, 'Ошибка')}: {response_data}")
                return response_data

    async def get_account_data(self) -> AccountData:
        """Get account data in Franchise - Общие данные аккаунта"""
        path = "/api/v1/franchise/account"
        params = {"in_short": "false"}
        response_data = await self._get_response_data_wb(method="GET",
                                                         path=path,
                                                         params=params,
                                                         prefix="account")
        return AccountData(**response_data)

    async def get_sales_data(self, office_ids: list[int], date_from: str, date_to: str) -> list[OfficeProceed]:
        """Get sales data - Товарооборот

        :param office_ids: List of Office id
        :param date_from: Date from - str
        :param date_to: Date to - str
        :return: List of OfficeProceed
        """
        path = "/api/v2/franchise/proceeds"
        office_ids_str = ",".join(map(str, office_ids))
        params = {
            "office_ids": office_ids_str,
            "from": date_from,
            "to": date_to,
        }
        response_data = await self._get_response_data_wb(method="GET", path=path, params=params, prefix="sales")
        return [OfficeProceed(**item) for item in response_data]

    async def get_reward_data(self, office_ids: list[int], date_from: str, date_to: str) -> list[RewardResponse]:
        """Get reward data - Вознаграждения

        :param office_ids: List of Office id
        :param date_from: Date from - str
        :param date_to: Date to - str
        :return: List of RewardResponse
        """
        path = "/api/v1/franchise/accruals"
        office_ids_str = ",".join(map(str, office_ids))
        params = {
            "office_ids": office_ids_str,
            "from": date_from,
            "to": date_to,
        }
        response_data = await self._get_response_data_wb(method="GET", path=path, params=params, prefix="reward")
        return [RewardResponse(**item) for item in response_data]

    async def get_shortages_data(self) -> ShortageResponse:
        """Get all shortages data - Недостачи

        :return: List of ShortageResponse
        """

        path = "/api/v2/franchise/shortages/offices"
        response_data = await self._get_response_data_wb(method="GET", path=path, prefix="shortages")
        return ShortageResponse(**response_data)

    async def get_shortage_details(self, shortage_id: int) -> ShksShortage:
        """Get details of shortage - Детализация недостачи по shortage_id

        :param shortage_id: Shortage id - int
        :return: ShksShortage
        """
        path = "/api/v2/franchise/shortages"
        params = {"shortage_id": shortage_id}
        response_data = await self._get_response_data_wb(method="GET", path=path, params=params, prefix="shks")
        return ShksShortage(**response_data)

    async def get_history_shortage(self, shortage_id: int) -> HistoryShortage:
        """Get history shortage - История недостачи

        :param shortage_id: Shortage id - int
        :return: HistoryShortage
        """
        path = "/api/v1/franchise/shortages/history"
        params = {"shortage_id": shortage_id}
        response_data = await self._get_response_data_wb(method="GET",
                                                         path=path,
                                                         params=params,
                                                         prefix="history_shortage")
        return HistoryShortage(**response_data)

    async def get_office_rates(self, office_ids: list[int]) -> list[OfficeRate]:
        """Get office rates - Получение рейтинга офиса

        :param office_ids: List of Office id
        :return: List of OfficeRate
        """
        path = "/api/v1/franchise/office/rates"
        office_ids_str = ",".join(map(str, office_ids))
        params = {"office_ids": office_ids_str}
        response_data = await self._get_response_data_wb(method="GET",
                                                         path=path,
                                                         params=params,
                                                         prefix="office_rates")
        return [OfficeRate(**item) for item in response_data]

    async def get_office_speed(self, office_ids: list[int]) -> list[OfficeSpeed]:
        """Get office speed - Время раскладки офисов

        :param office_ids: List of Office id
        :return: List of OfficeSpeed
        """
        path = "/api/v1/franchise/office/on-place"
        office_ids_str = ",".join(map(str, office_ids))
        params = {"office_ids": office_ids_str}
        response_data = await self._get_response_data_wb(method="GET", path=path, params=params, prefix="office_speed")
        return [OfficeSpeed(**item) for item in response_data]

    async def get_office_workload(self, office_ids: list[int]) -> list[OfficeWorkload]:
        """Get office workload - Загрузка офисов

        :param office_ids: List of Office id
        :return: List of OfficeWorkload
        """
        path = "/api/v1/franchise/office/info/workload"
        office_ids_str = ",".join(map(str, office_ids))
        params = {"office_ids": office_ids_str}
        response_data = await self._get_response_data_wb(method="GET",
                                                         path=path,
                                                         params=params,
                                                         prefix="office_workload")
        return [OfficeWorkload(**item) for item in response_data]

    async def get_operations(self, supplier_id: int) -> OperationsResponse:
        """Get all operations - Все операции - Детализация

        :param supplier_id: Supplier id - int
        :return: OperationsResponse
        """
        path = "/api/v1/franchise/payslip"
        params = {
            "supplier_id": supplier_id,
            "all": "true"
        }
        response_data = await self._get_response_data_wb(method="GET", path=path, params=params, prefix="operations")
        # Преобразуем данные перед валидацией
        transformed_data = transform_operations(response_data)

        return OperationsResponse(**transformed_data)


async def main():
    api_config = APIConfig(base_path="https://orr-franchise.wildberries.ru")
    access_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjRDRDg5Mjk2NDdCQkQ5RTI5N0IzRDk5MTU2NDhGOTNEMUE4QkRBNEFSUzI1NiIsInR5cCI6ImF0K2p3dCIsIng1dCI6IlROaVNsa2U3MmVLWHM5bVJWa2o1UFJxTDJrbyJ9.eyJleHAiOjE3MjMxOTgxNzgsImlzcyI6IklkZW50aXR5UG9zIiwiY2xpZW50X2lkIjoiZnJhbmNoaXNlIiwic3ViIjoiNzkyODI5NTE3MDkiLCJhdXRoX3RpbWUiOjE3MjMxOTcyNzgsImlkcCI6ImxvY2FsIiwicGhvbmUiOiI3OTI4Mjk1MTcwOSIsImlkIjoiMTAwNTE5MzgiLCJuYW1lIjoi0JrQsNC70LDRiNC90LjQutC-0LLQsCDQndCw0YLQsNC70YzRjyDQktCw0YHQuNC70YzQtdCy0L3QsCIsInBlcm1pc3Npb25zIjoiZnJhbmNoaXNlIiwiZnJfcm9sZSI6IjAiLCJzZXNzaW9uX2lkIjoiOGNmYjIzOGU5OTIyOWNmM2I2OTljMjlhNmUyZDdkZjkwMmRlYjc0ODMwOGM1OTAzMTc3Mjg1YjFkNWI5YTkxMCIsImp0aSI6IjU1RDRCMjc2RjE5N0Y0NDJCNEFEQTYyNzI5Q0IxRTUxIiwiaWF0IjoxNzIzMTk3Mjc4LCJzY29wZSI6WyJvZmZsaW5lX2FjY2VzcyJdLCJhbXIiOlsicGFzc3dvcmQiXX0.RwGoHcYcEqlFvsdwTKiO-H36Zrn9Y0t8zOXRgsuu_b_n56Ko6l2IaQ6YjNXkZGVhlGcwiBUR7r4yfF0vFXV-TabFiJRmi1CUgpJhv-JQeRTiKPO6UNT9Qt1mWIgtCjxwcAuZqWXz_PmFWzeWvrY4BWznviehEZ5eWy_Zu6qAx3Gw1sZTBZQR8gut0qDko16lFkQYbYEf76OGYBQSV03wz7LY8s_K8RMX_b1dIhR8lR5_DwbwyWhBFT0677NZORz-r75ExxMGrqzwuKuKtlK_GdMRovey88yGPUKN0q-R307GCo7w8POHmOR6vaY4aoWIrjtRTRqvm7MUisRIy5aMKQ"
    api_client = ApiClient(access_token=access_token, api_config=api_config)
    data = await api_client.get_operations(supplier_id=15730)
    print(data)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

