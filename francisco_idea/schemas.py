import xml.etree.ElementTree as ET

from typing import Optional
from sqlmodel import SQLModel, Relationship, Field
from settings import DATABASE_PATH


class SQLModelXmlParser(SQLModel):
    """
    built in element parser to sqlmodel.
    each field should have an alias attribute that will refer to the field name in xml.
    example: la_child_id will correspond to LAchildID if it's declared like:
        la_child_id: str = Field(alias='LAchildID')
    """

    def __init__(self, element: ET.Element, *args, **data):
        for key, field in self.__fields__.items():
            try:
                value = element.find(field.alias).text
            except AttributeError:
                continue
            print(key, value)
            data[field.alias] = value
        super().__init__(*args, **data)


class CINDetails(SQLModelXmlParser, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    reason_for_closure: Optional[str] = Field(alias="ReasonForClosure")
    primary_need_code: Optional[str] = Field(alias="PrimaryNeedCode")
    referral_nfa: Optional[str] = Field(alias="ReferralNFA")
    referral_source: Optional[str] = Field(alias="ReferralSource")
    initial_cpc_date: Optional[str] = Field(alias="DateOfInitialCPC")
    referral_date: Optional[str] = Field(alias="CINreferralDate")
    closure_date: Optional[str] = Field(alias="CINclosureDate")

    child: "Child" = Relationship(back_populates="cin_details")


class Characteristics(SQLModelXmlParser, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    disability: Optional[str] = Field(alias="Disabilities//Disability")
    ethnicity: Optional[str] = Field(alias="Ethnicity")

    child: "Child" = Relationship(back_populates="characteristics")


class Identifiers(SQLModelXmlParser, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    la_child_id: str = Field(alias="LAchildID")
    upn: str = Field(alias="UPN")
    birth_date: str = Field(alias="PersonBirthDate")
    death_date: Optional[str] = Field(alias="PersonDeathDate")
    gender: int = Field(alias="GenderCurrent")

    child: "Child" = Relationship(back_populates="identifiers")


class Child(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    identifiers_id: Optional[int] = Field(default=None, foreign_key="identifiers.id")
    identifiers: Optional[Identifiers] = Relationship(back_populates="child")

    characteristics_id: Optional[int] = Field(
        default=None, foreign_key="characteristics.id"
    )
    characteristics: Optional[Characteristics] = Relationship(back_populates="child")

    cin_details_id: Optional[int] = Field(default=None, foreign_key="cindetails.id")
    cin_details: Optional[CINDetails] = Relationship(back_populates="child")


sqlite_url = f"sqlite:///{DATABASE_PATH}"
