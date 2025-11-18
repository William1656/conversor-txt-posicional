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
    if s in {"left", "l", "esquerda"}:
        return "left"
    if s in {"right", "r", "direita"}:
        return "right"
    return default


def normalize_column_name(df: pd.DataFrame) -> None:
    df.columns = (
        df.columns
        .str.replace("\ufeff", "", regex=False)
        .str.strip()
        .str.lower()
    )


def normalize_layout(self) -> None:
    if self.layoutdf is None:
        raise ValueError("Layout não carregado.")

    if self.validated_layout:
        self.normalize_column_name(self.layoutdf)

        self.layoutdf['obrigatorio'] = self.layoutdf['obrigatorio'].apply(
            lambda x: self.parse_bool(x, default=False))

        self.layoutdf['alinhamento'] = self.layoutdf['alinhamento'].apply(
            lambda x: self.parse_allign(x, default="left"))

        self.layoutdf['campo'] = self.layoutdf['campo'].str.strip(
        ).str.lower()
    else:
        raise ValueError("Layout não validado.")


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


def verify_tamanho(df: pd.DataFrame) -> list:
    errors = []
    for i, (_, value) in enumerate(df["tamanho"].items(), start=1):
        if not str(value).isdigit():
            errors.append(
                f"Linha {i+1}: 'tamanho' deve conter apenas inteiros"
                f"(recebido '{value}').")
    return errors


def verify_preenchimento(df: pd.DataFrame) -> list:
    errors = []

    df["preenchimento"] = df["preenchimento"].apply(
        lambda x: " " if x is None or str(x).strip() == "" else str(x)
    )
    errors_lines = df.index[df["preenchimento"].astype(
        str).str.len() != 1].tolist()

    for i in errors_lines:
        errors.append(
            f"Linha {i+2}: 'preenchimento' "
            "deve ter apenas um caractere")
    return errors
