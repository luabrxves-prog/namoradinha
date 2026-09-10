import io
import os
import random
import tempfile
import threading
import time
import urllib.request
import tkinter as tk

from PIL import Image, ImageOps, ImageTk

try:
    import pygame
except Exception:
    pygame = None

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

DEXTER_IMAGE_URL = "https://img.youtube.com/vi/YQeUmSD1c3g/maxresdefault.jpg"

SOUND_URLS = {
    "dexter": "https://www.myinstants.com/media/sounds/dexter-meme.mp3",
    "fahh": "https://www.myinstants.com/media/sounds/fahhhh-loud.mp3",
    "xp": "https://www.myinstants.com/media/sounds/preview_4.mp3",
}

PROGRAMMING = [
    {
        "tag": "PYTHON / CLOSURES",
        "q": "Qual é a saída deste código?\n\nfuncs = [lambda: i for i in range(3)]\nprint([f() for f in funcs])",
        "options": ["[0, 1, 2]", "[2, 2, 2]", "[0, 0, 0]", "NameError"],
        "correct": 1,
        "answer": "[2, 2, 2]",
        "why": "As lambdas capturam a variável i por referência; quando executam, o loop já terminou em 2.",
    },
    {
        "tag": "SQL / WINDOW FUNCTION",
        "q": "Você precisa manter apenas o pedido mais recente de cada cliente sem perder as outras colunas. Qual abordagem é a mais adequada?",
        "options": [
            "GROUP BY cliente_id e MAX(data)",
            "DISTINCT cliente_id, *",
            "ROW_NUMBER() OVER (PARTITION BY cliente_id ORDER BY data DESC) e filtrar rn = 1",
            "ORDER BY data DESC LIMIT 1",
        ],
        "correct": 2,
        "answer": "ROW_NUMBER() ... rn = 1",
        "why": "A window function escolhe a linha inteira mais recente dentro de cada cliente.",
    },
    {
        "tag": "DATA ENGINEERING / IDEMPOTÊNCIA",
        "q": "Um pipeline pode reprocessar o mesmo lote depois de falhar. Qual desenho reduz melhor o risco de duplicar dados?",
        "options": [
            "INSERT puro em toda execução",
            "Chave determinística + UPSERT/MERGE + checkpoint",
            "Apagar a tabela inteira antes de cada carga",
            "Aumentar o timeout do job",
        ],
        "correct": 1,
        "answer": "Chave determinística + UPSERT/MERGE + checkpoint",
        "why": "O mesmo lote pode ser repetido sem mudar o resultado final.",
    },
    {
        "tag": "GIT / HISTÓRICO COMPARTILHADO",
        "q": "Um commit ruim já foi enviado para a main e outras pessoas já puxaram. Qual opção costuma ser mais segura para desfazer sem reescrever o histórico?",
        "options": ["git reset --hard HEAD~1", "git revert <sha>", "git clean -fd", "git rebase -i --root"],
        "correct": 1,
        "answer": "git revert <sha>",
        "why": "Revert cria um novo commit inverso e preserva o histórico compartilhado.",
    },
]

US = [
    {
        "q": "Qual data está salva no banco oficial como nosso primeiro encontro?",
        "options": ["31 de março", "2 de abril", "4 de abril", "10 de abril"],
        "correct": 1,
        "answer": "2 de abril",
        "right": "Mais que sua obrigação, macaquinha. 02/04 está versionado.",
        "panic": True,
    },
    {
        "q": "Se eu rodar SELECT nossa_musica FROM memorias LIMIT 1, o que volta?",
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
        "q": "Em qual mês aconteceu o primeiro 'eu te amo'?",
        "options": ["Abril", "Maio", "Junho", "Julho"],
        "correct": 1,
        "answer": "Maio",
    },
    {
        "q": "Qual desses programas eu excluiria de um dia perfeito com você?",
        "options": ["Jogar", "Ficar quietinhas", "Sair", "Nenhum deles"],
        "correct": 3,
        "answer": "Nenhum deles",
        "right": "Exato. Eu gosto de fazer tudo com você — inclusive absolutamente nada.",
    },
]

ME = [
    {
        "q": "Qual dessas alternativas descreve melhor minha relação com comida?",
        "options": [
            "Estrogonofe acima de tudo",
            "Japonês e acabou",
            "Salmão é sempre a primeira escolha",
            "A pergunta é inválida porque eu gosto de praticamente tudo",
        ],
        "correct": 3,
        "answer": "Eu gosto de praticamente tudo",
    },
    {
        "q": "Qual jogo fica no topo do meu ranking pessoal?",
        "options": ["Red Dead Redemption 2", "Valorant", "League of Legends", "Detroit: Become Human"],
        "correct": 3,
        "answer": "Detroit: Become Human",
    },
    {
        "q": "Sem pegadinha desta vez: qual é minha cor preferida?",
        "options": ["Marsala", "Marrom", "Roxo", "Preto"],
        "correct": 1,
        "answer": "Marrom",
    },
    {
        "q": "Qual seria, de verdade, o melhor cenário para um dia perfeito meu?",
        "options": ["Praia com sol", "Restaurante caro", "Festa até tarde", "Um dia com você"],
        "correct": 3,
        "answer": "Um dia com você",
        "right": "Acertou a mais importante. Te amo.",
    },
]

DEXTER = [
    {
        "q": "Quem é revelado como o Ice Truck Killer?",
        "options": ["Arthur Mitchell", "Brian Moser", "Miguel Prado", "James Doakes"],
        "correct": 1,
        "answer": "Brian Moser",
    },
    {
        "q": "Qual é o nome do barco do Dexter?",
        "options": ["Sea Escape", "Slice of Life", "Dark Passenger", "Bay Harbor"],
        "correct": 1,
        "answer": "Slice of Life",
    },
    {
        "q": "Quem acaba sendo responsabilizado publicamente como o Bay Harbor Butcher?",
        "options": ["Angel Batista", "James Doakes", "Frank Lundy", "Miguel Prado"],
        "correct": 1,
        "answer": "James Doakes",
    },
    {
        "q": "Quem mata Rita no final da quarta temporada?",
        "options": ["Brian Moser", "Travis Marshall", "Arthur Mitchell / Trinity", "Jordan Chase"],
        "correct": 2,
        "answer": "Arthur Mitchell / Trinity",
    },
]

LETTER = (
    "Oi, amor!\n\n"
    "Só queria agradecer por esses dois meses. A cada dia que passa eu vejo o quanto sou feliz por ter você.\n\n"
    "Você foi definitivamente a vida sorrindo pra mim. Eu me considero uma mulher de sorte — e espero ter essa sorte por toda a vida.\n\n"
    "Obrigada por ser meu bichinho, minha macaquinha, minha pessoa favorita e a vítima oficial das minhas piadas ruins, inclusive a campanha permanente pelo seu Uno.\n\n"
    "Eu gosto da gente do jeito que a gente é: das conversas, das risadas, dos jogos, dos silêncios, de Dexter e de tudo que ainda nem aconteceu.\n\n"
    "Um breve(s) relato de um sentimento enorme.\n\n"
    "Eu te amo."
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
        self.locked = False
        self.jobs = []
        self.photo_refs = []
        self.bg_particles = []
        self.sound_enabled = True
        self.audio_ready = False
        self.last_xp = 0.0

        self.canvas = tk.Canvas(root, bg=BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self._resize)

        self.stage = tk.Frame(self.canvas, bg=PANEL, highlightbackground=LINE, highlightthickness=1)
        self.stage_window = self.canvas.create_window(590, 380, window=self.stage, width=1030, height=650)

        self._spawn_background()
        self._animate_background()

        self.top = tk.Frame(self.stage, bg=PANEL, height=56)
        self.top.pack(fill="x")
        self.top.pack_propagate(False)
        self.label(self.top, "●", 11, GREEN, True, "Consolas").pack(side="left", padx=(24, 8))
        self.label(self.top, "love_system.exe", 10, TEXT, True, "Consolas").pack(side="left")
        self.path = self.label(self.top, "  / boot_sequence", 9, MUTED, False, "Consolas")
        self.path.pack(side="left")
        self.sound_btn = self.button(self.top, "SOM: ON", self.toggle_sound, compact=True)
        self.sound_btn.pack(side="right", padx=(6, 18), pady=10)
        self.status = self.label(self.top, "READY", 9, GREEN, True, "Consolas")
        self.status.pack(side="right", padx=8)
        tk.Frame(self.stage, bg=LINE, height=1).pack(fill="x")

        self.body = tk.Frame(self.stage, bg=PANEL)
        self.body.pack(fill="both", expand=True)

        threading.Thread(target=self._prepare_audio, daemon=True).start()
        self.show_home()

    def _resize(self, event):
        self.canvas.coords(self.stage_window, event.width / 2, event.height / 2)
        self.canvas.itemconfigure(
            self.stage_window,
            width=min(1080, max(920, event.width - 90)),
            height=min(690, max(620, event.height - 70)),
        )

    def clear(self):
        for job in self.jobs:
            try:
                self.root.after_cancel(job)
            except Exception:
                pass
        self.jobs.clear()
        self.photo_refs.clear()
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

    def button(self, parent, text, command, primary=False, big=False, compact=False):
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
            font=("Segoe UI", 9 if compact else (11 if big else 10), "bold"),
            padx=10 if compact else (24 if big else 18),
            pady=5 if compact else (14 if big else 10),
        )
        b.bind("<Enter>", lambda e: b.configure(bg=PINK_2 if primary else PANEL_3))
        b.bind("<Leave>", lambda e: b.configure(bg=PINK if primary else PANEL_2))
        return b

    def card(self, parent, bg=PANEL_2, padx=18, pady=16):
        return tk.Frame(parent, bg=bg, padx=padx, pady=pady, highlightbackground=LINE, highlightthickness=1)

    def eyebrow(self, parent, text, color=PINK):
        self.label(parent, text.upper(), 9, color, True, "Consolas").pack(anchor="w")

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        self.sound_btn.configure(text="SOM: ON" if self.sound_enabled else "SOM: OFF")

    def _prepare_audio(self):
        if pygame is None:
            return
        try:
            pygame.mixer.init()
            self.audio_ready = True
        except Exception:
            self.audio_ready = False

    def _sound_path(self, name):
        return os.path.join(tempfile.gettempdir(), f"love_system_{name}.mp3")

    def play_sound(self, name):
        if not self.sound_enabled:
            return
        if name == "xp":
            now = time.time()
            if now - self.last_xp < 1.0:
                return
            self.last_xp = now

        def worker():
            try:
                if not self.audio_ready:
                    self._prepare_audio()
                if not self.audio_ready:
                    return
                path = self._sound_path(name)
                if not os.path.exists(path):
                    req = urllib.request.Request(SOUND_URLS[name], headers={"User-Agent": "Mozilla/5.0"})
                    with urllib.request.urlopen(req, timeout=8) as response, open(path, "wb") as f:
                        f.write(response.read())
                pygame.mixer.music.load(path)
                pygame.mixer.music.play()
            except Exception:
                pass

        threading.Thread(target=worker, daemon=True).start()

    def _spawn_background(self):
        for _ in range(30):
            x = random.randint(0, 1180)
            y = random.randint(0, 760)
            item = self.canvas.create_text(
                x,
                y,
                text=random.choice(["·", "✦", "♡"]),
                fill=random.choice(["#332039", "#40233b", "#2b2133"]),
                font=("Segoe UI Symbol", random.randint(8, 15)),
            )
            self.canvas.tag_lower(item, self.stage_window)
            self.bg_particles.append((item, random.uniform(.07, .2)))

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

    def remote_image(self, parent, url, width, height, caption=None):
        frame = tk.Frame(parent, bg=BLACK, highlightbackground=LINE, highlightthickness=1)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=7) as response:
                raw = response.read()
            image = Image.open(io.BytesIO(raw)).convert("RGB")
            image = ImageOps.fit(image, (width, height), method=Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.photo_refs.append(photo)
            tk.Label(frame, image=photo, bg=BLACK, bd=0).pack()
        except Exception:
            self.label(frame, "imagem indisponível offline", 10, MUTED, False, "Consolas", bg=BLACK).pack(padx=40, pady=80)
        if caption:
            self.label(frame, caption, 8, MUTED, False, "Consolas", bg=BLACK).pack(anchor="w", padx=10, pady=8)
        return frame

    def show_home(self):
        self.clear()
        self.set_head("boot_sequence", "READY")
        wrap = tk.Frame(self.body, bg=PANEL)
        wrap.pack(fill="both", expand=True, padx=50, pady=34)

        self.eyebrow(wrap, "SISTEMA DE DOIS MESES DE NAMORO")
        self.label(wrap, "Um aplicativozinho especialmente para a Yasmin", 30, TEXT, True, wraplength=850, justify="left", anchor="w").pack(anchor="w", pady=(14, 4))
        self.label(wrap, "porque aparentemente eu virei dev.", 18, PINK_2, True).pack(anchor="w")
        self.label(
            wrap,
            "Feito pela Luana para a minha macaquinha. O sistema pode conter excesso de programação, Dexter, memes e decisões totalmente imparciais.",
            11,
            MUTED,
            wraplength=850,
            justify="left",
        ).pack(anchor="w", pady=(14, 20))

        terminal = self.card(wrap, bg=BLACK, padx=18, pady=16)
        terminal.pack(fill="x")
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
        self.label(terminal, "\n".join(logs), 10, GREEN, False, "Consolas", bg=BLACK, justify="left", anchor="w").pack(anchor="w")

        footer = tk.Frame(wrap, bg=PANEL)
        footer.pack(fill="x", pady=(22, 0))
        self.label(footer, "OWNER: LUANA  •  TARGET: YASMIN  •  BUILD: LOVE.V4", 8, MUTED, True, "Consolas").pack(side="left")
        self.button(footer, "ABRIR SISTEMA  →", self.show_dashboard, primary=True, big=True).pack(side="right")

    def show_dashboard(self):
        self.clear()
        self.set_head("relationship_health", "ONLINE")
        wrap = tk.Frame(self.body, bg=PANEL)
        wrap.pack(fill="both", expand=True, padx=44, pady=30)

        self.eyebrow(wrap, "RELATIONSHIP HEALTH")
        self.label(wrap, "Todos os sistemas operacionais. ❤️", 28, TEXT, True).pack(anchor="w", pady=(7, 4))
        self.label(wrap, "Dois meses em produção. Nenhum incidente crítico em aberto e nenhuma previsão de rollback.", 11, MUTED, wraplength=860, justify="left").pack(anchor="w")

        metrics = tk.Frame(wrap, bg=PANEL)
        metrics.pack(fill="x", pady=22)
        data = [
            ("COMPATIBILIDADE", "100%", "+∞% YoY"),
            ("UPTIME", "24/7", "sem manutenção"),
            ("LATÊNCIA DO ABRAÇO", "< 1s", "SLA cumprido"),
            ("RETENÇÃO", "∞", "churn: 0%"),
        ]
        for i, (name, value, sub) in enumerate(data):
            c = self.card(metrics, padx=15, pady=14)
            c.grid(row=0, column=i, padx=5, sticky="nsew")
            metrics.grid_columnconfigure(i, weight=1)
            self.label(c, name, 8, MUTED, True, "Consolas").pack(anchor="w")
            self.label(c, value, 21, TEXT, True, "Consolas").pack(anchor="w", pady=(7, 1))
            self.label(c, sub, 8, GREEN, False, "Consolas").pack(anchor="w")

        query = self.card(wrap, bg=BLACK, padx=18, pady=15)
        query.pack(fill="x")
        self.label(query, "SELECT pessoa_favorita FROM universo ORDER BY prioridade DESC LIMIT 1;", 10, PURPLE, False, "Consolas", bg=BLACK).pack(anchor="w")
        self.label(query, "> Yasmin", 11, GREEN, True, "Consolas", bg=BLACK).pack(anchor="w", pady=(6, 0))

        action = tk.Frame(wrap, bg=PANEL)
        action.pack(fill="x", pady=(22, 0))
        self.label(action, "Validação pendente: programação → nós → Luana → Dexter.", 10, MUTED).pack(side="left")
        self.button(action, "COMEÇAR VALIDAÇÃO  →", self.start_programming, primary=True).pack(side="right")

    def question_shell(self, path, phase, number, total, question, status="TESTING", hearts=False):
        self.clear()
        self.set_head(path, status)
        outer = tk.Frame(self.body, bg=PANEL)
        outer.pack(fill="both", expand=True, padx=52, pady=28)

        head = tk.Frame(outer, bg=PANEL)
        head.pack(fill="x")
        self.label(head, phase.upper(), 9, PINK if phase != "DEXTER" else RED, True, "Consolas").pack(side="left")
        self.label(head, f"CHECK {number:02d}/{total:02d}", 9, MUTED, True, "Consolas").pack(side="right")

        progress = tk.Frame(outer, bg=LINE, height=5)
        progress.pack(fill="x", pady=(12, 18))
        progress.pack_propagate(False)
        tk.Frame(progress, bg=PINK if phase != "DEXTER" else RED).place(relx=0, rely=0, relwidth=number / total, relheight=1)

        if hearts:
            hb = tk.Frame(outer, bg=PANEL)
            hb.pack(fill="x", pady=(0, 10))
            self.label(hb, "VIDAS", 8, MUTED, True, "Consolas").pack(side="left", padx=(0, 10))
            self.life_canvas = tk.Canvas(hb, width=220, height=42, bg=PANEL, highlightthickness=0)
            self.life_canvas.pack(side="left")
            self.refresh_lives()

        self.label(outer, question, 20, TEXT, True, wraplength=900, justify="left", anchor="w").pack(fill="x", anchor="w", pady=(7, 18))

        self.options_frame = tk.Frame(outer, bg=PANEL)
        self.options_frame.pack(fill="x")
        self.feedback = self.label(outer, "", 9, GREEN, True, "Consolas", wraplength=900, justify="left", anchor="w")
        self.feedback.pack(fill="x", anchor="w", pady=(13, 0))
        self.next_btn = self.button(outer, "PRÓXIMA  →", lambda: None, primary=True)
        return outer

    def fill_options(self, options, callback):
        self.option_buttons = []
        for i, option in enumerate(options):
            b = tk.Button(
                self.options_frame,
                text=f"  {chr(65+i)}   {option}",
                command=lambda n=i: callback(n),
                bg=PANEL_2,
                fg=TEXT,
                activebackground=PANEL_3,
                activeforeground=TEXT,
                relief="flat",
                bd=0,
                cursor="hand2",
                anchor="w",
                font=("Segoe UI", 10),
                padx=16,
                pady=11,
            )
            b.pack(fill="x", pady=4)
            b.bind("<Enter>", lambda e, btn=b: btn.configure(bg=PANEL_3) if str(btn["state"]) == "normal" else None)
            b.bind("<Leave>", lambda e, btn=b: btn.configure(bg=PANEL_2) if str(btn["state"]) == "normal" else None)
            self.option_buttons.append(b)

    def disable_options(self):
        for b in self.option_buttons:
            b.configure(state="disabled")

    def mark_correct(self, index):
        if isinstance(index, int) and 0 <= index < len(self.option_buttons):
            self.option_buttons[index].configure(bg="#203629", fg=GREEN, disabledforeground=GREEN)

    def mark_wrong(self, index):
        self.option_buttons[index].configure(bg="#3a2028", fg=RED, disabledforeground=RED)

    def common_answer(self, q, selected, score_attr, next_command, lose_heart=False):
        if self.locked:
            return
        self.locked = True
        self.disable_options()
        if selected == q["correct"]:
            setattr(self, score_attr, getattr(self, score_attr) + 1)
            self.mark_correct(selected)
            self.feedback.configure(text=q.get("right", f"[PASS] {q.get('why', 'Resposta validada.')}"), fg=GREEN)
        else:
            self.mark_wrong(selected)
            self.mark_correct(q["correct"])
            self.feedback.configure(text=f"[ERRO] A resposta correta era {q['answer']}. {q.get('why', '')}", fg=RED)
            self.play_sound("fahh")
            if lose_heart:
                self.lives = max(0, self.lives - 1)
                self.refresh_lives()
                self.break_heart_effect()
                if self.lives == 0:
                    self.play_sound("xp")
            if q.get("panic"):
                self.panic_overlay()
        self.next_btn.configure(command=next_command)
        self.next_btn.pack(anchor="e", pady=(14, 0))

    def start_programming(self):
        self.prog_score = 0
        self.index = 0
        self.render_programming()

    def render_programming(self):
        q = PROGRAMMING[self.index]
        self.locked = False
        self.question_shell("validation/programming", q["tag"], self.index + 1, len(PROGRAMMING), q["q"])
        self.fill_options(q["options"], self.answer_programming)

    def answer_programming(self, selected):
        self.common_answer(PROGRAMMING[self.index], selected, "prog_score", self.next_programming)

    def next_programming(self):
        if self.index < len(PROGRAMMING) - 1:
            self.index += 1
            self.render_programming()
        else:
            self.show_us_intro()

    def draw_heart(self, cv, x, y, size, color):
        r = size * .28
        cv.create_oval(x, y, x + 2 * r, y + 2 * r, fill=color, outline="")
        cv.create_oval(x + r, y, x + 3 * r, y + 2 * r, fill=color, outline="")
        cv.create_polygon(x, y + r, x + 3 * r, y + r, x + 1.5 * r, y + size, fill=color, outline="")

    def draw_broken_heart(self, cv, x, y, size):
        self.draw_heart(cv, x, y, size, "#5a3b48")
        cv.create_line(x + size * .44, y + size * .17, x + size * .58, y + size * .42, x + size * .47, y + size * .62, x + size * .61, y + size * .86, fill=RED, width=2)

    def refresh_lives(self):
        if not hasattr(self, "life_canvas") or not self.life_canvas.winfo_exists():
            return
        self.life_canvas.delete("all")
        for i in range(4):
            x = 8 + i * 50
            if i < self.lives:
                self.draw_heart(self.life_canvas, x, 7, 25, PINK)
            else:
                self.draw_broken_heart(self.life_canvas, x, 7, 25)

    def break_heart_effect(self):
        ov = tk.Canvas(self.body, bg="#160810", highlightthickness=0)
        ov.place(relx=.5, rely=.5, anchor="center", width=260, height=210)
        self.draw_heart(ov, 88, 42, 74, PINK)
        crack = ov.create_line(124, 52, 141, 82, 129, 103, 145, 133, fill=WHITE, width=4)
        pieces = []
        for _ in range(18):
            x = random.randint(84, 175)
            y = random.randint(70, 130)
            item = ov.create_oval(x, y, x + 5, y + 5, fill=RED, outline="")
            pieces.append((item, random.uniform(-2.5, 2.5), random.uniform(-4.2, -1.5)))

        def animate(step=0):
            if not ov.winfo_exists():
                return
            if step == 4:
                ov.itemconfigure(crack, fill=BLACK)
            for item, vx, vy in pieces:
                ov.move(item, vx, vy + step * .26)
            if step < 24:
                job = self.root.after(28, lambda: animate(step + 1))
                self.jobs.append(job)
            else:
                ov.destroy()

        animate()

    def panic_overlay(self):
        ov = tk.Frame(self.body, bg="#250a12", highlightbackground=RED, highlightthickness=2)
        ov.place(relx=.5, rely=.5, anchor="center", width=660, height=165)
        self.label(ov, "SYSTEM ERROR", 10, RED, True, "Consolas", bg="#250a12").pack(pady=(22, 5))
        self.label(ov, "02/04 NÃO ENCONTRADO NA RESPOSTA", 17, WHITE, True, "Consolas", bg="#250a12").pack()
        self.label(ov, "minha macaquinha está sob investigação", 9, MUTED, False, "Consolas", bg="#250a12").pack(pady=(10, 0))
        job = self.root.after(1350, ov.destroy)
        self.jobs.append(job)

    def show_us_intro(self):
        self.clear()
        self.set_head("phase/us", "HEARTS ARMED")
        wrap = tk.Frame(self.body, bg=PANEL)
        wrap.pack(fill="both", expand=True, padx=54, pady=38)
        self.eyebrow(wrap, "FASE 02 / NÓS DUAS")
        self.label(wrap, "Agora quero saber se você tá sabendo de nós.", 29, TEXT, True).pack(anchor="w", pady=(14, 6))
        self.label(wrap, "Quatro perguntas. Quatro corações. Errou? O FAHH toca e um coração quebra de verdade na tela.", 11, MUTED, wraplength=830, justify="left").pack(anchor="w", pady=(0, 14))
        preview = tk.Canvas(wrap, width=245, height=58, bg=PANEL, highlightthickness=0)
        preview.pack(anchor="w")
        for i in range(4):
            self.draw_heart(preview, 12 + i * 56, 12, 30, PINK)
        self.button(wrap, "COMEÇAR FASE 02  →", self.start_us, primary=True, big=True).pack(anchor="w", pady=(22, 0))

    def start_us(self):
        self.us_score = 0
        self.lives = 4
        self.index = 0
        self.render_us()

    def render_us(self):
        q = US[self.index]
        self.locked = False
        self.question_shell("validation/us", "NÓS DUAS", self.index + 1, len(US), q["q"], "HEARTS ACTIVE", hearts=True)
        self.fill_options(q["options"], self.answer_us)

    def answer_us(self, selected):
        self.common_answer(US[self.index], selected, "us_score", self.next_us, lose_heart=True)

    def next_us(self):
        if self.index < len(US) - 1:
            self.index += 1
            self.render_us()
        else:
            self.show_me_intro()

    def show_me_intro(self):
        self.clear()
        self.set_head("phase/luana", "PERSONAL DATA")
        wrap = tk.Frame(self.body, bg=PANEL)
        wrap.pack(fill="both", expand=True, padx=54, pady=40)
        self.eyebrow(wrap, "FASE 03 / SOBRE A LUANA")
        self.label(wrap, "Agora é sobre mim.", 30, TEXT, True).pack(anchor="w", pady=(15, 6))
        self.label(wrap, "Sem pegadinha preguiçosa. As respostas estão aí — você só precisa me conhecer.", 11, MUTED, wraplength=830, justify="left").pack(anchor="w")
        self.button(wrap, "VAMOS VER  →", self.start_me, primary=True, big=True).pack(anchor="w", pady=(28, 0))

    def start_me(self):
        self.me_score = 0
        self.index = 0
        self.render_me()

    def render_me(self):
        q = ME[self.index]
        self.locked = False
        self.question_shell("validation/luana", "LUANA", self.index + 1, len(ME), q["q"])
        self.fill_options(q["options"], self.answer_me)

    def answer_me(self, selected):
        self.common_answer(ME[self.index], selected, "me_score", self.next_me)

    def next_me(self):
        if self.index < len(ME) - 1:
            self.index += 1
            self.render_me()
        else:
            self.show_dexter_intro()

    def show_dexter_intro(self):
        self.clear()
        self.set_head("phase/dexter", "MIAMI METRO", RED)
        self.play_sound("dexter")
        wrap = tk.Frame(self.body, bg=PANEL)
        wrap.pack(fill="both", expand=True, padx=48, pady=28)

        left = tk.Frame(wrap, bg=PANEL)
        left.pack(side="left", fill="both", expand=True, padx=(0, 26))
        self.eyebrow(left, "FASE 04 / DEXTER", RED)
        self.label(left, "A prova que realmente importa.", 28, TEXT, True).pack(anchor="w", pady=(14, 6))
        self.label(left, "Nada de pergunta sobre o nome da irmã. Agora são detalhes que uma fã de Dexter tem obrigação moral de saber.", 11, MUTED, wraplength=540, justify="left").pack(anchor="w")
        self.button(left, "ABRIR ARQUIVO DEXTER  →", self.start_dexter, primary=True, big=True).pack(anchor="w", pady=(26, 0))

        media = self.remote_image(wrap, DEXTER_IMAGE_URL, 390, 300, "imagem real • trailer oficial de Dexter / Dexter Official")
        media.pack(side="right", anchor="n")

    def start_dexter(self):
        self.dexter_score = 0
        self.index = 0
        self.render_dexter()

    def render_dexter(self):
        q = DEXTER[self.index]
        self.locked = False
        self.question_shell("validation/dexter", "DEXTER", self.index + 1, len(DEXTER), q["q"], "CASE OPEN")
        self.fill_options(q["options"], self.answer_dexter)

    def answer_dexter(self, selected):
        self.common_answer(DEXTER[self.index], selected, "dexter_score", self.next_dexter)

    def next_dexter(self):
        if self.index < len(DEXTER) - 1:
            self.index += 1
            self.render_dexter()
        else:
            self.show_score()

    def show_score(self):
        self.clear()
        self.set_head("final_report", "COMPLETE")
        wrap = tk.Frame(self.body, bg=PANEL)
        wrap.pack(fill="both", expand=True, padx=46, pady=30)
        self.eyebrow(wrap, "FINAL REPORT", GREEN)
        self.label(wrap, "Tá, você passou.", 29, TEXT, True).pack(anchor="w", pady=(8, 4))
        self.label(wrap, "O score técnico existe para fins de auditoria. O score oficial continua 100% porque o sistema é meu.", 10, MUTED, wraplength=850, justify="left").pack(anchor="w")

        grid = tk.Frame(wrap, bg=PANEL)
        grid.pack(fill="x", pady=24)
        data = [
            ("PROGRAMAÇÃO", f"{self.prog_score}/4"),
            ("NÓS DUAS", f"{self.us_score}/4"),
            ("LUANA", f"{self.me_score}/4"),
            ("DEXTER", f"{self.dexter_score}/4"),
            ("COMPATIBILIDADE", "100%"),
        ]
        for i, (k, v) in enumerate(data):
            c = self.card(grid, padx=13, pady=13)
            c.grid(row=0, column=i, padx=4, sticky="nsew")
            grid.grid_columnconfigure(i, weight=1)
            self.label(c, k, 7, MUTED, True, "Consolas").pack(anchor="w")
            self.label(c, v, 18, TEXT, True, "Consolas").pack(anchor="w", pady=(7, 0))

        report = self.card(wrap, bg=BLACK, padx=18, pady=15)
        report.pack(fill="x")
        rows = [
            ("integridade_do_relacionamento", "OK"),
            ("risco_de_rollback", "0.00%"),
            ("dark_passenger_compatibility", "APROVADA"),
            ("proprietaria_do_uno", "YASMIN (por enquanto)"),
        ]
        for key, value in rows:
            row = tk.Frame(report, bg=BLACK)
            row.pack(fill="x", pady=3)
            self.label(row, key, 9, MUTED, False, "Consolas", bg=BLACK).pack(side="left")
            self.label(row, value, 9, GREEN, True, "Consolas", bg=BLACK).pack(side="right")

        self.button(wrap, "CONTINUAR PARA PERGUNTAS SÉRIAS  →", self.show_forever_question, primary=True, big=True).pack(anchor="e", pady=(20, 0))

    def _runaway_screen(self, path, eyebrow, question, subtitle, yes_text, yes_command):
        self.clear()
        self.set_head(path, "DECISION REQUIRED", PINK)
        wrap = tk.Frame(self.body, bg=PANEL)
        wrap.pack(fill="both", expand=True, padx=50, pady=34)
        self.eyebrow(wrap, eyebrow)
        self.label(wrap, question, 31, TEXT, True, wraplength=850, justify="left", anchor="w").pack(fill="x", anchor="w", pady=(16, 7))
        self.label(wrap, subtitle, 11, MUTED, wraplength=850, justify="left", anchor="w").pack(fill="x", anchor="w")

        field = tk.Frame(wrap, bg=BLACK, highlightbackground=LINE, highlightthickness=1)
        field.pack(fill="both", expand=True, pady=(22, 0))

        yes = self.button(field, yes_text, yes_command, primary=True, big=True)
        yes.place(relx=.28, rely=.52, anchor="center")

        no = self.button(field, "NÃO", lambda: self.dodge_no(no, field, yes_command))
        no.place(relx=.68, rely=.52, anchor="center")
        no.bind("<Enter>", lambda e: self.dodge_no(no, field, yes_command))
        return field

    def dodge_no(self, no_btn, field, yes_command):
        self.play_sound("xp")
        no_btn.place(relx=random.uniform(.15, .82), rely=random.uniform(.18, .82), anchor="center")
        yes_labels = ["SIM", "SIM ♡", "ÓBVIO", "SIM, LUANA", "CLARO QUE SIM"]
        for _ in range(3):
            b = self.button(field, random.choice(yes_labels), yes_command, primary=True, compact=True)
            b.place(relx=random.uniform(.08, .88), rely=random.uniform(.12, .88), anchor="center")

    def show_forever_question(self):
        self._runaway_screen(
            "decision/forever",
            "PERGUNTA SÉRIA #01",
            "Minha macaquinha, você quer ficar comigo pra vida toda?",
            "Atenção: o botão NÃO apresenta um bug conhecido e pode se recusar a cooperar.",
            "SIM, PRA VIDA TODA ♡",
            self.show_uno_question,
        )

    def show_uno_question(self):
        self._runaway_screen(
            "decision/uno",
            "PERGUNTA SERÍSSIMA #02",
            "E você vai me dar o seu Uno?",
            "Essa pergunta existe porque eu me recuso a abandonar essa pauta. Negociações seguem abertas.",
            "SIM, O UNO É SEU 🚗",
            self.show_letter,
        )

    def show_letter(self):
        self.clear()
        self.set_head("release_notes", "DEPLOYED", GREEN)
        wrap = tk.Frame(self.body, bg=PANEL)
        wrap.pack(fill="both", expand=True, padx=46, pady=26)
        self.eyebrow(wrap, "RELEASE SUCCESSFUL", GREEN)
        self.label(wrap, "Agora sem sistema.", 24, TEXT, True).pack(anchor="w", pady=(7, 13))

        paper = tk.Frame(wrap, bg=WHITE, padx=32, pady=24)
        paper.pack(fill="both", expand=True)
        self.label(paper, "Para minha macaquinha,", 15, "#7f3f5b", True, "Georgia", bg=WHITE, justify="left", anchor="w").pack(fill="x", anchor="w", pady=(0, 12))
        self.label(paper, LETTER, 11, "#4a3440", False, "Georgia", bg=WHITE, wraplength=870, justify="left", anchor="nw").pack(fill="both", expand=True, anchor="w")
        self.label(paper, "— Luana ♡", 12, "#9f4168", True, "Georgia", bg=WHITE).pack(anchor="e", pady=(8, 0))


def main():
    root = tk.Tk()
    LoveSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()
