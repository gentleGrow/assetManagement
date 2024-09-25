from fastapi import APIRouter, Depends, HTTPException, status
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.auth.security import verify_jwt_token
from app.common.schema.common_schema import DeleteResponse, PostResponse, PutResponse
from app.module.asset.enum import AccountType, AssetType, InvestmentBankType
from app.module.asset.model import Asset, AssetField, Stock
from app.module.asset.repository.asset_field_repository import AssetFieldRepository
from app.module.asset.repository.asset_repository import AssetRepository
from app.module.asset.repository.stock_repository import StockRepository
from app.module.asset.schema import (
    AssetFieldResponse,
    AssetStockPostRequest,
    AssetStockPutRequest,
    AssetStockResponse,
    BankAccountResponse,
    StockListResponse,
    StockListValue,
    UpdateAssetFieldRequest,
)
from app.module.asset.services.asset_field_service import AssetFieldService
from app.module.asset.services.asset_service import AssetService
from app.module.asset.services.asset_stock_service import AssetStockService
from app.module.asset.services.dividend_service import DividendService
from app.module.asset.services.exchange_rate_service import ExchangeRateService
from app.module.asset.services.stock_daily_service import StockDailyService
from app.module.asset.services.stock_service import StockService
from app.module.auth.constant import DUMMY_USER_ID
from app.module.auth.model import User  # noqa: F401 > relationship 설정시 필요합니다.
from app.module.auth.schema import AccessToken
from database.dependency import get_mysql_session_router, get_redis_pool

asset_stock_router = APIRouter(prefix="/v1")


@asset_stock_router.get("/asset-field", summary="자산 필드를 반환합니다.", response_model=AssetFieldResponse)
async def get_asset_field(
    session: AsyncSession = Depends(get_mysql_session_router),
    token: AccessToken = Depends(verify_jwt_token),
) -> AssetFieldResponse:
    asset_field: list[str] = await AssetFieldService.get_asset_field(session, token.get("user"))
    return AssetFieldResponse(asset_field)


@asset_stock_router.put("/asset-field", summary="자산 필드를 변경합니다.", response_model=PutResponse)
async def update_asset_field(
    request_data: UpdateAssetFieldRequest,
    session: AsyncSession = Depends(get_mysql_session_router),
    token: AccessToken = Depends(verify_jwt_token),
) -> PutResponse:
    UpdateAssetFieldRequest.validate_request_data(request_data)

    asset_field = await AssetFieldRepository.get(session, token.get("user"))
    await AssetFieldRepository.update(
        session, AssetField(id=asset_field.id, user_id=token.get("user"), field_preference=request_data.root)
    )
    return PutResponse(status_code=status.HTTP_200_OK, content="자산관리 필드를 성공적으로 수정 하였습니다.")


@asset_stock_router.get("/bank-accounts", summary="증권사와 계좌 리스트를 반환합니다.", response_model=BankAccountResponse)
async def get_bank_account_list() -> BankAccountResponse:
    investment_bank_list = [bank.value for bank in InvestmentBankType]
    account_list = [account.value for account in AccountType]

    return BankAccountResponse(investment_bank_list=investment_bank_list, account_list=account_list)


@asset_stock_router.get("/stocks", summary="주시 종목 코드를 반환합니다.", response_model=StockListResponse)
async def get_stock_list(session: AsyncSession = Depends(get_mysql_session_router)) -> StockListResponse:
    stock_list: list[Stock] = await StockRepository.get_all(session)

    return StockListResponse([StockListValue(name=stock.name, code=stock.code) for stock in stock_list])


@asset_stock_router.get("/sample/assetstock", summary="임시 자산 정보를 반환합니다.", response_model=AssetStockResponse)
async def get_sample_asset_stock(
    session: AsyncSession = Depends(get_mysql_session_router), redis_client: Redis = Depends(get_redis_pool)
) -> AssetStockResponse:
    assets: list[Asset] = await AssetRepository.get_eager(session, DUMMY_USER_ID, AssetType.STOCK)
    validation_response = AssetStockResponse.validate_assets(assets)
    if validation_response:
        return validation_response

    stock_daily_map = await StockDailyService.get_map_range(session, assets)
    lastest_stock_daily_map = await StockDailyService.get_latest_map(session, assets)
    dividend_map = await DividendService.get_recent_map(session, assets)
    exchange_rate_map = await ExchangeRateService.get_exchange_rate_map(redis_client)
    current_stock_price_map = await StockService.get_current_stock_price(redis_client, lastest_stock_daily_map, assets)

    not_found_stock_codes: list[str] = StockService.check_not_found_stock(
        stock_daily_map, current_stock_price_map, assets
    )
    if not_found_stock_codes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"다음의 주식 코드를 찾지 못 했습니다.": not_found_stock_codes}
        )

    stock_assets: list[dict] = await AssetStockService.get_stock_assets(
        session, DUMMY_USER_ID, assets, stock_daily_map, current_stock_price_map, dividend_map, exchange_rate_map
    )

    total_asset_amount = AssetStockService.get_total_asset_amount(assets, current_stock_price_map, exchange_rate_map)
    total_invest_amount = AssetStockService.get_total_investment_amount(assets, stock_daily_map, exchange_rate_map)
    total_dividend_amount = DividendService.get_total_dividend(assets, dividend_map, exchange_rate_map)

    return AssetStockResponse.parse(stock_assets, total_asset_amount, total_invest_amount, total_dividend_amount)


@asset_stock_router.get("/assetstock", summary="사용자의 자산 정보를 반환합니다.", response_model=AssetStockResponse)
async def get_asset_stock(
    token: AccessToken = Depends(verify_jwt_token),
    redis_client: Redis = Depends(get_redis_pool),
    session: AsyncSession = Depends(get_mysql_session_router),
) -> AssetStockResponse:
    assets: list[Asset] = await AssetRepository.get_eager(session, token.get("user"), AssetType.STOCK)

    validation_response = AssetStockResponse.validate_assets(assets)
    if validation_response:
        return validation_response

    stock_daily_map = await StockDailyService.get_map_range(session, assets)
    lastest_stock_daily_map = await StockDailyService.get_latest_map(session, assets)
    dividend_map = await DividendService.get_recent_map(session, assets)
    exchange_rate_map = await ExchangeRateService.get_exchange_rate_map(redis_client)
    current_stock_price_map = await StockService.get_current_stock_price(redis_client, lastest_stock_daily_map, assets)

    not_found_stock_codes: list[str] = StockService.check_not_found_stock(
        stock_daily_map, current_stock_price_map, assets
    )
    if not_found_stock_codes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"다음의 주식 코드를 찾지 못 했습니다.": not_found_stock_codes}
        )

    stock_assets: list[dict] = await AssetStockService.get_stock_assets(
        session, token.get("user"), assets, stock_daily_map, current_stock_price_map, dividend_map, exchange_rate_map
    )

    total_asset_amount = AssetStockService.get_total_asset_amount(assets, current_stock_price_map, exchange_rate_map)
    total_invest_amount = AssetStockService.get_total_investment_amount(assets, stock_daily_map, exchange_rate_map)
    total_dividend_amount = DividendService.get_total_dividend(assets, dividend_map, exchange_rate_map)

    return AssetStockResponse.parse(stock_assets, total_asset_amount, total_invest_amount, total_dividend_amount)


@asset_stock_router.post("/assetstock", summary="자산관리 정보를 등록합니다.", response_model=PostResponse)
async def create_asset_stock(
    request_data: AssetStockPostRequest,
    token: AccessToken = Depends(verify_jwt_token),
    session: AsyncSession = Depends(get_mysql_session_router),
) -> PostResponse:
    stock = await StockRepository.get_by_code(session, request_data.stock_code)
    if stock is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{request_data.stock_code}를 찾지 못 했습니다.")

    await AssetStockService.save_asset_stock_by_post(session, request_data, stock.id, token.get("user"))
    return PostResponse(status_code=status.HTTP_201_CREATED, content="주식 자산 성공적으로 등록 했습니다.")


@asset_stock_router.put("/assetstock", summary="주식 자산을 수정합니다.", response_model=PutResponse)
async def update_asset_stock(
    request_data: AssetStockPutRequest,
    token: AccessToken = Depends(verify_jwt_token),
    session: AsyncSession = Depends(get_mysql_session_router),
) -> PutResponse:
    asset = await AssetRepository.get_asset_by_id(session, request_data.id)
    if asset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{request_data.id} id에 해당하는 자산을 찾지 못 했습니다.")

    stock = await StockRepository.get_by_code(session, request_data.stock_code)
    if stock is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{request_data.stock_code}를 찾지 못 했습니다.")

    await AssetService.save_asset_by_put(session, request_data, asset, stock.id)
    return PutResponse(status_code=status.HTTP_200_OK, content="주식 자산을 성공적으로 수정 하였습니다.")


@asset_stock_router.delete("/assetstock/{asset_id}", summary="자산을 삭제합니다.", response_model=DeleteResponse)
async def delete_asset_stock(
    asset_id: int,
    token: AccessToken = Depends(verify_jwt_token),
    session: AsyncSession = Depends(get_mysql_session_router),
) -> DeleteResponse:
    try:
        await AssetRepository.delete_asset(session, asset_id)
        return DeleteResponse(status_code=status.HTTP_200_OK, content="주식 자산이 성공적으로 삭제 되었습니다.")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
