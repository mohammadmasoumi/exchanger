from pydantic import BaseModel


class MockExchangerResponse(BaseModel):
    transaction_id: str
    success: bool
