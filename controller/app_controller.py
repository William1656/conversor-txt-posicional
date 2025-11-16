from model.converter import convert_to_positional_text, EXPECTED_COLUMNS
import os


class Controller:
    def __init__(self, view) -> None:
        self.view = view
        self.layout_path = ''
        self.input_path = ''
        self.output_path = ''

    def has_paths(self) -> bool:
        errors = []
        if not self.layout_path:
            errors.append("Caminho do layout não foi definido.")
        if not self.input_path:
            errors.append("Caminho do arquivo de entrada não foi definido.")
        if not self.output_path:
            errors.append("Caminho do arquivo de saída não foi definido.")
        if errors:
            self.view.show_error("\n".join(errors))
            return False
        return True

    def convert_file(self) -> None:
        if self.has_paths():
            try:
                convert_to_positional_text(
                    self.input_path, self.layout_path, self.output_path)
                self.view.show_message("Conversão concluída com sucesso!")
            except Exception as e:
                self.view.show_error(f"Erro durante a conversão: {e}")

    def exit_application(self) -> None:
        self.view.close()

    def download_sample_layout(self, path) -> None:
        file_name = "layout.csv"
        output_path = os.path.join(path, file_name)
        sample_layout_content = ','.join(EXPECTED_COLUMNS).capitalize() + '\n'
        try:
            with open(output_path, "w", encoding="utf-8-sig") as f:
                f.write(sample_layout_content)
            self.view.show_message(
                "Layout de exemplo 'layout.csv' foi salvo com sucesso.")
        except Exception as e:
            self.view.show_error(f"Erro ao salvar layout de exemplo: {e}")

    def set_layout_path(self, path: str) -> None:
        self.layout_path = path

    def set_input_path(self, path: str) -> None:
        self.input_path = path

    def set_output_path(self, path: str) -> None:
        self.output_path = path


if __name__ == '__main__':
    ...
