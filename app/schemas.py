from pydantic import BaseModel, ConfigDict
from pydantic import Field

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=72)


class UserResponse(BaseModel):
    id: int
    username: str
    balance: float
    role: str
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ItemCreate(BaseModel):
    title: str
    description: str | None = None
    price: float = Field(gt=0)
    category_id: int


class ItemResponse(BaseModel):
    id: int
    title: str
    price: float
    is_sold: bool
    owner_id: int
    buyer_id: int | None = None
    category_id: int
    model_config = ConfigDict(from_attributes=True)

class CategoryCreate(BaseModel):
    name: str


class CategoryResponse(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

class TransactionResponse(BaseModel):
    id: int
    item_id: int
    seller_id: int
    buyer_id: int
    price: float
    model_config = ConfigDict(from_attributes=True)