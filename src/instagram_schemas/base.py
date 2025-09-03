"""Instagram base model."""

from pydantic import (
    BaseModel,
    ConfigDict,
    model_serializer,
)
from pydantic.alias_generators import to_camel


class InstagramBase(BaseModel):
    """Core fields for Instagram user."""

    model_config = ConfigDict(
        alias_generator=to_camel, populate_by_name=True, extra="ignore"
    )

    @model_serializer(mode="wrap")
    def model_serializer_with_mongodb_id(self, handler, info):
        """Custom serializer that converts id to _id for MongoDB."""
        # Use the default serializer first
        data = handler(self)

        # Convert id to _id regardless of serialization mode
        if "id" in data:
            data["_id"] = data.pop("id")

        return data
