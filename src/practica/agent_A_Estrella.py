from practica.estat import Estat
from practica.joc import Viatger
from queue import PriorityQueue


class AgentAEstrella(Viatger):
    """
    Agent que aplica l'algorisme A* per trobar un camí eficient cap al destí.
    Utilitza una cua de prioritat on la prioritat ve donada per la funció heurística de l'estat.
    """

    def __init__(self, *args, **kwargs):
        """
        Inicialitza l'agent i les estructures de dades de cerca.
        """
        super(AgentAEstrella, self).__init__(*args, **kwargs)
        self.__frontera = None
        self.__tancat = None
        self.__cami_exit = None


    def cerca(self, estat_inicial):
        """
        Executa l'algorisme A* des d'un estat inicial.
        Args:
            estat_inicial (Estat): Estat des del qual s'inicia la cerca.
        Returns:
            bool: Cert si s'ha trobat un camí cap al destí; Fals altrament.
        """
        self.__frontera = PriorityQueue()
        self.__tancat = set()
        exit = False

        self.__frontera.put((estat_inicial.heuristica(self), estat_inicial))
        estat_actual = None

        # Iteram entre els estats possibles del laberint fins a trobar el camí de sortida.
        while self.__frontera:
            _, estat_actual = self.__frontera.get()

            # Omitim els estats que ja s'han tancat.
            if estat_actual in self.__tancat:
                continue

            # Si hem trobat la meta, sortim del bucle.
            if estat_actual.es_meta():
                break

            # Afegim els estats possibles de l'estat actual al bucle.
            for f in estat_actual.genera_fills():
                self.__frontera.put((f.heuristica(self), f))

            self.__tancat.add(estat_actual)

        if estat_actual.es_meta():
            self.__cami_exit = estat_actual.cami
            exit = True

        return exit


    def actua(self, percepcio: dict):
        """
        Decideix l'acció a realitzar segons la percepció estat_actual.
            - Si encara no s'ha calculat, inicia la cerca BFS des de l'estat estat_actual.
            - Si hi ha un camí calculat, retorna la següent acció del camí.
        Args:
            percepcio (dict): Informació del joc (parets, destí, agents, mida i torn).
        Returns:
            tuple[str, str|None]: Acció i direcció (o None) segons el pla; "ESPERAR" si no hi ha acció.
        """
        if self.__cami_exit is None:
            estat_inicial = Estat(
                pos_agent=percepcio["AGENTS"][self.nom],
                pos_agents=percepcio["AGENTS"],
                pos_parets=percepcio["PARETS"],
                mida=percepcio["MIDA"],
                desti=percepcio["DESTI"],
                torn=percepcio["TORN"]
            )

            self.cerca(estat_inicial)

        if self.__cami_exit:
            tipus, direccio = self.__cami_exit.pop(0)
            match tipus:
                case "MOURE":
                    return "MOURE", direccio

                case "BOTAR":
                    return "BOTAR", direccio

                case "POSAR_PARET":
                    return "POSAR_PARET", direccio

        return "ESPERAR", None
