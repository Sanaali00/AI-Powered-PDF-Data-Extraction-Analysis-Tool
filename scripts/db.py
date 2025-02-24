from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from config import DATABASE  # Ensure DATABASE contains correct SQLite path

Base = declarative_base()


class ExtractedData(Base):
    """ORM Model for storing extracted PDF data."""
    __tablename__ = "extracted_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    text = Column(Text, nullable=True)
    table = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    entities = Column(Text, nullable=True)
    classification = Column(String(255), nullable=True)


engine = create_engine(f"sqlite:///{DATABASE['database']}", echo=True)
Session = sessionmaker(bind=engine)


def init_db():
    """Initialize the database tables."""
    Base.metadata.create_all(engine)
    print("✅ Database initialized successfully.")


def save_extracted_data(filename, text, table, summary, entities, classification):
    """Save extracted data to SQLite database."""
    session = Session()
    try:
        data = ExtractedData(
            filename=filename,
            text=text,
            table=table,
            summary=summary,
            entities=str(entities),
            classification=classification
        )
        session.add(data)
        session.commit()
        print("✅ Data saved successfully!")
    except Exception as e:
        session.rollback()
        print(f"❌ Error saving data: {e}")
    finally:
        session.close()
