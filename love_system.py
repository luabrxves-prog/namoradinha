import tkinter as tk

APP_BG = "#0d0b14"
PANEL = "#17131f"
PANEL_2 = "#211827"
TEXT = "#fff7fb"
MUTED = "#ad9bad"
PINK = "#ff77aa"
PINK_2 = "#ff9fc4"
GREEN = "#84f0b4"
PURPLE = "#c7a6ff"
LINE = "#382a3e"

LUANA = "Luana"
YASMIN = "Yasmin"

QUESTOES = [
    (
        "MEMÓRIA",
        "Onde você acha que eu armazenaria nossos melhores momentos?",
        [
            "PostgreSQL com backup diário",
            "Data Lake em múltiplas regiões",
            "No meu coração, sem política de retenção",
            "final_final_agora_vai.xlsx",
        ],
        2,
        "Registro persistido com sucesso. Retenção: para sempre.",
    ),
    (
        "PIPELINE",
        "Se nosso namoro fosse um ETL, qual seria a transformação principal?",
        [
            "Normalizar sentimentos em 3FN",
            "Transformar dias comuns em memórias favoritas",
            "Remover duplicatas de beijo",
            "Converter amor para parquet",
        ],
        1,
        "Qualidade dos dados: apaixonante.",
    ),
    (
        "SQL",
        "O que esta query deveria retornar?\n\nSELECT futuro FROM vida WHERE pessoa = 'você';",
        [
            "NULL",
            "Timeout",
            "Todas as linhas que eu ainda quero viver ao seu lado",
            "Permission denied",
        ],
        2,
        "Resultado maior do que a capacidade da tela.",
    ),
    (
        "GOVERNANÇA",
        "Quem tem permissão de escrita na tabela coracao_da_yasmin?",
        ["PUBLIC", "admin", "Somente você", "Qualquer service account"],
        2,
        "RBAC atualizado. Acesso exclusivo concedido.",
    ),
    (
        "DEPLOY",
        "Última aprovação antes de colocar nossa próxima versão em produção:",
        [
            "Aprovar deploy sem rollback",
            "Mais 30 dias de homologação",
            "Abrir RFC",
            "Esperar a próxima sprint",
        ],
        0,
        "Deploy aprovado. Release: nós_duas.v∞",
    ),
]


class LoveSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("love_system.exe")
        self.root.geometry("1060x700")
        self.root.minsize(900, 620)
        self.root.configure(bg=APP_BG)

        self.score = 0
        self.q_index = 0
        self.locked = False
        self.after_jobs = []

        self.shell = tk.Frame(root, bg=PANEL, highlightbackground=LINE, highlightthickness=1)
        self.shell.pack(fill="both", expand=True, padx=34, pady=28)

        self.topbar = tk.Frame(self.shell, bg=PANEL, height=58)
        self.topbar.pack(fill="x")
        self.topbar.pack_propagate(False)

        tk.Label(self.topbar, text="●", bg=PANEL, fg=GREEN, font=("Consolas", 12, "bold")).pack(side="left", padx=(22, 8))
        tk.Label(self.topbar, text="love_system.exe", bg=PANEL, fg=TEXT, font=("Consolas", 10, "bold")).pack(side="left")
        self.path_label = tk.Label(self.topbar, text="  / boot_sequence", bg=PANEL, fg=MUTED, font=("Consolas", 9))
        self.path_label.pack(side="left")
        self.status_label = tk.Label(self.topbar, text="INITIALIZING", bg=PANEL, fg=GREEN, font=("Consolas", 9, "bold"))
        self.status_label.pack(side="right", padx=22)
        tk.Frame(self.shell, bg=LINE, height=1).pack(fill="x")

        self.body = tk.Frame(self.shell, bg=PANEL)
        self.body.pack(fill="both", expand=True)

        self.show_boot()

    def clear(self):
        for job in self.after_jobs:
            try:
                self.root.after_cancel(job)
            except Exception:
                pass
        self.after_jobs.clear()
        for widget in self.body.winfo_children():
            widget.destroy()

    def set_header(self, path, status="ONLINE"):
        self.path_label.configure(text=f"  / {path}")
        self.status_label.configure(text=status)

    def label(self, parent, text, size=12, color=TEXT, bold=False, font="Segoe UI", **kwargs):
        return tk.Label(
            parent,
            text=text,
            bg=kwargs.pop("bg", parent.cget("bg")),
            fg=color,
            font=(font, size, "bold" if bold else "normal"),
            **kwargs,
        )

    def button(self, parent, text, command, primary=False):
        bg = PINK if primary else PANEL_2
        fg = APP_BG if primary else TEXT
        active = PINK_2 if primary else "#35253d"
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=active,
            activeforeground=fg,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            padx=18,
            pady=11,
        )

    def show_boot(self):
        self.clear()
        self.set_header("boot_sequence", "INITIALIZING")

        wrap = tk.Frame(self.body, bg=PANEL)
        wrap.pack(fill="both", expand=True, padx=48, pady=34)

        self.label(wrap, "SISTEMA DE DOIS MESES DE NAMORO", 10, PINK, True, "Consolas").pack(anchor="w")
        self.label(wrap, "INITIALIZING LOVE SYSTEM", 28, TEXT, True, "Consolas").pack(anchor="w", pady=(7, 8))
        self.label(
            wrap,
            "Um aplicativozinho especialmente para a Yasmin porque aparentemente eu virei dev",
            11,
            MUTED,
        ).pack(anchor="w", pady=(0, 22))

        terminal_box = tk.Frame(wrap, bg="#09070d", highlightbackground="#28202d", highlightthickness=1)
        terminal_box.pack(fill="both", expand=True)

        self.terminal = tk.Text(
            terminal_box,
            bg="#09070d",
            fg=GREEN,
            insertbackground=GREEN,
            relief="flat",
            bd=0,
            font=("Consolas", 11),
            wrap="word",
            padx=18,
            pady=16,
        )
        self.terminal.pack(fill="both", expand=True)
        self.terminal.configure(state="disabled")

        self.boot_lines = [
            "[OK] carregando memórias compartilhadas...",
            "[OK] conectando ao cluster: coracao_da_yasmin",
            "[OK] validando credenciais do meu bichinho...",
            "[OK] identidade detectada: Meu amor",
            "[OK] procurando motivos para continuar juntas...",
            "[WARN] resultado excedeu o limite máximo de linhas",
            "[OK] inicializando meu aplicativozinho ∞",
            "",
            "SYSTEM READY.",
        ]
        self.boot_index = 0
        self._boot_next()

    def _boot_next(self):
        if self.boot_index < len(self.boot_lines):
            line = self.boot_lines[self.boot_index]
            self.terminal.configure(state="normal")
            self.terminal.insert("end", line + "\n")
            self.terminal.see("end")
            self.terminal.configure(state="disabled")
            self.boot_index += 1
            job = self.root.after(320 if line else 130, self._boot_next)
            self.after_jobs.append(job)
            return

        self.status_label.configure(text="READY")
        btn = self.button(self.body, "ABRIR SISTEMA  →", self.show_dashboard, primary=True)
        btn.pack(pady=(0, 24))

    def show_dashboard(self):
        self.clear()
        self.set_header("relationship_dashboard", "ONLINE")

        body = tk.Frame(self.body, bg=PANEL)
        body.pack(fill="both", expand=True, padx=42, pady=30)

        self.label(body, "RELATIONSHIP HEALTH", 10, PINK, True, "Consolas").pack(anchor="w")
        self.label(body, "Todos os sistemas operacionais. ❤️", 25, TEXT, True).pack(anchor="w", pady=(6, 4))
        self.label(body, "Dois meses em produção. Nenhum incidente crítico em aberto.", 11, MUTED).pack(anchor="w")

        metrics = tk.Frame(body, bg=PANEL)
        metrics.pack(fill="x", pady=24)
        cards = [
            ("COMPATIBILIDADE", "100%", "+∞% YoY"),
            ("UPTIME", "24/7", "sem manutenção"),
            ("LATÊNCIA DO ABRAÇO", "<1s", "SLA cumprido"),
            ("RETENÇÃO", "∞", "churn: 0%"),
        ]
        for i, (name, value, sub) in enumerate(cards):
            card = tk.Frame(metrics, bg=PANEL_2, padx=14, pady=14)
            card.grid(row=0, column=i, padx=5, sticky="nsew")
            metrics.grid_columnconfigure(i, weight=1)
            self.label(card, name, 8, MUTED, True, "Consolas").pack(anchor="w")
            self.label(card, value, 19, TEXT, True, "Consolas").pack(anchor="w", pady=(7, 2))
            self.label(card, sub, 8, GREEN, False, "Consolas").pack(anchor="w")

        query = tk.Frame(body, bg="#0a0810", padx=18, pady=15)
        query.pack(fill="x", pady=8)
        self.label(query, "SELECT pessoa_favorita FROM universo LIMIT 1;", 11, PURPLE, False, "Consolas", bg="#0a0810").pack(anchor="w")
        self.label(query, "> Yasmin", 11, GREEN, True, "Consolas", bg="#0a0810").pack(anchor="w", pady=(7, 0))

        footer = tk.Frame(body, bg=PANEL)
        footer.pack(fill="x", pady=(22, 0))
        self.label(footer, "Existe uma validação pendente antes da próxima release.", 10, MUTED).pack(side="left")
        self.button(footer, "EXECUTAR VALIDAÇÃO  →", self.start_quiz, primary=True).pack(side="right")

    def start_quiz(self):
        self.score = 0
        self.q_index = 0
        self.render_question()

    def render_question(self):
        self.clear()
        self.set_header("validation", "ONLINE")
        self.locked = False

        cat, question, options, correct, feedback = QUESTOES[self.q_index]
        body = tk.Frame(self.body, bg=PANEL)
        body.pack(fill="both", expand=True, padx=48, pady=32)

        top = tk.Frame(body, bg=PANEL)
        top.pack(fill="x")
        self.label(top, cat, 10, PINK, True, "Consolas").pack(side="left")
        self.label(top, f"CHECK {self.q_index + 1}/{len(QUESTOES)}", 9, MUTED, False, "Consolas").pack(side="right")

        progress = tk.Frame(body, bg=LINE, height=6)
        progress.pack(fill="x", pady=(14, 28))
        progress.pack_propagate(False)
        fill = tk.Frame(progress, bg=PINK)
        fill.place(relx=0, rely=0, relwidth=(self.q_index + 1) / len(QUESTOES), relheight=1)

        self.label(body, question, 22, TEXT, True, wraplength=820, justify="left").pack(anchor="w", pady=(0, 22))

        self.choice_buttons = []
        for idx, option in enumerate(options):
            btn = tk.Button(
                body,
                text=f"{chr(65 + idx)}   {option}",
                command=lambda n=idx: self.answer(n),
                bg=PANEL_2,
                fg=TEXT,
                activebackground="#35253d",
                activeforeground=TEXT,
                relief="flat",
                bd=0,
                cursor="hand2",
                font=("Segoe UI", 10),
                anchor="w",
                padx=16,
                pady=12,
            )
            btn.pack(fill="x", pady=4)
            self.choice_buttons.append(btn)

        self.feedback_label = self.label(body, "", 9, GREEN, True, "Consolas")
        self.feedback_label.pack(anchor="w", pady=(16, 0))

        self.next_btn = self.button(body, "PRÓXIMO CHECK  →", self.next_question, primary=True)

    def answer(self, selected):
        if self.locked:
            return
        self.locked = True

        _, _, _, correct, feedback = QUESTOES[self.q_index]
        for btn in self.choice_buttons:
            btn.configure(state="disabled")

        self.choice_buttons[correct].configure(bg="#203629", fg=GREEN, disabledforeground=GREEN)

        if selected == correct:
            self.score += 1
            self.feedback_label.configure(text="[PASS] " + feedback)
        else:
            self.feedback_label.configure(text="[OVERRIDE] Resposta aceita. Este sistema é tendencioso a seu favor.")

        if self.q_index == len(QUESTOES) - 1:
            self.next_btn.configure(text="GERAR RELATÓRIO FINAL  →")
        self.next_btn.pack(anchor="e", pady=(18, 0))

    def next_question(self):
        if self.q_index < len(QUESTOES) - 1:
            self.q_index += 1
            self.render_question()
        else:
            self.show_report()

    def show_report(self):
        self.clear()
        self.set_header("final_report", "SUCCESS")

        body = tk.Frame(self.body, bg=PANEL)
        body.pack(fill="both", expand=True, padx=48, pady=34)
        self.label(body, "VALIDATION COMPLETE", 10, GREEN, True, "Consolas").pack(anchor="w")
        self.label(body, "Compatibilidade afetiva: 100%", 26, TEXT, True).pack(anchor="w", pady=(6, 5))
        self.label(body, f"Score técnico: {self.score}/{len(QUESTOES)} • score oficial: APROVADA PARA SEMPRE", 10, MUTED).pack(anchor="w")

        report = tk.Frame(body, bg="#0a0810", padx=18, pady=16)
        report.pack(fill="x", pady=24)
        rows = [
            ("integridade_do_relacionamento", "OK"),
            ("qualidade_das_memorias", "EXCELENTE"),
            ("risco_de_rollback", "0.00%"),
            ("previsao_de_futuro", "PROMISSORA"),
            ("recomendacao_modelo", "CONTINUAR_JUNTAS"),
        ]
        for key, value in rows:
            row = tk.Frame(report, bg="#0a0810")
            row.pack(fill="x", pady=4)
            self.label(row, key, 10, MUTED, False, "Consolas", bg="#0a0810").pack(side="left")
            self.label(row, value, 10, GREEN, True, "Consolas", bg="#0a0810").pack(side="right")

        self.label(body, "Há apenas uma ação pendente para concluir o deploy.", 10, MUTED).pack(anchor="w")
        self.button(body, "ABRIR SOLICITAÇÃO DE DEPLOY  →", self.show_contract, primary=True).pack(anchor="e", pady=(18, 0))

    def show_contract(self):
        self.clear()
        self.set_header("deployment_approval", "ACTION REQUIRED")

        body = tk.Frame(self.body, bg=PANEL)
        body.pack(fill="both", expand=True, padx=48, pady=34)
        self.label(body, "CHANGE REQUEST #LOVE-∞", 10, PINK, True, "Consolas").pack(anchor="w")
        self.label(body, "Renovação automática do nosso contrato", 25, TEXT, True).pack(anchor="w", pady=(6, 6))
        self.label(body, "Escopo: continuar sendo nós duas, com novas memórias, novas versões e zero intenção de rollback.", 10, MUTED, wraplength=820, justify="left").pack(anchor="w")

        card = tk.Frame(body, bg=PANEL_2, padx=18, pady=14)
        card.pack(fill="x", pady=24)
        for key, value in [
            ("OWNER", "Luana"),
            ("APPROVER", "Yasmin"),
            ("ENVIRONMENT", "production"),
            ("DURATION", "indefinida"),
            ("ROLLBACK PLAN", "não aplicável"),
            ("RISK", "excesso de carinho"),
        ]:
            row = tk.Frame(card, bg=PANEL_2)
            row.pack(fill="x", pady=4)
            self.label(row, key, 9, MUTED, False, "Consolas").pack(side="left")
            self.label(row, value, 9, TEXT, True, "Consolas").pack(side="right")

        self.label(body, "Você aprova esta release?", 18, TEXT, True).pack(anchor="w", pady=(2, 10))
        buttons = tk.Frame(body, bg=PANEL)
        buttons.pack(fill="x")
        self.button(buttons, "SIM, DEPLOY AGORA ♡", self.show_letter, primary=True).pack(side="left")
        self.review_btn = self.button(buttons, "PRECISO REVISAR", self.review)
        self.review_btn.pack(side="left", padx=10)
        self.review_texts = ["REVISÃO JÁ FEITA", "RFC APROVADA", "SEM BLOQUEIOS", "TENTA O BOTÃO ROSA 😌"]
        self.review_i = 0

    def review(self):
        self.review_btn.configure(text=self.review_texts[self.review_i % len(self.review_texts)])
        self.review_i += 1

    def show_letter(self):
        self.clear()
        self.set_header("release_notes", "DEPLOYED")

        body = tk.Frame(self.body, bg=PANEL)
        body.pack(fill="both", expand=True, padx=48, pady=28)
        self.label(body, "RELEASE SUCCESSFUL ♡", 10, GREEN, True, "Consolas").pack(anchor="w")
        self.label(body, "Agora sem linguagem técnica.", 22, TEXT, True).pack(anchor="w", pady=(6, 14))

        paper = tk.Frame(body, bg="#fff7fb", padx=28, pady=24)
        paper.pack(fill="both", expand=True)
        self.label(paper, "Para Yasmin, meu bichinho,", 18, "#943e63", True, "Georgia", bg="#fff7fb").pack(anchor="w")

        text = (
            "Eu podia simplesmente te entregar uma carta. Mas, como agora eu sou dev, resolvi complicar um pouquinho.\n\n"
            "Você é engenheira de dados, então achei justo construir um sistema inteiro só para chegar à conclusão mais óbvia de todas: "
            "eu escolheria você em qualquer banco, linguagem, arquitetura, ambiente ou versão deste mundo.\n\n"
            "Obrigada por dividir a vida comigo. Pelas conversas, pelas risadas, pelos dias leves e também pelos dias em que a gente precisa debugar as coisas com mais calma.\n\n"
            "Quero continuar colecionando memórias com você até nosso Data Lake emocional ficar absurdamente caro para armazenar.\n\n"
            "Feliz dois meses de namoro. Eu te amo. ❤️"
        )
        self.label(paper, text, 12, "#4b3540", False, "Georgia", bg="#fff7fb", wraplength=800, justify="left").pack(anchor="w", pady=(14, 8))
        self.label(paper, "— Luana ♡", 12, "#a14067", True, "Georgia", bg="#fff7fb").pack(anchor="e")


def main():
    root = tk.Tk()
    LoveSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()
