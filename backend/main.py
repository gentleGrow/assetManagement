from os import getenv

from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.api.asset.v1.router import asset_stock_router
from app.api.auth.v1.router import auth_router
from app.api.chart.v1.router import chart_router
from app.module.asset.model import Asset  # noqa: F401 > table 생성 시 필요합니다.
from app.module.auth.model import User  # noqa: F401 > table 생성 시 필요합니다.

app = FastAPI()

load_dotenv()

SESSION_KEY = getenv("SESSION_KEY", None)

app.add_middleware(SessionMiddleware, secret_key=SESSION_KEY)

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(chart_router, prefix="/api/chart", tags=["chart"])
app.include_router(asset_stock_router, prefix="/api", tags=["asset"])
