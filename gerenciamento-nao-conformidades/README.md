# Gerenciamento de Não Conformidades

Aplicação em Python para o gerenciamento de não conformidades, com interface gráfica simples em **português brasileiro**. Permite visualizar, editar, excluir e clonar registros de não conformidades.

## Estrutura do Projeto

```bash
gerenciamento-nao-conformidades/
├── src/
│   ├── main.py
│   ├── gui/
│   │   └── interface.py
│   ├── models/
│   │   └── registro.py
│   ├── controllers/
│   │   └── registro_controller.py
│   └── utils/
│       └── helpers.py
├── requirements.txt
└── README.md
```

## Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/gerenciamento-nao-conformidades.git
   cd gerenciamento-nao-conformidades
   ```

2. **Crie um ambiente virtual (opcional, mas recomendado):**
   ```bash
   python -m venv venv
   # Ative no Windows:
   venv\Scripts\activate
   # Ou no Linux/Mac:
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

## Execução

Para iniciar a aplicação, execute:

```bash
python src/main.py
```

## Funcionalidades

- **Visualização:** Tabela com NÚMERO DE REGISTRO, DATA DE ABERTURA, RESUMO DA NÃO CONFORMIDADE e STATUS.
- **Detalhamento/Edição:** Clique no NÚMERO DE REGISTRO para ver todos os detalhes e editar todos os campos, exceto o NÚMERO DE REGISTRO (único e sequencial).
- **Exclusão:** Remova registros indesejados.
- **Clonagem:** Duplique registros facilmente.

## Exemplo de Uso

1. Abra o terminal e execute o comando de execução.
2. Na tela principal, visualize todas as não conformidades.
3. Clique no NÚMERO DE REGISTRO para detalhar, editar, excluir ou clonar.

## Contribuição

Contribuições são bem-vindas! Abra uma *issue* ou envie um *pull request*.

---

**Desenvolvido em Python 3.8+**