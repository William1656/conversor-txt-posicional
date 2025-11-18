import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from assets_manager import load_icon


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class MainView(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Conversor TXT posicional")
        self.geometry("650x400")
        self.setup_ui()

    def setup_ui(self):
        self.title_label = ctk.CTkLabel(
            self, text="Conversor TXT posicional", font=ctk.CTkFont(
                size=28, weight="bold"), text_color="#FFFFFF")
        self.title_label.grid(row=0, column=0, columnspan=3, pady=(20, 10))

        self.input_entry = ctk.CTkEntry(
            self, width=500, placeholder_text="Caminho do arquivo de entrada",
            height=40)
        self.input_entry.grid(row=1, column=0, padx=(20, 10), pady=10)
        self.input_browse_button = ctk.CTkButton(
            self, text="Arquivo", width=100, height=40,
            command=self.select_input_file)
        self.input_browse_button.grid(row=1, column=1, pady=10)

        self.layout_entry = ctk.CTkEntry(
            self, width=500, placeholder_text="Caminho do arquivo de layout",
            height=40)
        self.layout_entry.grid(row=2, column=0, padx=(20, 10), pady=10)
        self.layout_browse_button = ctk.CTkButton(
            self, text="Arquivo", width=100, height=40,
            command=self.select_layout_file)
        self.layout_browse_button.grid(row=2, column=1, pady=10)

        self.output_entry = ctk.CTkEntry(
            self, width=500, placeholder_text="Salvar arquivo de saída em",
            height=40)
        self.output_entry.grid(row=3, column=0, padx=(20, 10), pady=10)
        self.output_browse_button = ctk.CTkButton(
            self, text="Arquivo", width=100, height=40,
            command=self.select_output_file)
        self.output_browse_button.grid(row=3, column=1, pady=10)

        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=4, column=0, columnspan=3, pady=20)

        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.columnconfigure(2, weight=1)

        self.download_button = ctk.CTkButton(
            self.button_frame, text="",
            fg_color="transparent", text_color="#000000", width=35,
            height=35, image=load_icon('download.png'), compound="left",
            command=self.download_sample_layout)
        self.download_button.grid(row=0, column=0, padx=10)

        self.convert_button = ctk.CTkButton(
            self.button_frame, text="", fg_color="transparent", width=35,
            height=35, text_color="#000000", image=load_icon('convert.png'),
            compound="left", command=self.convert_file)
        self.convert_button.grid(row=0, column=1, padx=10)

        self.help_button = ctk.CTkButton(
            self.button_frame, text="", fg_color="transparent", width=35,
            height=35, text_color="#000000", image=load_icon('help.png'),
            compound="left", command=self.help_info)
        self.help_button.grid(row=0, column=2, padx=10)

    def select_input_file(self) -> None:
        file_path = ctk.filedialog.askopenfilename(
            title="Selecione o arquivo de entrada",
            filetypes=[
                ("Excel Files", "*.xlsx"),
                ("Excel 97-2003", "*.xls"),
                ("Todos os arquivos", "*.*")
            ]
        )
        if file_path:
            self.input_entry.delete(0, ctk.END)
            self.input_entry.insert(0, file_path)
            self.controller.set_input_path(file_path)

    def select_layout_file(self) -> None:
        file_path = ctk.filedialog.askopenfilename(
            title="Selecione o arquivo de layout",
            filetypes=[("CSV Files", "*.csv"), ("Todos os arquivos", "*.*")]
        )
        if file_path:
            self.layout_entry.delete(0, ctk.END)
            self.layout_entry.insert(0, file_path)
            self.controller.set_layout_path(file_path)

    def select_output_file(self) -> None:
        file_path = ctk.filedialog.asksaveasfilename(
            title="Salvar arquivo de saída como",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("Todos os arquivos", "*.*")]
        )
        if file_path:
            self.output_entry.delete(0, ctk.END)
            self.output_entry.insert(0, file_path)
            self.controller.set_output_path(file_path)

    def download_sample_layout(self) -> None:
        folder_path = ctk.filedialog.askdirectory(
            title="Selecione a pasta para salvar o layout de exemplo"
        )
        if folder_path:
            self.controller.download_sample_layout(folder_path)

    def convert_file(self) -> None:
        self.controller.convert_file()

    def help_info(self) -> None:
        help_message = (
            "Instruções de uso:\n\n"
            "1. Selecione o arquivo de entrada (Excel .xlsx ou .xls).\n"
            "2. Selecione o arquivo de layout (CSV).\n"
            "3. Escolha onde salvar o arquivo de saída (.txt).\n"
            "4. Clique no ícone de conversão para iniciar o processo.\n\n"
            "Para baixar um layout de exemplo, clique no ícone de download."
        )
        CTkMessagebox(title="Ajuda", message=help_message, icon="info")

    def show_error(self, msg):
        CTkMessagebox(title="Erro", message=msg,
                      icon="cancel", height=300, width=1000)

    def show_message(self, msg):
        CTkMessagebox(title="Mensagem", message=msg, icon="check")


if __name__ == "__main__":
    app = MainView(None)
    app.mainloop()
