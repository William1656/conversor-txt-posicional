# Conversor Excel → TXT posicional com Layout Personalizável

Ferramenta para converter planilhas Excel em arquivos TXT seguindo layouts configuráveis, usada em importações para ERPs, bancos e sistemas diversos.

O sistema oferece:

- Configuração de layout via CSV  
- Validação automática de erros  
- Tratamento completo de alinhamento, preenchimento, tamanhos e formatações  
- Vários tipos de formatação aplicados automaticamente  
- Quebra de registros dentro do TXT  
- Regras especiais de anulação de campos  
- Interface com download de modelo pronto  

---

## Instalação

Para instalar e executar o projeto a partir do código-fonte:

```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO

# (Opcional) Criar ambiente virtual
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux/macOS

# Instalar dependências
pip install -r requirements.txt

# Executar o aplicativo
python main.py



## Como usar

1. Abra o programa.  
2. Baixe o **modelo de layout** pela interface.  
3. Edite o CSV conforme suas necessidades.  
4. Selecione o arquivo Excel e o arquivo de layout.  
5. Clique em **Converter** para gerar o TXT.  
6. Verifique as mensagens em caso de problemas.

---

## Documentação completa do Layout

A documentação do layout está separada para facilitar a leitura:

**Aqui:** [`docs/LAYOUT.md`](docs/LAYOUT.md)

---

## Exemplo simples de uso

- Excel com colunas: `Agencia`, `Conta`, `Nome`, `Valor`  
- Layout CSV define tamanho, alinhamento e regras  
- TXT gerado segue 100% o layout especificado

---
