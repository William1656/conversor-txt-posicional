import pandas as pd
import re
import unicodedata


def format_as_money(value: str, decimals: int = 2) -> int:
    value = value.replace(",", ".")
    try:
        value_float = float(value)
    except Exception:
        raise ValueError('Não foi possivel aplicar a formatacao "3"\n'
                         ''f'"{value}" não é um numero')
    fator = 10 ** decimals
    return int(round(value_float * fator))


def only_digits(value: str) -> str:
    return re.sub(r"\D", "", value or "")


def remove_accents(value: str) -> str:
    if value is None:
        return ""
    nfkd = unicodedata.normalize('NFKD', value)
    return "".join([c for c in nfkd if not unicodedata.combining(c)])


FORMATTERS = {
    "1": only_digits,
    "2": remove_accents,
    "3": format_as_money
}


def apply_format_rules(value: str, code: str) -> str:
    formatter = FORMATTERS.get(code)
    if formatter:
        value = formatter(value)
    return value


def verify_formatacao(row: pd.Series) -> str | None:
    value = str(row['formatacao'])
    if not value:
        return None
    if value not in FORMATTERS:
        return ((f' formatação "{value}" não existe \n'
                 f'Regras disponiveis: {list(FORMATTERS.keys())}'))
    return None
