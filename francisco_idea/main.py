import xml.etree.ElementTree as ET

from database import (
    create_child,
    create_db_and_tables,
    read_all_from_model,
    sqlmodel_to_df,
)
from settings import DATABASE_PATH
from schemas import Child, Identifiers, Characteristics
import os


def parse_xml(file):
    tree = ET.parse(file)
    message = tree.getroot()
    childrenContainer = message.find("Children")
    childs = childrenContainer.findall("Child")
    for child in childs:
        create_child(child)


def xml_to_sql(file_name: str, reset: bool = False):
    if reset and os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
    create_db_and_tables()
    with open(file_name, "r") as file:
        parse_xml(file)


def sql_to_pandas():
    childs = read_all_from_model(Child)
    identifiers = read_all_from_model(Identifiers)
    characteristics = read_all_from_model(Characteristics)
    print(sqlmodel_to_df(childs))
    print(sqlmodel_to_df(identifiers))
    print(sqlmodel_to_df(characteristics))


if __name__ == "__main__":
    # call this first once, to fill the database
    xml_to_sql(file_name="francisco_idea/data.xml", reset=True)

    # call it whenever, to read data
    sql_to_pandas()
