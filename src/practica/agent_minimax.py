from practica.estat import Estat
from practica.joc import Viatger


class AgentMinimax(Viatger):
    """
    Agent que utilitza l'algorisme Minimax amb poda alfa-beta per a jocs de dos jugadors.
    Avalua els estats amb una heurística i explora fins a una profunditat limitada,
    tallant branques que no poden millorar el resultat mitjançant alfa-beta.
    """

    def __init__(self, *args, **kwargs):
        """
        Inicialitza l'agent Minimax.
        """
        super(AgentMinimax, self).__init__(*args, **kwargs)
        self.__tancat = None


    def cerca(self, estat: Estat, alpha, beta, torn_max=True, profunditat=0, prof_max=5):
        """
        Aplica Minimax amb poda alfa-beta des d'un estat donat.
        Args:
            estat (Estat): Estat actual del joc.
            alpha (float): Millor valor assegurat per al max fins ara.
            beta (float): Millor valor assegurat per al min fins ara.
            torn_max (bool): Si True, li toca al jugador maximitzador.
            profunditat (int): Profunditat actual de la recerca.
            prof_max (int): Profunditat màxima de recerca.
        Returns:
            tuple[Estat, float|int]: El millor estat fill i el seu valor.
        """
        self.__tancat = set()

        # Si hem arribat al final o al límit de profunditat
        if profunditat > prof_max or estat.es_meta():
            res = (1 if not torn_max else -1)
            return estat, res

        millor_valor = -float('inf') if torn_max else float('inf')
        millor_node = None

        # Generam tots els estats fills possibles de l'estat actual, en cas de no tenir-ne retornam el mateix.
        fills = estat.genera_fills()
        if not fills:
            heuristica = estat.heuristica(self)
            if not torn_max:
                heuristica = -heuristica
            return estat, heuristica

        # Altrament, els iteram per trobar el millor.
        for fill in fills:
            # Omitim els estats que ja s'han tancat.
            if fill in self.__tancat:
                continue

            # Cercam recursivament l'arbre de possibilitats.
            node_actual, punt_fill = self.cerca(fill, alpha, beta, not torn_max, profunditat + 1)

            # Guardam el millor resultat.
            if torn_max:
                alpha = max(alpha, punt_fill)
                if punt_fill > millor_valor:
                    millor_valor, millor_node = punt_fill, fill

            elif not torn_max:
                beta = min(beta, punt_fill)
                if punt_fill < millor_valor:
                    millor_valor, millor_node = punt_fill, fill

            self.__tancat.add(fill)

            # Sortim de la iteració en cas de poda.
            if alpha >= beta:
                break

        return (millor_node if millor_node else estat,
                millor_valor if millor_node else 0)


    def actua(self, percepcio: dict):
        """
        Decideix l'acció segons el resultat de Minimax des de la percepció actual.
        Construeix l'estat inicial a partir de la percepció i executa la cerca Minimax amb poda alfa-beta.
        Retorna la primera acció del millor camí.
        Args:
            percepcio (dict): Informació del joc (posicions, parets, mida, destí i torn).
        Returns:
            tuple[str, str|None]: Acció i direcció (si escau), o ("ESPERAR", None) si no hi ha accions.
        """
        estat_inicial = Estat(
            pos_agent=percepcio["AGENTS"][self.nom],
            pos_agents=percepcio["AGENTS"],
            pos_parets=percepcio["PARETS"],
            mida=percepcio["MIDA"],
            desti=percepcio["DESTI"],
            torn=percepcio["TORN"]
        )

        millor_estat, _ = self.cerca(estat_inicial, alpha=-float('inf'), beta=float('inf'))

        if millor_estat and millor_estat.cami:
            return millor_estat.cami[0]

        return "ESPERAR", None
