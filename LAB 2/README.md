# LAB-2 – Automazione con Python  
*Client HTTP configurabile, logging strutturato e parsing JSON*

&gt; Durata: ~45 min (30 min coding + 15 min test)  
&gt; Difficoltà: principiante → intermedio

---

## Obiettivi
- Creare un **client HTTP riutilizzabile** (wrapper `requests`)  
- Gestire configurazioni via **YAML + env-var** (pattern 12-factor)  
- Implementare **logging JSON** con rotazione automatica  
- Parsare risposte JSON e gestire errori HTTP  
- *(extra)* Aggiungere retry, autenticazione Bearer, CLI `argparse`

---

## 0. Prerequisiti
- Python ≥ 3.9  
- virtualenv già creato (vedi LAB-0)  
- nessun altro software richiesto

---

## 1. Setup iniziale
```bash
git clone &lt;repo&gt;  # oppure crea cartella manualmente
cd lab2-automazione-http
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -U pip requests pyyaml python-json-logger
```

---
## 2. Struttura dal Progetto

``` bash
lab2-automazione-http/
├── README.md              # questo file
├── config.yaml
├── client_http.py
├── main.py
├── requirements.txt
└── log/                   # creato automaticamente
```
