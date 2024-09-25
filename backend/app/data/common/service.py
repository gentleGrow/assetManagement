import os

import boto3
import pandas as pd
from dotenv import find_dotenv, load_dotenv
from icecream import ic

from app.data.common.config import (
    AUSTRALIA_STOCK_FILEPATH,
    BRAZIL_STOCK_FILEPATH,
    CANADA_STOCK_FILEPATH,
    CHINA_STOCK_FILEPATH,
    ENVIRONMENT,
    FRANCE_STOCK_FILEPATH,
    GERMANY_STOCK_FILEPATH,
    HONGKONG_STOCK_FILEPATH,
    INDIA_STOCK_FILEPATH,
    ITALY_STOCK_FILEPATH,
    JAPAN_STOCK_FILEPATH,
    KOREA_STOCK_FILEPATH,
    NETHERLAND_STOCK_FILEPATH,
    S3_BUCKET_STOCK_FILES,
    SPAIN_STOCK_FILEPATH,
    SWITZERLAND_STOCK_FILEPATH,
    UK_STOCK_FILEPATH,
    USA_STOCK_FILEPATH,
)
from app.module.asset.schema import StockInfo
from database.enum import EnvironmentType

load_dotenv(find_dotenv())

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

s3_client = boto3.client("s3")


class StockCodeFileReader:
    @staticmethod
    def get_stock_code_list_bundle() -> list[list[StockInfo]]:
        usa_stock_code_list = StockCodeFileReader._read_stock_codes_from_excel(
            StockCodeFileReader._get_path(USA_STOCK_FILEPATH)
        )
        japan_stock_code_list = StockCodeFileReader._read_stock_codes_from_excel(
            StockCodeFileReader._get_path(JAPAN_STOCK_FILEPATH)
        )
        australia_stock_code_list = StockCodeFileReader._read_stock_codes_from_excel(
            StockCodeFileReader._get_path(AUSTRALIA_STOCK_FILEPATH)
        )
        brazil_stock_code_list = StockCodeFileReader._read_stock_codes_from_excel(
            StockCodeFileReader._get_path(BRAZIL_STOCK_FILEPATH)
        )
        canada_stock_code_list = StockCodeFileReader._read_stock_codes_from_excel(
            StockCodeFileReader._get_path(CANADA_STOCK_FILEPATH)
        )
        china_stock_code_list = StockCodeFileReader._read_stock_codes_from_excel(
            StockCodeFileReader._get_path(CHINA_STOCK_FILEPATH)
        )
        france_stock_code_list = StockCodeFileReader._read_stock_codes_from_excel(
            StockCodeFileReader._get_path(FRANCE_STOCK_FILEPATH)
        )
        germany_stock_code_list = StockCodeFileReader._read_stock_codes_from_excel(
            StockCodeFileReader._get_path(GERMANY_STOCK_FILEPATH)
        )
        hongkong_stock_code_list = StockCodeFileReader._read_stock_codes_from_excel(
            StockCodeFileReader._get_path(HONGKONG_STOCK_FILEPATH)
        )
        india_stock_code_list = StockCodeFileReader._read_stock_codes_from_excel(
            StockCodeFileReader._get_path(INDIA_STOCK_FILEPATH)
        )
        italy_stock_code_list = StockCodeFileReader._read_stock_codes_from_excel(
            StockCodeFileReader._get_path(ITALY_STOCK_FILEPATH)
        )
        netherland_stock_code_list = StockCodeFileReader._read_stock_codes_from_excel(
            StockCodeFileReader._get_path(NETHERLAND_STOCK_FILEPATH)
        )
        spain_stock_code_list = StockCodeFileReader._read_stock_codes_from_excel(
            StockCodeFileReader._get_path(SPAIN_STOCK_FILEPATH)
        )
        switzerland_stock_code_list = StockCodeFileReader._read_stock_codes_from_excel(
            StockCodeFileReader._get_path(SWITZERLAND_STOCK_FILEPATH)
        )
        uk_stock_code_list = StockCodeFileReader._read_stock_codes_from_excel(
            StockCodeFileReader._get_path(UK_STOCK_FILEPATH)
        )
        korea_stock_code_list = StockCodeFileReader._read_stock_codes_from_excel(
            StockCodeFileReader._get_path(KOREA_STOCK_FILEPATH)
        )
        return [
            usa_stock_code_list,
            japan_stock_code_list,
            australia_stock_code_list,
            brazil_stock_code_list,
            canada_stock_code_list,
            china_stock_code_list,
            france_stock_code_list,
            germany_stock_code_list,
            hongkong_stock_code_list,
            india_stock_code_list,
            italy_stock_code_list,
            netherland_stock_code_list,
            spain_stock_code_list,
            switzerland_stock_code_list,
            uk_stock_code_list,
            korea_stock_code_list,
        ]

    @staticmethod
    def get_korea_stock_code_list() -> list[StockInfo]:
        return StockCodeFileReader._read_stock_codes_from_excel(StockCodeFileReader._get_path(KOREA_STOCK_FILEPATH))

    @staticmethod
    def get_all_stock_code_list() -> list[StockInfo]:
        usa_stock_code_list = StockCodeFileReader._read_stock_codes_from_excel(
            StockCodeFileReader._get_path(USA_STOCK_FILEPATH)
        )
        japan_stock_code_list = StockCodeFileReader._read_stock_codes_from_excel(
            StockCodeFileReader._get_path(JAPAN_STOCK_FILEPATH)
        )
        australia_stock_code_list = StockCodeFileReader._read_stock_codes_from_excel(
            StockCodeFileReader._get_path(AUSTRALIA_STOCK_FILEPATH)
        )
        brazil_stock_code_list = StockCodeFileReader._read_stock_codes_from_excel(
            StockCodeFileReader._get_path(BRAZIL_STOCK_FILEPATH)
        )
        canada_stock_code_list = StockCodeFileReader._read_stock_codes_from_excel(
            StockCodeFileReader._get_path(CANADA_STOCK_FILEPATH)
        )
        china_stock_code_list = StockCodeFileReader._read_stock_codes_from_excel(
            StockCodeFileReader._get_path(CHINA_STOCK_FILEPATH)
        )
        france_stock_code_list = StockCodeFileReader._read_stock_codes_from_excel(
            StockCodeFileReader._get_path(FRANCE_STOCK_FILEPATH)
        )
        germany_stock_code_list = StockCodeFileReader._read_stock_codes_from_excel(
            StockCodeFileReader._get_path(GERMANY_STOCK_FILEPATH)
        )
        hongkong_stock_code_list = StockCodeFileReader._read_stock_codes_from_excel(
            StockCodeFileReader._get_path(HONGKONG_STOCK_FILEPATH)
        )
        india_stock_code_list = StockCodeFileReader._read_stock_codes_from_excel(
            StockCodeFileReader._get_path(INDIA_STOCK_FILEPATH)
        )
        italy_stock_code_list = StockCodeFileReader._read_stock_codes_from_excel(
            StockCodeFileReader._get_path(ITALY_STOCK_FILEPATH)
        )
        netherland_stock_code_list = StockCodeFileReader._read_stock_codes_from_excel(
            StockCodeFileReader._get_path(NETHERLAND_STOCK_FILEPATH)
        )
        spain_stock_code_list = StockCodeFileReader._read_stock_codes_from_excel(
            StockCodeFileReader._get_path(SPAIN_STOCK_FILEPATH)
        )
        switzerland_stock_code_list = StockCodeFileReader._read_stock_codes_from_excel(
            StockCodeFileReader._get_path(SWITZERLAND_STOCK_FILEPATH)
        )
        uk_stock_code_list = StockCodeFileReader._read_stock_codes_from_excel(
            StockCodeFileReader._get_path(UK_STOCK_FILEPATH)
        )
        korea_stock_code_list = StockCodeFileReader._read_stock_codes_from_excel(
            StockCodeFileReader._get_path(KOREA_STOCK_FILEPATH)
        )
        return (
            usa_stock_code_list
            + japan_stock_code_list
            + australia_stock_code_list
            + brazil_stock_code_list
            + canada_stock_code_list
            + china_stock_code_list
            + france_stock_code_list
            + germany_stock_code_list
            + hongkong_stock_code_list
            + india_stock_code_list
            + italy_stock_code_list
            + netherland_stock_code_list
            + spain_stock_code_list
            + switzerland_stock_code_list
            + uk_stock_code_list
            + korea_stock_code_list
        )

    @staticmethod
    def _read_stock_codes_from_excel(filepath: str) -> list[StockInfo]:
        try:
            df = pd.read_excel(
                filepath, usecols=["Symbol", "Company Name", "Country", "Code"], header=0, dtype={"Symbol": str}
            )
            df.columns = ["Symbol", "Company_Name", "Country", "Code"]
        except Exception as e:
            ic(f"Unexpected error: {e}")
            raise

        stock_infos = []
        for row in df.itertuples(index=False):
            try:
                stock_info = StockInfo(
                    code=str(row.Symbol),
                    name=str(row.Company_Name),
                    country=str(row.Country),
                    market_index=str(row.Code),
                )

                stock_infos.append(stock_info)
            except AttributeError as e:
                ic(f"AttributeError: {e}, row: {row}")

        return stock_infos

    @staticmethod
    def _download_file_from_s3(bucket: str, key: str, local_path: str) -> str:
        try:
            s3_client.download_file(bucket, key, local_path)
            return local_path
        except Exception as e:
            ic(f"Unexpected error: {e}")
            raise

    @staticmethod
    def _get_path(filepath) -> str:
        if ENVIRONMENT == EnvironmentType.DEV:
            return filepath
        else:
            return StockCodeFileReader._download_and_get_path(filepath)

    @staticmethod
    def _download_and_get_path(s3_key) -> str:
        local_path = f"/tmp/{os.path.basename(s3_key)}"

        StockCodeFileReader._download_file_from_s3(S3_BUCKET_STOCK_FILES, s3_key, local_path)  # type: ignore
        return local_path


# class로 전환을 마친 후 모두 삭제 하겠습니다.
def download_file_from_s3(bucket: str, key: str, local_path: str) -> str:
    try:
        s3_client.download_file(bucket, key, local_path)
        return local_path
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise


def read_stock_codes_from_excel(filepath: str) -> list[StockInfo]:
    try:
        df = pd.read_excel(
            filepath, usecols=["Symbol", "Company Name", "Country", "Code"], header=0, dtype={"Symbol": str}
        )
        df.columns = ["Symbol", "Company_Name", "Country", "Code"]
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

    stock_infos = []
    for row in df.itertuples(index=False):
        try:
            stock_info = StockInfo(
                code=str(row.Symbol),
                name=str(row.Company_Name),
                country=str(row.Country),
                market_index=str(row.Code),
            )

            stock_infos.append(stock_info)
        except AttributeError as e:
            print(f"AttributeError: {e}, row: {row}")

    return stock_infos


def get_all_stock_code_list() -> list[StockInfo]:
    usa_stock_code_list = read_stock_codes_from_excel(get_path(USA_STOCK_FILEPATH))
    japan_stock_code_list = read_stock_codes_from_excel(get_path(JAPAN_STOCK_FILEPATH))
    australia_stock_code_list = read_stock_codes_from_excel(get_path(AUSTRALIA_STOCK_FILEPATH))
    brazil_stock_code_list = read_stock_codes_from_excel(get_path(BRAZIL_STOCK_FILEPATH))
    canada_stock_code_list = read_stock_codes_from_excel(get_path(CANADA_STOCK_FILEPATH))
    china_stock_code_list = read_stock_codes_from_excel(get_path(CHINA_STOCK_FILEPATH))
    france_stock_code_list = read_stock_codes_from_excel(get_path(FRANCE_STOCK_FILEPATH))
    germany_stock_code_list = read_stock_codes_from_excel(get_path(GERMANY_STOCK_FILEPATH))
    hongkong_stock_code_list = read_stock_codes_from_excel(get_path(HONGKONG_STOCK_FILEPATH))
    india_stock_code_list = read_stock_codes_from_excel(get_path(INDIA_STOCK_FILEPATH))
    italy_stock_code_list = read_stock_codes_from_excel(get_path(ITALY_STOCK_FILEPATH))
    netherland_stock_code_list = read_stock_codes_from_excel(get_path(NETHERLAND_STOCK_FILEPATH))
    spain_stock_code_list = read_stock_codes_from_excel(get_path(SPAIN_STOCK_FILEPATH))
    switzerland_stock_code_list = read_stock_codes_from_excel(get_path(SWITZERLAND_STOCK_FILEPATH))
    uk_stock_code_list = read_stock_codes_from_excel(get_path(UK_STOCK_FILEPATH))
    korea_stock_code_list = read_stock_codes_from_excel(get_path(KOREA_STOCK_FILEPATH))
    return (
        usa_stock_code_list
        + japan_stock_code_list
        + australia_stock_code_list
        + brazil_stock_code_list
        + canada_stock_code_list
        + china_stock_code_list
        + france_stock_code_list
        + germany_stock_code_list
        + hongkong_stock_code_list
        + india_stock_code_list
        + italy_stock_code_list
        + netherland_stock_code_list
        + spain_stock_code_list
        + switzerland_stock_code_list
        + uk_stock_code_list
        + korea_stock_code_list
    )


def get_path(filepath) -> str:
    if ENVIRONMENT == EnvironmentType.DEV:
        return filepath
    else:
        return download_and_get_path(filepath)


def download_and_get_path(s3_key) -> str:
    local_path = f"/tmp/{os.path.basename(s3_key)}"

    download_file_from_s3(S3_BUCKET_STOCK_FILES, s3_key, local_path)  # type: ignore
    return local_path


# class로 전환을 마친 후 모두 삭제 하겠습니다.
