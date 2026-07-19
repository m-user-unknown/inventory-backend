from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine

# Import all models so they're registered on Base.metadata before create_all runs
from app.models import product, purchase, sales, user  # noqa: F401

from app.routers import auth, product as product_router, purchase as purchase_router
from app.routers import sales as sales_router, stock as stock_router, report as report_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name, version=settings.app_version)

# NOTE: wide-open CORS is convenient for local dev; restrict allow_origins before deploying.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(product_router.router)
app.include_router(purchase_router.router)
app.include_router(sales_router.router)
app.include_router(stock_router.router)
app.include_router(report_router.router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "service": settings.app_name, "version": settings.app_version}
