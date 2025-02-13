import pandas as pd
from fastapi import FastAPI, Header, Security
from fastapi.security import APIKeyHeader
from typing import Annotated


def verify_header(access_token=Security(APIKeyHeader(name="access-token"))):
    return access_token


def to_dict_data(data: pd.DataFrame) -> pd.DataFrame:
    try:
        data = data.transpose()
        data.rename(columns=data.iloc[0], inplace=True)
        data = data.drop(data.index[0])

        return data
    except Exception:
        print(FileNotFoundError)


def sort_value_use_key(data, column) -> pd.DataFrame:
    df = pd.DataFrame(data)
    df = df.sort_values(column)
    return df
