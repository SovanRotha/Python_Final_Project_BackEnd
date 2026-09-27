from pydantic import BaseModel, ConfigDict, Field


class PackingItemCreate(BaseModel):
    packing_list_id: int

    name: str = Field(
        min_length=1,
        max_length=255
    )

    category: str | None = Field(
        default=None,
        max_length=100
    )

    quantity: int = Field(
        default=1,
        ge=1
    )

    is_packed: bool = False


class PackingItemUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255
    )

    category: str | None = Field(
        default=None,
        max_length=100
    )

    quantity: int | None = Field(
        default=None,
        ge=1
    )

    is_packed: bool | None = None


class PackingItemRead(PackingItemCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
