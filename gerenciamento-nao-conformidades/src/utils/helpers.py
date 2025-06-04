def validar_data(data):
    # Função para validar se a data está no formato correto (DD/MM/AAAA)
    try:
        dia, mes, ano = map(int, data.split('/'))
        if 1 <= dia <= 31 and 1 <= mes <= 12 and ano > 0:
            return True
    except ValueError:
        return False
    return False

def formatar_resumo(resumo):
    # Função para formatar o resumo, limitando o número de caracteres
    return resumo[:100] + '...' if len(resumo) > 100 else resumo

def calcular_total_produto_reprovado(qtd_reprovada, valor_unitario):
    # Função para calcular o total de produtos reprovados
    return qtd_reprovada * valor_unitario if qtd_reprovada and valor_unitario else 0

def gerar_codigo_unico():
    # Função para gerar um código único para cada registro
    import uuid
    return str(uuid.uuid4())