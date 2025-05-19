import streamlit as st
from streamlit_option_menu import option_menu
import cvxpy as cp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(page_title="Branch and Bound Knapsack", layout="wide")

# Fonction de résolution du problème sac à dos avec CVXPY
def branch_and_bound_knapsack(values, weights, capacity):
    n = len(values)
    x = cp.Variable(n, boolean=True)  # Variables binaires (0-1)
    objective = cp.Maximize(values @ x)
    constraints = [weights @ x <= capacity]
    prob = cp.Problem(objective, constraints)

    # ✅ Utiliser un solveur compatible pour les variables booléennes
    prob.solve(solver=cp.GLPK_MI)

    return x.value, prob.value

# Interface principale
def main():
    with st.sidebar:
        choice = option_menu("Menu", ["Entrée des données", "Résultat"],
                             icons=["pencil", "graph-up"], menu_icon="cast", default_index=0)
    
    if choice == "Entrée des données":
        st.header("Entrer les données du problème sac à dos")

        # Nombre d'objets à insérer
        n = st.number_input("Nombre d'objets", min_value=1, max_value=20, value=5)

        # Valeurs et poids des objets par défaut
        st.markdown("## Valeurs et poids des objets")
        default_data = {
            "Valeur": [10, 20, 30, 40, 50][:n],
            "Poids": [1, 3, 4, 5, 7][:n]
        }
        df = pd.DataFrame(default_data)

        # Permettre l'édition des données
        edited_df = st.data_editor(df, num_rows="dynamic")

        # Capacité maximale du sac
        capacity = st.number_input("Capacité maximale du sac à dos", min_value=1, value=10)

        # Bouton de résolution
        if st.button("Résoudre"):
            values = np.array(edited_df["Valeur"])
            weights = np.array(edited_df["Poids"])
            solution, val = branch_and_bound_knapsack(values, weights, capacity)

            st.session_state["solution"] = solution
            st.session_state["valeur"] = val
            st.session_state["values"] = values
            st.session_state["weights"] = weights
            st.session_state["capacity"] = capacity
            st.success("Résolution terminée! Passez à l’onglet Résultat.")
    
    elif choice == "Résultat":
        if "solution" not in st.session_state:
            st.warning("Veuillez d'abord saisir les données et résoudre le problème.")
            return

        st.header("Résultats")

        solution = st.session_state["solution"]
        values = st.session_state["values"]
        weights = st.session_state["weights"]
        capacity = st.session_state["capacity"]
        val = st.session_state["valeur"]

        st.write(f"Valeur optimale : **{val:.2f}**")
        poids_total = np.sum(weights * solution)
        st.write(f"Poids total : **{poids_total:.2f}** / {capacity}")

        # Liste des objets choisis
        chosen = [f"Objet {i+1}" for i, x in enumerate(solution) if x > 0.5]
        st.write("Objets choisis :", chosen)

        # Affichage graphique des décisions
        fig, ax = plt.subplots()
        ax.bar(range(len(solution)), solution, color='skyblue')
        ax.set_xticks(range(len(solution)))
        ax.set_xticklabels([f"O{i+1}" for i in range(len(solution))])
        ax.set_ylabel("Choix (1=oui, 0=non)")
        ax.set_title("Objets sélectionnés")
        st.pyplot(fig)

if __name__ == "__main__":
    main()

