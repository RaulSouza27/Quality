class RegistroController:
    def __init__(self):
        self.registros = []

    def criar_registro(self, registro):
        self.registros.append(registro)

    def editar_registro(self, numero_registro, novos_dados):
        for registro in self.registros:
            if registro.numero_registro == numero_registro:
                registro.__dict__.update(novos_dados)
                return True
        return False

    def excluir_registro(self, numero_registro):
        for registro in self.registros:
            if registro.numero_registro == numero_registro:
                self.registros.remove(registro)
                return True
        return False

    def clonar_registro(self, numero_registro):
        for registro in self.registros:
            if registro.numero_registro == numero_registro:
                novo_registro = Registro(**registro.__dict__)
                self.registros.append(novo_registro)
                return novo_registro
        return None

    def listar_registros(self):
        return self.registros