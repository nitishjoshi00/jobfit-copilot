from sqlmodel import SQLModel, create_engine, Session
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@127.0.0.1:5432/jobfit"
)

# 👇 print the URL we’re actually using (for troubleshooting)
print("Using DATABASE_URL:", DATABASE_URL)

# pool_pre_ping helps if connections go stale
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)

def init_db():
    # 👇 try a quick connection first so errors are obvious
    try:
        with engine.connect() as conn:
            conn.exec_driver_sql("SELECT 1;")
            print("DB connection OK ✅")
    except Exception as e:
        print("DB connection FAILED ❌", repr(e))
        raise

    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
