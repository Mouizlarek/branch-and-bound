import numpy as np
import pandas as pd
import cvxpy as cp
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_option_menu import option_menu

# --- Fonction pour générer un DataFrame d'objets ---
def create_items_dataframe(n, values, weights):
    df = pd.DataFrame({
        "Valeur": values,
        "Poids": weights,
        "Valeur/Poids": np.array(values) / np.array(weights)
    })
    return df

# --- Résolution du problème du sac à dos via cvxpy (relaxation continue) ---
def solve_knapsack_cvxpy(df, max_weight):
    n = len(df)
    x = cp.Variable(n)

    values = df["Valeur"].values
    weights = df["Poids"].values

    # Objectif : maximiser la valeur totale
    objective = cp.Maximize(values @ x)

    # Contraintes : poids total <= max_weight, 0 <= x <= 1 (relaxation)
    constraints = [
        weights @ x <= max_weight,
        x >= 0,
        x <= 1
    ]

    problem = cp.Problem(objective, constraints)
    problem.solve()

    # Résultat et décision
    selected = x.value
    return selected, problem.value

# --- Visualisation des résultats ---
def plot_results(df, selected, max_weight):
    fig, ax = plt.subplots(figsize=(8,5))
    indices = np.arange(len(df))
    ax.bar(indices, df["Valeur"], label="Valeur")
    ax.bar(indices, df["Poids"], label="Poids", alpha=0.5)
    ax.bar(indices, selected * df["Valeur"], label="Valeur sélectionnée", alpha=0.7)
    ax.set_xlabel("Objets")
    ax.set_ylabel("Valeur / Poids")
    ax.legend()
    ax.set_title(f"Sélection continue (relaxation) - Poids max = {max_weight}")
    st.pyplot(fig)

# --- Interface Streamlit ---
def main():
    st.title("Problème du sac à dos 0-1 avec CVXPY et Streamlit")

    with st.sidebar:
        choice = option_menu("Menu", ["Saisie manuelle", "Exemple automatique"], 
                             icons=["pencil", "box-seam"], menu_icon="cast", default_index=0)

    if choice == "Saisie manuelle":
        n = st.number_input("Nombre d'objets", min_value=1, step=1, value=5)

        values = []
        weights = []
        for i in range(int(n)):
            val = st.number_input(f"Valeur de l'objet {i+1}", value=10.0)
            w = st.number_input(f"Poids de l'objet {i+1}", value=5.0)
            values.append(val)
            weights.append(w)

        max_weight = st.number_input("Poids maximal du sac", min_value=0.1, value=20.0)

    else:
        # Exemple automatique
        n = 6
        values = [60, 100, 120, 80, 30, 50]
        weights = [10, 20, 30, 40, 50, 10]
        max_weight = 100
        st.write("Exemple avec ces objets :")
        df_example = create_items_dataframe(n, values, weights)
        st.dataframe(df_example)

    df = create_items_dataframe(n, values, weights)
    selected, max_profit = solve_knapsack_cvxpy(df, max_weight)

    st.write(f"**Profit maximal (relaxé) :** {max_profit:.2f}")
    st.write("**Sélection (valeurs entre 0 et 1, relaxation) :**")
    st.write(selected)

    plot_results(df, selected, max_weight)

if __name__ == "__main__":
    main()
