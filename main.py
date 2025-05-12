from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from src import SessionLocal, engine, Base, fetch_campgrounds, save_campgrounds

app = FastAPI()

# DB tablolarını oluştur
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

@app.post("/scrape")
def scrape_campgrounds(db: Session = Depends(get_db)):
    try:
        data = fetch_campgrounds()
        save_campgrounds(db, data)
        return {"status": "success", "count": len(data)}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
