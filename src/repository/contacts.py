from typing import List
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel
from datetime import date, timedelta
from sqlalchemy import func


async def get_contacts(skip: int, limit: int, user: User, db: Session):
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def create_contact(body: ContactModel, user: User, db: Session):
    print(body.first_name)
    contact = Contact(first_name=body.first_name, last_name=body.last_name, email=body.email,
                      phone=body.phone, birt_day=body.birt_day, user_id=user.id)

    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def get_contact_by_id(contact_id: int, user: User, db: Session) -> Contact | None:
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def update_contact(contact_id: int, body: ContactModel, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birt_day = body.birt_day
        db.commit()
    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def get_contacts_by_info(contact_info: str, user: User, db: Session):
    contacts = db.query(Contact).filter(Contact.user_id == user.id).filter(
        or_(Contact.first_name.ilike(f'%{contact_info}%'),
            Contact.last_name.ilike(f'%{contact_info}%'),
            Contact.email.ilike(f'%{contact_info}%'),
            ))
    return contacts


async def birthday(user: User, db: Session):
    current_day = date.today()
    date_to = date.today() + timedelta(days=7)
    this_year = current_day.year
    next_year = current_day.year + 1
    contacts = db.query(Contact).filter(Contact.user_id == user.id).filter(
        or_(
            func.to_date(func.concat(func.to_char(Contact.birt_day, "DDMM"), this_year), "DDMMYYYY").between(
                current_day, date_to),
            func.to_date(func.concat(func.to_char(Contact.birt_day, "DDMM"), next_year), "DDMMYYYY").between(
                current_day, date_to)
        )
    ).all()
    return contacts
