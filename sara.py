import tkinter as tk
from tkinter import ttk
import csv
liste_personne = []

MAIN_BG_COLOR = '#e6f2ff'  # fond bleu clair pastel
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 600

class Personne:
    def __init__(self, nom, prenom, matricule, categorie,salaire_base, primes=[], retenues=[]):
        self.nom = nom
        self.prenom = prenom
        self.matricule = matricule
        self.categorie = categorie
        self.salaire_base = salaire_base
       
        self.primes = primes
        self.retenues = retenues
        self.salaire_brut = self.calcul_salaire_brut()
        self.salaire_net = self.calcul_salaire_net()
      
        
    def calcul_salaire_brut(self):
        return self.salaire_base + sum(m for l, m in self.primes)

    def calcul_salaire_net(self):
        return self.salaire_brut - sum(m for l, m in self.retenues)

    def affichage(self):
        print(f"Nom : {self.nom}")
        print(f"Prénom : {self.prenom}")
        print(f"Matricule : {self.matricule}")
        print(f"Catégorie : {self.categorie}")
        print("Primes :")
        for label, montant in self.primes:
            print(f"  - {label} : {montant} FCFA")
        print("Retenues :")
        for label, montant in self.retenues:
            print(f"  - {label} : {montant} FCFA")
            
        print(f"Salaire brut : {self.salaire_brut} FCFA")
        print(f"Salaire net : {self.salaire_net} FCFA")    

    
# Dictionnaires de primes et retenues selon les catégories
primes_par_categorie = {"A1": {"Logement": 50000, "Technicite":30000, "Enseignement": 40000, "Recherche":50000},
                      "A2":{"Logement": 40000, "Technicite":20000, "Enseignement": 30000, "Recherche":40000}, 
                      "B1": {"Logement": 25000, "Technicite":1000, "Enseignement": 20000, "Recherche":25000}, 
                      "C":{"Logement":15000, "Technicite":5000, "Enseignement": 15000, "Recherche": 15000}}

retenues_par_categorie =   {"A1": {"pension_retraite":0, "depense_audio": 750, "credit_foncier":10000},
                        
                        "A2": {"pension_retraite":10, "depense_audio": 750, "credit_foncier":10000},
                        "B1": {"pension_retraite":10, "depense_audio": 750, "credit_foncier":10000},
                        "C": {"pension_retraite":10, "depense_audio": 750, "credit_foncier":10000},}   



def creer_personne():
    nom = entre_nom.get()
    prenom = entre_prenom.get()
    matricule = entre_matricule.get()
    salaire_base = int(entre_salaire_base.get())
    enfants = int(entre_nbrenfants.get())
    categorie = entre_categorie.get()
    
    allocation = 4500 * enfants
    primes = [(label, prime_montants[label]) for label, var in prime_vars.items() if var.get() ]
    primes.append(("allocation familiale", allocation))
    total_primes = sum(m for l , m in primes)
    
    
   
   
    
    
    
    salaire_brut = salaire_base + total_primes
    impot = int(salaire_brut*0.10)
    
    retenues = [(label, retenue_montants[label]) for label, var in retenue_vars.items() if var.get() ]
    retenues.append(("impot", impot))
    total_retenus = sum(m for l , m in retenues)
    
    
    salaire_net = salaire_brut - total_retenus
    
    
  
    p = Personne(nom, prenom, matricule, categorie, salaire_base, primes, retenues)
   
    liste_personne.append(p)
    p.affichage()

def afficher_options(event):
    for widget in frame_dynamique.winfo_children():
     widget.destroy()

    cat = entre_categorie.get()
    
    global prime_vars, prime_montants, retenue_vars, retenue_montants
    prime_vars = {}
    prime_montants = {}
    retenue_vars = {}
    retenue_montants = {}

    # Affichage des primes
    if cat in primes_par_categorie:
        tk.Label(frame_dynamique, text="Primes :", font=('Arial', 10, 'bold')).pack()
        for label, montant in primes_par_categorie[cat].items():
            var = tk.BooleanVar()
            prime_vars[label] = var
            prime_montants[label] = montant
            cb = tk.Checkbutton(frame_dynamique, text=f"{label} : {montant} FCFA", variable=var)
            cb.pack(anchor='w')

    # Affichage des retenues
    if cat in retenues_par_categorie:
        tk.Label(frame_dynamique, text="Retenues :", font=('Arial', 10, 'bold')).pack()
        for label, montant in retenues_par_categorie[cat].items():
            var = tk.BooleanVar()
            retenue_vars[label] = var
            retenue_montants[label] = montant
            cb = tk.Checkbutton(frame_dynamique, text=f"{label} : {montant} FCFA", variable=var)
            cb.pack(anchor='w')
            
def sauvegarder_csv():
    with open('bulletin.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        # Entêtes
        writer.writerow(['Nom', 'Prénom', 'Matricule', 'Catégorie', 'Salaire Base', 'Primes', 'Retenues', 'Salaire Brut', 'Salaire Net'])
        
        # Lignes
        for p in liste_personne:
            primes_str = ", ".join([f"{label}:{montant}" for label, montant in p.primes])
            retenues_str = ", ".join([f"{label}:{montant}" for label, montant in p.retenues])
            writer.writerow([p.nom, p.prenom, p.matricule, p.categorie, p.salaire_base, primes_str, retenues_str, p.salaire_brut, p.salaire_net])           

# Interface
fen = tk.Tk()
fen.title("Bulletin de paye")
fen.configure(bg=MAIN_BG_COLOR)
fen.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
fen.resizable(False, False)

tk.Label(fen, text="Nom").pack()
entre_nom = tk.Entry(fen)
entre_nom.pack()

tk.Label(fen, text="Prénom").pack()
entre_prenom = tk.Entry(fen)
entre_prenom.pack()

tk.Label(fen, text="Matricule").pack()
entre_matricule = tk.Entry(fen)
entre_matricule.pack()

tk.Label(fen, text="Salaire de base").pack()
entre_salaire_base = tk.Entry(fen)
entre_salaire_base.pack()

tk.Label(fen, text= "nombre d'enfants").pack()
entre_nbrenfants = tk.Entry(fen)
entre_nbrenfants.pack()

tk.Label(fen, text="Catégorie").pack()
entre_categorie = ttk.Combobox(fen, values=["A1", "A2", "B1", "C"])
entre_categorie.pack()
entre_categorie.bind("<<ComboboxSelected>>", afficher_options)



frame_dynamique = tk.Frame(fen)
frame_dynamique.pack(pady=10)

tk.Button(fen, text="Créer", command=creer_personne).pack(pady=10)
tk.Button(fen, text="Sauvegarder CSV", command=sauvegarder_csv).pack(pady=5)


fen.mainloop()
