from pydantic import BaseModel, Field

class TodoInput(BaseModel):
    title: str = Field(..., min_length=1, max_length=300)

    class Config:
        extra = "ignore"  # Reject unknown client fields
