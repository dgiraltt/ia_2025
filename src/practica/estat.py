import copy
import practica


class Estat:
    """
    Representa l'estat del joc del laberint i proporciona operacions de generació i avaluació d'estats.
    Conté la posició de l'agent actual, posicions de tots els agents, parets, mida del taulell, destí,
    camí recorregut, cost acumulat i el torn actual (nom de l'agent que mou).
    """
    MOVIMENTS = {
        "N": (0, -1),
        "S": (0, 1),
        "E": (1, 0),
        "O": (-1, 0),
    }
    COSTS = {
        "MOURE": 1,
        "BOTAR": 2,
        "POSAR_PARET": 3,
        "ESPERAR": 0,
    }

    def __init__(self, pos_agent, pos_agents, pos_parets, mida, desti, cami=None, cost=0, torn=None):
        """
        Crea un nou estat del laberint.
        Args:
            pos_agent (tuple[int, int]): Posició de l'agent actual (x, y).
            pos_agents (dict[str, tuple[int, int]]): Posicions de tots els agents per nom.
            pos_parets (iterable[tuple[int, int]]): Conjunt o llista de parets ocupades.
            mida (tuple[int, int]): Dimensions del taulell (ample, alt).
            desti (tuple[int, int]): Posició objectiu a assolir.
            cami (list[tuple[str, str]]|None): Seqüència d'accions realitzades fins ara.
            cost (int|float): Cost acumulat de les accions.
            torn (str|None): Nom de l'agent al qual li toca moure.
        """
        self.pos_agent = pos_agent
        self.pos_agents = pos_agents
        self.pos_parets = set(pos_parets)
        self.mida = mida
        self.desti = tuple(desti)
        self.cami = [] if cami is None else list(cami)
        self.cost = cost
        self.torn = torn


    def __lt__(self, other):
        """
        Defineix l'operació de menor que entre estats.
        Retorna sempre False perquè no necessitam un ordre natural entre estats;
        s'usa per evitar comparacions quan es fan servir estructures com PriorityQueue.
        """
        return False


    def transicio(self, accio):
        """
        Aplica una acció sobre l'estat i retorna el nou estat resultant (si és vàlid).
        Args:
            accio (tuple[str, str|None]): Parella (tipus, direcció). Tipus en {"MOURE","BOTAR","POSAR_PARET","ESPERAR"}.
        Returns:
            Estat|None: Nou estat després d'aplicar l'acció, o None si l'acció no és aplicable.
        """
        tipus, direccio = accio

        # Omitim accions no vàlides.
        if tipus not in self.COSTS.keys() or direccio not in self.MOVIMENTS:
            return None

        # Processam les accions segons el seu tipus, seguint la direcció donada.
        if tipus == "ESPERAR":
            nou_estat = copy.deepcopy(self)
            nou_estat.cami.append(("ESPERAR", None))
            nou_estat.cost += self.COSTS.get("ESPERAR", 0)
            return nou_estat

        x, y = self.pos_agent
        dx, dy = self.MOVIMENTS[direccio]
        posObjectiu = None
        posParet = None

        match tipus:
            case "BOTAR":
                posObjectiu = (x + 2 * dx, y + 2 * dy)
                posParet = (x, y)
                if posObjectiu in self.pos_parets:
                    return None

            case "MOURE":
                posObjectiu = (x + dx, y + dy)
                posParet = (x, y)
                if posObjectiu in self.pos_parets:
                    return None

            case "POSAR_PARET":
                posObjectiu = self.pos_agents[self.torn]
                posParet = (x + dx, y + dy)
                if posParet in self.pos_parets or posParet == self.desti:
                    return None

        nou_estat = copy.deepcopy(self)
        nou_estat.pos_agent = posObjectiu
        nou_estat.pos_parets.add(posParet)
        nou_estat.cost += self.COSTS[tipus]
        nou_estat.cami.append((tipus, direccio))
        return nou_estat


    def genera_fills(self):
        """
        Genera tots els estats fills accessibles des de l'estat actual.
        Considera les accions possibles: "ESPERAR", "MOURE", "BOTAR" (si hi ha paret davant)
        i "POSAR_PARET" (si la casella objectiu és dins del taulell i accessible).
        Returns:
            list[Estat]: Llista d'estats resultants vàlids.
        """
        fills = []

        # Afegim l'estat on esperem en el cas que l'agent quedés atrapat.
        fill = self.transicio(("ESPERAR", None))
        if fill is not None:
            fills.append(fill)

        # Per cada direcció possible, afegim la transició corresponent.
        for direccio in self.MOVIMENTS:
            dx, dy = self.MOVIMENTS[direccio]

            # Acció MOURE
            nx, ny = self.pos_agent[0] + dx, self.pos_agent[1] + dy
            if 0 <= nx < self.mida[0] and 0 <= ny < self.mida[1]:
                fill = self.transicio(("MOURE", direccio))
                if fill is not None:
                    fills.append(fill)

            # Acció BOTAR
            px, py = self.pos_agent[0] + dx, self.pos_agent[1] + dy
            if (px, py) in self.pos_parets:
                nx, ny = self.pos_agent[0] + 2 * dx, self.pos_agent[1] + 2 * dy
                if 0 <= nx < self.mida[0] and 0 <= ny < self.mida[1]:
                    fill = self.transicio(("BOTAR", direccio))
                    if fill is not None:
                        fills.append(fill)

            # Acció POSAR_PARET
            px, py = self.pos_agent[0] + dx, self.pos_agent[1] + dy
            if 0 <= px < self.mida[0] and 0 <= py < self.mida[1]:
                fill = self.transicio(("POSAR_PARET", direccio))
                if fill is not None:
                    fills.append(fill)

        return fills


    def es_meta(self):
        """
        Determina si la posició de l'agent coincideix amb el destí.
        Returns:
            bool: Cert si la posició de l'agent coincideix amb el destí; en cas contrari, Fals.
        """
        return self.desti == self.pos_agent


    def heuristica(self, agent):
        """
        Calcula una estimació heurística del valor d'aquest estat per a diferents tipus d'agents.
            - Si l'agent és de tipus 'AgentMinimax' (joc de dos jugadors), empra una heurística
              diferencial basada en la distància Manhattan al destí de l'agent actual i de l'oponent:
              valor = distància(oponent → destí) - distància(actual → destí). Un valor positiu
              indica avantatge per a l'agent del torn actual.
            - Per a la resta d'agents (p. ex. A* o BFS amb cost), retorna el cost acumulat més
            l'estimació Manhattan des de la posició actual fins al destí.
        Args:
            agent: Instància de l'agent que avalua l'estat (p. ex. 'AgentMinimax' o d'altres).
        Returns:
            int: Valor heurístic; més gran és millor per a l'agent actual en Minimax,
            i per a A* representa una estimació del cost total (cost acumulat + distància Manhattan).
        """
        if isinstance(agent, practica.agent_minimax.AgentMinimax) and len(self.pos_agents) > 1:
            # Si l'agent és Minimax i té un rival, calcularem la distància entre ells.
            actual = self.torn
            oponent = [a for a in self.pos_agents.keys() if a != actual][0]

            x1, y1 = self.pos_agents[actual]
            x2, y2 = self.pos_agents[oponent]

            # Distàncies Manhattan al destí de cada agent.
            d1 = abs(x1 - self.desti[0]) + abs(y1 - self.desti[1])
            d2 = abs(x2 - self.desti[0]) + abs(y2 - self.desti[1])

            # Diferència de distàncies: positiu si l'actual està més a prop que l'oponent.
            return d2 - d1

        else:
            # De no ser el cas, calculam la heurística amb Manhattan.
            h = abs(self.pos_agent[0] - self.desti[0]) + abs(self.pos_agent[1] - self.desti[1])
            return self.cost + h
