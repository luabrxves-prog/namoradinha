import tkinter as tk
from tkinter import font

BG = "#0b0910"
SURFACE = "#15111c"
CARD = "#201827"
CARD_2 = "#291d31"
TEXT = "#fff8fc"
MUTED = "#aa98a8"
PINK = "#ff6fa9"
PINK_2 = "#ff9bc4"
GREEN = "#7de5ae"
RED = "#ff6e83"
PURPLE = "#c9a7ff"
LINE = "#392b40"
WHITE = "#fffafb"

PROGRAMMING = [
    {
        "tag": "PYTHON / EXCEPTIONS",
        "q": "Em Python, qual bloco é executado mesmo que aconteça um erro dentro de try?",
        "options": ["except", "else", "finally", "raise"],
        "correct": 2,
        "answer": "finally",
        "success": "Isso. finally fica até o fim — comportamento que eu apoio bastante por aqui. ♡",
    },
    {
        "tag": "SQL / AGREGAÇÃO",
        "q": "Depois de um GROUP BY, qual cláusula você usa para filtrar os grupos pelo resultado de uma agregação?",
        "options": ["WHERE", "HAVING", "ORDER BY", "DISTINCT"],
        "correct": 1,
        "answer": "HAVING",
        "success": "Perfeito. HAVING passou na validação. Nosso dataset segue consistente. ♡",
    },
    {
        "tag": "GIT / VERSIONAMENTO",
        "q": "Depois de git add ., qual comando registra um snapshot das mudanças no histórico local?",
        "options": [
            "git push origin main",
            "git checkout -b amor",
            "git commit -m \"eu te amo\"",
            "git status --forever",
        ],
        "correct": 2,
        "answer": "git commit -m \"eu te amo\"",
        "success": "Commit aprovado. Mensagem excelente, inclusive. ♡",
    },
]

US = [
    {
        "q": "Qual foi o dia do nosso primeiro encontro?",
        "options": ["28 de março", "2 de abril", "10 de abril", "22 de abril"],
        "correct": 1,
        "right": "Mais que sua obrigação 😌 2 de abril está devidamente versionado na minha memória.",
        "wrong": "FATAL ERROR: COMO ASSIM AMOR? 😭 O sistema sofreu uma pequena pane emocional.",
        "crash": True,
    },
    {
        "q": "Qual é a nossa música?",
        "options": [
            "Me Chamando de Paixão — Jorge Ben Jor",
            "Meu — Djavan",
            "Deusa do Amor — Caetano Veloso",
            "Ensaio Sobre Ela — Cícero",
        ],
        "correct": 1,
        "right": "Correto: Meu — Djavan. Essa tabela eu não aceito inconsistência. ♡",
        "wrong": "ALERTA: playlist corrompida. A resposta era Meu — Djavan.",
    },
    {
        "q": "Em qual mês falamos o primeiro “eu te amo”?",
        "options": ["Março", "Abril", "Maio", "Junho"],
        "correct": 2,
        "right": "Maio. Registro encontrado com integridade de 100%. ♡",
        "wrong": "Quase! O primeiro “eu te amo” foi em maio. Coração descontado, amor preservado.",
    },
    {
        "q": "O que a gente mais gosta de fazer juntas?",
        "options": ["Jogar", "Ficar quietinhas", "Sair", "Ir pra praia"],
        "correct": "all",
        "right": "Aceito. Na verdade eu gosto de fazer tudo com você. Até não fazer nada. ♡",
        "wrong": "",
    },
]

ME = [
    {
        "q": "Qual é a minha comida preferida?",
        "options": ["Estrogonofe", "Rabada", "Salmão", "Japonês"],
        "correct": "all",
        "right": "Amor, eu gosto de tudo 😭 Essa pergunta foi arquitetada sem requisito funcional.",
    },
    {
        "q": "Qual é o meu jogo preferido?",
        "options": ["Red Dead Redemption 2", "Valorant", "League of Legends", "Detroit: Become Human"],
        "correct": 3,
        "right": "Detroit: Become Human. Finalmente um dado confiável nesse pipeline. 🎮",
        "wrong": "O certo é Detroit: Become Human. Mas esse sistema é tendencioso a seu favor, então eu ainda te amo.",
    },
    {
        "q": "Qual é a minha cor preferida?",
        "options": ["Rosa", "Azul", "Roxo", "Preto"],
        "correct": None,
        "right": "",
        "wrong": "Nenhuma 😌 Você sabe que é marrom. Essa era uma questão-trap e não vale perder ponto.",
        "trap": True,
    },
    {
        "q": "Qual seria o dia perfeito pra mim?",
        "options": ["Praia", "Bar", "Restaurante", "Festa"],
        "correct": None,
        "right": "",
        "wrong": "Nenhuma das opções. Um dia com você. Te amo. ♡",
        "trap": True,
    },
]


class LoveSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("love_system.exe")
        self.root.geometry("1180x760")
        self.root.minsize(1000, 690)
        self.root.configure(bg=BG)

        self.prog_index = 0
        self.prog_attempts = 0
        self.prog_score = 0
        self.us_index = 0
        self.us_score = 0
        self.lives = 4
        self.me_index = 0
        self.me_score = 0
        self.locked = False
        self.jobs = []

        self.frame = tk.Frame(root, bg=SURFACE, highlightbackground=LINE, highlightthickness=1)
        self.frame.pack(fill="both", expand=True, padx=28, pady=24)

        self.header = tk.Frame(self.frame, bg=SURFACE, height=58)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        tk.Label(self.header, text="●", bg=SURFACE, fg=GREEN, font=("Consolas", 12, "bold")).pack(side="left", padx=(22, 8))
        tk.Label(self.header, text="love_system.exe", bg=SURFACE, fg=TEXT, font=("Consolas", 10, "bold")).pack(side="left")
        self.path = tk.Label(self.header, text="  / boot", bg=SURFACE, fg=MUTED, font=("Consolas", 9))
        self.path.pack(side="left")
        self.status = tk.Label(self.header, text="READY", bg=CARD_2, fg=GREEN, font=("Consolas", 9, "bold"), padx=12, pady=5)
        self.status.pack(side="right", padx=22)
        tk.Frame(self.frame, bg=LINE, height=1).pack(fill="x")

        self.body = tk.Frame(self.frame, bg=SURFACE)
        self.body.pack(fill="both", expand=True)

        self.show_home()

    def clear(self):
        for job in self.jobs:
            try:
                self.root.after_cancel(job)
            except Exception:
                pass
        self.jobs.clear()
        for w in self.body.winfo_children():
            w.destroy()

    def set_head(self, path, status="ONLINE", status_color=GREEN):
        self.path.configure(text=f"  / {path}")
        self.status.configure(text=status, fg=status_color)

    def label(self, parent, text, size=12, color=TEXT, bold=False, family="Segoe UI", **kw):
        return tk.Label(
            parent,
            text=text,
            bg=kw.pop("bg", parent.cget("bg")),
            fg=color,
            font=(family, size, "bold" if bold else "normal"),
            **kw,
        )

    def pill(self, parent, text, color=PINK):
        box = tk.Frame(parent, bg=CARD_2, padx=10, pady=5)
        self.label(box, text, 9, color, True, "Consolas").pack()
        return box

    def button(self, parent, text, command, primary=False, width=None, big=False):
        bg = PINK if primary else CARD_2
        fg = BG if primary else TEXT
        active = PINK_2 if primary else "#3a2943"
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
            font=("Segoe UI", 12 if big else 10, "bold"),
            padx=24 if big else 18,
            pady=15 if big else 11,
            width=width,
        )

    def card(self, parent, padx=18, pady=16, bg=CARD):
        return tk.Frame(parent, bg=bg, padx=padx, pady=pady, highlightbackground=LINE, highlightthickness=1)

    def title_block(self, parent, eyebrow, title, subtitle=None):
        self.label(parent, eyebrow.upper(), 9, PINK, True, "Consolas").pack(anchor="w")
        self.label(parent, title, 26, TEXT, True).pack(anchor="w", pady=(6, 4))
        if subtitle:
            self.label(parent, subtitle, 10, MUTED, wraplength=900, justify="left").pack(anchor="w")

    def show_home(self):
        self.clear()
        self.set_head("boot_sequence", "READY")
        wrap = tk.Frame(self.body, bg=SURFACE)
        wrap.pack(fill="both", expand=True, padx=42, pady=36)

        hero = tk.Frame(wrap, bg=SURFACE)
        hero.pack(fill="x")
        left = tk.Frame(hero, bg=SURFACE)
        left.pack(side="left", fill="both", expand=True)
        right = self.card(hero, padx=22, pady=20, bg="#0b0810")
        right.pack(side="right", fill="y", padx=(24, 0))

        self.pill(left, "2 MESES • LUANA + YASMIN", PINK).pack(anchor="w")
        self.label(left, "Um aplicativo especialmente\npara minha amada,", 30, TEXT, True).pack(anchor="w", pady=(18, 6))
        self.label(left, "porque aparentemente eu virei dev.", 18, PINK_2, True).pack(anchor="w")
        self.label(
            left,
            "Um pequeno sistema em produção para validar duas coisas: seu conhecimento técnico e o quanto você sabe sobre nós.",
            11, MUTED, wraplength=600, justify="left"
        ).pack(anchor="w", pady=(16, 22))

        cta = self.button(left, "ABRIR SISTEMA  →", self.show_dashboard, primary=True, big=True)
        cta.pack(anchor="w", pady=(4, 0))

        self.label(right, "BOOT LOG", 9, PURPLE, True, "Consolas", bg="#0b0810").pack(anchor="w")
        logs = [
            "[OK] memórias carregadas",
            "[OK] cluster: coracao_da_yasmin",
            "[OK] credencial: meu bichinho",
            "[OK] identidade: Meu amor",
            "[WARN] amor excedeu limite",
            "[OK] meu aplicativozinho ∞",
            "",
            "SYSTEM READY.",
        ]
        self.label(right, "\n".join(logs), 10, GREEN, False, "Consolas", bg="#0b0810", justify="left").pack(anchor="w", pady=(14, 0))

        bottom = tk.Frame(wrap, bg=SURFACE)
        bottom.pack(fill="x", side="bottom", pady=(30, 0))
        for i, (k, v) in enumerate([("BUILD", "love.v2"), ("OWNER", "Luana"), ("TARGET", "Yasmin")]):
            c = self.card(bottom, padx=14, pady=10)
            c.grid(row=0, column=i, padx=(0 if i == 0 else 8, 0), sticky="ew")
            bottom.grid_columnconfigure(i, weight=1)
            self.label(c, k, 8, MUTED, True, "Consolas").pack(anchor="w")
            self.label(c, v, 11, TEXT, True, "Consolas").pack(anchor="w", pady=(4, 0))

    def show_dashboard(self):
        self.clear()
        self.set_head("relationship_health", "ONLINE")
        wrap = tk.Frame(self.body, bg=SURFACE)
        wrap.pack(fill="both", expand=True, padx=42, pady=28)

        self.title_block(wrap, "Relationship Health", "Todos os sistemas operacionais. ♡", "Dois meses em produção. Nenhum incidente crítico registrado.")

        grid = tk.Frame(wrap, bg=SURFACE)
        grid.pack(fill="x", pady=22)
        metrics = [
            ("COMPATIBILIDADE", "100%", "modelo altamente confiante"),
            ("UPTIME", "24/7", "sem janela de manutenção"),
            ("BEIJOS DADOS", "< 1000", "precisamos escalar isso"),
            ("BRIGAS", "0", "se eu não lembro, nunca existiu"),
            ("“EU TE AMO”", "∞", "contador estourou"),
        ]
        positions = [(0,0),(0,1),(0,2),(1,0),(1,1)]
        for idx, (name, value, sub) in enumerate(metrics):
            r, c = positions[idx]
            card = self.card(grid, padx=16, pady=14)
            card.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
            grid.grid_columnconfigure(c, weight=1)
            self.label(card, name, 8, MUTED, True, "Consolas").pack(anchor="w")
            self.label(card, value, 20, TEXT, True, "Consolas").pack(anchor="w", pady=(7, 2))
            self.label(card, sub, 8, GREEN, False, "Consolas").pack(anchor="w")

        action = self.card(wrap, padx=18, pady=16, bg="#0b0810")
        action.pack(fill="x", pady=(10, 0))
        l = tk.Frame(action, bg="#0b0810")
        l.pack(side="left", fill="both", expand=True)
        self.label(l, "PRÓXIMA ETAPA", 8, PURPLE, True, "Consolas", bg="#0b0810").pack(anchor="w")
        self.label(l, "Agora quero que você responda com todo o seu conhecimento.", 12, TEXT, True, bg="#0b0810").pack(anchor="w", pady=(4, 2))
        self.label(l, "São 3 perguntas de programação. Você tem duas tentativas por pergunta.", 9, MUTED, bg="#0b0810").pack(anchor="w")
        self.button(action, "INICIAR TESTE  →", self.start_programming, primary=True).pack(side="right", padx=(18, 0))

    def start_programming(self):
        self.prog_index = 0
        self.prog_attempts = 0
        self.prog_score = 0
        self.render_programming()

    def render_programming(self):
        self.clear()
        self.set_head("knowledge_check/programming", "TESTING")
        self.locked = False
        self.prog_attempts = 0
        q = PROGRAMMING[self.prog_index]

        wrap = tk.Frame(self.body, bg=SURFACE)
        wrap.pack(fill="both", expand=True, padx=48, pady=30)

        top = tk.Frame(wrap, bg=SURFACE)
        top.pack(fill="x")
        self.pill(top, q["tag"], PURPLE).pack(side="left")
        self.label(top, f"{self.prog_index + 1} / {len(PROGRAMMING)}", 10, MUTED, True, "Consolas").pack(side="right")

        self.label(wrap, q["q"], 23, TEXT, True, wraplength=900, justify="left").pack(anchor="w", pady=(28, 22))
        self.option_box = tk.Frame(wrap, bg=SURFACE)
        self.option_box.pack(fill="x")
        self.option_buttons = []
        for i, opt in enumerate(q["options"]):
            b = tk.Button(
                self.option_box,
                text=f"{chr(65+i)}   {opt}",
                command=lambda n=i: self.answer_programming(n),
                bg=CARD,
                fg=TEXT,
                activebackground=CARD_2,
                activeforeground=TEXT,
                relief="flat",
                bd=0,
                cursor="hand2",
                anchor="w",
                font=("Segoe UI", 11),
                padx=18,
                pady=13,
            )
            b.pack(fill="x", pady=5)
            self.option_buttons.append(b)

        self.prog_feedback = self.label(wrap, "Tentativas disponíveis: 2", 10, MUTED, True, "Consolas", wraplength=900, justify="left")
        self.prog_feedback.pack(anchor="w", pady=(18, 0))
        self.prog_next = self.button(wrap, "PRÓXIMA PERGUNTA  →", self.next_programming, primary=True)

    def answer_programming(self, selected):
        if self.locked:
            return
        q = PROGRAMMING[self.prog_index]
        if selected == q["correct"]:
            self.locked = True
            self.prog_score += 1
            self.option_buttons[selected].configure(bg="#20372a", fg=GREEN)
            for b in self.option_buttons:
                b.configure(state="disabled")
            self.prog_feedback.configure(text="[PASS] " + q["success"], fg=GREEN)
            self.prog_next.configure(text="CONTINUAR  →" if self.prog_index == len(PROGRAMMING)-1 else "PRÓXIMA PERGUNTA  →")
            self.prog_next.pack(anchor="e", pady=(20, 0))
            return

        self.prog_attempts += 1
        self.option_buttons[selected].configure(bg="#3b2028", fg=RED)
        if self.prog_attempts == 1:
            self.prog_feedback.configure(text="Quase, amor. Respira, lê de novo e tenta mais uma vez. Agora vai. ♡", fg=PINK_2)
            self.option_buttons[selected].configure(state="disabled")
        else:
            self.locked = True
            for b in self.option_buttons:
                b.configure(state="disabled")
            self.option_buttons[q["correct"]].configure(bg="#20372a", fg=GREEN, disabledforeground=GREEN)
            self.prog_feedback.configure(
                text=f"Tudo bem, amor. A resposta era {q['answer']}. Eu te amo mesmo assim. ♡",
                fg=PINK_2,
            )
            self.prog_next.configure(text="CONTINUAR  →" if self.prog_index == len(PROGRAMMING)-1 else "PRÓXIMA PERGUNTA  →")
            self.prog_next.pack(anchor="e", pady=(20, 0))

    def next_programming(self):
        if self.prog_index < len(PROGRAMMING)-1:
            self.prog_index += 1
            self.render_programming()
        else:
            self.show_us_intro()

    def show_us_intro(self):
        self.clear()
        self.set_head("knowledge_check/us", "NEW STAGE")
        wrap = tk.Frame(self.body, bg=SURFACE)
        wrap.pack(fill="both", expand=True, padx=48, pady=42)

        self.pill(wrap, "FASE 02 • NÓS DUAS", PINK).pack(anchor="w")
        self.label(wrap, "Agora que você já testou seu\nconhecimento em programação…", 29, TEXT, True).pack(anchor="w", pady=(18, 8))
        self.label(wrap, "quero saber se tá sabendo de nós.", 21, PINK_2, True).pack(anchor="w")
        self.label(wrap, "Você começa com 4 corações. Errou? O sistema cobra um pedágio emocional. Acertou? Mais que sua obrigação.", 11, MUTED, wraplength=800, justify="left").pack(anchor="w", pady=(18, 22))

        preview = self.card(wrap, padx=18, pady=14)
        preview.pack(fill="x", pady=(4, 24))
        self.label(preview, "VIDAS DISPONÍVEIS", 8, MUTED, True, "Consolas").pack(anchor="w")
        self.label(preview, "♥  ♥  ♥  ♥", 24, PINK, True, "Segoe UI Symbol").pack(anchor="w", pady=(6, 0))

        self.button(wrap, "COMEÇAR TESTE SOBRE NÓS  →", self.start_us, primary=True, big=True).pack(anchor="w")

    def start_us(self):
        self.us_index = 0
        self.us_score = 0
        self.lives = 4
        self.render_us()

    def hearts_text(self):
        return "♥ " * self.lives + "♡ " * (4 - self.lives)

    def render_us(self):
        self.clear()
        self.set_head("knowledge_check/us", "HEARTS ACTIVE")
        self.locked = False
        q = US[self.us_index]

        wrap = tk.Frame(self.body, bg=SURFACE)
        wrap.pack(fill="both", expand=True, padx=48, pady=28)
        top = tk.Frame(wrap, bg=SURFACE)
        top.pack(fill="x")
        self.pill(top, "NÓS DUAS", PINK).pack(side="left")
        self.life_label = self.label(top, self.hearts_text(), 17, PINK, True, "Segoe UI Symbol")
        self.life_label.pack(side="right")
        self.label(wrap, f"Pergunta {self.us_index + 1} de {len(US)}", 9, MUTED, True, "Consolas").pack(anchor="w", pady=(20, 5))
        self.label(wrap, q["q"], 24, TEXT, True, wraplength=900, justify="left").pack(anchor="w", pady=(0, 20))

        self.us_buttons = []
        for i, opt in enumerate(q["options"]):
            b = tk.Button(
                wrap, text=f"{chr(65+i)}   {opt}",
                command=lambda n=i: self.answer_us(n),
                bg=CARD, fg=TEXT, activebackground=CARD_2, activeforeground=TEXT,
                relief="flat", bd=0, cursor="hand2", anchor="w",
                font=("Segoe UI", 11), padx=18, pady=13,
            )
            b.pack(fill="x", pady=5)
            self.us_buttons.append(b)

        self.us_feedback = self.label(wrap, "", 10, GREEN, True, "Consolas", wraplength=900, justify="left")
        self.us_feedback.pack(anchor="w", pady=(18, 0))
        self.us_next = self.button(wrap, "PRÓXIMA  →", self.next_us, primary=True)

    def answer_us(self, selected):
        if self.locked:
            return
        self.locked = True
        q = US[self.us_index]
        for b in self.us_buttons:
            b.configure(state="disabled")

        correct = q["correct"] == "all" or selected == q["correct"]
        if correct:
            self.us_score += 1
            self.us_buttons[selected].configure(bg="#20372a", fg=GREEN, disabledforeground=GREEN)
            self.us_feedback.configure(text=q["right"], fg=GREEN)
        else:
            self.lives = max(0, self.lives - 1)
            self.life_label.configure(text=self.hearts_text(), fg=RED)
            if isinstance(q["correct"], int):
                self.us_buttons[q["correct"]].configure(bg="#20372a", fg=GREEN, disabledforeground=GREEN)
            self.us_buttons[selected].configure(bg="#3b2028", fg=RED, disabledforeground=RED)
            self.us_feedback.configure(text=q["wrong"], fg=RED)
            if q.get("crash"):
                self.fake_crash()

        self.us_next.configure(text="IR PARA A PRÓXIMA FASE  →" if self.us_index == len(US)-1 else "PRÓXIMA  →")
        self.us_next.pack(anchor="e", pady=(18, 0))

    def fake_crash(self):
        overlay = tk.Frame(self.body, bg="#2a0c14", highlightbackground=RED, highlightthickness=2)
        overlay.place(relx=.5, rely=.5, anchor="center", width=660, height=190)
        self.label(overlay, "SYSTEM PANIC", 10, RED, True, "Consolas", bg="#2a0c14").pack(pady=(22, 4))
        self.label(overlay, "COMO ASSIM VOCÊ ERROU O PRIMEIRO ENCONTRO? 😭", 17, WHITE, True, bg="#2a0c14").pack()
        self.label(overlay, "Reiniciando dignidade do sistema…", 10, MUTED, False, "Consolas", bg="#2a0c14").pack(pady=(10, 0))
        job = self.root.after(1500, overlay.destroy)
        self.jobs.append(job)

    def next_us(self):
        if self.us_index < len(US)-1:
            self.us_index += 1
            self.render_us()
        else:
            self.show_me_intro()

    def show_me_intro(self):
        self.clear()
        self.set_head("knowledge_check/luana", "FINAL QUIZ")
        wrap = tk.Frame(self.body, bg=SURFACE)
        wrap.pack(fill="both", expand=True, padx=48, pady=44)
        self.pill(wrap, "FASE 03 • VOCÊ ME CONHECE?", PURPLE).pack(anchor="w")
        self.label(wrap, "Agora vamos verificar\na base de dados “Luana”.", 29, TEXT, True).pack(anchor="w", pady=(18, 8))
        self.label(wrap, "Algumas perguntas são honestas. Outras foram claramente escritas por alguém tendenciosa.", 11, MUTED, wraplength=780, justify="left").pack(anchor="w", pady=(10, 24))
        self.button(wrap, "INICIAR ÚLTIMA FASE  →", self.start_me, primary=True, big=True).pack(anchor="w")

    def start_me(self):
        self.me_index = 0
        self.me_score = 0
        self.render_me()

    def render_me(self):
        self.clear()
        self.set_head("knowledge_check/luana", "TESTING")
        self.locked = False
        q = ME[self.me_index]

        wrap = tk.Frame(self.body, bg=SURFACE)
        wrap.pack(fill="both", expand=True, padx=48, pady=28)
        top = tk.Frame(wrap, bg=SURFACE)
        top.pack(fill="x")
        self.pill(top, "CONHECIMENTO SOBRE LUANA", PURPLE).pack(side="left")
        self.label(top, f"{self.me_index + 1} / {len(ME)}", 10, MUTED, True, "Consolas").pack(side="right")

        self.label(wrap, q["q"], 24, TEXT, True, wraplength=900, justify="left").pack(anchor="w", pady=(28, 20))
        self.me_buttons = []
        for i, opt in enumerate(q["options"]):
            b = tk.Button(
                wrap, text=f"{chr(65+i)}   {opt}",
                command=lambda n=i: self.answer_me(n),
                bg=CARD, fg=TEXT, activebackground=CARD_2, activeforeground=TEXT,
                relief="flat", bd=0, cursor="hand2", anchor="w",
                font=("Segoe UI", 11), padx=18, pady=13,
            )
            b.pack(fill="x", pady=5)
            self.me_buttons.append(b)

        self.me_feedback = self.label(wrap, "", 10, GREEN, True, "Consolas", wraplength=900, justify="left")
        self.me_feedback.pack(anchor="w", pady=(18, 0))
        self.me_next = self.button(wrap, "PRÓXIMA  →", self.next_me, primary=True)

    def answer_me(self, selected):
        if self.locked:
            return
        self.locked = True
        q = ME[self.me_index]
        for b in self.me_buttons:
            b.configure(state="disabled")

        if q["correct"] == "all":
            self.me_score += 1
            self.me_buttons[selected].configure(bg="#20372a", fg=GREEN, disabledforeground=GREEN)
            self.me_feedback.configure(text=q["right"], fg=GREEN)
        elif q.get("trap"):
            self.me_score += 1
            self.me_buttons[selected].configure(bg="#33243b", fg=PINK_2, disabledforeground=PINK_2)
            self.me_feedback.configure(text=q["wrong"], fg=PINK_2)
        elif selected == q["correct"]:
            self.me_score += 1
            self.me_buttons[selected].configure(bg="#20372a", fg=GREEN, disabledforeground=GREEN)
            self.me_feedback.configure(text=q["right"], fg=GREEN)
        else:
            self.me_buttons[selected].configure(bg="#3b2028", fg=RED, disabledforeground=RED)
            self.me_buttons[q["correct"]].configure(bg="#20372a", fg=GREEN, disabledforeground=GREEN)
            self.me_feedback.configure(text=q["wrong"], fg=PINK_2)

        self.me_next.configure(text="VER SCORE FINAL  →" if self.me_index == len(ME)-1 else "PRÓXIMA  →")
        self.me_next.pack(anchor="e", pady=(18, 0))

    def next_me(self):
        if self.me_index < len(ME)-1:
            self.me_index += 1
            self.render_me()
        else:
            self.show_score()

    def show_score(self):
        self.clear()
        self.set_head("final_report", "PASSED")
        wrap = tk.Frame(self.body, bg=SURFACE)
        wrap.pack(fill="both", expand=True, padx=44, pady=28)

        self.title_block(wrap, "Final report", "Validação concluída com sucesso. ♡", "O algoritmo terminou a análise. A decisão técnica continua extremamente parcial.")
        scores = tk.Frame(wrap, bg=SURFACE)
        scores.pack(fill="x", pady=20)

        data = [
            ("PROGRAMAÇÃO", f"{self.prog_score}/3", "conhecimento técnico"),
            ("SOBRE NÓS", f"{self.us_score}/4", f"{self.lives} coração(ões) restante(s)"),
            ("SOBRE LUANA", f"{self.me_score}/4", "modelo tendencioso"),
            ("SCORE AFETIVO", "100%", "não negociável"),
        ]
        for i, (name, value, sub) in enumerate(data):
            card = self.card(scores, padx=15, pady=14)
            card.grid(row=0, column=i, padx=5, sticky="nsew")
            scores.grid_columnconfigure(i, weight=1)
            self.label(card, name, 8, MUTED, True, "Consolas").pack(anchor="w")
            self.label(card, value, 21, TEXT, True, "Consolas").pack(anchor="w", pady=(7, 2))
            self.label(card, sub, 8, GREEN, False, "Consolas").pack(anchor="w")

        report = self.card(wrap, padx=18, pady=14, bg="#0b0810")
        report.pack(fill="x", pady=(6, 18))
        for k, v in [
            ("compatibilidade", "100%"),
            ("risco_de_rollback", "0.00%"),
            ("recomendacao_modelo", "CONTINUAR_JUNTAS"),
            ("próxima_ação", "APROVAR_DEPLOY"),
        ]:
            row = tk.Frame(report, bg="#0b0810")
            row.pack(fill="x", pady=4)
            self.label(row, k, 9, MUTED, False, "Consolas", bg="#0b0810").pack(side="left")
            self.label(row, v, 9, GREEN, True, "Consolas", bg="#0b0810").pack(side="right")

        self.button(wrap, "ABRIR SOLICITAÇÃO DE DEPLOY  →", self.show_deploy, primary=True, big=True).pack(anchor="e")

    def show_deploy(self):
        self.clear()
        self.set_head("deployment_approval", "ACTION REQUIRED", PINK)
        wrap = tk.Frame(self.body, bg=SURFACE)
        wrap.pack(fill="both", expand=True, padx=48, pady=32)

        self.pill(wrap, "CHANGE REQUEST #LOVE-∞", PINK).pack(anchor="w")
        self.label(wrap, "Renovação da nossa versão em produção.", 27, TEXT, True).pack(anchor="w", pady=(16, 5))
        self.label(wrap, "Escopo: continuar sendo nós duas, criar novas memórias e manter rollback permanentemente desabilitado.", 10, MUTED, wraplength=880, justify="left").pack(anchor="w")

        card = self.card(wrap, padx=20, pady=16)
        card.pack(fill="x", pady=24)
        fields = [
            ("OWNER", "Luana"),
            ("APPROVER", "Yasmin"),
            ("ENVIRONMENT", "production"),
            ("DURATION", "indefinida"),
            ("ROLLBACK", "não aplicável"),
            ("RISK", "excesso de carinho"),
        ]
        for i, (k, v) in enumerate(fields):
            row = tk.Frame(card, bg=CARD)
            row.grid(row=i//2, column=i%2, sticky="ew", padx=12, pady=7)
            card.grid_columnconfigure(i%2, weight=1)
            self.label(row, k, 8, MUTED, True, "Consolas").pack(side="left")
            self.label(row, v, 9, TEXT, True, "Consolas").pack(side="right")

        self.label(wrap, "Yasmin, você aprova esta release?", 18, TEXT, True).pack(anchor="w", pady=(4, 12))
        buttons = tk.Frame(wrap, bg=SURFACE)
        buttons.pack(fill="x")
        self.button(buttons, "APROVAR DEPLOY ♡", self.show_letter, primary=True, big=True).pack(side="left")
        self.review_btn = self.button(buttons, "PRECISO REVISAR", self.review)
        self.review_btn.pack(side="left", padx=10)
        self.review_texts = ["REVISÃO CONCLUÍDA", "SEM BLOQUEIOS", "RFC APROVADA", "AMOR, CLICA NO ROSA 😌"]
        self.review_i = 0

    def review(self):
        self.review_btn.configure(text=self.review_texts[self.review_i % len(self.review_texts)])
        self.review_i += 1

    def show_letter(self):
        self.clear()
        self.set_head("release_notes", "DEPLOYED")
        wrap = tk.Frame(self.body, bg=SURFACE)
        wrap.pack(fill="both", expand=True, padx=42, pady=24)

        self.label(wrap, "RELEASE SUCCESSFUL ♡", 9, GREEN, True, "Consolas").pack(anchor="w")
        self.label(wrap, "Agora sem linguagem técnica.", 22, TEXT, True).pack(anchor="w", pady=(5, 12))

        paper = tk.Frame(wrap, bg=WHITE, padx=30, pady=24)
        paper.pack(fill="both", expand=True)
        self.label(paper, "Para Yasmin, meu bichinho,", 18, "#8c3b5c", True, "Georgia", bg=WHITE).pack(anchor="w")
        text = (
            "Eu podia simplesmente te entregar uma carta. Mas aparentemente eu virei dev, então resolvi construir um sistema inteiro para dizer uma coisa muito simples.\n\n"
            "Eu amo dividir a vida com você. Amo nossos momentos, nossas conversas, nossas risadas, jogar juntas, sair, ir pra praia e também ficar quietinha do seu lado sem precisar fazer absolutamente nada.\n\n"
            "Esses dois meses são só o começo de um banco de dados que eu espero nunca precisar limpar, arquivar ou colocar política de retenção. Quero continuar criando memória com você em todas as versões que vierem depois dessa.\n\n"
            "Obrigada por ser minha amada, meu bichinho e minha pessoa favorita.\n\n"
            "Feliz dois meses pra nós. Eu te amo. ❤️"
        )
        self.label(paper, text, 12, "#4b3540", False, "Georgia", bg=WHITE, wraplength=930, justify="left").pack(anchor="w", pady=(14, 8))
        self.label(paper, "— Luana ♡", 12, "#9e4168", True, "Georgia", bg=WHITE).pack(anchor="e")


def main():
    root = tk.Tk()
    LoveSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()
