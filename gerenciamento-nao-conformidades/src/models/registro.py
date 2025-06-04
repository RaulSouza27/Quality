class Registro:
    def __init__(self, numero_registro, data_abertura, resumo, status, analista_operador,
                 codigo_produto, produto, lote, total_produto_reprovado, unidade_medida,
                 valor_total, defeito, modo_defeito, descricao, data_producao,
                 hora_producao, acao_imediata, responsavel_acao_imediata,
                 possivel_abraangencia):
        self.numero_registro = numero_registro
        self.data_abertura = data_abertura
        self.resumo = resumo
        self.status = status
        self.analista_operador = analista_operador
        self.codigo_produto = codigo_produto
        self.produto = produto
        self.lote = lote
        self.total_produto_reprovado = total_produto_reprovado
        self.unidade_medida = unidade_medida
        self.valor_total = valor_total
        self.defeito = defeito
        self.modo_defeito = modo_defeito
        self.descricao = descricao
        self.data_producao = data_producao
        self.hora_producao = hora_producao
        self.acao_imediata = acao_imediata
        self.responsavel_acao_imediata = responsavel_acao_imediata
        self.possivel_abraangencia = possivel_abraangencia

    def editar_registro(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def excluir_registro(self):
        # Lógica para excluir o registro
        pass

    def clonar_registro(self):
        return Registro(
            self.numero_registro,
            self.data_abertura,
            self.resumo,
            self.status,
            self.analista_operador,
            self.codigo_produto,
            self.produto,
            self.lote,
            self.total_produto_reprovado,
            self.unidade_medida,
            self.valor_total,
            self.defeito,
            self.modo_defeito,
            self.descricao,
            self.data_producao,
            self.hora_producao,
            self.acao_imediata,
            self.responsavel_acao_imediata,
            self.possivel_abraangencia
        )