from practica.agent_amplada import AgentAmplada
from practica.agent_A_Estrella import AgentAEstrella
from practica.agent_minimax import AgentMinimax
from practica.joc import Laberint


def main():
    """
    Inicialitza el laberint, els agents, i comença la simulació.
    """
    mida = (10, 10)

    agents = [
        #AgentAmplada(nom="AgentAmplada"),
        #AgentAEstrella(nom="AgentAEstrella"),
        AgentMinimax(nom="AgentMinimax1"),
        AgentMinimax(nom="AgentMinimax2"),
    ]

    lab = Laberint(agents, mida_taulell=mida)
    lab.comencar()


if __name__ == "__main__":
    main()
