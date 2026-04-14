import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from rdkit import Chem
from rdkit.Chem import Descriptors
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class AdvancedDrugAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Drug-Likeness Analyzer Pro")
        self.root.geometry("1200x850")
        
        self.thresholds = {
            "lipinski": {"mw_max": 500, "logp_max": 5.0, "hbd_max": 5, "hba_max": 10, "weight": 0.30},
            "veber": {"rotb_max": 10, "tpsa_max": 140.0, "weight": 0.20},
            "ghose": {"mw_range": (160, 480), "logp_range": (-0.4, 5.6), "weight": 0.20},
            "egan": {"logp_max": 5.88, "tpsa_max": 131.6, "weight": 0.15},
            "bostrom": {"mw_max": 300, "logp_max": 3.0, "weight": 0.15}
        }
        self.setup_ui()

    def setup_ui(self):
        # Top Input Area
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.pack(side="top", fill="x")
        
        ttk.Label(top_frame, text="SMILES:").pack(side="left", padx=5)
        self.entry = ttk.Entry(top_frame, width=60)
        self.entry.insert(0, "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O") # Ibuprofen
        self.entry.pack(side="left", padx=5, fill="x", expand=True)
        
        ttk.Button(top_frame, text="Analyze", command=self.analyze).pack(side="left", padx=5)

        # Main Body
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        # Left Side: Text Results
        self.output = scrolledtext.ScrolledText(main_frame, width=40, font=("Consolas", 10))
        self.output.pack(side="left", fill="y", padx=10, pady=10)
        self.output.tag_configure("header", font=("Consolas", 11, "bold"))
        self.output.tag_configure("score", font=("Consolas", 12, "bold"), foreground="blue")

        # Right Side: Visual Graph
        self.fig, self.ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
        self.canvas = FigureCanvasTkAgg(self.fig, master=main_frame)
        self.canvas.get_tk_widget().pack(side="right", fill="both", expand=True)

    def calculate_descriptors(self, mol):
        return {
            "MW": round(Descriptors.MolWt(mol), 2),
            "LogP": round(Descriptors.MolLogP(mol), 2),
            "HBD": Descriptors.NumHDonors(mol),
            "HBA": Descriptors.NumHAcceptors(mol),
            "TPSA": round(Descriptors.TPSA(mol), 2),
            "RotB": Descriptors.NumRotatableBonds(mol)
        }

    def evaluate_rules(self, d):
        scores = {}
        scores["lipinski"] = 100 if sum([d["MW"] > 500, d["LogP"] > 5, d["HBD"] > 5, d["HBA"] > 10]) <= 1 else 0
        scores["veber"] = 100 if sum([d["RotB"] > 10, d["TPSA"] > 140]) == 0 else 0
        scores["ghose"] = 100 if (160 <= d["MW"] <= 480) and (-0.4 <= d["LogP"] <= 5.6) else 0
        scores["egan"] = 100 if d["LogP"] <= 5.88 and d["TPSA"] <= 131.6 else 0
        scores["bostrom"] = 100 if d["MW"] <= 300 and d["LogP"] <= 3.0 else 0
        return scores

    def update_graph(self, scores):
        self.ax.clear()
        categories = [k.capitalize() for k in scores.keys()]
        values = list(scores.values())
        
        # Radar charts need to "close the loop"
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        values += values[:1]
        angles += angles[:1]

        self.ax.fill(angles, values, color='blue', alpha=0.25)
        self.ax.plot(angles, values, color='blue', linewidth=2)
        self.ax.set_xticks(angles[:-1])
        self.ax.set_xticklabels(categories)
        self.ax.set_yticklabels([]) # Hide numerical radial labels for cleaner look
        self.ax.set_ylim(0, 100)
        self.ax.set_title("Rule Compliance Profile", va='bottom')
        self.canvas.draw()

    def analyze(self):
        smiles = self.entry.get().strip()
        mol = Chem.MolFromSmiles(smiles)
        if not mol:
            messagebox.showerror("Error", "Invalid SMILES")
            return

        desc = self.calculate_descriptors(mol)
        scores = self.evaluate_rules(desc)
        final_score = sum(scores[k] * self.thresholds[k]["weight"] for k in scores)

        # Update Text Output
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, f"PROPERTIES:\n", "header")
        for k, v in desc.items(): self.output.insert(tk.END, f"{k}: {v}\n")
        self.output.insert(tk.END, f"\nGLOBAL SCORE: {final_score:.1f}%\n", "score")

        # Update Visuals
        self.update_graph(scores)

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedDrugAnalyzer(root)
    root.mainloop()
