import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from config import DATABASE  # Importing database config

Base = declarative_base()

class ExtractedData(Base):
    __tablename__ = "extracted_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    text = Column(Text, nullable=True)  # Changed to Text for longer storage
    table = Column(Text, nullable=True)  # Changed to Text for longer storage
    summary = Column(Text, nullable=True)  # Changed to Text for longer summaries
    entities = Column(Text, nullable=True)  # Changed to Text for entity extraction
    classification = Column(String(255), nullable=True)

# Create the engine once and reuse it
engine = create_engine(f"{DATABASE['type']}://{DATABASE['user']}:{DATABASE['password']}@{DATABASE['host']}:{DATABASE['port']}/{DATABASE['database']}")
Session = sessionmaker(bind=engine)

def init_db():
    """Initialize the database tables."""
    Base.metadata.create_all(engine)
    print("✅ Database initialized successfully.")

def save_extracted_data(filename, text, table, summary, entities, classification):
    """Save extracted data to database."""
    session = Session()

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
    session.close()
    print("✅ Data saved successfully!")
