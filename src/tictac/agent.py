""" Agent Minimax.

Mòdul en el qual es desenvolupa un agent Minimax amb poda alfa-beta per resoldre el problema del
Tic Tac Toe.

Creat per: Miquel Miró Nicolau (UIB), 2024
"""
from iaLib import agent
from tictac.estat import Estat


class Agent(agent.Agent):
    def __init__(self, poda = False):
        super(Agent, self).__init__(long_memoria=1)
        self.__visitats = None
        self.__cami_exit = None
        self.__poda = poda

    def cerca(self, estat: Estat, alpha, beta, torn_max=True):
        if estat.es_meta():
            return estat, (1 if not torn_max else -1)

        puntuacio_fills = []

        for fill in estat.genera_fills():
            if fill not in self.__visitats:
                punt_fill = self.cerca(fill, alpha, beta, not torn_max)

                if self.__poda:
                    if torn_max:
                        alpha = max(alpha, punt_fill[1])
                    else:
                        beta = min(beta, punt_fill[1])

                    if alpha > beta:
                        break

                self.__visitats[fill] = punt_fill
            puntuacio_fills.append(self.__visitats[fill])

        puntuacio_fills = sorted(puntuacio_fills, key=lambda x: x[1])
        if torn_max:
            return puntuacio_fills[0]
        else:
            return puntuacio_fills[-1]


    def actua(self, percepcio: entorn.Percepcio) -> Accio | tuple[Accio, object]:
        self.__visitats = dict()
        estat_inicial = Estat(percepcio["taulell"], self.jugador)

        res = self.cerca(estat_inicial, alpha=-float('inf'), beta=float('inf'))

        if isinstance(res, tuple) and res[0].accions_previes is not None and len(res[0].accions_previes) > 0:
            solucio, punt = res
            return Accio.POSAR, solucio.accions_previes
        else:
            return Accio.ESPERAR
