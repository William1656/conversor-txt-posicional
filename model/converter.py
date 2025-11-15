import pandas as pd
import unicodedata
import re


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


def only_digits(value: str) -> str:
    return re.sub(r"\D", "", value or "")


def remove_accents(value: str) -> str:
    if value is None:
        return ""
    nfkd = unicodedata.normalize('NFKD', value)
    return "".join([c for c in nfkd if not unicodedata.combining(c)])


FORMATTERS = {
    1: only_digits,
    2: remove_accents
}


def parse_format_rules(rules_str: str) -> list:
    if rules_str is None or rules_str.strip() == "":
        return []
    parts = [part.strip() for part in rules_str.split(";")]
    formatters = []
    for part in parts:
        if not part.isdigit():
            raise ValueError(
                f"Valor inválido em format_rules: '{part}'. "
                "Use apenas números separados por ';'."
            )
        num = int(part)
        if num not in FORMATTERS:
            raise ValueError(
                f"Regra de formatação desconhecida: '{num}'. "
                f"Regras disponíveis: {list(FORMATTERS.keys())}"
            )
        formatters.append(num)
    return formatters


def apply_format_rules(value: str, codes: list[int]) -> str:
    for code in codes:
        formatter = FORMATTERS.get(code)
        if formatter:
            value = formatter(value)
    return value


def validate_layout_df(df: pd.DataFrame) -> None:
    errors = []
    expected_columns = {
        "campo", "tamanho", "formatacao",
        "alinhamento",	"preenchimento",
        "obrigatorio"
    }
    df_columns = set(df.columns)
    missing_columns = expected_columns - df_columns
    exceding_columns = df_columns - expected_columns
    if missing_columns:
        errors.append(
            f"Colunas faltando no layout: {', '.join(missing_columns)}"
        )
    if exceding_columns:
        errors.append(
            f"Colunas inesperadas no layout: {', '.join(exceding_columns)}"
        )

    for i, (_, value) in enumerate(df["tamanho"].items(), start=1):
        if not str(value).isdigit():
            errors.append(
                f"Linha {i}: 'tamanho' deve conter apenas inteiros"
                f"(recebido '{value}').")

    valid_align = {"left", "right"}
    for i, (_, value) in enumerate(df["alinhamento"].items(), start=1):
        v = str(value).strip().lower()
        if v not in valid_align:
            errors.append(
                f"Linha {i}: align inválido '{value}'. Use: left, right.")

    bad_fill = df[df["preenchimento"].map(lambda s: len(str(s)) != 1)]
    if not bad_fill.empty:
        lines = (bad_fill.index + 2).tolist()
        errors.append(
            "Valores inválidos na coluna 'preenchimento' "
            f"nas linhas: {lines}. "
            "O preenchimento deve ser um único caractere."
        )

    for i, (_, rules) in enumerate(df["formatacao"].items()):
        try:
            parse_format_rules(rules)
        except Exception as e:
            errors.append(f"Linha {i}: erro em formatacao → {e}")

    if errors:
        raise ValueError(
            "Foram encontrados erros no layout:\n" +
            "\n".join(f"- {e}" for e in errors)
        )


def read_layout(layout_path: str) -> tuple[pd.DataFrame, int]:
    df = pd.read_csv(
        layout_path,
        sep=None, engine="python",
        dtype=str,
        keep_default_na=False,
        encoding="utf-8-sig"
    )
    df.columns = (
        df.columns
        .str.replace("\ufeff", "", regex=False)
        .str.strip()
        .str.lower()
    )
    validate_layout_df(df)

    df['obrigatorio'] = df['obrigatorio'].apply(
        lambda x: parse_bool(x, default=False))

    df['alinhamento'] = df['alinhamento'].apply(
        lambda x: parse_allign(x, default="left"))

    return df, df["tamanho"].sum()


if __name__ == '__main__':
    df, record_length = read_layout('model/layoutFornecedores.csv')
