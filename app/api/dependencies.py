from data.session import SessionLocal


def get_db():
    """
    Provides a database session to the dependent functions
    using FastAPI's dependency injection.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
