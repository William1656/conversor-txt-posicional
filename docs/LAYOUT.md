# Layout de Conversão (layout.csv)

Este documento descreve o funcionamento do arquivo **layout.csv**, utilizado pelo conversor para gerar arquivos TXT estruturados a partir de planilhas Excel.

Cada linha do layout representa **um campo** que será processado, formatado e inserido no arquivo final.

---

# Colunas do Layout

A tabela abaixo descreve cada coluna existente no layout e seu propósito.

| Coluna           | Descrição |
|------------------|-----------|
| **Campo**        | Nome do campo (identificação). |
| **Tamanho**      | Número total de caracteres do campo no arquivo final. |
| **Decimais**     | Quantidade de casas decimais incluídas dentro do tamanho total. Usado geralmente com valores monetários. |
| **Alinhamento**  | `D` = Direita, `E` = Esquerda — posicionamento do valor. |
| **Preenchimento**| Caractere utilizado para preencher espaços restantes. |
| **Obrigatorio**  | `S` ou `N` — exige que o campo tenha valor. |
| **Formatacao**   | Código numérico que ativa uma regra automática (lista abaixo). |
| **Novo registro**| `S` ou `N` — força a quebra de linha no TXT. |
| **Anular**       | Caractere que, se presente no Excel, faz o campo ser ignorado. |

---
Regra geral:

Depois disso o valor é ajustado para o **Tamanho** total com alinhamento e preenchimento definidos.

A coluna Decimais é **especialmente importante quando usada com Formatação 3 (format_as_money)** e com **Formatacao 4 (zero_as_blank)**.

---

# Regras de Formatação (Formatacao)

A coluna **Formatacao** recebe um número que ativa regras automáticas no valor.
Formatações podem ser combinadas sendo separadas por ";".

```python
FORMATTERS = {
    "1": only_digits,
    "2": remove_accents,
    "3": format_as_money,
    "4": zero_as_blank
}
```
## **1 - Apenas números**

Usado para remover qualquer caractere que não seja número

Exemplo: `"CPF 123.456-78"` → `"12345678"`

## **2 - Remover caracteres especiais**
Remove acentos, símbolos e caracteres não ASCII.  
Exemplo: `"AÇÃO"` → `"ACAO"`

## **3 - Numericos com decimais**
Funciona em conjunto com a coluna **Decimais**:

- Remove vírgula ou ponto do número.
- EXIGE que o campo seja preenchido com valores numericos

Exemplo:  
- Tamanho = 10  
- Decimais = 2  
- Valor = `45,70`  
→ `"000004570"`

## **4 - Zero como nulo**
Alguns sistemas não aceitam campos com zeros; precisam vir como **espaços em branco**.  
Esse formatter transforma zeros em espaços após o processamento.

- EXIGE que o campo seja preenchido com valores numericos 

Exemplo:

| Valor Original | Após Regras | Após `zero_as_blank` |
|----------------|-------------|------------------------|
| `00000`        | `00000`     | `     `               |

Esse comportamento facilita integrações com sistemas bancários e ERPs mais antigos.

# Sobre a coluna **Decimais**

A coluna **Decimais** indica quantas casas decimais devem ser usadas dentro do valor final.

Exemplos práticos:

| Tamanho | Decimais | Valor Excel | Valor Final |
|---------|----------|-------------|--------------|
| 10      | 2        | 123,45      | `0000123450` |
| 8       | 3        | 1,234       | `0012340`    |
| 12      | 2        | 0           | `000000000000` *(a menos que Formatacao = 4)* |

# Coluna **Anular**

Esta coluna define um **caractere de anulação**.

Se o software encontrar esse caractere no valor do campo **ele ignora completamente o valor**, como se fosse vazio.

Exemplos:

| Valor recebido | Anular | Resultado |
|----------------|--------|-----------|
| `*` | `*` | (campo removido) |
| `NULL` | `N` | `NULL` |
| `-` | `-` | (campo removido) |

---

# Exemplo Completo de layout.csv

Abaixo um exemplo ilustrativo de como deve ficar um layout real:


| Campo     | Tamanho | Decimais | Alinhamento | Preenchimento | Obrigatorio | Formatacao | Novo Registro | Anular |
|-----------|---------|----------|-------------|----------------|-------------|------------|---------------|--------|
| Codigo    | 10      |         | D           | 0              | S           | 2          | N             |        |
| Nome      | 40      |         | E           | (espaço)       | S           | 1          | N             |        |
| Valor     | 12      | 2        | D           | 0              | S           | 4          | N             |        |
| Descricao | 50      |         | E           | (espaço)       | N           | 3          | S             |        |
| Cancelado | 1       |         | E           | (espaço)       | N           |           | N             | *      |


# Fluxo Simplificado

O sistema lê o layout linha por linha.

Para cada linha:

-Lê o valor correspondente no Excel

-Verifica "Obrigatorio"

-Aplica "Anular"

-Aplica Formatacao (se houver)

-Ajusta tamanho, alinhamento e preenchimento

-Se "Novo registro = S", quebra a linha antes daquele campo

-Gera o campo final com tamanho fixo



# Como Testar o Layout Antes de Usar

1. Crie ou edite o arquivo `layout.csv`.

2. Abra o programa e carregue esse layout.

3. Utilize a função **"Baixar Modelo"** para gerar um Excel já no formato correto.

4. Preencha o Excel com valores reais.

5. Clique em **Converter** e verifique se o TXT final respeita:
   - Tamanho dos campos
   - Alinhamento
   - Preenchimento
   - Regras de formatação
   - Quebra de linha (Novo Registro)
