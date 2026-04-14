# Drug-Likeness Analyzer Pro

**Drug-Likeness Analyzer Pro** is a medicinal chemistry tool designed to evaluate and visualize the drug-likeness of small molecules. By processing SMILES strings, the application calculates key physicochemical properties and assesses compliance across five industry-standard filters.

The tool features a **Radar Chart (Spider Plot)** visualization, allowing researchers to see a molecule's "Rule Compliance Profile" at a glance.

## ✨ Features

*   **Property Calculation:** MW, LogP, HBD, HBA, TPSA, and Rotatable Bonds via RDKit.
*   **Multi-Rule Assessment:** Simultaneous evaluation of Lipinski, Veber, Ghose, Egan, and Bostrom filters.
*   **Dynamic Visualization:** Real-time Radar Chart generation using Matplotlib.
*   **Weighted Scoring:** A global drug-likeness percentage based on research-driven weights.
*   **Publication Ready:** High-resolution export functionality for figures (300 DPI).

## 🧪 Validated Medicinal Chemistry Filters

The analyzer utilizes verified thresholds from the following landmark studies:

1.  **Lipinski's Rule of Five (1997):** Evaluates oral bioavailability based on MW ≤ 500, LogP ≤ 5, HBD ≤ 5, and HBA ≤ 10.
2.  **Veber Filter (2002):** Focuses on molecular flexibility (RotB ≤ 10) and polar surface area (TPSA ≤ 140 Å²).
3.  **Ghose Filter (1999):** Sets ranges for drug-like preference (MW: 160–480, LogP: -0.4–5.6).
4.  **Egan Filter (2000):** Predicting absorption via LogP ≤ 5.88 and TPSA ≤ 131.6 Å².
5.  **Bostrom Lead-likeness (2012):** Stricter criteria for identifying promising starting leads (MW ≤ 300, LogP ≤ 3)

![WhatsApp Image 2026-04-14 at 8 28 19 PM](https://github.com/user-attachments/assets/709483e9-53c0-41b0-948d-2a073c6f7f1f)

## 🚀 Getting Started

### Prerequisites
*   Python 3.8 or higher
*   RDKit
*   Matplotlib
*   NumPy

### Installation
```bash
# Clone the repository
git clone https://github.com/N1S55M-X/DrugLikeness-Analyzer-Pro.git

# Install dependencies
pip install rdkit matplotlib numpy
