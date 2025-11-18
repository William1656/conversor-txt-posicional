class LayoutField:
    def __init__(self, row):
        self.name = row["campo"]
        self.length = int(row["tamanho"])
        self.align = row["alinhamento"]
        self.fill = row["preenchimento"]
        self.format_rule = row["formatacao"]
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
