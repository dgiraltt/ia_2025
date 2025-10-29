from monedes import joc#, agent
from monedes.solucio import agent

def main():
    ag_mon = agent.AgentMoneda()
    joc_mon = joc.Moneda([ag_mon], random_order=True)
    joc_mon.comencar()


if __name__ == "__main__":
    main()
