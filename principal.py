import produto
import estoque
import fornecedor
import compra
import cliente
import validacao

def testa_fornecedor():
    fornecedor.testa_carregar_fornecedores()
    fornecedor.testa_salvar_fornecedores()
    fornecedor.testa_cadastrar_fornecedor()
    fornecedor.testa_listar_fornecedores()
    fornecedor.testa_associar_produto_fornecedor()
    fornecedor.testa_listar_produtos_por_fornecedor()
    fornecedor.testa_buscar_fornecedores_do_produto()
    fornecedor.testa_contatar_fornecedor()
    fornecedor.testa_gerar_relatorio_fornecedores()


#Testes automaticos
testa_fornecedor()
cliente.testa_funcoes_cliente()
validacao.testa_funcoes_validacao()
