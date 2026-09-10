import math
import random
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk, ImageFilter

BG = "#0d0b14"
PANEL = "#17131f"
PANEL_2 = "#211827"
PANEL_3 = "#2a1d31"
TEXT = "#fff7fb"
MUTED = "#ad9bad"
PINK = "#ff77aa"
PINK_2 = "#ff9fc4"
PURPLE = "#c7a6ff"
GREEN = "#84f0b4"
RED = "#ff718a"
LINE = "#382a3e"
BLACK = "#09070d"
WHITE = "#fff8fb"

PROGRAMMING = [
    {
        "tag": "PYTHON",
        "q": "Em Python, qual bloco é executado mesmo que aconteça um erro dentro de try?",
        "options": ["except", "else", "finally", "raise"],
        "correct": 2,
        "answer": "finally",
    },
    {
        "tag": "SQL",
        "q": "Depois de um GROUP BY, qual cláusula filtra os grupos usando o resultado de uma agregação?",
        "options": ["WHERE", "HAVING", "ORDER BY", "DISTINCT"],
        "correct": 1,
        "answer": "HAVING",
    },
    {
        "tag": "GIT",
        "q": "Depois de git add ., qual comando registra um snapshot das mudanças no histórico local?",
        "options": [
            "git push origin main",
            "git checkout -b amor",
            "git commit -m \"eu te amo\"",
            "git status",
        ],
        "correct": 2,
        "answer": "git commit -m \"eu te amo\"",
    },
]

US = [
    {
        "q": "Qual foi o dia do nosso primeiro encontro?",
        "options": ["28 de março", "2 de abril", "10 de abril", "22 de abril"],
        "correct": 1,
        "answer": "2 de abril",
        "right": "Mais que sua obrigação.",
        "panic": True,
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
        "answer": "Meu — Djavan",
    },
    {
        "q": "Em qual mês falamos o primeiro “eu te amo”?",
        "options": ["Março", "Abril", "Maio", "Junho"],
        "correct": 2,
        "answer": "Maio",
    },
    {
        "q": "O que a gente mais gosta de fazer juntas?",
        "options": ["Jogar", "Ficar quietinhas", "Sair", "Ir pra praia"],
        "correct": "all",
        "answer": "Tudo",
        "right": "Eu gosto de fazer tudo com você.",
    },
]

ME = [
    {
        "q": "Qual é a minha comida preferida?",
        "options": ["Estrogonofe", "Rabada", "Salmão", "Japonês"],
        "correct": "all",
        "answer": "Todas",
        "right": "Amor, eu gosto de tudo.",
    },
    {
        "q": "Qual é o meu jogo preferido?",
        "options": ["Red Dead Redemption 2", "Valorant", "League of Legends", "Detroit: Become Human"],
        "correct": 3,
        "answer": "Detroit: Become Human",
        "wrong": "O certo é Detroit: Become Human. Esse sistema é tendencioso a seu favor.",
    },
    {
        "q": "Qual é a minha cor preferida?",
        "options": ["Rosa", "Azul", "Roxo", "Preto"],
        "correct": None,
        "answer": "Marrom",
        "trap": True,
        "wrong": "Nenhuma. Você sabe que é marrom.",
    },
    {
        "q": "Qual seria o dia perfeito pra mim?",
        "options": ["Praia", "Bar", "Restaurante", "Festa"],
        "correct": None,
        "answer": "Um dia com você",
        "trap": True,
        "wrong": "Nenhuma das opções. Um dia com você. Te amo.",
    },
]

DEXTER = [
    {
        "q": "Qual é o trabalho do Dexter na Miami Metro?",
        "options": ["Detetive de homicídios", "Analista de padrões de sangue", "Médico legista", "Promotor"],
        "correct": 1,
        "answer": "Analista de padrões de sangue",
    },
    {
        "q": "Qual é o nome do barco do Dexter?",
        "options": ["Dark Passenger", "Slice of Life", "Bay Harbor", "Sea Escape"],
        "correct": 1,
        "answer": "Slice of Life",
    },
    {
        "q": "Qual é o nome da irmã do Dexter?",
        "options": ["Rita Morgan", "Lumen Morgan", "Debra Morgan", "Hannah Morgan"],
        "correct": 2,
        "answer": "Debra Morgan",
    },
    {
        "q": "Quem é revelado como o Ice Truck Killer?",
        "options": ["Arthur Mitchell", "Miguel Prado", "Brian Moser", "James Doakes"],
        "correct": 2,
        "answer": "Brian Moser",
    },
]

LETTER = (
    "Oi, amor! Só queria agradecer por esses dois meses, a cada dia que passa eu vejo o quanto eu sou feliz por ter você.\n\n"
    "Você foi definitivamente a vida sorrindo pra mim.\n\n"
    "Me considero uma mulher de sorte.\n\n"
    "E espero ter essa sorte por toda a vida.\n\n"
    "Obrigada por ser meu bichinho.\n\n"
    "Um breve(s) relato de um sentimento enorme."
)


class LoveSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("love_system.exe")
        self.root.geometry("1180x760")
        self.root.minsize(980, 680)
        self.root.configure(bg=BG)

        self.prog_score = 0
        self.us_score = 0
        self.me_score = 0
        self.dexter_score = 0
        self.lives = 4
        self.index = 0
        self.attempts = 0
        self.locked = False
        self.jobs = []
        self.art_refs = []
        self.bg_particles = []

        self.canvas = tk.Canvas(root, bg=BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self._resize)

        self.stage = tk.Frame(self.canvas, bg=PANEL)
        self.stage_window = self.canvas.create_window(590, 380, window=self.stage, width=1020, height=650)

        self._spawn_background()
        self._animate_background()

        self.top = tk.Frame(self.stage, bg=PANEL, height=55)
        self.top.pack(fill="x")
        self.top.pack_propagate(False)
        self.label(self.top, "●", 11, GREEN, True, "Consolas").pack(side="left", padx=(24, 8))
        self.label(self.top, "love_system.exe", 10, TEXT, True, "Consolas").pack(side="left")
        self.path = self.label(self.top, "  / boot_sequence", 9, MUTED, False, "Consolas")
        self.path.pack(side="left")
        self.status = self.label(self.top, "READY", 9, GREEN, True, "Consolas")
        self.status.pack(side="right", padx=24)
        tk.Frame(self.stage, bg=LINE, height=1).pack(fill="x")

        self.body = tk.Frame(self.stage, bg=PANEL)
        self.body.pack(fill="both", expand=True)
        self.show_home()

    # ---------- UI CORE ----------
    def _resize(self, event):
        self.canvas.coords(self.stage_window, event.width / 2, event.height / 2)
        self.canvas.itemconfigure(
            self.stage_window,
            width=min(1060, max(900, event.width - 90)),
            height=min(680, max(610, event.height - 70)),
        )

    def clear(self):
        for job in self.jobs:
            try:
                self.root.after_cancel(job)
            except Exception:
                pass
        self.jobs.clear()
        self.art_refs.clear()
        for w in self.body.winfo_children():
            w.destroy()

    def set_head(self, path, status="ONLINE", color=GREEN):
        self.path.configure(text=f"  / {path}")
        self.status.configure(text=status, fg=color)

    def label(self, parent, text, size=12, color=TEXT, bold=False, family="Segoe UI", **kw):
        return tk.Label(
            parent,
            text=text,
            bg=kw.pop("bg", parent.cget("bg")),
            fg=color,
            font=(family, size, "bold" if bold else "normal"),
            **kw,
        )

    def button(self, parent, text, command, primary=False, big=False):
        bg = PINK if primary else PANEL_2
        fg = BG if primary else TEXT
        active = PINK_2 if primary else PANEL_3
        b = tk.Button(
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
            font=("Segoe UI", 11 if big else 10, "bold"),
            padx=24 if big else 18,
            pady=14 if big else 10,
        )
        b.bind("<Enter>", lambda e: b.configure(bg=PINK_2 if primary else PANEL_3))
        b.bind("<Leave>", lambda e: b.configure(bg=PINK if primary else PANEL_2))
        return b

    def card(self, parent, bg=PANEL_2, padx=18, pady=16):
        return tk.Frame(parent, bg=bg, padx=padx, pady=pady, highlightbackground=LINE, highlightthickness=1)

    def eyebrow(self, parent, text, color=PINK):
        self.label(parent, text.upper(), 9, color, True, "Consolas").pack(anchor="w")

    # ---------- BACKGROUND ----------
    def _spawn_background(self):
        self.bg_particles.clear()
        for _ in range(34):
            x = random.randint(0, 1180)
            y = random.randint(0, 760)
            kind = random.choice(["·", "✦", "♡"])
            item = self.canvas.create_text(
                x, y, text=kind,
                fill=random.choice(["#332039", "#40233b", "#2b2133"]),
                font=("Segoe UI Symbol", random.randint(8, 15)),
            )
            self.canvas.tag_lower(item, self.stage_window)
            self.bg_particles.append((item, random.uniform(.07, .22)))

    def _animate_background(self):
        h = max(self.canvas.winfo_height(), 760)
        w = max(self.canvas.winfo_width(), 1180)
        for item, speed in self.bg_particles:
            x, y = self.canvas.coords(item)
            y -= speed
            if y < -20:
                y = h + 20
                x = random.randint(10, max(20, w - 10))
            self.canvas.coords(item, x, y)
        self.root.after(35, self._animate_background)

    # ---------- ART ----------
    def make_art(self, kind, width=330, height=230):
        im = Image.new("RGB", (width, height), "#0b0810")
        d = ImageDraw.Draw(im)

        # gradient background
        for y in range(height):
            t = y / max(1, height - 1)
            r = int(15 + 26 * t)
            g = int(9 + 10 * t)
            b = int(22 + 24 * t)
            d.line((0, y, width, y), fill=(r, g, b))

        if kind == "home":
            for i in range(8):
                x = 38 + i * 38
                d.ellipse((x, 35 + (i % 2) * 10, x + 9, 44 + (i % 2) * 10), fill="#ff77aa")
            d.rounded_rectangle((42, 82, width-42, 175), 18, outline="#63304d", width=2, fill="#160d19")
            d.text((68, 104), "LUANA  +  YASMIN", fill="#fff7fb")
            d.text((68, 136), "2 MONTHS / BUILD OK", fill="#84f0b4")
        elif kind == "dashboard":
            pts = []
            for x in range(20, width-20, 22):
                y = 135 + int(35 * math.sin(x / 32))
                pts.append((x, y))
            d.line(pts, fill="#ff77aa", width=4)
            d.line((18, 185, width-18, 185), fill="#382a3e", width=1)
            d.text((22, 28), "RELATIONSHIP HEALTH", fill="#c7a6ff")
            d.text((22, 58), "100%", fill="#fff7fb")
            d.text((118, 64), "stable", fill="#84f0b4")
        elif kind == "programming":
            d.rounded_rectangle((22, 26, width-22, height-24), 14, fill="#09070d", outline="#3a2942")
            lines = [
                ("def love():", "#c7a6ff"),
                ("    while True:", "#fff7fb"),
                ("        print('eu te amo')", "#84f0b4"),
                ("", "#fff7fb"),
                ("> status: running", "#ff77aa"),
            ]
            yy = 55
            for text, color in lines:
                d.text((45, yy), text, fill=color)
                yy += 27
        elif kind == "us":
            # sunset-like card
            for y in range(height):
                t = y / height
                color = (int(32 + 95*t), int(16 + 36*t), int(45 + 55*t))
                d.line((0, y, width, y), fill=color)
            d.ellipse((width-120, 38, width-62, 96), fill="#ffb2c9")
            d.rectangle((0, 165, width, height), fill="#160f1d")
            d.arc((95, 110, 170, 190), 200, 340, fill="#ff77aa", width=6)
            d.arc((155, 110, 230, 190), 200, 340, fill="#ff77aa", width=6)
            d.text((28, 28), "NÓS DUAS", fill="#fff7fb")
        elif kind == "me":
            d.rounded_rectangle((35, 40, 145, 150), 18, fill="#694f3f", outline="#a9866f", width=2)
            d.text((55, 88), "MARROM", fill="#fff7fb")
            d.rounded_rectangle((175, 70, 290, 145), 28, fill="#1c1523", outline="#6b4a78", width=2)
            d.ellipse((196, 99, 212, 115), fill="#ff77aa")
            d.ellipse((225, 99, 241, 115), fill="#c7a6ff")
            d.text((36, 178), "LUANA.DAT", fill="#84f0b4")
        elif kind == "dexter":
            # blood-spatter / Miami-night visual inspired by the series, no character likeness
            d.rectangle((0, 145, width, height), fill="#0b1118")
            for x, hh in [(20,45),(48,70),(82,52),(112,88),(150,64),(190,98),(232,58),(268,80),(305,50)]:
                d.rectangle((x, 145-hh, x+18, 145), fill="#18222d")
            for _ in range(24):
                x = random.randint(15, width-15)
                y = random.randint(18, 130)
                rr = random.randint(2, 8)
                d.ellipse((x-rr, y-rr, x+rr, y+rr), fill=random.choice(["#7f101b", "#b41425", "#d3263b"]))
            d.text((24, 176), "DEXTER / MIAMI", fill="#fff7fb")
            d.text((24, 198), "series_check", fill="#ff718a")
        elif kind == "score":
            vals = [0.82, 0.95, 0.88, 1.0]
            colors = ["#ff77aa", "#c7a6ff", "#84f0b4", "#ff9fc4"]
            yy = 44
            for i, v in enumerate(vals):
                d.rounded_rectangle((28, yy, width-28, yy+20), 10, fill="#23172a")
                d.rounded_rectangle((28, yy, 28+int((width-56)*v), yy+20), 10, fill=colors[i])
                yy += 40
            d.text((28, 198), "VALIDATION COMPLETE", fill="#84f0b4")
        elif kind == "deploy":
            nodes = [(55, 120), (130, 72), (205, 120), (278, 70)]
            for a, b in zip(nodes, nodes[1:]):
                d.line((a[0],a[1],b[0],b[1]), fill="#5a3c64", width=4)
            for x, y in nodes:
                d.ellipse((x-14,y-14,x+14,y+14), fill="#ff77aa", outline="#ffb0cf")
            d.text((40, 178), "DEPLOY: WAITING APPROVAL", fill="#fff7fb")
        elif kind == "letter":
            d.rounded_rectangle((30, 24, width-30, height-22), 14, fill="#fff8fb")
            d.line((54, 64, width-55, 64), fill="#e6cbd7", width=2)
            yy = 85
            for ln in [220, 195, 230, 175]:
                d.line((55, yy, 55+ln, yy), fill="#d9c2cc", width=2)
                yy += 26
            # heart mark
            d.ellipse((width-88, height-72, width-60, height-44), fill="#ff77aa")
            d.ellipse((width-68, height-72, width-40, height-44), fill="#ff77aa")
            d.polygon([(width-92,height-58),(width-36,height-58),(width-64,height-30)], fill="#ff77aa")

        return im

    def art_widget(self, parent, kind, width=330, height=230):
        im = self.make_art(kind, width, height)
        photo = ImageTk.PhotoImage(im)
        self.art_refs.append(photo)
        return tk.Label(parent, image=photo, bg=BLACK, bd=0)

    # ---------- HOME ----------
    def show_home(self):
        self.clear()
        self.set_head("boot_sequence", "READY")
        wrap = tk.Frame(self.body, bg=PANEL)
        wrap.pack(fill="both", expand=True, padx=46, pady=34)

        left = tk.Frame(wrap, bg=PANEL)
        left.pack(side="left", fill="both", expand=True)
        right = tk.Frame(wrap, bg=PANEL)
        right.pack(side="right", padx=(28, 0))

        self.eyebrow(left, "SISTEMA DE DOIS MESES DE NAMORO")
        self.label(left, "Um aplicativo especialmente\npara minha amada,", 28, TEXT, True).pack(anchor="w", pady=(14, 5))
        self.label(left, "porque aparentemente eu virei dev.", 18, PINK_2, True).pack(anchor="w")
        self.label(
            left,
            "Feito por mim. Para você. E com uma quantidade desnecessária de telas porque eu me empolguei.",
            11, MUTED, wraplength=590, justify="left",
        ).pack(anchor="w", pady=(16, 24))

        cta = self.button(left, "ABRIR SISTEMA  →", self.show_dashboard, primary=True, big=True)
        cta.pack(anchor="w")

        terminal = self.card(left, bg=BLACK, padx=16, pady=14)
        terminal.pack(fill="x", pady=(24, 0))
        logs = [
            "[OK] carregando memórias compartilhadas...",
            "[OK] conectando ao cluster: coracao_da_yasmin",
            "[OK] validando credenciais do meu bichinho...",
            "[OK] identidade detectada: Meu amor",
            "[OK] procurando motivos para continuar juntas...",
            "[WARN] resultado excedeu o limite máximo de linhas",
            "[OK] inicializando meu aplicativozinho ∞",
            "SYSTEM READY.",
        ]
        self.label(terminal, "\n".join(logs), 9, GREEN, False, "Consolas", bg=BLACK, justify="left").pack(anchor="w")

        self.art_widget(right, "home", 330, 330).pack()
        meta = self.card(right, padx=14, pady=12)
        meta.pack(fill="x", pady=(12, 0))
        for k, v in [("OWNER", "Luana"), ("TARGET", "Yasmin"), ("BUILD", "love.v3")]:
            row = tk.Frame(meta, bg=PANEL_2)
            row.pack(fill="x", pady=3)
            self.label(row, k, 8, MUTED, True, "Consolas").pack(side="left")
            self.label(row, v, 9, TEXT, True, "Consolas").pack(side="right")

    # ---------- DASHBOARD ----------
    def show_dashboard(self):
        self.clear()
        self.set_head("relationship_health", "ONLINE")
        wrap = tk.Frame(self.body, bg=PANEL)
        wrap.pack(fill="both", expand=True, padx=40, pady=28)

        top = tk.Frame(wrap, bg=PANEL)
        top.pack(fill="x")
        left = tk.Frame(top, bg=PANEL)
        left.pack(side="left", fill="both", expand=True)
        self.eyebrow(left, "RELATIONSHIP HEALTH")
        self.label(left, "Todos os sistemas operacionais.", 25, TEXT, True).pack(anchor="w", pady=(6, 3))
        self.label(left, "Dois meses em produção.", 10, MUTED).pack(anchor="w")
        self.art_widget(top, "dashboard", 300, 150).pack(side="right")

        grid = tk.Frame(wrap, bg=PANEL)
        grid.pack(fill="x", pady=20)
        metrics = [
            ("COMPATIBILIDADE", "100%"),
            ("UPTIME", "24/7"),
            ("BEIJOS DADOS", "MENOS DE MIL"),
            ("BRIGAS", "SE NÃO LEMBRO, NÃO EXISTIU"),
            ("VEZES QUE FALAMOS EU TE AMO", "∞"),
        ]
        positions = [(0,0),(0,1),(0,2),(1,0),(1,1)]
        for i, (name, value) in enumerate(metrics):
            r, c = positions[i]
            card = self.card(grid, padx=14, pady=13)
            card.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
            grid.grid_columnconfigure(c, weight=1)
            self.label(card, name, 7, MUTED, True, "Consolas", wraplength=240, justify="left").pack(anchor="w")
            self.label(card, value, 15 if len(value)<18 else 10, TEXT, True, "Consolas", wraplength=260, justify="left").pack(anchor="w", pady=(7,0))

        action = self.card(wrap, bg=BLACK, padx=18, pady=14)
        action.pack(fill="x", pady=(7,0))
        txt = tk.Frame(action, bg=BLACK)
        txt.pack(side="left", fill="both", expand=True)
        self.label(txt, "AGORA QUERO QUE VOCÊ RESPONDA COM TODO SEU CONHECIMENTO", 9, PURPLE, True, "Consolas", bg=BLACK).pack(anchor="w")
        self.label(txt, "3 perguntas de programação. Duas tentativas por pergunta.", 10, MUTED, bg=BLACK).pack(anchor="w", pady=(5,0))
        self.button(action, "COMEÇAR  →", self.start_programming, primary=True).pack(side="right", padx=(18,0))

    # ---------- GENERIC QUESTION LAYOUT ----------
    def question_shell(self, path, tag, number, total, question, art_kind, status="TESTING"):
        self.clear()
        self.set_head(path, status)
        wrap = tk.Frame(self.body, bg=PANEL)
        wrap.pack(fill="both", expand=True, padx=42, pady=28)
        main = tk.Frame(wrap, bg=PANEL)
        main.pack(fill="both", expand=True)
        left = tk.Frame(main, bg=PANEL)
        left.pack(side="left", fill="both", expand=True)
        right = tk.Frame(main, bg=PANEL)
        right.pack(side="right", padx=(26, 0), anchor="n")

        head = tk.Frame(left, bg=PANEL)
        head.pack(fill="x")
        self.eyebrow(head, tag)
        self.label(head, f"{number}/{total}", 9, MUTED, True, "Consolas").pack(side="right")
        self.label(left, question, 20, TEXT, True, wraplength=610, justify="left").pack(anchor="w", pady=(18,18))
        self.options_frame = tk.Frame(left, bg=PANEL)
        self.options_frame.pack(fill="x")
        self.feedback = self.label(left, "", 10, GREEN, True, "Consolas", wraplength=650, justify="left")
        self.feedback.pack(anchor="w", pady=(16,0))
        self.next_btn = self.button(left, "PRÓXIMA  →", lambda: None, primary=True)
        self.art_widget(right, art_kind, 300, 250).pack()
        return left

    def fill_options(self, options, callback):
        self.option_buttons = []
        for i, option in enumerate(options):
            b = tk.Button(
                self.options_frame,
                text=f"{chr(65+i)}   {option}",
                command=lambda n=i: callback(n),
                bg=PANEL_2, fg=TEXT,
                activebackground=PANEL_3, activeforeground=TEXT,
                relief="flat", bd=0, cursor="hand2", anchor="w",
                font=("Segoe UI", 10), padx=16, pady=11,
            )
            b.pack(fill="x", pady=4)
            b.bind("<Enter>", lambda e, btn=b: btn.configure(bg=PANEL_3) if str(btn['state']) == 'normal' else None)
            b.bind("<Leave>", lambda e, btn=b: btn.configure(bg=PANEL_2) if str(btn['state']) == 'normal' else None)
            self.option_buttons.append(b)

    def disable_options(self):
        for b in self.option_buttons:
            b.configure(state="disabled")

    def mark_correct(self, index):
        if isinstance(index, int):
            self.option_buttons[index].configure(bg="#203629", fg=GREEN, disabledforeground=GREEN)

    def mark_wrong(self, index):
        self.option_buttons[index].configure(bg="#3a2028", fg=RED, disabledforeground=RED)

    # ---------- PROGRAMMING ----------
    def start_programming(self):
        self.prog_score = 0
        self.index = 0
        self.render_programming()

    def render_programming(self):
        q = PROGRAMMING[self.index]
        self.locked = False
        self.attempts = 0
        self.question_shell("knowledge/programming", q["tag"], self.index+1, len(PROGRAMMING), q["q"], "programming")
        self.fill_options(q["options"], self.answer_programming)
        self.feedback.configure(text="Tentativas: 2", fg=MUTED)
        self.next_btn.configure(command=self.next_programming)

    def answer_programming(self, selected):
        if self.locked:
            return
        q = PROGRAMMING[self.index]
        if selected == q["correct"]:
            self.locked = True
            self.prog_score += 1
            self.disable_options()
            self.mark_correct(q["correct"])
            self.feedback.configure(text="Isso. Te amo.", fg=GREEN)
            self.next_btn.pack(anchor="e", pady=(18,0))
            return
        self.attempts += 1
        self.mark_wrong(selected)
        self.option_buttons[selected].configure(state="disabled")
        if self.attempts == 1:
            self.feedback.configure(text="Errou. Tenta de novo. Agora vai.", fg=PINK_2)
        else:
            self.locked = True
            self.disable_options()
            self.mark_correct(q["correct"])
            self.feedback.configure(text=f"Tudo bem, amor. A resposta era {q['answer']}. Eu te amo.", fg=PINK_2)
            self.next_btn.pack(anchor="e", pady=(18,0))

    def next_programming(self):
        if self.index < len(PROGRAMMING)-1:
            self.index += 1
            self.render_programming()
        else:
            self.show_us_intro()

    # ---------- HEARTS ----------
    def heart_canvas(self, parent, lives=None, width=220, height=58):
        lives = self.lives if lives is None else lives
        cv = tk.Canvas(parent, width=width, height=height, bg=parent.cget("bg"), highlightthickness=0)
        for i in range(4):
            x = 20 + i*50
            self.draw_heart(cv, x, 15, 26, PINK if i < lives else "#4b3547")
        return cv

    def draw_heart(self, cv, x, y, size, color):
        r = size * .28
        cv.create_oval(x, y, x+2*r, y+2*r, fill=color, outline="")
        cv.create_oval(x+r, y, x+3*r, y+2*r, fill=color, outline="")
        cv.create_polygon(x, y+r, x+3*r, y+r, x+1.5*r, y+size, fill=color, outline="")

    def show_us_intro(self):
        self.clear()
        self.set_head("knowledge/us", "NEW STAGE")
        wrap = tk.Frame(self.body, bg=PANEL)
        wrap.pack(fill="both", expand=True, padx=48, pady=38)
        left = tk.Frame(wrap, bg=PANEL)
        left.pack(side="left", fill="both", expand=True)
        right = tk.Frame(wrap, bg=PANEL)
        right.pack(side="right", padx=(30,0))
        self.eyebrow(left, "FASE 02 / NÓS DUAS")
        self.label(left, "Agora que você já testou seu\nconhecimento em programação…", 25, TEXT, True).pack(anchor="w", pady=(16,6))
        self.label(left, "quero saber se tá sabendo de nós.", 18, PINK_2, True).pack(anchor="w")
        self.label(left, "Você começa com quatro vidas. Se errar, machuca um coração meu e perde uma.", 11, MUTED, wraplength=590, justify="left").pack(anchor="w", pady=(18,8))
        self.heart_canvas(left, 4).pack(anchor="w", pady=(8,22))
        self.button(left, "COMEÇAR  →", self.start_us, primary=True, big=True).pack(anchor="w")
        self.art_widget(right, "us", 320, 320).pack()

    def start_us(self):
        self.us_score = 0
        self.lives = 4
        self.index = 0
        self.render_us()

    def render_us(self):
        q = US[self.index]
        self.locked = False
        left = self.question_shell("knowledge/us", "NÓS DUAS", self.index+1, len(US), q["q"], "us", "HEARTS ACTIVE")
        hb = tk.Frame(left, bg=PANEL)
        hb.pack(fill="x", before=self.options_frame, pady=(0,8))
        self.label(hb, "VIDAS", 8, MUTED, True, "Consolas").pack(side="left", padx=(0,8))
        self.life_canvas = self.heart_canvas(hb)
        self.life_canvas.pack(side="left")
        self.fill_options(q["options"], self.answer_us)
        self.next_btn.configure(command=self.next_us)

    def answer_us(self, selected):
        if self.locked:
            return
        self.locked = True
        q = US[self.index]
        self.disable_options()
        correct = q["correct"] == "all" or selected == q["correct"]
        if correct:
            self.us_score += 1
            self.mark_correct(selected)
            self.feedback.configure(text=q.get("right", "Isso. Te amo."), fg=GREEN)
        else:
            self.lives = max(0, self.lives-1)
            self.mark_wrong(selected)
            self.mark_correct(q["correct"])
            self.life_canvas.destroy()
            self.life_canvas = self.heart_canvas(self.options_frame.master)
            self.feedback.configure(text=f"Errou. Machucou um coração meu. A resposta era {q['answer']}.", fg=RED)
            if q.get("panic"):
                self.panic_overlay()
        self.next_btn.pack(anchor="e", pady=(18,0))

    def panic_overlay(self):
        ov = tk.Frame(self.body, bg="#250a12", highlightbackground=RED, highlightthickness=2)
        ov.place(relx=.5, rely=.5, anchor="center", width=650, height=175)
        self.label(ov, "SYSTEM ERROR", 10, RED, True, "Consolas", bg="#250a12").pack(pady=(24,6))
        self.label(ov, "02/04 NÃO ENCONTRADO NA RESPOSTA", 17, WHITE, True, "Consolas", bg="#250a12").pack()
        self.label(ov, "reiniciando…", 9, MUTED, False, "Consolas", bg="#250a12").pack(pady=(12,0))
        job = self.root.after(1300, ov.destroy)
        self.jobs.append(job)

    def next_us(self):
        if self.index < len(US)-1:
            self.index += 1
            self.render_us()
        else:
            self.show_me_intro()

    # ---------- LUANA ----------
    def show_me_intro(self):
        self.clear()
        self.set_head("knowledge/luana", "NEXT")
        wrap = tk.Frame(self.body, bg=PANEL)
        wrap.pack(fill="both", expand=True, padx=48, pady=40)
        left = tk.Frame(wrap, bg=PANEL)
        left.pack(side="left", fill="both", expand=True)
        self.eyebrow(left, "FASE 03 / VENDO SE ELA ME CONHECE")
        self.label(left, "Agora é sobre mim.", 29, TEXT, True).pack(anchor="w", pady=(18,7))
        self.label(left, "Sem pressão. Mas eu vou ver o score no final.", 12, PINK_2, True).pack(anchor="w")
        self.button(left, "INICIAR  →", self.start_me, primary=True, big=True).pack(anchor="w", pady=(28,0))
        self.art_widget(wrap, "me", 330, 330).pack(side="right", padx=(28,0))

    def start_me(self):
        self.me_score = 0
        self.index = 0
        self.render_me()

    def render_me(self):
        q = ME[self.index]
        self.locked = False
        self.question_shell("knowledge/luana", "LUANA", self.index+1, len(ME), q["q"], "me")
        self.fill_options(q["options"], self.answer_me)
        self.next_btn.configure(command=self.next_me)

    def answer_me(self, selected):
        if self.locked:
            return
        self.locked = True
        q = ME[self.index]
        self.disable_options()
        if q["correct"] == "all":
            self.me_score += 1
            self.mark_correct(selected)
            self.feedback.configure(text=q.get("right", "Isso. Te amo."), fg=GREEN)
        elif q.get("trap"):
            self.me_score += 1
            self.mark_wrong(selected)
            self.feedback.configure(text=q["wrong"], fg=PINK_2)
        elif selected == q["correct"]:
            self.me_score += 1
            self.mark_correct(selected)
            self.feedback.configure(text="Isso. Te amo.", fg=GREEN)
        else:
            self.mark_wrong(selected)
            self.mark_correct(q["correct"])
            self.feedback.configure(text=q.get("wrong", f"A resposta era {q['answer']}."), fg=PINK_2)
        self.next_btn.pack(anchor="e", pady=(18,0))

    def next_me(self):
        if self.index < len(ME)-1:
            self.index += 1
            self.render_me()
        else:
            self.show_dexter_intro()

    # ---------- DEXTER ----------
    def show_dexter_intro(self):
        self.clear()
        self.set_head("knowledge/dexter", "BONUS STAGE", RED)
        wrap = tk.Frame(self.body, bg=PANEL)
        wrap.pack(fill="both", expand=True, padx=48, pady=40)
        left = tk.Frame(wrap, bg=PANEL)
        left.pack(side="left", fill="both", expand=True)
        self.eyebrow(left, "FASE BÔNUS / DEXTER", RED)
        self.label(left, "Tá, mas e a nossa série?", 29, TEXT, True).pack(anchor="w", pady=(18,7))
        self.label(left, "Quatro perguntas. Miami Metro está observando.", 11, MUTED).pack(anchor="w")
        self.button(left, "ABRIR ARQUIVO DEXTER  →", self.start_dexter, primary=True, big=True).pack(anchor="w", pady=(28,0))
        self.art_widget(wrap, "dexter", 340, 340).pack(side="right", padx=(30,0))

    def start_dexter(self):
        self.dexter_score = 0
        self.index = 0
        self.render_dexter()

    def render_dexter(self):
        q = DEXTER[self.index]
        self.locked = False
        self.question_shell("knowledge/dexter", "DEXTER", self.index+1, len(DEXTER), q["q"], "dexter", "CASE OPEN")
        self.fill_options(q["options"], self.answer_dexter)
        self.next_btn.configure(command=self.next_dexter)

    def answer_dexter(self, selected):
        if self.locked:
            return
        self.locked = True
        q = DEXTER[self.index]
        self.disable_options()
        if selected == q["correct"]:
            self.dexter_score += 1
            self.mark_correct(selected)
            self.feedback.configure(text="Isso. Te amo.", fg=GREEN)
        else:
            self.mark_wrong(selected)
            self.mark_correct(q["correct"])
            self.feedback.configure(text=f"Não. Era {q['answer']}.", fg=RED)
        self.next_btn.pack(anchor="e", pady=(18,0))

    def next_dexter(self):
        if self.index < len(DEXTER)-1:
            self.index += 1
            self.render_dexter()
        else:
            self.show_score()

    # ---------- SCORE / DEPLOY / LETTER ----------
    def show_score(self):
        self.clear()
        self.set_head("final_report", "COMPLETE")
        wrap = tk.Frame(self.body, bg=PANEL)
        wrap.pack(fill="both", expand=True, padx=42, pady=28)
        top = tk.Frame(wrap, bg=PANEL)
        top.pack(fill="x")
        left = tk.Frame(top, bg=PANEL)
        left.pack(side="left", fill="both", expand=True)
        self.eyebrow(left, "FINAL REPORT", GREEN)
        self.label(left, "Tá, você passou.", 27, TEXT, True).pack(anchor="w", pady=(8,3))
        self.label(left, "O resultado afetivo continua 100% independentemente do resto.", 10, MUTED).pack(anchor="w")
        self.art_widget(top, "score", 300, 180).pack(side="right")

        grid = tk.Frame(wrap, bg=PANEL)
        grid.pack(fill="x", pady=22)
        data = [
            ("PROGRAMAÇÃO", f"{self.prog_score}/3"),
            ("NÓS DUAS", f"{self.us_score}/4"),
            ("LUANA", f"{self.me_score}/4"),
            ("DEXTER", f"{self.dexter_score}/4"),
            ("COMPATIBILIDADE", "100%"),
        ]
        for i, (k,v) in enumerate(data):
            c = self.card(grid, padx=14, pady=13)
            c.grid(row=0, column=i, padx=4, sticky="nsew")
            grid.grid_columnconfigure(i, weight=1)
            self.label(c, k, 7, MUTED, True, "Consolas").pack(anchor="w")
            self.label(c, v, 18, TEXT, True, "Consolas").pack(anchor="w", pady=(7,0))

        self.button(wrap, "ABRIR SOLICITAÇÃO DE DEPLOY  →", self.show_deploy, primary=True, big=True).pack(anchor="e", pady=(14,0))

    def show_deploy(self):
        self.clear()
        self.set_head("deployment_approval", "ACTION REQUIRED", PINK)
        wrap = tk.Frame(self.body, bg=PANEL)
        wrap.pack(fill="both", expand=True, padx=48, pady=32)
        left = tk.Frame(wrap, bg=PANEL)
        left.pack(side="left", fill="both", expand=True)
        self.eyebrow(left, "CHANGE REQUEST #LOVE-∞")
        self.label(left, "Pronta pra próxima versão?", 27, TEXT, True).pack(anchor="w", pady=(16,5))
        self.label(left, "OWNER: Luana\nAPPROVER: Yasmin\nENVIRONMENT: production\nDURATION: indefinida\nROLLBACK: não aplicável", 10, MUTED, False, "Consolas", justify="left").pack(anchor="w", pady=(16,22))
        buttons = tk.Frame(left, bg=PANEL)
        buttons.pack(anchor="w")
        self.button(buttons, "APROVAR DEPLOY  ♡", self.show_letter, primary=True, big=True).pack(side="left")
        self.review = self.button(buttons, "NÃO", self.move_no)
        self.review.pack(side="left", padx=10)
        self.art_widget(wrap, "deploy", 330, 300).pack(side="right", padx=(30,0))

    def move_no(self):
        choices = ["TEM CERTEZA?", "REVISA ISSO", "CLICA NO ROSA", "NÃO ACEITO"]
        self.review.configure(text=random.choice(choices))
        self.review.pack_configure(padx=random.randint(6,50))

    def show_letter(self):
        self.clear()
        self.set_head("release_notes", "DEPLOYED")
        wrap = tk.Frame(self.body, bg=PANEL)
        wrap.pack(fill="both", expand=True, padx=38, pady=24)
        left = tk.Frame(wrap, bg=PANEL)
        left.pack(side="left", fill="both", expand=True)
        self.eyebrow(left, "RELEASE SUCCESSFUL", GREEN)
        self.label(left, "Agora sem sistema.", 22, TEXT, True).pack(anchor="w", pady=(6,12))
        paper = tk.Frame(left, bg=WHITE, padx=28, pady=22)
        paper.pack(fill="both", expand=True)
        self.label(paper, LETTER, 12, "#4a3440", False, "Georgia", bg=WHITE, wraplength=610, justify="left").pack(anchor="w")
        self.label(paper, "— Luana", 12, "#9f4168", True, "Georgia", bg=WHITE).pack(anchor="e", pady=(10,0))
        self.art_widget(wrap, "letter", 300, 390).pack(side="right", padx=(24,0))


def main():
    root = tk.Tk()
    LoveSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()
