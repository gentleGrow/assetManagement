from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import StrictBool
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.auth.security import verify_jwt_token
from app.common.schema.json_schema import JsonResponse
from app.module.asset.enum import AccountType, AssetType, InvestmentBankType
from app.module.asset.model import Asset, AssetStock, Dividend, Stock, StockDaily
from app.module.asset.repository.asset_repository import AssetRepository
from app.module.asset.repository.dividend_repository import DividendRepository
from app.module.asset.repository.stock_daily_repository import StockDailyRepository
from app.module.asset.repository.stock_repository import StockRepository
from app.module.asset.schema import (
    BankAccountResponse,
    StockAssetRequest,
    StockAssetResponse,
    StockListResponse,
    StockListResponseValue,
)
from app.module.asset.service import (
    check_not_found_stock,
    get_current_stock_price,
    get_exchange_rate_map,
    get_stock_assets,
    get_total_asset_amount,
    get_total_dividend,
    get_total_investment_amount,
)
from app.module.auth.constant import DUMMY_USER_ID
from app.module.auth.model import User  # noqa: F401 > relationship 설정시 필요합니다.
from app.module.auth.schema import AccessToken
from database.dependency import get_mysql_session_router, get_redis_pool

asset_stock_router = APIRouter(prefix="/v1")


@asset_stock_router.get("/bank-accounts", summary="증권사와 계좌 리스트를 반환합니다.", response_model=BankAccountResponse)
async def get_bank_account_list(session: AsyncSession = Depends(get_mysql_session_router)) -> BankAccountResponse:
    investment_bank_list = [bank.value for bank in InvestmentBankType]

    account_list = [account.value for account in AccountType]

    return BankAccountResponse(investment_bank_list=investment_bank_list, account_list=account_list)


@asset_stock_router.get("/stocks", summary="주시 종목 코드를 반환합니다.", response_model=StockListResponse)
async def get_stocklist(session: AsyncSession = Depends(get_mysql_session_router)) -> StockListResponse:
    stock_list: list[Stock] = await StockRepository.get_all(session)

    stock_response_list = [StockListResponseValue(name=stock.name, code=stock.code) for stock in stock_list]

    return StockListResponse(stock_list=stock_response_list)


@asset_stock_router.get("/dummy/assetstock", summary="임시 자산 정보를 반환합니다.", response_model=StockAssetResponse)
async def get_dummy_assets(
    session: AsyncSession = Depends(get_mysql_session_router),
    redis_client: Redis = Depends(get_redis_pool),
    base_currency: StrictBool = Query(True, description="원화는 True, 종목통화는 False"),
) -> StockAssetResponse:
    if base_currency not in [True, False]:
        raise HTTPException(status_code=400, detail="올바른 parameter가 넘어 오지 않았습니다. 원화는 True, 종목통화는 False")

    assets: list[Asset] = await AssetRepository.get_eager(session, DUMMY_USER_ID, AssetType.STOCK)

    if len(assets) == 0:
        return StockAssetResponse(
            stock_assets=[],
            total_asset_amount=0.0,
            total_invest_amount=0.0,
            total_profit_rate=0.0,
            total_profit_amount=0.0,
            total_dividend_amount=0.0,
        )

    stock_code_date_pairs = [(asset.asset_stock.stock.code, asset.asset_stock.purchase_date) for asset in assets]
    stock_codes = [asset.asset_stock.stock.code for asset in assets]
    stock_dailies: list[StockDaily] = await StockDailyRepository.get_stock_dailies_by_code_and_date(
        session, stock_code_date_pairs
    )

    lastest_stock_dailies: list[StockDaily] = await StockDailyRepository.get_latest(session, stock_codes)
    lastest_stock_daily_map = {daily.code: daily for daily in lastest_stock_dailies}

    dividends: list[Dividend] = await DividendRepository.get_dividends_recent(session, stock_codes)

    dividend_map = {dividend.stock_code: dividend.dividend for dividend in dividends}
    exchange_rate_map = await get_exchange_rate_map(redis_client)
    stock_daily_map = {(daily.code, daily.date): daily for daily in stock_dailies}

    current_stock_price_map = await get_current_stock_price(redis_client, lastest_stock_daily_map, stock_codes)

    not_found_stock_codes: list[str] = check_not_found_stock(stock_daily_map, current_stock_price_map, assets)
    if not_found_stock_codes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"다음의 주식 코드를 찾지 못 했습니다.": not_found_stock_codes}
        )

    stock_assets = get_stock_assets(
        assets, stock_daily_map, current_stock_price_map, dividend_map, base_currency, exchange_rate_map
    )

    total_asset_amount = get_total_asset_amount(assets, current_stock_price_map, exchange_rate_map)
    total_invest_amount = get_total_investment_amount(assets, stock_daily_map, exchange_rate_map)
    total_dividend_amount = get_total_dividend(assets, dividend_map, exchange_rate_map)

    return StockAssetResponse.parse(stock_assets, total_asset_amount, total_invest_amount, total_dividend_amount)


@asset_stock_router.get("/assetstock", summary="사용자의 자산 정보를 반환합니다.", response_model=StockAssetResponse)
async def get_assets(
    token: AccessToken = Depends(verify_jwt_token),
    redis_client: Redis = Depends(get_redis_pool),
    session: AsyncSession = Depends(get_mysql_session_router),
    base_currency: StrictBool = Query(True, description="원화는 True, 종목통화는 False"),
) -> StockAssetResponse:
    user_id = token.get("user")
    if user_id is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자 id를 찾지 못하였습니다.")

    if base_currency not in [True, False]:
        raise HTTPException(status_code=400, detail="올바른 parameter가 넘어 오지 않았습니다. 원화는 True, 종목통화는 False")

    assets: list[Asset] = await AssetRepository.get_eager(session, user_id, AssetType.STOCK)

    if len(assets) == 0:
        return StockAssetResponse(
            stock_assets=[],
            total_asset_amount=0.0,
            total_invest_amount=0.0,
            total_profit_rate=0.0,
            total_profit_amount=0.0,
            total_dividend_amount=0.0,
        )

    stock_code_date_pairs = [(asset.asset_stock.stock.code, asset.asset_stock.purchase_date) for asset in assets]
    stock_codes = [asset.asset_stock.stock.code for asset in assets]
    stock_dailies: list[StockDaily] = await StockDailyRepository.get_stock_dailies_by_code_and_date(
        session, stock_code_date_pairs
    )

    dividends: list[Dividend] = await DividendRepository.get_dividends_recent(session, stock_codes)
    dividend_map = {dividend.stock_code: dividend.dividend for dividend in dividends}
    exchange_rate_map = await get_exchange_rate_map(redis_client)
    stock_daily_map = {(daily.code, daily.date): daily for daily in stock_dailies}

    lastest_stock_dailies: list[StockDaily] = await StockDailyRepository.get_latest(session, stock_codes)
    lastest_stock_daily_map = {daily.code: daily for daily in lastest_stock_dailies}
    current_stock_price_map = await get_current_stock_price(redis_client, lastest_stock_daily_map, stock_codes)

    not_found_stock_codes: list[str] = check_not_found_stock(stock_daily_map, current_stock_price_map, assets)
    if not_found_stock_codes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"not_found_stock_codes": not_found_stock_codes}
        )

    stock_assets = get_stock_assets(
        assets, stock_daily_map, current_stock_price_map, dividend_map, base_currency, exchange_rate_map
    )

    total_asset_amount = get_total_asset_amount(assets, current_stock_price_map, exchange_rate_map)
    total_invest_amount = get_total_investment_amount(assets, stock_daily_map, exchange_rate_map)
    total_dividend_amount = get_total_dividend(assets, dividend_map, exchange_rate_map)

    return StockAssetResponse.parse(stock_assets, total_asset_amount, total_invest_amount, total_dividend_amount)


@asset_stock_router.post("/assetstock", summary="자산관리 정보를 등록합니다.", response_model=JsonResponse)
async def create_assets(
    transaction_data: list[StockAssetRequest],
    token: dict = Depends(verify_jwt_token),
    session: AsyncSession = Depends(get_mysql_session_router),
) -> JsonResponse:
    user_id = token.get("user")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자 id를 찾지 못하였습니다.")

    assets_to_create = []

    stock_codes = [asset_data.stock_code for asset_data in transaction_data]
    stocks = await StockRepository.get_by_codes(session, stock_codes)
    stocks_map = {stock.code: stock for stock in stocks}

    for asset_data in transaction_data:
        if asset_data.id is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="주식 자산 데이터 안에 id 값이 없어야 합니다.")

        stock = stocks_map.get(asset_data.stock_code)
        if stock is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"종목 코드 {asset_data.stock_code}에 해당하는 주식을 찾을 수 없습니다."
            )

        new_asset = Asset(
            asset_type=AssetType.STOCK,
            user_id=user_id,
            asset_stock=AssetStock(
                account_type=asset_data.account_type,
                investment_bank=asset_data.investment_bank,
                purchase_currency_type=asset_data.purchase_currency_type,
                purchase_date=asset_data.buy_date,
                purchase_price=asset_data.purchase_price,
                quantity=asset_data.quantity,
                stock_id=stock.id,
            ),
        )
        assets_to_create.append(new_asset)

    await AssetRepository.save_assets(session, assets_to_create)
    return JsonResponse(status_code=status.HTTP_200_OK, content={"detail": "주식 자산 테이블을 성공적으로 등록하였습니다."})


@asset_stock_router.put("/assetstock", summary="자산관리 정보를 수정합니다.", response_model=JsonResponse)
async def update_assets(
    transaction_data: list[StockAssetRequest],
    token: dict = Depends(verify_jwt_token),
    session: AsyncSession = Depends(get_mysql_session_router),
) -> JsonResponse:
    user_id = token.get("user")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자 id를 찾지 못하였습니다.")

    asset_ids = [asset_data.id for asset_data in transaction_data if asset_data.id]

    assets_to_update = []

    existing_assets = await AssetRepository.get_assets_by_ids(session, asset_ids)

    existing_assets_map = {asset.id: asset for asset in existing_assets}

    stock_codes = [asset_data.stock_code for asset_data in transaction_data]

    stocks = await StockRepository.get_by_codes(session, stock_codes)
    stocks_map = {stock.code: stock for stock in stocks}

    for asset_data in transaction_data:
        stock = stocks_map.get(asset_data.stock_code)
        if stock is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"종목 코드 {asset_data.stock_code}에 해당하는 주식을 찾을 수 없습니다."
            )

        asset = existing_assets_map.get(asset_data.id)
        if asset is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Asset ID {asset_data.id}를 찾을 수 없습니다.")

        asset.asset_stock.account_type = asset_data.account_type
        asset.asset_stock.investment_bank = asset_data.investment_bank
        asset.asset_stock.purchase_currency_type = asset_data.purchase_currency_type
        asset.asset_stock.purchase_date = asset_data.buy_date
        asset.asset_stock.purchase_price = asset_data.purchase_price
        asset.asset_stock.quantity = asset_data.quantity
        asset.asset_stock.stock_id = stock.id

        assets_to_update.append(asset)

    await AssetRepository.save_assets(session, assets_to_update)
    return JsonResponse(status_code=status.HTTP_200_OK, content={"detail": "주식 자산 테이블을 성공적으로 수정하였습니다."})


@asset_stock_router.delete("/assetstock/{asset_id}", summary="자산을 삭제합니다.", response_model=JsonResponse)
async def delete_asset(
    asset_id: int,
    token: dict = Depends(verify_jwt_token),
    session: AsyncSession = Depends(get_mysql_session_router),
) -> JsonResponse:
    try:
        await AssetRepository.delete_asset(session, asset_id)
        return JsonResponse(status_code=status.HTTP_200_OK, content={"detail": "주식 자산이 성공적으로 삭제되었습니다."})
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
