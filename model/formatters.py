import pandas as pd
import re
import unicodedata


def only_digits(value: str) -> str:
    return re.sub(r"\D", "", value or "")


def remove_accents(value: str) -> str:
    if value is None:
        return ""
    nfkd = unicodedata.normalize('NFKD', value)
    return "".join([c for c in nfkd if not unicodedata.combining(c)])


FORMATTERS = {
    "1": only_digits,
    "2": remove_accents
}


def apply_format_rules(value: str, code: int) -> str:
    formatter = FORMATTERS.get(code)
    if formatter:
        value = formatter(value)
    return value


def verify_formatacao(df: pd.DataFrame) -> list:
    errors = []
    for i, (_, row) in enumerate(df.iterrows(), start=1):
        try:
            value = row['formatacao']
            if not value:
                continue
            if not value in FORMATTERS:
                raise ValueError
        except Exception:
            errors.append((f'Linha {i+1}: formatação "{value}" não existe \n'
                           f'Regras disponiveis: {list(FORMATTERS.keys())}'))
    return errors
