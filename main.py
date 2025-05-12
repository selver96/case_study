from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from src import SessionLocal, engine, Base, fetch_campgrounds

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Scraper API is running."}

@app.get("/scrape")
async def scrape_campgrounds(db: Session = Depends(get_db)):
    try:
        data = await fetch_campgrounds(db)
        return {"status": "success", "count": len(data)}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
