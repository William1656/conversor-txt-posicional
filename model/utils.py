import pandas as pd

EXPECTED_COLUMNS = [
    "campo", "tamanho", "alinhamento",
    "preenchimento", "obrigatorio",
    "formatacao"
]


def parse_bool(x: str, default: bool = False) -> bool:
    if x is None:
        return default
    s = str(x).strip().lower()
    if s in {"true", "t", "1", "y", "yes", "s", "sim"}:
        return True
    if s in {"false", "f", "0", "n", "no", "nao", "não"}:
        return False
    return default


def parse_allign(x: str, default: str = "left") -> str:
    if x is None:
        return default
    s = str(x).strip().lower()
    if s in {"left", "l", "esquerda", "e"}:
        return "left"
    if s in {"right", "r", "direita", "d"}:
        return "right"
    return default


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


def verify_preenchimento(row: pd.Series, i: int) -> str | None:
    error = len(row['preenchimento']) != 1
    if error:
        return f'Linha {i+1}: Preenchimento deve ter um caractere'
    return None
