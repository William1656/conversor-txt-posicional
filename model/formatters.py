import pandas as pd
import re
import unicodedata


def zero_as_blank(value: str, length: int) -> str:
    value = value.replace(",", ".")
    try:
        value_float = float(value)
    except Exception:
        raise ValueError('Não foi possivel aplicar a formatacao "4"\n'
                         ''f'"{value}" não é um numero')
    if value_float == 0:
        return ' '*length
    return value


def format_as_money(value: str, decimals: int = 2) -> str:
    value = value.replace(",", ".")
    try:
        value_float = float(value)
    except Exception:
        raise ValueError('Não foi possivel aplicar a formatacao "3"\n'
                         ''f'"{value}" não é um numero')
    fator = 10 ** decimals
    return str(round(value_float * fator))


def only_digits(value: str) -> str:
    return re.sub(r"\D", "", value or "")


def remove_accents(value: str) -> str:
    if value is None:
        return ""
    nfkd = unicodedata.normalize('NFKD', value)
    return "".join([c for c in nfkd if not unicodedata.combining(c)]).upper()


FORMATTERS = {
    "1": only_digits,
    "2": remove_accents,
    "3": format_as_money,
    "4": zero_as_blank
}


def apply_format_rules(value: str, codes: list[str], length: int) -> str:
    for code in codes:
        formatter = FORMATTERS.get(code)
        if formatter:
            if formatter == zero_as_blank:
                value = formatter(value, length)
            else:
                value = formatter(value)
    return value


def verify_formatacao(row: pd.Series) -> list | None:
    errors = []
    splited = str(row['formatacao']).split(';')
    for value in splited:
        if not value:
            continue
        if value not in FORMATTERS:
            errors.append((f' Formatação "{value}" não existe \n'
                           'Use números separados por ";"\n'
                           f'Regras disponiveis: {list(FORMATTERS.keys())}'))
    if errors:
        return errors
    return None
