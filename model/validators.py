import pandas as pd

EXPECTED_COLUMNS = [
    "campo", "tamanho", "decimais", "alinhamento",
    "preenchimento", "obrigatorio",
    "formatacao", "novo registro", "anular"
]


def verify_columns(missing: set, exceding: set) -> list:
    errors = []
    if missing:
        errors.append(
            f"Colunas faltando no layout: {', '.join(missing)}"
        )

    if exceding:
        errors.append(
            f"Colunas inesperadas no layout: {', '.join(exceding)}"
        )
    return errors


def verify_tamanho(row: pd.Series, i: int) -> str | None:
    value = row.get('tamanho', '')
    if not str(value).isdigit():
        return (
            f"Linha {i+1}: 'tamanho' deve conter apenas inteiros"
            f"(recebido '{value}').")
    return None


def verify_decimais(row: pd.Series, i: int) -> str | None:
    value = row.get('decimais', '')
    if not value:
        return None
    if not str(value).isdigit():
        return (
            f"Linha {i+1}: 'decimais' deve conter apenas inteiros"
            f"(recebido '{value}').")
    return None


def verify_preenchimento(row: pd.Series, i: int) -> str | None:
    error = len(row['preenchimento']) != 1
    if error:
        return f'Linha {i+1}: Preenchimento deve ter um caractere'
    return None
