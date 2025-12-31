from datetime import datetime

# TODO: Crie a Classe Veiculo e armazene sua marca, modelo e ano como atributos:
class Veiculo:
    def __init__(self, marca, modelo, ano):
        self.marca = marca
        self.modelo = modelo
        self.ano = ano

    def verificar_antiguidade(self):
        anoAtual = datetime.now().year
        idade = anoAtual - self.ano
        if idade >= 22:
            return f"Veículo antigo"
        else:
            return f"Veículo novo"
        
    # TODO: Implemente o método verificar_antiguidade e calcule a diferença entre o ano atual e o ano do veículo:
    
y = datetime.now().strftime("%Y")
# Entrada direta
marca = input("Digite a marca do seu carro").strip()
modelo = input("Digite o modelo do carro").strip()
ano = int(input("Digite o ano de fabricacao do carro").strip())

# Instanciando o objeto e verificando a antiguidade
veiculo = Veiculo(marca, modelo, ano)
print(veiculo.verificar_antiguidade())