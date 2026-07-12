from pydantic import BaseModel, ConfigDict, Field


class DeliveryQuoteRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    option_id: str = Field(alias="optionId")
    distance_km: float = Field(alias="distanceKm", gt=0)
