import math
import random
import tkinter as tk
from tkinter import ttk

# ============================================================
# VERSAO ELABORADA - PERSONALIZE ESTES CAMPOS
# ============================================================
SEU_NOME = "Yasmin"
NOME_DELA = "Meu amor"
DATA_DO_NAMORO = "10/09"
TEMPO_JUNTAS = "mais um capítulo da nossa história"

CARTA_FINAL = (
    "Eu podia simplesmente te entregar uma carta.\n\n"
    "Mas você é engenheira de dados, então achei justo construir um sistema "
    "inteiro só para chegar à conclusão mais óbvia de todas: eu escolheria você "
    "em qualquer banco, linguagem, arquitetura, ambiente ou versão deste mundo.\n\n"
    "Obrigada por dividir a vida comigo. Pelas conversas, pelas risadas, pelos "
    "dias leves e também pelos dias em que a gente precisou debugar as coisas "
    "com mais calma.\n\n"
    "Quero continuar colecionando memórias com você até nosso Data Lake emocional "
    "ficar absurdamente caro para armazenar.\n\n"
    "Feliz aniversário de namoro. Eu te amo."
)

QUESTOES = [
    {
        "categoria": "MEMÓRIA",
        "pergunta": "Onde você acha que eu armazenaria nossos melhores momentos?",
        "opcoes": [
            "PostgreSQL com backup diário",
            "Data Lake em múltiplas regiões",
            "No meu coração, sem política de retenção",
            "final_final_agora_vai.xlsx",
        ],
        "correta": 2,
        "feedback": "Registro persistido com sucesso. Retenção: para sempre.",
    },
    {
        "categoria": "PIPELINE",
        "pergunta": "Se nosso namoro fosse um ETL, qual seria a transformação principal?",
        "opcoes": [
            "Normalizar sentimentos em 3FN",
            "Transformar dias comuns em memórias favoritas",
            "Remover duplicatas de beijo",
            "Converter amor para parquet",
        ],
        "correta": 1,
        "feedback": "Transformação validada. Qualidade dos dados: apaixonante.",
    },
    {
        "categoria": "OBSERVABILIDADE",
        "pergunta": "Qual métrica deveria gerar alerta crítico no nosso relacionamento?",
        "opcoes": [
            "Latência do abraço acima de 5 segundos",
            "Número de cafés por dia",
            "CPU do notebook em 90%",
            "Quantidade de abas abertas",
        ],
        "correta": 0,
        "feedback": "Alerta configurado. Auto-healing: abraço imediato.",
    },
    {
        "categoria": "SQL",
        "pergunta": "O que esta query deveria retornar?\n\nSELECT futuro FROM vida WHERE pessoa = 'você';",
        "opcoes": [
            "NULL",
            "Timeout",
            "Todas as linhas que eu ainda quero viver ao seu lado",
            "Permission denied",
        ],
        "correta": 2,
        "feedback": "Query executada. Resultado maior do que a capacidade da tela.",
    },
    {
        "categoria": "INCIDENT RESPONSE",
        "pergunta": "Se um dia nosso sistema apresentar erro 500, qual é o protocolo?",
        "opcoes": [
            "Culpar a infraestrutura",
            "Abrir Sev-1 no relacionamento",
            "Conversar, respirar, abraçar e resolver juntas",
            "Reiniciar o roteador",
        ],
        "correta": 2,
        "feedback": "Runbook aprovado. MTTR estimado: um abraço e uma conversa.",
    },
    {
        "categoria": "GOVERNANÇA",
        "pergunta": "Quem tem permissão de escrita na tabela coracao_da_yasmin?",
        "opcoes": [
            "PUBLIC",
            "admin",
            "Somente você",
            "Qualquer service account",
        ],
        "correta": 2,
        "feedback": "RBAC atualizado. Acesso exclusivo concedido.",
    },
    {
        "categoria": "DEPLOY",
        "pergunta": "Última aprovação antes de colocar nossa próxima versão em produção:",
        "opcoes": [
            "Aprovar deploy sem rollback",
            "Solicitar mais 30 dias de homologação",
            "Abrir RFC",
            "Esperar a próxima sprint",
        ],
        "correta": 0,
        "feedback": "Deploy aprovado. Release: nós_duas.v∞",
    },
]


class LoveSystem:
    BG = "#0d0b14"
    PANEL = "#17131f"
    PANEL_2 = "#211827"
    PINK = "#ff77aa"
    PINK_2 = "#ff9fc4"
    PURPLE = "#c7a6ff"
    TEXT = "#fff7fb"
    MUTED = "#ad9bad"
    GREEN = "#84f0b4"
    RED = "#ff7d95"
    LINE = "#382a3e"

    def __init__(self, root):
        self.root = root
        self.root.title("love_system.exe")
        self.root.geometry("1120x720")
        self.root.minsize(980, 650)
        self.root.configure(bg=self.BG)

        self.score = 0
        self.index = 0
        self.answer_locked = False
        self.hearts = []
        self.timer_jobs = []

        self.canvas = tk.Canvas(root, bg=self.BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self._resize)

        self.stage = tk.Frame(self.canvas, bg=self.PANEL)
        self.stage_window = self.canvas.create_window(560, 360, window=self.stage, width=940, height=590)

        self._spawn_background()
        self._animate_background()
        self.show_boot()

    # --------------------------------------------------------
    # CORE UI
    # --------------------------------------------------------
    def _resize(self, event):
        self.canvas.coords(self.stage_window, event.width / 2, event.height / 2)
        self.canvas.itemconfigure(
            self.stage_window,
            width=min(980, max(860, event.width - 110)),
            height=min(620, max(560, event.height - 90)),
        )

    def clear_stage(self):
        for job in self.timer_jobs:
            try:
                self.root.after_cancel(job)
            except Exception:
                pass
        self.timer_jobs.clear()
        for widget in self.stage.winfo_children():
            widget.destroy()

    def label(self, parent, text, size=12, color=None, bold=False, font="Segoe UI", **kwargs):
        return tk.Label(
            parent,
            text=text,
            bg=kwargs.pop("bg", parent.cget("bg")),
            fg=color or self.TEXT,
            font=(font, size, "bold" if bold else "normal"),
            **kwargs,
        )

    def button(self, parent, text, command, primary=False, width=None):
        bg = self.PINK if primary else self.PANEL_2
        fg = self.BG if primary else self.TEXT
        active = self.PINK_2 if primary else "#35253d"
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
            pady=10,
            width=width,
        )

    def topbar(self, section, status="ONLINE"):
        bar = tk.Frame(self.stage, bg=self.PANEL, height=45)
        bar.pack(fill="x", padx=28, pady=(20, 8))
        bar.pack_propagate(False)

        self.label(bar, "●", 12, self.GREEN, bold=True).pack(side="left", padx=(0, 8))
        self.label(bar, "love_system.exe", 10, self.TEXT, bold=True, font="Consolas").pack(side="left")
        self.label(bar, f"  /  {section}", 9, self.MUTED, font="Consolas").pack(side="left")
        self.label(bar, status, 9, self.GREEN, bold=True, font="Consolas").pack(side="right")

        tk.Frame(self.stage, bg=self.LINE, height=1).pack(fill="x", padx=28)

    # --------------------------------------------------------
    # BACKGROUND
    # --------------------------------------------------------
    def _spawn_background(self):
        self.hearts.clear()
        for _ in range(26):
            x = random.randint(0, 1100)
            y = random.randint(0, 720)
            item = self.canvas.create_text(
                x,
                y,
                text=random.choice(["♡", "·", "✦"]),
                fill=random.choice(["#342139", "#42263d", "#2d2235"]),
                font=("Segoe UI Symbol", random.randint(9, 17)),
            )
            self.canvas.tag_lower(item, self.stage_window)
            self.hearts.append((item, random.uniform(0.08, 0.26)))

    def _animate_background(self):
        h = max(self.canvas.winfo_height(), 720)
        w = max(self.canvas.winfo_width(), 1120)
        for item, speed in self.hearts:
            x, y = self.canvas.coords(item)
            y -= speed
            if y < -20:
                y = h + 20
                x = random.randint(10, max(20, w - 10))
            self.canvas.coords(item, x, y)
        self.root.after(35, self._animate_background)

    # --------------------------------------------------------
    # SCENE 1 - BOOT
    # --------------------------------------------------------
    def show_boot(self):
        self.clear_stage()
        self.topbar("boot_sequence", "INITIALIZING")

        wrap = tk.Frame(self.stage, bg=self.PANEL)
        wrap.pack(fill="both", expand=True, padx=55, pady=30)

        self.label(wrap, "INITIALIZING LOVE SYSTEM", 23, self.TEXT, bold=True, font="Consolas").pack(anchor="w", pady=(0, 8))
        self.label(
            wrap,
            f"release especial • {DATA_DO_NAMORO} • author: {SEU_NOME}",
            10,
            self.MUTED,
            font="Consolas",
        ).pack(anchor="w", pady=(0, 24))

        terminal_box = tk.Frame(wrap, bg="#09070d", padx=20, pady=18)
        terminal_box.pack(fill="both", expand=True)

        self.terminal = tk.Text(
            terminal_box,
            bg="#09070d",
            fg=self.GREEN,
            insertbackground=self.GREEN,
            relief="flat",
            bd=0,
            font=("Consolas", 11),
            height=16,
            wrap="word",
        )
        self.terminal.pack(fill="both", expand=True)
        self.terminal.configure(state="disabled")

        self.boot_lines = [
            "[OK] carregando memórias compartilhadas...",
            "[OK] conectando ao cluster: coracao_da_yasmin",
            "[OK] validando credenciais da pessoa favorita...",
            f"[OK] identidade detectada: {NOME_DELA}",
            "[OK] verificando histórico de risadas... volume acima do esperado",
            "[OK] procurando motivos para continuar juntas...",
            "[WARN] resultado excedeu o limite máximo de linhas",
            "[OK] inicializando pipeline_romantico_v∞",
            "",
            "SYSTEM READY.",
        ]
        self.boot_i = 0
        self._boot_next()

    def _boot_next(self):
        if self.boot_i < len(self.boot_lines):
            line = self.boot_lines[self.boot_i]
            self.terminal.configure(state="normal")
            self.terminal.insert("end", line + "\n")
            self.terminal.see("end")
            self.terminal.configure(state="disabled")
            self.boot_i += 1
            job = self.root.after(420 if line else 180, self._boot_next)
            self.timer_jobs.append(job)
            return

        self.start_btn = self.button(self.stage, "ABRIR SISTEMA  →", self.show_dashboard, primary=True)
        self.start_btn.pack(pady=(0, 28))

    # --------------------------------------------------------
    # SCENE 2 - DASHBOARD
    # --------------------------------------------------------
    def show_dashboard(self):
        self.clear_stage()
        self.topbar("relationship_dashboard")

        body = tk.Frame(self.stage, bg=self.PANEL)
        body.pack(fill="both", expand=True, padx=35, pady=24)

        hero = tk.Frame(body, bg=self.PANEL)
        hero.pack(fill="x", pady=(0, 20))
        self.label(hero, "RELATIONSHIP HEALTH", 10, self.PINK, bold=True, font="Consolas").pack(anchor="w")
        self.label(hero, "Todos os sistemas operacionais. ❤️", 25, self.TEXT, bold=True).pack(anchor="w", pady=(5, 4))
        self.label(
            hero,
            f"Analisando {TEMPO_JUNTAS}. Nenhum incidente crítico em aberto.",
            11,
            self.MUTED,
        ).pack(anchor="w")

        metrics = tk.Frame(body, bg=self.PANEL)
        metrics.pack(fill="x", pady=12)
        data = [
            ("COMPATIBILIDADE", "100%", "+∞% YoY"),
            ("UPTIME", "24/7", "sem manutenção"),
            ("LATÊNCIA DO ABRAÇO", "< 1s", "SLA cumprido"),
            ("RETENÇÃO", "∞", "churn: 0%"),
        ]
        for i, (name, value, sub) in enumerate(data):
            card = tk.Frame(metrics, bg=self.PANEL_2, padx=16, pady=14)
            card.grid(row=0, column=i, padx=6, sticky="nsew")
            metrics.grid_columnconfigure(i, weight=1)
            self.label(card, name, 8, self.MUTED, bold=True, font="Consolas").pack(anchor="w")
            self.label(card, value, 20, self.TEXT, bold=True, font="Consolas").pack(anchor="w", pady=(7, 2))
            self.label(card, sub, 8, self.GREEN, font="Consolas").pack(anchor="w")

        query = tk.Frame(body, bg="#0a0810", padx=18, pady=16)
        query.pack(fill="x", pady=18)
        self.label(query, "SELECT pessoa_favorita FROM universo LIMIT 1;", 11, self.PURPLE, font="Consolas", bg="#0a0810").pack(anchor="w")
        self.label(query, f"> {NOME_DELA}", 11, self.GREEN, bold=True, font="Consolas", bg="#0a0810").pack(anchor="w", pady=(7, 0))

        footer = tk.Frame(body, bg=self.PANEL)
        footer.pack(fill="x", pady=(10, 0))
        self.label(
            footer,
            "Existe uma validação pendente antes da próxima release.",
            10,
            self.MUTED,
        ).pack(side="left")
        self.button(footer, "EXECUTAR VALIDAÇÃO  →", self.start_quiz, primary=True).pack(side="right")

    # --------------------------------------------------------
    # SCENE 3 - QUIZ
    # --------------------------------------------------------
    def start_quiz(self):
        self.score = 0
        self.index = 0
        self.show_question()

    def show_question(self):
        self.clear_stage()
        self.answer_locked = False
        q = QUESTOES[self.index]
        self.topbar(f"validation/{q['categoria'].lower().replace(' ', '_')}")

        outer = tk.Frame(self.stage, bg=self.PANEL)
        outer.pack(fill="both", expand=True, padx=48, pady=24)

        head = tk.Frame(outer, bg=self.PANEL)
        head.pack(fill="x")
        self.label(head, q["categoria"], 9, self.PINK, bold=True, font="Consolas").pack(side="left")
        self.label(
            head,
            f"CHECK {self.index + 1:02d}/{len(QUESTOES):02d}",
            9,
            self.MUTED,
            bold=True,
            font="Consolas",
        ).pack(side="right")

        progress_bg = tk.Frame(outer, bg=self.LINE, height=5)
        progress_bg.pack(fill="x", pady=(13, 28))
        progress_bg.pack_propagate(False)
        tk.Frame(progress_bg, bg=self.PINK).place(
            relx=0,
            rely=0,
            relwidth=(self.index + 1) / len(QUESTOES),
            relheight=1,
        )

        self.label(
            outer,
            q["pergunta"],
            19,
            self.TEXT,
            bold=True,
            wraplength=760,
            justify="left",
        ).pack(anchor="w", pady=(0, 24))

        self.answer_buttons = []
        answers = tk.Frame(outer, bg=self.PANEL)
        answers.pack(fill="both", expand=True)

        letters = ["A", "B", "C", "D"]
        for i, option in enumerate(q["opcoes"]):
            btn = tk.Button(
                answers,
                text=f"  {letters[i]}   {option}",
                command=lambda idx=i: self.answer(idx),
                bg=self.PANEL_2,
                fg=self.TEXT,
                activebackground="#34253b",
                activeforeground=self.TEXT,
                relief="flat",
                bd=0,
                cursor="hand2",
                font=("Segoe UI", 10),
                anchor="w",
                padx=16,
                pady=11,
            )
            btn.pack(fill="x", pady=5)
            self.answer_buttons.append(btn)

        self.feedback = self.label(outer, "", 10, self.GREEN, bold=True, font="Consolas")
        self.feedback.pack(anchor="w", pady=(16, 0))

    def answer(self, choice):
        if self.answer_locked:
            return
        self.answer_locked = True

        q = QUESTOES[self.index]
        correct = q["correta"]
        for b in self.answer_buttons:
            b.configure(state="disabled")

        self.answer_buttons[correct].configure(
            state="normal",
            bg="#24392f",
            fg=self.GREEN,
        )

        if choice == correct:
            self.score += 1
            text = f"[PASS] {q['feedback']}"
        else:
            text = "[OVERRIDE] Resposta aceita. Este sistema é tendencioso a seu favor."

        self.feedback.configure(text=text)
        next_text = "GERAR RELATÓRIO FINAL  →" if self.index == len(QUESTOES) - 1 else "PRÓXIMO CHECK  →"
        self.button(self.stage, next_text, self.next_question, primary=True).pack(pady=(0, 24))

    def next_question(self):
        if self.index < len(QUESTOES) - 1:
            self.index += 1
            self.show_question()
        else:
            self.show_report()

    # --------------------------------------------------------
    # SCENE 4 - REPORT
    # --------------------------------------------------------
    def show_report(self):
        self.clear_stage()
        self.topbar("final_report", "SUCCESS")

        body = tk.Frame(self.stage, bg=self.PANEL)
        body.pack(fill="both", expand=True, padx=48, pady=25)

        self.label(body, "VALIDATION COMPLETE", 9, self.GREEN, bold=True, font="Consolas").pack(anchor="w")
        self.label(body, "Compatibilidade afetiva: 100%", 28, self.TEXT, bold=True).pack(anchor="w", pady=(8, 5))
        self.label(
            body,
            f"Score técnico: {self.score}/{len(QUESTOES)} • score oficial: APROVADA PARA SEMPRE",
            10,
            self.MUTED,
            font="Consolas",
        ).pack(anchor="w", pady=(0, 20))

        report = tk.Frame(body, bg="#0a0810", padx=22, pady=18)
        report.pack(fill="x", pady=(0, 18))
        lines = [
            ("integridade_do_relacionamento", "OK"),
            ("qualidade_das_memorias", "EXCELENTE"),
            ("risco_de_rollback", "0.00%"),
            ("previsao_de_futuro", "PROMISSORA"),
            ("recomendacao_modelo", "CONTINUAR_JUNTAS"),
        ]
        for key, value in lines:
            row = tk.Frame(report, bg="#0a0810")
            row.pack(fill="x", pady=3)
            self.label(row, key, 10, self.MUTED, font="Consolas", bg="#0a0810").pack(side="left")
            self.label(row, value, 10, self.GREEN, bold=True, font="Consolas", bg="#0a0810").pack(side="right")

        self.label(
            body,
            "Há apenas uma ação pendente para concluir o deploy.",
            11,
            self.TEXT,
        ).pack(anchor="w", pady=(12, 15))
        self.button(body, "ABRIR SOLICITAÇÃO DE DEPLOY  →", self.show_contract, primary=True).pack(anchor="w")

    # --------------------------------------------------------
    # SCENE 5 - CONTRACT / FINAL
    # --------------------------------------------------------
    def show_contract(self):
        self.clear_stage()
        self.topbar("deployment_approval", "ACTION REQUIRED")

        body = tk.Frame(self.stage, bg=self.PANEL)
        body.pack(fill="both", expand=True, padx=55, pady=26)

        self.label(body, "CHANGE REQUEST #LOVE-∞", 9, self.PINK, bold=True, font="Consolas").pack(anchor="w")
        self.label(body, "Renovação automática do nosso contrato", 26, self.TEXT, bold=True).pack(anchor="w", pady=(8, 5))
        self.label(
            body,
            "Escopo: continuar sendo nós duas, com novas memórias, novas versões e zero intenção de rollback.",
            11,
            self.MUTED,
            wraplength=760,
            justify="left",
        ).pack(anchor="w", pady=(0, 22))

        contract = tk.Frame(body, bg=self.PANEL_2, padx=22, pady=18)
        contract.pack(fill="x")
        fields = [
            ("OWNER", SEU_NOME),
            ("APPROVER", NOME_DELA),
            ("ENVIRONMENT", "production"),
            ("DURATION", "indefinida"),
            ("ROLLBACK PLAN", "não aplicável"),
            ("RISK", "risco alto de excesso de carinho"),
        ]
        for key, value in fields:
            row = tk.Frame(contract, bg=self.PANEL_2)
            row.pack(fill="x", pady=3)
            self.label(row, key, 9, self.MUTED, bold=True, font="Consolas", bg=self.PANEL_2).pack(side="left")
            self.label(row, value, 9, self.TEXT, font="Consolas", bg=self.PANEL_2).pack(side="right")

        self.label(body, "Você aprova esta release?", 16, self.TEXT, bold=True).pack(anchor="w", pady=(24, 14))
        actions = tk.Frame(body, bg=self.PANEL, height=55)
        actions.pack(fill="x")

        self.button(actions, "SIM, DEPLOY AGORA  ♡", self.show_letter, primary=True).pack(side="left")
        self.no_btn = self.button(actions, "PRECISO REVISAR", self._move_no_button)
        self.no_btn.pack(side="left", padx=12)

        self.label(
            body,
            "* mudança irreversível apenas no sentido de eu continuar te amando amanhã também",
            8,
            self.MUTED,
            font="Consolas",
        ).pack(anchor="w", pady=(14, 0))

    def _move_no_button(self):
        messages = [
            "REVISÃO JÁ FEITA",
            "RFC APROVADA",
            "SEM BLOQUEIOS",
            "TENTA O BOTÃO ROSA 😌",
        ]
        self.no_btn.configure(text=random.choice(messages))
        # pequeno deslocamento visual sem tirar o botão da tela
        try:
            self.no_btn.pack_configure(padx=random.randint(18, 90))
        except Exception:
            pass

    def show_letter(self):
        self.clear_stage()
        self.topbar("release_notes", "DEPLOYED")

        body = tk.Frame(self.stage, bg=self.PANEL)
        body.pack(fill="both", expand=True, padx=58, pady=24)

        self.label(body, "RELEASE SUCCESSFUL  ♡", 9, self.GREEN, bold=True, font="Consolas").pack(anchor="w")
        self.label(body, "Agora sem linguagem técnica.", 26, self.TEXT, bold=True).pack(anchor="w", pady=(8, 16))

        letter = tk.Frame(body, bg="#fff7fb", padx=28, pady=24)
        letter.pack(fill="both", expand=True)

        tk.Label(
            letter,
            text=f"Para {NOME_DELA},",
            bg="#fff7fb",
            fg="#553441",
            font=("Georgia", 15, "bold"),
            anchor="w",
        ).pack(fill="x", pady=(0, 12))

        tk.Label(
            letter,
            text=CARTA_FINAL,
            bg="#fff7fb",
            fg="#4b3540",
            font=("Georgia", 11),
            wraplength=760,
            justify="left",
            anchor="nw",
        ).pack(fill="both", expand=True)

        tk.Label(
            letter,
            text=f"— {SEU_NOME}  ♡",
            bg="#fff7fb",
            fg="#a14067",
            font=("Georgia", 12, "bold"),
            anchor="e",
        ).pack(fill="x", pady=(12, 0))

        self._celebrate()

    def _celebrate(self):
        width = max(self.canvas.winfo_width(), 1120)
        height = max(self.canvas.winfo_height(), 720)
        for _ in range(24):
            item = self.canvas.create_text(
                random.randint(20, width - 20),
                height + random.randint(0, 220),
                text=random.choice(["♥", "♡", "✦"]),
                fill=random.choice([self.PINK, self.PINK_2, self.PURPLE, self.GREEN]),
                font=("Segoe UI Symbol", random.randint(13, 23), "bold"),
            )
            self.canvas.tag_lower(item, self.stage_window)
            self.hearts.append((item, random.uniform(0.45, 1.1)))


def main():
    root = tk.Tk()
    LoveSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()
