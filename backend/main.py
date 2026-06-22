from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.routes import auth, doctors, admin, blog, bookings

app = FastAPI(title="MediCare API")

os.makedirs("uploads/avatars", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def start_database():
    await init_db()

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(doctors.router, prefix="/api/doctors", tags=["Doctors"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(blog.router, prefix="/api/blogs", tags=["Blogs"])
app.include_router(bookings.router, prefix="/api/bookings", tags=["Bookings"])

@app.get("/")
def read_root():
    return {"message": "MediCare API is running"}
