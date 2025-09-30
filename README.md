# Quantum Money Simulation

Based on **Wiesner’s Quantum Money Scheme**, this project simulates the printing and verification of quantum bills.  
It also models the behavior of **malicious agents** attempting to counterfeit these bills, in order to demonstarte the resilience of quantum cryptography against forgery.

You can view the main **simulation results** in the Jupyter notebook file (`test.ipynb`) and explore the test scripts located in the `tests/` folder.

---

### 🕵️ Counterfeiters Simulated

- **Regular Attacker**  
  Withdraws a legitimate bill, then attempts to forge it by **randomly guessing** the basis and value of each qubit.

- **Statistical Attacker**  
  Iteratively measures the qubits in a withdrawn bill (collapsing the original note) and then tries to deposit both the **real** and the **forged** version.

- **Entangled Attacker**  
  Uses **quantum entanglement** to extract information about each qubit’s basis and value. By iteratively measuring multiple withdrawn notes, the attacker keeps the most promising candidate, increasing the likelihood of a successful forgery.

---

## ⚙️ Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/jair-espinoza/quantum-money-simulation.git
cd quantum-money-simulation
pip install -r requirements.txt
