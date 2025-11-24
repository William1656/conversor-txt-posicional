import pandas as pd
import model.utils as utils
import model.validators as val
import model.formatters as formatter
from model.layout import LayoutField
import os


class Model:
    sample_file_name = "layout.csv"

    def __init__(self) -> None:
        self.final_file_lines: list[str] = []
        self.layout_fields: list[LayoutField] = []

    def load_layout(self, layout_path: str) -> pd.DataFrame:
        df = pd.read_csv(
            layout_path,
            sep=None, engine="python",
            dtype=str,
            keep_default_na=False,
            encoding="utf-8-sig",
        )
        df.columns = (
            df.columns
            .str.replace("\ufeff", "", regex=False)
            .str.strip()
            .str.lower()
        )

        return df

    def validate_layout(self, df: pd.DataFrame) -> None:
        errors = []
        expected_columns = set(val.EXPECTED_COLUMNS)
        df_columns = set(df.columns)
        missing_columns = expected_columns - df_columns
        exceding_columns = df_columns - expected_columns

        errors.extend(val.verify_columns(
            missing_columns, exceding_columns))

        if errors:
            raise ValueError(
                "❌Foram encontrados erros no layout:\n" +
                "\n".join(f"- {e}" for e in errors)
            )

        for i, (_, row) in enumerate(df.iterrows(), start=1):
            tam = val.verify_tamanho(row, i)
            pre = val.verify_preenchimento(row, i)
            form = formatter.verify_formatacao(row)
            dec = val.verify_decimais(row, i)
            if tam is not None:
                errors.append(tam)
            if pre is not None:
                errors.append(pre)
            if form is not None:
                errors.extend(form)
            if dec is not None:
                errors.append(dec)

        df['obrigatorio'] = df['obrigatorio'].apply(
            lambda x: utils.parse_bool(x, default=False))

        df['novo registro'] = df['novo registro'].apply(
            lambda x: utils.parse_bool(x, default=False))

        df['alinhamento'] = df['alinhamento'].apply(
            lambda x: utils.parse_allign(x, default="left"))

        df['campo'] = df['campo'].str.strip().str.lower()

        if errors:
            raise ValueError(
                "❌Foram encontrados erros no layout:\n" +
                "\n".join(f"- {e}" for e in errors)
            )

    def set_layout_fields(self, df) -> None:
        self.layout_fields.clear()

        self.layout_fields = [
            LayoutField(row)
            for _, row in df.iterrows()
        ]

    def read_input_df(self, input_path: str) -> pd.DataFrame:
        try:
            df = pd.read_excel(input_path, dtype=str, keep_default_na=False)
            df.columns = [str(c).strip().lower() for c in df.columns]
        except Exception as e:
            raise ValueError(f"❌Erro ao ler arquivo de entrada: {e}")
        return df

    def verify_required_values(self, df: pd.DataFrame) -> list[str]:
        errors = []
        for field in self.layout_fields:
            for i, (_, row) in enumerate(df.iterrows(), start=1):
                value = row.get(field.name, "")
                if field.required and (
                        value is None or str(value).strip() == ""):
                    errors.append(
                        f"linha {i+1}"
                        f"Campo obrigatório '{field.name}' está vazio.")
        return errors

    def validate_input_df(self, df) -> None:
        errors = []
        defined_columns = [field.name for field in self.layout_fields]
        missing_fields_in_input = [
            field for field in defined_columns
            if field not in df.columns
        ]
        if missing_fields_in_input:
            errors.append(
                f"Campos faltando no arquivo de entrada: "
                f"{', '.join(missing_fields_in_input)}"
            )
        required = self.verify_required_values(df)
        if required:
            errors.extend(required)

        if errors:
            raise ValueError(
                "❌Foram encontrados erros na entrada:\n" +
                "\n".join(f"- {e}" for e in errors)
            )

    def transform_input_values(self, df) -> None:
        self.final_file_lines.clear()
        read_errors = []
        for i, (_, row) in enumerate(df.iterrows()):
            try:
                final_string = ''
                for field in self.layout_fields:
                    value = row.get(field.name, "")
                    value = formatter.apply_format_rules(
                        value, field.format_rule,
                        field.length, field.decimals)
                    value = field.format_value(value)
                    final_string += value
                self.final_file_lines.append(final_string)

            except Exception as e:
                read_errors.append(f'Linha {i+2}: {e}')
                continue
        if read_errors:
            raise ValueError(
                "❌Foram encontrados erros na entrada:\n" +
                "\n".join(f"- {e}" for e in read_errors)
            )

    def convert_to_text(self, output_path: str) -> None:
        with open(output_path, 'w', encoding='CP1252') as f:
            for i, line in enumerate(self.final_file_lines):
                f.write(line)
                if i < len(self.final_file_lines) - 1:
                    f.write('\n')

    def download_sample_layout(self, path) -> None:
        output_path = os.path.join(path, self.sample_file_name)
        capitalized_columns = [c.capitalize()
                               for c in val.EXPECTED_COLUMNS]
        sample_layout_content = ';'.join(
            capitalized_columns) + '\n'
        try:
            with open(output_path, "w", encoding="utf-8-sig") as f:
                f.write(sample_layout_content)
        except Exception as e:
            raise ValueError(f"❌Erro ao salvar layout de exemplo: {e}")
