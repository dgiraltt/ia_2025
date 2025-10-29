import copy
from victoria import victoria


class Estat:

    def __init__(self, taulell, fitxa: str, accions_previes: list = None):
        if accions_previes is None:
            accions_previes = []

        self.taulell = taulell
        self.accions_previes = accions_previes
        self.fitxa = fitxa

        self.__es_meta = None


    @staticmethod
    def gira(fitxa):
        if fitxa == "0":
            return "X"
        else:
            return "0"


    def genera_fills(self):
        fills = []

        for pos_x in range(len(self.taulell)):
            for pos_y in range(len(self.taulell[0])):
                casella = self.taulell[pos_x][pos_y]
                if casella == " ":
                    nou_estat = copy.deepcopy(self)

                    nou_estat.taulell[pos_x][pos_y] = self.fitxa
                    nou_estat.accions_previes.append((pos_x, pos_y))
                    nou_estat.fitxa = Estat.gira(self.fitxa)
                    nou_estat.__es_meta = None

                    fills.append(nou_estat)

        return fills


    def es_meta(self, posicio: tuple) -> bool:
        return victoria(self.taulell, posicio)

