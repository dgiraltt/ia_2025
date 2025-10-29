"""
Tasca a fer:
    - Implementa la funció `generate_episode` per generar un episodi seguint una política
        epsilon-greedy.
    - Completa el bucle principal a `main` per actualitzar els valors Q utilitzant l'algorisme de
        Monte Carlo amb política epsilon-greedy.
"""
from gridworld import joc
import numpy as np
import random


def generate_episode(env, state, policy, epsilon):
    """Genera un episodi seguint una política epsilon-greedy.

    Args:
        env: L'entorn GridWorld
        state: Estat inicial
        policy: Taula Q (política actual)
        epsilon: Probabilitat d'exploració

    Returns:
        List de tuples (estat, acció, recompensa)
    """
    episode = []
    env.reset(state)
    current_state = state

    # Continuar fins que l'agent arribi a un estat terminal (per GridWorld, límit d'iteracions)
    max_steps = 100  # Límit per evitar bucles infinits

    for _ in range(max_steps):
        # Seleccionar acció amb política epsilon-greedy
        if random.random() < epsilon:
            # Exploració: acció aleatòria
            action_idx = random.randint(0, 3)
        else:
            # Explotació: millor acció segons Q
            action_idx = np.argmax(policy[current_state[0], current_state[1], :])

        action = env.actions[action_idx]

        # Executar acció
        next_state, reward = env.step(action)

        # Guardar transició
        episode.append((current_state, action_idx, reward))

        # Condició de terminació: si arribem a una cel·la amb recompensa alta
        if reward >= 5.0:
            break

        current_state = next_state

    return episode


def main():
    y = 0.9 # Gamma
    episodis = 2000
    epsilon = 0.1  # Probabilitat d'exploració

    Q = np.zeros((5, 5, 4), dtype=float)
    env = joc.GridWorld((0, 0), (5, 5))
    returns = dict()

    for ep in range(episodis):
        initial_state = random.randint(0, 4), random.randint(0, 4)

        # Generar un episodi
        episode = generate_episode(env, initial_state, Q, epsilon)

        # Calcular el retorn G per cada pas de l'episodi
        G = 0
        visited_state_actions = set()

        # Recórrer l'episodi en ordre invers (de final a inici)
        for t in range(len(episode) - 1, -1, -1):
            state, action, reward = episode[t]

            # Actualitzar el retorn acumulat
            G = y * G + reward

            # First-visit MC: només actualitzar si és la primera vegada que visitem (estat, acció)
            state_action = (state[0], state[1], action)
            if state_action not in visited_state_actions:
                visited_state_actions.add(state_action)

                # Afegir el retorn a la llista de retorns per aquesta parella (estat, acció)
                if state_action not in returns:
                    returns[state_action] = []
                returns[state_action].append(G)

                # Actualitzar Q com la mitjana dels retorns
                Q[state[0], state[1], action] = np.mean(returns[state_action])

        # Opcional: mostrar progrés cada 100 episodis
        if (ep + 1) % 100 == 0:
            print(f"Episodi {ep + 1}/{episodis} completat")

    # Mostrar la política òptima apresa
    print("\nPolítica òptima apresa (millor acció per cada estat):")
    action_names = ['N', 'S', 'O', 'E']
    for i in range(5):
        for j in range(5):
            best_action_idx = np.argmax(Q[i, j, :])
            print(f"({i},{j}): {action_names[best_action_idx]}", end="  ")
        print()

    # Mostrar valors Q finals
    print("\nValors Q finals:")
    print(Q)


if __name__ == "__main__":
    main()
