from sqlalchemy import (Integer, String, ForeignKey, Date)
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship


Base = declarative_base()

class PhoneNumber(Base):
    """Class for phone number"""
    __tablename__ = "phone_numbers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    phone_number: Mapped[str] = mapped_column(String(15), nullable=True)
    contact_id: Mapped[str] = mapped_column(Integer, ForeignKey("contacts.id"))
    contact: Mapped['Contact'] = relationship("Contact", back_populates="phone_numbers")


class Email(Base):
    """Class for email"""
    __tablename__ = "emails"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(128), nullable=True)
    contact_id: Mapped[str] = mapped_column(Integer, ForeignKey("contacts.id"))
    contact: Mapped['Contact'] = relationship("Contact", back_populates="emails")


class Contact(Base):
    """Class for contact"""
    __tablename__ = "contacts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(64), nullable=True)
    last_name: Mapped[str] = mapped_column(String(64), nullable=True)
    date_of_birthday: Mapped[Date] = mapped_column(Date, nullable=True)
    additional_data: Mapped[str] = mapped_column(String(256), nullable=True)
    phone_numbers: Mapped[list[PhoneNumber]] = relationship("PhoneNumber", back_populates="contact", cascade="all, delete-orphan")
    emails: Mapped[list[Email]] = relationship("Email", back_populates="contact", cascade="all, delete-orphan")