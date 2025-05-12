from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from src import SessionLocal, engine, Base, fetch_campgrounds, save_campgrounds

app = FastAPI()

# DB tablolarını oluştur
# Base.metadata.create_all(bind=engine)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
# db: Session = Depends(get_db)
@app.get("/")
def root():
    return {"message": "Scraper API is running."}

@app.get("/scrape")
async def scrape_campgrounds():
    try:
        data = await fetch_campgrounds()
        # save_campgrounds(db, data)
        return {"status": "success", "count": len(data)}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
