from pydantic import BaseModel, Field


class AvatarSeedRequest(BaseModel):
    seed: str = Field(
        ...,
        min_length=1,
        description="Unique seed string used to generate the avatar, such as a username or user ID.",
        example="johndoe",
    )
