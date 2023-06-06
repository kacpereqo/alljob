from fastapi import status
from fastapi.exceptions import HTTPException


class OffertsErrors:
    @staticmethod
    def offerts_count_greater_than_40():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="offset cannot be greater than limit by more than 40",
        )
