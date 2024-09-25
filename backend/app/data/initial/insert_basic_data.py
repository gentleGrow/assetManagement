import asyncio

from icecream import ic
from sqlalchemy.ext.asyncio import AsyncSession

from app.module.asset.constant import (
    ACCOUNT_TYPES,
    INVESTMENT_BANKS,
    PURCHASE_DATES,
    PURCHASECURRENCYTYPES,
    STOCK_CODES,
    STOCK_QUANTITIES,
)
from app.module.asset.enum import AssetType, StockAsset
from app.module.asset.model import Asset, AssetField, AssetStock
from app.module.asset.repository.asset_field_repository import AssetFieldRepository
from app.module.asset.repository.asset_repository import AssetRepository
from app.module.asset.repository.stock_repository import StockRepository
from app.module.auth.constant import ADMIN_USER_ID, DUMMY_USER_ID
from app.module.auth.enum import ProviderEnum, UserRoleEnum
from app.module.auth.model import User
from app.module.auth.repository import UserRepository
from app.module.chart.repository import TipRepository
from database.dependency import get_mysql_session


async def create_initial_users(session: AsyncSession):
    check_admin_user = await UserRepository.get(session, ADMIN_USER_ID)
    check_dummy_user = await UserRepository.get(session, DUMMY_USER_ID)

    if check_admin_user and check_dummy_user:
        return False

    if check_admin_user is None:
        admin_user = User(
            id=ADMIN_USER_ID,
            social_id="admin_social_id",
            provider=ProviderEnum.GOOGLE,
            role=UserRoleEnum.ADMIN,
            nickname="admin_user",
        )
        await UserRepository.create(session, admin_user)

    if check_dummy_user is None:
        dummy_user = User(
            id=DUMMY_USER_ID,
            social_id="dummy_social_id",
            provider=ProviderEnum.GOOGLE,
            nickname="dummy_user",
        )

        await UserRepository.create(session, dummy_user)

    ic("[create_initial_users] 성공적으로 admin과 더미 유저를 생성 했습니다.")

    return True


async def create_dummy_assets(session: AsyncSession):
    assets_exist = await AssetRepository.get_assets(session, DUMMY_USER_ID)
    if assets_exist:
        ic("이미 dummy assets을 저장하였습니다.")
        return

    stock_list = await StockRepository.get_by_codes(session, STOCK_CODES)
    stock_dict = {stock.code: stock for stock in stock_list}

    assets = []

    for i in range(len(STOCK_CODES)):
        stock = stock_dict.get(STOCK_CODES[i])
        if not stock:
            continue

        asset = Asset(
            asset_type=AssetType.STOCK.value,
            user_id=DUMMY_USER_ID,
        )

        AssetStock(
            purchase_price=None,
            purchase_date=PURCHASE_DATES[i],
            purchase_currency_type=PURCHASECURRENCYTYPES[i],
            quantity=STOCK_QUANTITIES[i],
            investment_bank=INVESTMENT_BANKS[i],
            account_type=ACCOUNT_TYPES[i],
            asset=asset,
            stock=stock,
        )

        assets.append(asset)

    await AssetRepository.save_assets(session, assets)
    ic("[create_dummy_assets] 더미 유저에 assets을 성공적으로 생성 했습니다.")


async def create_investment_tip(session: AsyncSession):
    investment_tips = [
        {"id": 1, "tip": "초보 투자자는 분산 투자를 고려하세요."},
        {"id": 2, "tip": "장기적인 투자 목표를 설정하세요."},
        {"id": 3, "tip": "리스크를 관리하기 위해 포트폴리오를 다양화하세요."},
        {"id": 4, "tip": "시장 변동에 대해 과민반응하지 마세요."},
        {"id": 5, "tip": "투자 결정을 내리기 전에 충분한 조사를 하세요."},
        {"id": 6, "tip": "수익률에 집착하지 말고 꾸준히 투자하세요."},
        {"id": 7, "tip": "시장을 예측하려고 하지 마세요."},
        {"id": 8, "tip": "전문가의 조언을 경청하되, 스스로 결정하세요."},
        {"id": 9, "tip": "장기적으로 안정적인 자산에 투자하세요."},
        {"id": 10, "tip": "자신의 리스크 허용 범위를 이해하세요."},
    ]

    await TipRepository.save_invest_tips(session, investment_tips)
    ic("[create_investment_tip] investment_tips를 성공적으로 생성 했습니다.")


async def create_asset_field(session: AsyncSession):
    asset_field = await AssetFieldRepository.get(session, DUMMY_USER_ID)
    if asset_field:
        ic("이미 asset_field를 저장하였습니다.")
        return

    fields_to_disable = ["stock_volume", "purchase_currency_type", "purchase_price", "purchase_amount"]
    field_preference = [field for field in [field.value for field in StockAsset] if field not in fields_to_disable]

    asset_field = AssetField(user_id=DUMMY_USER_ID, field_preference=field_preference)

    await AssetFieldRepository.save(session, asset_field)


async def main():
    async with get_mysql_session() as session:
        try:
            await create_initial_users(session)
        except Exception as err:
            ic(f"유저 생성 중 에러가 생겼습니다. {err=}")

        try:
            await create_dummy_assets(session)
        except Exception as err:
            ic(f"dummy asset 생성 중 에러가 생겼습니다. {err=}")

        try:
            await create_investment_tip(session)
        except Exception as err:
            ic(f"investment tip 생성 중 에러가 생겼습니다. {err=}")

        try:
            await create_asset_field(session)
        except Exception as err:
            ic(f"asset_field 생성 중 에러가 생겼습니다. {err=}")


if __name__ == "__main__":
    asyncio.run(main())
