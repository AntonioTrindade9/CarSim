import keyboard
import time

class Carro:
    def __init__(self, modelo, ano, capacidade_tanque):
        self.modelo = modelo
        self.ano = ano

        # Energia
        self.combustivel = capacidade_tanque
        self.bateria = 100.0

        # Estado do motor
        self.carro_ligado = False
        self.virabrequim_girando = False
        self.rpm = 0
        self.fase = "admissao"

        # Movimento
        self.velocidade = 0

        # Controle
        self.rpm_ideal = 900
        self.fases = ["admissao", "compressao", "explosao", "escape"]
        self.fase_index = 0

    def dar_partida(self):
        if self.carro_ligado:
            print("O carro já está ligado")
            return

        if self.combustivel <= 0:
            print("Sem combustível")
            return

        if self.bateria <= 0:
            print("Bateria descarregada")
            return

        self.carro_ligado = True
        print("O carro deu partida")

        self.motor_de_arranque()

    def motor_de_arranque(self):
        self.rpm = 250
        self.bateria -= 1
        self.virabrequim_girando = True
        print("Virabrequim começa a girar")

    def injecao_combustivel(self):
        if not self.virabrequim_girando:
            return False

        mistura = 14.7
        if 13 <= mistura <= 16:
            return True
        return False

    def ignicao(self):
        if self.rpm > 200 and self.fase == "explosao":
            self.gerar_forca()

    def gerar_forca(self):
        self.rpm += 150
    
    def atualizar_ciclo(self):
        self.fase = self.fases[self.fase_index]
        self.fase_index = (self.fase_index + 1) % 4

    def controle_marcha_lenta(self):
        erro = self.rpm_ideal - self.rpm
        self.rpm += erro * 0.1
    #Acelera o carro, gastando gasolina e aumentando o rpm e velocidade
    def acelerar(self):
        if not self.carro_ligado:
            print("Carro desligado")
            return

        self.rpm += 300
        self.velocidade += 10
        self.combustivel -= 0.5

        print(f"Vel: {self.velocidade} km/h | RPM: {int(self.rpm)} | Gas: {self.combustivel}")

        self.verificar_combustivel()
    #Verificar se ainda tem combustível pra rodar
    def verificar_combustivel(self):
        if self.combustivel <= 0:
            self.combustivel = 0
            print("Combustível acabou")
            self.desligar()
    #Desligar bem, desliga o motor
    def desligar(self):
        if not self.carro_ligado:
            return

        self.carro_ligado = False
        self.virabrequim_girando = False
        self.rpm = 0
        self.velocidade = 0

    print("Motor desligado")
    #Update serve para ver o estado atual do motor
    def update(self):
        if not self.carro_ligado:
            return

        self.atualizar_ciclo()

        if self.injecao_combustivel():
            self.ignicao()

        self.controle_marcha_lenta()

carro = Carro("Peugeot 206", 2001, 50)

keyboard.add_hotkey("a", carro.dar_partida)
keyboard.add_hotkey("w", carro.acelerar)
keyboard.add_hotkey("d", carro.desligar)

print("Controles:")
print("A = dar partida | W = acelerar | D = desligar | ESC = sair")

try:
    while True:
        carro.update()
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
