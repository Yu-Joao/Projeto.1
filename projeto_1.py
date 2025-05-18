import tkinter as tk
from tkinter import ttk
import re

def traduzir_codigo(codigo, origem, destino):
    origem = origem.lower()
    destino = destino.lower()
    linhas = codigo.strip().split('\n')
    traduzidas = []

    for linha in linhas:
        linha_strip = linha.strip()

        # PRINT
        if origem == 'python' and linha_strip.startswith("print("):
            conteudo = linha_strip[6:-1]
            if destino == 'javascript':
                traduzidas.append(f"console.log({conteudo});")
            elif destino == 'java':
                traduzidas.append(f"System.out.println({conteudo});")
            elif destino == 'ruby':
                traduzidas.append(f"puts {conteudo}")

        elif origem == 'javascript' and "console.log" in linha_strip:
            conteudo = linha_strip.split("console.log(")[1].rstrip(");")
            if destino == 'python':
                traduzidas.append(f"print({conteudo})")
            elif destino == 'java':
                traduzidas.append(f"System.out.println({conteudo});")
            elif destino == 'ruby':
                traduzidas.append(f"puts {conteudo}")

        elif origem == 'java' and "System.out.println" in linha_strip:
            conteudo = linha_strip.split("System.out.println(")[1].rstrip(");")
            if destino == 'python':
                traduzidas.append(f"print({conteudo})")
            elif destino == 'javascript':
                traduzidas.append(f"console.log({conteudo});")
            elif destino == 'ruby':
                traduzidas.append(f"puts {conteudo}")

        elif origem == 'ruby' and linha_strip.startswith("puts "):
            conteudo = linha_strip[5:]
            if destino == 'python':
                traduzidas.append(f"print({conteudo})")
            elif destino == 'javascript':
                traduzidas.append(f"console.log({conteudo});")
            elif destino == 'java':
                traduzidas.append(f"System.out.println({conteudo});")

        # IF, ELIF, ELSE
        elif "if " in linha_strip:
            cond = linha_strip.replace("if ", "").replace(":", "")
            if destino == 'python':
                traduzidas.append(f"if {cond}:")
            elif destino in ['javascript', 'java']:
                traduzidas.append(f"if ({cond}) {{")
            elif destino == 'ruby':
                traduzidas.append(f"if {cond}")

        elif "elif " in linha_strip:
            cond = linha_strip.replace("elif ", "").replace(":", "")
            if destino == 'python':
                traduzidas.append(f"elif {cond}:")
            elif destino in ['javascript', 'java']:
                traduzidas.append(f"}} else if ({cond}) {{")
            elif destino == 'ruby':
                traduzidas.append(f"elsif {cond}")

        elif "else" in linha_strip:
            if destino == 'python':
                traduzidas.append("else:")
            elif destino in ['javascript', 'java']:
                traduzidas.append("} else {")
            elif destino == 'ruby':
                traduzidas.append("else")

        # FOR (Python range)
        elif origem == 'python' and "for" in linha_strip and "in range" in linha_strip:
            match = re.match(r"for (\w+) in range\((\d+)\):", linha_strip)
            if match:
                var, limite = match.groups()
                if destino == 'javascript':
                    traduzidas.append(f"for (let {var} = 0; {var} < {limite}; {var}++) {{")
                elif destino == 'java':
                    traduzidas.append(f"for (int {var} = 0; {var} < {limite}; {var}++) {{")
                elif destino == 'ruby':
                    traduzidas.append(f"for {var} in 0...{limite}")

        # WHILE
        elif "while " in linha_strip:
            cond = linha_strip.replace("while", "").replace(":", "").strip()
            if destino == 'python':
                traduzidas.append(f"while {cond}:")
            elif destino in ['javascript', 'java']:
                traduzidas.append(f"while ({cond}) {{")
            elif destino == 'ruby':
                traduzidas.append(f"while {cond}")

        # ARITMÉTICA
        elif any(op in linha_strip for op in ['+', '-', '*', '/', '%']):
            traduzidas.append(linha_strip + ("" if destino in ['ruby', 'python'] else ";"))

        # LINHA EM BRANCO
        elif linha_strip == "":
            if destino in ['javascript', 'java']:
                traduzidas.append("}")
            elif destino == 'ruby':
                traduzidas.append("end")

        else:
            traduzidas.append("// " + linha_strip)

    if destino in ['javascript', 'java']:
        traduzidas.append("}")

    return "\n".join(traduzidas)

# Função chamada ao clicar no botão
def ao_traduzir():
    entrada = entrada_texto.get("1.0", tk.END)
    origem = origem_combo.get()
    destino = destino_combo.get()
    resultado = traduzir_codigo(entrada, origem, destino)
    saida_texto.delete("1.0", tk.END)
    saida_texto.insert(tk.END, resultado)

# === GUI COM MODO ESCURO ===
janela = tk.Tk()
janela.title("Conversor de Código")
janela.configure(bg="#1e1e1e")

estilo = ttk.Style(janela)
janela.geometry("800x600")
estilo.theme_use("default")
estilo.configure("TLabel", background="#1e1e1e", foreground="white", font=("Consolas", 12))
estilo.configure("TButton", background="#3a3a3a", foreground="white", font=("Consolas", 12))
estilo.configure("TCombobox", fieldbackground="#2e2e2e", background="#2e2e2e", foreground="white")

# Widgets
ttk.Label(janela, text="Linguagem de origem:").pack(pady=5)
origem_combo = ttk.Combobox(janela, values=["Python", "JavaScript", "Java", "Ruby"])
origem_combo.pack()

ttk.Label(janela, text="Linguagem de destino:").pack(pady=5)
destino_combo = ttk.Combobox(janela, values=["Python", "JavaScript", "Java", "Ruby"])
destino_combo.pack()

ttk.Label(janela, text="Código de entrada:").pack(pady=5)
entrada_texto = tk.Text(janela, height=10, bg="#2d2d2d", fg="white", insertbackground="white")
entrada_texto.pack(fill="both", expand=True, padx=10, pady=5)

ttk.Button(janela, text="Traduzir", command=ao_traduzir).pack(pady=10)

ttk.Label(janela, text="Código traduzido:").pack(pady=5)
saida_texto = tk.Text(janela, height=10, bg="#2d2d2d", fg="white", insertbackground="white")
saida_texto.pack(fill="both", expand=True, padx=10, pady=5)

janela.mainloop()
