class Pedido:
    def __init__(self):
        self.itens = [] 
    
    # TODO: Crie um método chamado adicionar_item que recebe um preço e adiciona à lista de itens:
    def adicionar_item(self, preco):
        # TODO: Adicione o preço do item à lista:
        self.itens.append(float(preco))

    # TODO: Crie um método chamado calcular_total que retorna a soma de todos os preços da lista:
    def calcular_total(self):
        # TODO: Retorne a soma de todos os preços
        return f"{sum(self.itens):.2f}"

quantidade_pedidos = int(input("Entre com a quantidade de pedidos ").strip())

pedido = Pedido()

for _ in range(quantidade_pedidos):
    entrada = input("Digite o nome e o preco ").strip()
    nome, preco = entrada.rsplit(" ", 1)
    #TODO: Chame o método adicionar_item corretamente: 
    pedido.adicionar_item(preco)
# TODO: Exiba o total formatado com duas casas decimais:
print(pedido.calcular_total())