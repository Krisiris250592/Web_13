from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from src.database.models import User
from src.database.db import get_db
from src.schemas import ContactModel, ContactResponse
import src.repository.contacts as contacts_repository
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                        user: User = Depends(auth_service.get_current_user)):
    contacts = await contacts_repository.get_contacts(skip, limit, user, db)
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Contacts with requested parameters not found")
    return contacts


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         user: User = Depends(auth_service.get_current_user)):
    return await contacts_repository.create_contact(body, user, db)


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db),
                       user: User = Depends(auth_service.get_current_user)):
    contact = await contacts_repository.get_contact_by_id(contact_id, user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db),
                         user: User = Depends(auth_service.get_current_user)):
    contact = await contacts_repository.update_contact(contact_id, body, user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db),
                         user: User = Depends(auth_service.get_current_user)):
    contact = await contacts_repository.remove_contact(contact_id, user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.get("/find/{contact_info}", response_model=List[ContactResponse])
async def read_contacts_by_info(contact_info: str, db: Session = Depends(get_db),
                                user: User = Depends(auth_service.get_current_user)):
    contacts = await contacts_repository.get_contacts_by_info(contact_info, user, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contacts


@router.get("/birthday", response_model=List[ContactResponse])
async def read_contacts_by_info(db: Session = Depends(get_db),
                                user: User = Depends(auth_service.get_current_user)):
    contacts = await contacts_repository.birthday(user,db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacts not found")
    return contacts
