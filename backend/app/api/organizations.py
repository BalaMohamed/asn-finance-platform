from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter()


@router.post("/organizations", response_model=schemas.OrganizationResponse)
def create_organization(
    organization_data: schemas.OrganizationCreate,
    db: Session = Depends(get_db)
):
    existing_org = (
        db.query(models.Organization)
        .filter(models.Organization.name == organization_data.name)
        .first()
    )

    if existing_org:
        raise HTTPException(status_code=400, detail="Organization already exists")

    new_org = models.Organization(name=organization_data.name)

    db.add(new_org)
    db.commit()
    db.refresh(new_org)

    return new_org


@router.get("/organizations", response_model=list[schemas.OrganizationResponse])
def get_organizations(db: Session = Depends(get_db)):
    organizations = db.query(models.Organization).order_by(models.Organization.id.asc()).all()
    return organizations


@router.get("/organizations/{organization_id}", response_model=schemas.OrganizationResponse)
def get_organization(organization_id: int, db: Session = Depends(get_db)):
    organization = (
        db.query(models.Organization)
        .filter(models.Organization.id == organization_id)
        .first()
    )

    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    return organization