class LayoutField:
    def __init__(self, row):
        self.name = row["campo"]
        self.length = int(row["tamanho"])
        self.align = row["alinhamento"]
        self.fill = row["preenchimento"]
        self.format_rule = row["formatacao"]
        self.required = row["obrigatorio"]
        self.new_line = row["novo registro"]
        self.decimals = row["decimais"]
        self.null_char = row["anular"]

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
        if self.new_line:
            value = '\n' + value
        return value
