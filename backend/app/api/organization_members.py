from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter()


@router.post("/members", response_model=schemas.OrganizationMemberResponse)
def create_member(
    member_data: schemas.OrganizationMemberCreate,
    db: Session = Depends(get_db)
):
    organization = (
        db.query(models.Organization)
        .filter(models.Organization.id == member_data.organization_id)
        .first()
    )

    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    new_member = models.OrganizationMember(
        name=member_data.name,
        role=member_data.role.value,
        organization_id=member_data.organization_id
    )

    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return new_member


@router.get("/members", response_model=list[schemas.OrganizationMemberResponse])
def get_members(organization_id: int, db: Session = Depends(get_db)):
    members = (
        db.query(models.OrganizationMember)
        .filter(models.OrganizationMember.organization_id == organization_id)
        .order_by(models.OrganizationMember.id.asc())
        .all()
    )
    return members


@router.get("/members/{member_id}", response_model=schemas.OrganizationMemberResponse)
def get_member(member_id: int, organization_id: int, db: Session = Depends(get_db)):
    member = (
        db.query(models.OrganizationMember)
        .filter(
            models.OrganizationMember.id == member_id,
            models.OrganizationMember.organization_id == organization_id
        )
        .first()
    )

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    return member