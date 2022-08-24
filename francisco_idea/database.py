import xml.etree.ElementTree as ET
from sqlmodel import Session, SQLModel, create_engine, select
import pandas as pd

from schemas import sqlite_url, CINDetails, Characteristics, Identifiers, Child


engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_child(child_element: ET.Element) -> Child:
    with Session(engine) as session:
        # create identifiers, characteristics and details
        child_identifier = Identifiers(element=child_element.find("ChildIdentifiers"))
        child_characteristics = Characteristics(
            element=child_element.find("ChildCharacteristics")
        )
        cin_details = CINDetails(element=child_element.find("CINdetails"))

        # commit data
        session.add(child_identifier)
        session.add(child_characteristics)
        session.add(cin_details)
        session.commit()

        # create child
        child = Child(
            identifiers_id=child_identifier.id,
            characteristics_id=child_characteristics.id,
            cin_details_id=cin_details.id,
        )
        session.add(child)
        session.commit()
        return child


def read_all_from_model(model: SQLModel):
    with Session(engine) as session:
        instances = session.exec(select(model)).all()
    return instances


def sqlmodel_to_df(objects: list[SQLModel], set_index: bool = True) -> pd.DataFrame:
    """Converts SQLModel objects into a Pandas DataFrame.
    Usage
    ----------
    df = sqlmodel_to_df(list_of_sqlmodels)
    Parameters
    ----------
    :param objects: List[SQLModel]: List of SQLModel objects to be converted.
    :param set_index: bool: Sets the first column, usually the primary key, to dataframe index."""

    records = [obj.dict() for obj in objects]
    columns = list(objects[0].schema()["properties"].keys())
    df = pd.DataFrame.from_records(records, columns=columns)
    return df.set_index(columns[0]) if set_index else df
