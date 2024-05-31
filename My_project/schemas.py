from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field


class PhoneNumberModel(BaseModel):
    """Base model for phone number"""
    phone_number: str = Field(max_length=15)


class PhoneNumberResponse(PhoneNumberModel):
    """Response model for phone number"""
    id: int

    class Config:
        orm_mode = True


class EmailModel(BaseModel):
    """Base model for email"""
    email: str = Field(max_length=128)


class EmailResponse(EmailModel):
    """Response model for email"""
    id: int

    class Config:
        orm_mode = True


class ContactModel(BaseModel):
    """Base model for contact"""
    first_name: str = Field(max_length=64)
    last_name: str = Field(max_length=64)
    date_of_birthday: date
    additional_data: Optional[str] = Field(max_length=256, default=None)
    phone_numbers: List[PhoneNumberModel]
    emails: List[EmailModel]


class ContactUpdateMidel(BaseModel):
    first_name: Optional[str] = Field(max_length=64)
    last_name: Optional[str] = Field(max_length=64)
    date_of_birthday: Optional[date]
    additional_data: Optional[str] = Field(max_length=256, default=None)
    phone_numbers: List[PhoneNumberModel]
    emails: List[EmailModel]


class ContactResponse(ContactModel):
    """Response model for contact"""
    id: int

    class Config:
        orm_mode = True

