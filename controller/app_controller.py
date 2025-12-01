from view.view import MainView
from model.model import Model


class Controller:
    def __init__(self) -> None:
        self.view = MainView(controller=self)
        self.model = Model()
        self.layout_path = ''
        self.input_path = ''
        self.output_path = ''

    def _has_paths(self) -> bool:
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

    def convert_file(self, num: str) -> None:
        if self._has_paths():
            try:
                layout_df = self.model.load_layout(self.layout_path)
                input_df = self.model.read_input_df(self.input_path)
                self.model.validate_layout(layout_df)
                self.model.set_layout_fields(layout_df)
                self.model.validate_input_df(input_df)
                self.model.transform_input_values(input_df)
                self.model.set_num_files(num)
                self.model.convert_to_text(self.output_path)
                self.view.show_message('Conversão realizada com sucesso!')
            except Exception as e:
                self.view.show_error(f'{e}')

    def download_sample_layout(self, path: str) -> None:
        try:
            self.model.download_sample_layout(path)
            self.view.show_message('Arquivo exemplo salvo com sucesso!')
        except Exception as e:
            self.view.show_error(f'Erro ao baixar layout exemplo: {e}')

    def set_layout_path(self, path: str) -> None:
        self.layout_path = path

    def set_input_path(self, path: str) -> None:
        self.input_path = path

    def set_output_path(self, path: str) -> None:
        self.output_path = path

    def run(self) -> None:
        self.view.mainloop()
