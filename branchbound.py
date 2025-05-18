# 🧮 Problème du sac à dos 0-1 avec Branch and Bound (version console)

def get_input():
    # Saisie du nombre d'objets
    while True:
        try:
            n = int(input("Entrez le nombre d'objets : "))
            if n > 0:
                break
            else:
                print("Veuillez entrer un entier strictement positif.")
        except ValueError:
            print("Ce n'est pas un entier valide.")
    
    p, w = [], []
    for i in range(n):
        while True:
            try:
                val = float(input(f"Valeur de l'objet {i+1} : "))
                break
            except ValueError:
                print("Ce n'est pas un réel valide.")
        while True:
            try:
                poids = float(input(f"Poids de l'objet {i+1} : "))
                break
            except ValueError:
                print("Ce n'est pas un réel valide.")
        p.append(val)
        w.append(poids)
    
    # Saisie du poids maximum
    while True:
        try:
            W = float(input("Poids maximal du sac : "))
            if W > 0:
                break
            else:
                print("Le poids doit être positif.")
        except ValueError:
            print("Ce n'est pas un réel valide.")
    
    return n, W, p, w


# 🧮 Fonction de score pour trier les objets (valeur / poids)
def score(i, p, w):
    return p[i] / w[i]


# 🎯 Fonction de borne supérieure pour un nœud donné
def get_bound(node, n, W, p, w, p_per_weight):
    if node.weight >= W:
        return 0
    result = node.profit
    j = node.level + 1
    totweight = node.weight
    while j < n and totweight + w[j] <= W:
        totweight += w[j]
        result += p[j]
        j += 1
    if j < n:
        result += (W - totweight) * p_per_weight[j]
    return result


# 📦 Classe de nœud (sommet de l'arbre de décision)
class Node:
    def __init__(self, level, profit, weight):
        self.level = level
        self.profit = profit
        self.weight = weight
        self.items = []
        self.bound = 0
        self.label = ""
        self.parent = None

    def set_parent(self, parent):
        self.parent = parent


# ⏳ File de priorité (triée selon la borne)
class PriorityQueue:
    def __init__(self):
        self.pqueue = []

    def insert(self, node):
        i = 0
        while i < len(self.pqueue) and self.pqueue[i].bound > node.bound:
            i += 1
        self.pqueue.insert(i, node)

    def remove(self):
        if not self.pqueue:
            return None
        return self.pqueue.pop()

    def is_empty(self):
        return len(self.pqueue) == 0


# 🧠 Algorithme principal : Branch and Bound
def knapsack(n, W, p, w):
    # Tri décroissant par valeur/poids
    items = sorted(range(n), key=lambda i: p[i]/w[i], reverse=True)
    p = [p[i] for i in items]
    w = [w[i] for i in items]
    p_per_weight = [p[i] / w[i] for i in range(n)]
    realitems = [[i, items[i]] for i in range(n)]

    maxprofit = 0
    bestitems = []
    nodes_generated = 0
    pq = PriorityQueue()

    # Nœud racine
    v = Node(-1, 0, 0)
    v.bound = get_bound(v, n, W, p, w, p_per_weight)
    pq.insert(v)
    nodes_generated += 1

    while not pq.is_empty():
        v = pq.remove()
        if v.bound > maxprofit:
            u = Node(v.level + 1, v.profit + p[v.level + 1], v.weight + w[v.level + 1])
            u.items = v.items.copy()
            u.items.append(u.level)
            u.set_parent(v)
            u.label = "Y" + str(realitems[u.level][1] + 1)
            nodes_generated += 1

            if u.weight <= W and u.profit > maxprofit:
                maxprofit = u.profit
                bestitems = u.items.copy()

            u.bound = get_bound(u, n, W, p, w, p_per_weight)
            if u.bound > maxprofit:
                pq.insert(u)

            # Exclusion de l'objet
            u2 = Node(u.level, v.profit, v.weight)
            u2.items = v.items.copy()
            u2.set_parent(v)
            u2.label = "N" + str(realitems[u2.level][1] + 1)
            u2.bound = get_bound(u2, n, W, p, w, p_per_weight)
            nodes_generated += 1

            if u2.bound > maxprofit:
                pq.insert(u2)

    # Récupération des indices réels
    for i in range(len(bestitems)):
        bestitems[i] = realitems[bestitems[i]][1] + 1

    # Résultat final
    print("\n✅ Résultat final")
    print("Profit maximal :", maxprofit)
    print("Objets à prendre (indices d'origine) :", sorted(bestitems))
    print("Sommets générés (B&B) :", nodes_generated)
    print("Sommets par énumération complète :", 2**n)
    print("Sommets économisés :", 2**n - nodes_generated)


# 🏁 Programme principal
if _name_ == "_main_":
    n, W, p, w = get_input()
    knapsack(n, W, p, w)
