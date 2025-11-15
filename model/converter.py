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

    bad_fill = df[df["preenchimento"].map(lambda s: len(str(s)) != 1)]
    if not bad_fill.empty:
        lines = (bad_fill.index + 2).tolist()
        errors.append(
            "Valores inválidos na coluna 'preenchimento' "
            f"nas linhas: {lines}. "
            "O preenchimento deve ser um único caractere."
        )

    for i, (_, rules) in enumerate(df["formatacao"].items(), start=1):
        try:
            parse_format_rules(rules)
        except Exception as e:
            errors.append(f"Linha {i}: erro em formatacao → {e}")

    if errors:
        raise ValueError(
            "Foram encontrados erros no layout:\n" +
            "\n".join(f"- {e}" for e in errors)
        )


def read_layout(layout_path: str) -> pd.DataFrame:
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

    df['obrigatorio'] = df['obrigatorio'].apply(
        lambda x: parse_bool(x, default=False))

    df['alinhamento'] = df['alinhamento'].apply(
        lambda x: parse_allign(x, default="left"))

    df['campo'] = df['campo'].str.strip().str.lower()

    return df


class LayoutField:
    def __init__(self, row):
        self.name = row["campo"]
        self.length = int(row["tamanho"])
        self.align = row["alinhamento"]
        self.fill = row["preenchimento"]
        self.format_rules = row["formatacao"]
        self.required = row["obrigatorio"]

    def format_value(self, value: str) -> str:
        if value is None:
            value = ""
        value = str(value)

        if len(value) > self.length:
            value = value[:self.length]

        pad = self.fill * max(0, self.length - len(value))
        if self.align == "right":
            value = pad + value
        else:
            value = value + pad
        return value


def read_input_df(input_path: str) -> pd.DataFrame:
    try:
        df = pd.read_excel(input_path, dtype=str, keep_default_na=False)
        df.columns = [str(c).strip().lower() for c in df.columns]
        return df
    except Exception as e:
        raise ValueError(f"Erro ao ler arquivo de entrada: {e}")


def verify_required_values(field: LayoutField, value: str) -> None:
    if field.required and (value is None or str(value).strip() == ""):
        raise ValueError(f"Campo obrigatório '{field.name}' está vazio.")


def transform_input_values(
        input_path: str, layout_path: str, output_path: str) -> list:
    input_df = read_input_df(input_path)
    layout_df = read_layout(layout_path)

    layout_rows = [LayoutField(row) for _, row in layout_df.iterrows()]
    layout_defined_fields = [field.name for field in layout_rows]
    missing_fields_in_input = [
        field for field in layout_defined_fields
        if field not in input_df.columns
    ]

    if missing_fields_in_input:
        raise ValueError(
            f"Campos faltando no arquivo de entrada: "
            f"{', '.join(missing_fields_in_input)}"
        )
    final_file_lines = []
    read_errors = []

    for i, (_, row) in enumerate(input_df.iterrows()):
        try:
            final_file_string = ''
            for field in layout_rows:
                cell_value = row.get(field.name, "")
                cell_value = apply_format_rules(
                    cell_value, parse_format_rules(field.format_rules))
                try:
                    verify_required_values(field, cell_value)
                except ValueError as ve:
                    read_errors.append(f'Linha {i + 2}: {ve}')

                cell_value = field.format_value(cell_value)
                final_file_string += cell_value

            final_file_lines.append(final_file_string)

        except Exception as e:
            read_errors.append(f'Linha {i}: {e}')
            continue

    if read_errors:
        raise ValueError(
            "Foram encontrados erros ao processar o arquivo de entrada:\n" +
            "\n".join(f"- {e}" for e in read_errors)
        )
    return final_file_lines


def convert_to_positional_text(
        input_path: str, layout_path: str, output_path: str) -> None:
    lines = transform_input_values(input_path, layout_path, output_path)
    with open(output_path, 'w', encoding='CP1252') as f:
        for i, line in enumerate(lines):
            f.write(line)
            if i < len(lines) - 1:
                f.write('\n')


if __name__ == '__main__':
    path1 = 'entrada_teste.xlsx'
    path2 = 'model/layoutFornecedores.csv'
    convert_to_positional_text(path1, path2, 'saida.txt')
