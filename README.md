# Painel de Gerenciamento de Não Conformidades (NCs)

[](https://www.python.org/)
[](https://docs.python.org/3/library/tkinter.html)
[](https://matplotlib.org/)
[](https://www.google.com/search?q=LICENSE)

## 🌟 Visão Geral

O **Painel de Gerenciamento de Não Conformidades (NCs)** é uma ferramenta intuitiva e prática desenvolvida em Python para simplificar o registro, a visualização e a análise de não conformidades em diversos contextos (industrial, controle de qualidade, etc.). A ferramenta oferece uma interface gráfica amigável, armazenamento persistente de dados e recursos de visualização para uma gestão eficiente dos desvios.

Este projeto nasce como avaliação prática supervisionada (APS) da disciplina de Lógica de Programação, da turma de Engenharia de Produção do centro universitário Unifametro, ministrada pelo Profº Msc Kaio Mesquita, aplicando conceitos fundamentais de programação de forma aplicada: desde a lógica algorítmica e estruturas de controle de fluxo, até a manipulação eficiente de dados e a criação de interfaces gráficas.

### Por que este projeto?

Em muitos cenários, o controle de não conformidades ainda é feito de forma manual ou em planilhas que, com o tempo, se tornam difíceis de gerenciar e analisar. Nosso painel propõe uma solução centralizada que:

  * **Padroniza o registro**: Garante que todas as informações relevantes sejam capturadas.
  * **Centraliza os dados**: Facilita o acesso e a consulta por toda a equipe.
  * **Oferece visualização clara**: Permite identificar tendências e problemas rapidamente.
  * **É configurável**: Adapta-se a diferentes contextos e tipos de não conformidades.

## 🚀 Guia Rápido: Primeiros Passos

Siga estes passos simples para ter o Painel de NCs rodando em sua máquina.

### Pré-requisitos

Certifique-se de ter o **Python 3.x** instalado. Você pode baixá-lo em [python.org](https://www.python.org/downloads/).

Em seguida, instale as bibliotecas Python necessárias:

```bash
pip install tkcalendar matplotlib
```

### Instalação e Execução

1.  **Clone o Repositório**:

    ```bash
    git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git # Substitua pela URL do seu projeto
    cd SEU_REPOSITORIO # Navegue até a pasta do projeto
    ```

2.  **Preparação dos Arquivos de Dados**:
    O sistema armazena suas configurações e registros de NCs em arquivos JSON: `config.json` e `ncs.json`.

      * **Na primeira execução**, o programa criará `config.json` com configurações padrão e `ncs.json` vazio.
      * **Para popular com dados de exemplo**: Você pode adicionar o conteúdo de exemplo fornecido na seção de "Exemplos de Dados" diretamente em `ncs.json`.

3.  **Execute a Aplicação**:

    ```bash
    python App-v2.py
    ```

    A janela principal do "Painel de Gerenciamento de Não Conformidades" será exibida.

## 🛠️ Como Usar

O aplicativo é dividido em seções para facilitar o gerenciamento:

### 1\. Menu Principal

Esta é a tela de boas-vindas. Nela, você pode:

  * **PAINEL DE NÃO CONFORMIDADES**: Acesse a área principal de gerenciamento das NCs.
  * **CONFIGURAÇÕES**: Personalize as opções do sistema (unidades, defeitos, produtos).
  * **SOBRE**: Obtenha informações sobre a aplicação e a versão.
  * **SAIR DO PROGRAMA**: Feche o aplicativo.

<p align="center">
  <img src="https://github.com/user-attachments/assets/12cbec63-af60-40a7-98ed-ff0682c9ac83" alt="Menu Principal" width="600"/>
  <br>
  <em>(Exemplo do menu principal)</em>
</p>

### 2\. Painel de Não Conformidades

A tela central onde você visualiza e interage com os registros.

  * **Tabela de NCs**: Todos os registros são listados aqui. As linhas são coloridas para destacar o tipo de defeito (cores configuráveis\!).
  * **Botões de Ação**:
      * **REGISTRAR NOVA**: Abre um formulário para inserir uma nova NC.
      * **EDITAR**: Edita a NC selecionada na tabela.
      * **EXCLUIR**: Remove a NC selecionada.
      * **VOLTAR**: Retorna ao Menu Principal.
      * **EXCLUIR TUDO**: Remove *todos* os registros (com confirmação).
      * **GRÁFICO POR DEFEITO**: Gera um gráfico de barras mostrando a distribuição dos defeitos.
      * **GRÁFICO POR STATUS**: Gera um gráfico de pizza com o status atual das NCs.

<p align="center">
  <img src="https://github.com/user-attachments/assets/1ec30429-08bf-411d-9c59-dfc93697e8c5" alt="Formulário de Registro/Edição de NC" width="500"/>
  <br>
  <em>(Tela de criação e edição das não conformidades)</em>
</p>

### 3\. Formulário de Registro/Edição

A janela para inserir ou modificar detalhes de uma NC.

  * **Campos de Preenchimento**: `Data da Ocorrência`, `Produto` (com código automático), `Total Reprovado`, `Unidade de Medida`, `Defeito`, `Descrição` (com contador de caracteres), `Data de Produção`, `Ação Imediata` e `Responsável pela Ação`.
  * **Validação**: O sistema verifica se campos essenciais estão preenchidos corretamente (ex: `Total Reprovado` deve ser um número, `Descrição` tem limite de 400 caracteres).
  * **Salvar/Cancelar**: Botões para finalizar ou abortar a operação.

### 4\. Configurações

Gerencie as listas que o sistema usa.

  * **Unidades de Medida**: Adicione, modifique ou remova unidades.
  * **Defeitos**: Adicione, modifique ou remova tipos de defeitos.
  * **Produtos**: Adicione, modifique ou remova produtos, cada um com seu nome e código.
  * **Salvar Configurações**: Lembre-se de salvar suas alterações para que elas persistam.

<p align="center">
  <img src="https://github.com/user-attachments/assets/a741e6c2-edc8-423a-b338-1755940cd8d1" alt="Configurações" width="600"/>
  <br>
  <em>(Tela de modificação dos parâmetros internos)</em>
</p>

### 5\. Gráficos de Análise

Visualize os dados de suas não conformidades de forma gráfica.

  * **Gráfico por Defeito**: Mostra quais defeitos são mais frequentes.
  * **Gráfico por Status**: Exibe a proporção de NCs abertas, fechadas, etc.

<p align="center">
  <img src="https://github.com/user-attachments/assets/11428c7d-6c0a-49bb-9e33-025ce53191f4" alt="Gráfico de Exemplo" width="400"/>
  <br>
  <em>(Gráficos de exemplo)</em>
</p>

## ⚙️ Arquivos de Dados (JSON)

Os dados da aplicação são armazenados em dois arquivos JSON na mesma pasta do `App-v2.py`:

  * **`ncs.json`**: Contém uma lista de objetos, onde cada objeto representa uma não conformidade registrada.

    ```json
    [
      {
        "numero_registro": "2025-0001",
        "data_ocorrencia": "01/01/2025",
        "codigo_produto": "0001X0001",
        "produto": "PRODUTO INTERNO",
        "total_reprovado": 50,
        "unidade": "KG",
        "defeito": "ASPECTO DO PRODUTO OU MP",
        "descricao": "PRODUTO COM COLORAÇÃO IRREGULAR, DIFERENTE DO PADRÃO ESTABELECIDO.",
        "descricao_resumida": "PRODUTO COM COLORAÇÃO IRREGULAR, DIFE...",
        "data_producao": "30/12/2024",
        "acao_imediata": "RETRABALHAR",
        "responsavel_acao": "João Silva",
        "status": "Aberta"
      },
      // ... mais registros
    ]
    ```

  * **`config.json`**: Armazena as configurações globais da aplicação, incluindo as listas personalizáveis e o mapeamento de cores para os defeitos.

    ```json
    {
      "unidades": [
        "KG",
        "L",
        "PEÇ",
        "TON",
        "ROL",
        "BD"
      ],
      "defeitos": [
        "Aspecto do produto ou MP",
        "Avarias em baldes",
        "Avarias em caixas",
        "Avarias em latas",
        "Avarias em sacarias Transferência",
        "Avarias no strech",
        "Consistência na mistura",
        "Contaminação",
        "Cor despadronizada",
        "Desempenho pós cura",
        "Desvio de peso ou quantidade",
        "Embalagem com defeito Fornecedor",
        "Falha de informação do datador"
      ],
      "cores_defeitos": {
        "ASPECTO DO PRODUTO OU MP": "#FFB6B6",
        "AVARIAS EM BALDES": "#FFD580",
        "AVARIAS EM CAIXAS": "#FFFACD",
        "AVARIAS EM LATAS": "#B6FFB6",
        "AVARIAS EM SACARIAS TRANSFERÊNCIA": "#B6E0FF",
        "AVARIAS NO STRECH": "#B6B6FF",
        "CONSISTÊNCIA NA MISTURA": "#E0B6FF",
        "CONTAMINAÇÃO": "#FFB6E0",
        "COR DESPADRONIZADA": "#FFDEB6",
        "DESEMPENHO PÓS CURA": "#B6FFD5",
        "DESVIO DE PESO OU QUANTIDADE": "#B6FFF6",
        "EMBALAGEM COM DEFEITO FORNECEDOR": "#E0FFB6",
        "FALHA DE INFORMAÇÃO DO DATADOR": "#FFB6C1"
      },
      "produtos": [
        {
          "nome": "PRODUTO INTERNO",
          "codigo": "0001X0001"
        },
        {
          "nome": "PRODUTO EXTERNO",
          "codigo": "0001X0002"
        },
        {
          "nome": "PRODUTO FLEXÍVEL",
          "codigo": "0001X0003"
        },
        {
          "nome": "PRODUTO COLORIDO 1",
          "codigo": "0002X0001"
        },
        {
          "nome": "PRODUTO COLORIDO 2",
          "codigo": "0002X0002"
        },
        {
          "nome": "PRODUTO COLORIDO 3",
          "codigo": "0002X0003"
        }
      ]
    }
    ```

## 🧠 Conceitos de Programação Aplicados

Este projeto é uma demonstração prática de diversos conceitos fundamentais da programação:

  * **Estruturas de Dados**:
      * **Listas (`list`)**: Usadas para armazenar coleções ordenadas de itens (ex: `self.ncs` para todos os registros, listas de unidades, defeitos).
      * **Dicionários (`dict`)**: Essenciais para representar objetos complexos (ex: cada não conformidade é um dicionário, configurações globais, mapeamento de produtos e cores).
      * **Combinações**: A lista de produtos, por exemplo, é uma `list` de `dict`s, ilustrando a flexibilidade na modelagem de dados.
  * **Lógica de Programação e Algoritmos**:
      * **Geração de Número de Registro**: Um algoritmo simples garante um número de registro sequencial e único por ano (`ANO-SEQUENCIAL`).
      * **Resumo de Descrição**: Lógica para truncar strings longas.
      * **Contagem para Gráficos**: Algoritmos de agregação de dados para preparar as informações para visualização.
  * **Controle de Fluxo**:
      * **Estruturas Condicionais (`if`, `elif`, `else`)**: Empregadas para validação de entradas (números, texto vazio, comprimento máximo), tomada de decisões (editar vs. criar, verificar arquivos, confirmações de exclusão) e navegação entre telas.
      * **Estruturas de Repetição (`for`)**: Utilizadas para iterar sobre coleções (registros de NCs, listas de configuração), popular a tabela, processar dados para relatórios e aplicar estilos dinâmicos (cores).
  * **Manipulação de Arquivos (`json`, `os`)**: Carregamento e salvamento de dados em formato JSON para garantir a persistência das informações da aplicação.
  * **Programação Orientada a Objetos (POO)**: A classe `PainelNCApp` encapsula toda a lógica e os dados da aplicação, promovendo modularidade e reutilização de código através de métodos.
  * **Tratamento de Erros e Usabilidade**:
      * **Mensagens de Erro/Aviso**: Utilização de `tkinter.messagebox` para feedback claro ao usuário sobre entradas inválidas ou operações que exigem confirmação.
      * **Interface Amigável**: Design com botões claros, labels descritivos, validações visuais (contador de caracteres) e feedback imediato.

## 🤝 Contribuições

Contribuições são bem-vindas\! Se você tiver sugestões, melhorias ou quiser reportar um bug, sinta-se à vontade para abrir uma *issue* ou enviar um *pull request*.

## Comando para gerar o executável

Para gerar o executável que rode em qualquer computador é necessário rodar o seguinte comando no terminal na pasta onde estiver o arquivo.

```bash
python -m PyInstaller --onefile --windowed --name "Nome para o exceutável" arquivo.py
```
1. Lembre-se de substituir "Nome para o Executável" por algum nome que queria dar.
2. Substitua também "arquivo.py" pelo ponto focal do seu arquivo, onde o método _main_ estiver

## 📄 Licença

Este projeto está sob a licença MIT. Consulte o arquivo [LICENSE](https://www.google.com/search?q=LICENSE) para mais detalhes.

-----

**Desenvolvedores:**

  * Vicente Neto - https://github.com/Vinenop7991

**Versão:** 1.0.0_090625
**Ano:** 2025

-----
