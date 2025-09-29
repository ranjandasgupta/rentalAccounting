import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .config import settings
from .database import Base, engine
from .routers import common, basic, accounts, transactions, reports, audits

# Create tables if not exist (for demo / dev). For prod, use migrations.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Rental Accounting API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(common.router)
app.include_router(basic.router)
app.include_router(accounts.router)
app.include_router(transactions.router)
app.include_router(reports.router)
app.include_router(audits.router)

# Serve the simple frontend from STATIC_DIR (index.html)
static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), settings.STATIC_DIR))
if os.path.isdir(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

    @app.get("/")
    async def root():
        return FileResponse(os.path.join(static_path, "index.html"))
