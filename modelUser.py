from typing import Union
from pydantic import BaseModel

class ModelUser(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None