from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_

from My_project.database.models import Contact, PhoneNumber, Email, User
from My_project.schemas import ContactModel, ContactUpdateMidel

async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()

async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id )).first()

async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    contact = Contact(first_name=body.first_name,
                      last_name=body.last_name,
                      date_of_birthday=body.date_of_birthday,
                      additional_data=body.additional_data,
                      phone_numbers=[PhoneNumber(phone_number=phone.phone_number) for phone in body.phone_numbers],
                      emails=[Email(email=email.email) for email in body.emails],
                      user=user)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

async def update_contact(contact_id: int, body: ContactUpdateMidel, user: User, db: Session) -> Contact:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.date_of_birthday = body.date_of_birthday
        contact.additional_data = body.additional_data
        contact.user = user

        db.query(PhoneNumber).filter(PhoneNumber.contact_id == contact.id).delete()
        for phone in body.phone_numbers:
            new_phone_number = PhoneNumber(phone_number=phone.phone_number,
                                    contact_id=contact.id)
            db.add(new_phone_number)

        db.query(Email).filter(Email.contact_id == contact.id).delete()
        for email in body.emails:
            new_email = Email(email=email.email, contact_id=contact.id)
            db.add(new_email)

        db.commit()
        db.refresh(contact)

    return contact

async def remove_contact(contact_id: int, db: Session) -> Contact|None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
