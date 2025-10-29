from practica.estat import Estat
from practica.joc import Viatger


class AgentAmplada(Viatger):
    """
    Agent que realitza una cerca en amplada (BFS) per trobar un camí cap al destí en el laberint.
    """

    def __init__(self, *args, **kwargs):
        """
        Inicialitza l'agent i les estructures de dades de cerca.
        """
        super(AgentAmplada, self).__init__(*args, **kwargs)
        self.__frontera = None
        self.__tancat = None
        self.__cami_exit = None


    def cerca(self, estat_inicial: Estat):
        """
        Executa una cerca en amplada (BFS) des d'un estat inicial.
        Args:
            estat_inicial (Estat): Estat a partir del qual comença la cerca.
        Returns:
            bool: Cert si s'ha trobat un camí al destí, Fals en cas contrari.
        """
        self.__frontera = []
        self.__tancat = set()
        exit = False

        self.__frontera.append(estat_inicial)
        estat_actual = None

        # Iteram entre els estats possibles del laberint fins a trobar el camí de sortida.
        while self.__frontera:
            estat_actual = self.__frontera.pop(0)

            # Omitim els estats que ja s'han tancat.
            if estat_actual in self.__tancat:
                continue

            # Si hem trobat la meta, sortim del bucle.
            if estat_actual.es_meta():
                break

            # Afegim els estats possibles de l'estat actual al bucle.
            for f in estat_actual.genera_fills():
                self.__frontera.append(f)

            self.__tancat.add(estat_actual)

        if estat_actual.es_meta():
            self.__cami_exit = estat_actual.cami
            exit = True

        return exit


    def actua(self, percepcio: dict):
        """
        Decideix l'acció a realitzar segons la percepció actual.
            - Si encara no s'ha calculat, inicia la cerca BFS des de l'estat actual.
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
