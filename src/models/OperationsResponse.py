from typing import Optional, List, Any

from pydantic import BaseModel, Field


class Operation(BaseModel):
    """Model for Operation

    :arg dt : date Дата
    :arg oper_type : operation type Тип операции
        - 1 - операция Недостача
        - 2 - операция Премирование
        - 3 - операция Депремирование
        - 4 - операция Брак ШК / Коллективная ответственность
        - 5 - операция Вывод средств на реквизиты
        - 6 - операция Вознаграждения по продажам

    """
    dt: str
    oper_type: int
    oper_amount: float
    comment: Optional[str] = Field(default=None)
    grouped: Optional[List["Operation"]] = None


class OperationsByDate(BaseModel):
    date: str
    operations: list[Operation]


class OperationsResponse(BaseModel):
    balance: float
    currency_code: str
    plan_payment_date: str
    details: list[OperationsByDate]


Operation.update_forward_refs()


# Функции для преобразования данных с вложенными grouped
def transform_grouped(data: Any) -> Any:
    if isinstance(data, list):
        return [Operation(**item) for item in data]
    return data


def transform_operations(data: dict) -> dict:
    for detail in data['details']:
        for operation in detail['operations']:
            if operation.get('grouped') is not None:
                operation['grouped'] = transform_grouped(operation['grouped'])
    return data
