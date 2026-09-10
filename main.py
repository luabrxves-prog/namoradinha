import random
import tkinter as tk
from tkinter import messagebox


# ============================================================
# PERSONALIZE AQUI ANTES DE GERAR O .EXE
# ============================================================
SEU_NOME = "Yasmin"
NOME_DELA = "Meu amor"
DATA_DO_NAMORO = "10/09"

MENSAGEM_FINAL = (
    "Eu podia ter feito flores, uma carta ou comprado alguma coisa bonita...\n\n"
    "Mas como você transforma dados em coisas incríveis, eu quis transformar "
    "um pouquinho do que eu sinto por você em código.\n\n"
    "Obrigada por ser minha pessoa favorita, minha melhor parceria e o meu "
    "lugar seguro. Que a gente continue construindo essa história juntas, "
    "um commit, uma viagem, uma risada e um abraço por vez.\n\n"
    "Feliz aniversário de namoro. Eu te amo. ❤️"
)


QUESTOES = [
    {
        "pergunta": "1. Em qual banco de dados eu guardaria nossos melhores momentos?",
        "opcoes": [
            "PostgreSQL",
            "Um Data Lake infinito",
            "No meu coração",
            "Numa planilha chamada final_v7_agora_vai.xlsx",
        ],
        "correta": 2,
        "feedback": "Primary key encontrada: você. ❤️",
    },
    {
        "pergunta": "2. Se o nosso namoro fosse um pipeline, qual seria o ETL correto?",
        "opcoes": [
            "Extract, Transform, Load",
            "Eu, Tu e Love",
            "Erro, Timeout e Log",
            "Excel, Teams e LinkedIn",
        ],
        "correta": 1,
        "feedback": "Pipeline saudável, sem dados corrompidos e com muito carinho.",
    },
    {
        "pergunta": "3. Qual é a melhor estratégia de backup para nós duas?",
        "opcoes": [
            "Snapshot semanal",
            "Replicação multi-região",
            "Criar cada vez mais memórias juntas",
            "Pendrive na gaveta",
        ],
        "correta": 2,
        "feedback": "Backup confirmado. Retenção: para sempre. 💾💕",
    },
    {
        "pergunta": "4. Se um dia der erro 500 no nosso sistema, o que fazemos?",
        "opcoes": [
            "Desliga e liga de novo",
            "Abre um chamado",
            "Debuga com conversa, abraço e alguma coisa gostosa",
            "Culpa a infraestrutura",
        ],
        "correta": 2,
        "feedback": "Incidente resolvido. SLA do abraço: imediato.",
    },
    {
        "pergunta": "5. O que essa consulta retorna?\n\nSELECT * FROM futuro WHERE voce = 'comigo';",
        "opcoes": [
            "0 rows",
            "Uma exception",
            "Todas as linhas que eu quero viver",
            "NULL",
        ],
        "correta": 2,
        "feedback": "Query aprovada em produção. ✨",
    },
    {
        "pergunta": "6. Qual é o SLA mínimo de carinho aceitável neste relacionamento?",
        "opcoes": [
            "80%",
            "95%",
            "99,9%",
            "100% + margem para cafuné extra",
        ],
        "correta": 3,
        "feedback": "Monitoramento saudável: carinho acima da meta. 📈",
    },
    {
        "pergunta": "7. Última validação antes do deploy: você aceita continuar comigo?",
        "opcoes": [
            "SIM, em produção e sem rollback",
            "Talvez depois da homologação",
            "Vou abrir uma RFC",
            "Só se tiver documentação",
        ],
        "correta": 0,
        "feedback": "Deploy autorizado. Ambiente: nós duas. ❤️",
    },
]


class LoveQuizApp:
    BG = "#fff4f8"
    CARD = "#ffffff"
    PRIMARY = "#c74774"
    PRIMARY_DARK = "#9f3158"
    TEXT = "#402f37"
    MUTED = "#846d77"
    SOFT = "#f9dce7"
    SUCCESS = "#7f3855"

    def __init__(self, root):
        self.root = root
        self.root.title("Nosso Quiz ❤️")
        self.root.geometry("920x650")
        self.root.minsize(820, 600)
        self.root.configure(bg=self.BG)

        self.indice = 0
        self.pontos = 0
        self.respondida = False
        self.botoes_resposta = []

        self.canvas = tk.Canvas(root, bg=self.BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self._redesenhar_fundo)

        self.card = tk.Frame(self.canvas, bg=self.CARD, padx=44, pady=36)
        self.card_window = self.canvas.create_window(460, 325, window=self.card, width=760, height=520)

        self._mostrar_inicio()
        self._criar_coracoes()
        self._animar_coracoes()

    def _redesenhar_fundo(self, event):
        self.canvas.coords(self.card_window, event.width / 2, event.height / 2)
        largura = min(760, max(700, event.width - 90))
        altura = min(540, max(510, event.height - 90))
        self.canvas.itemconfigure(self.card_window, width=largura, height=altura)

    def _limpar_card(self):
        for widget in self.card.winfo_children():
            widget.destroy()

    def _label(self, texto, tamanho=12, negrito=False, cor=None, wrap=660, pady=0):
        fonte = ("Segoe UI", tamanho, "bold" if negrito else "normal")
        lbl = tk.Label(
            self.card,
            text=texto,
            font=fonte,
            fg=cor or self.TEXT,
            bg=self.CARD,
            wraplength=wrap,
            justify="center",
        )
        lbl.pack(pady=pady)
        return lbl

    def _botao(self, texto, comando, destaque=False):
        bg = self.PRIMARY if destaque else self.SOFT
        fg = "white" if destaque else self.PRIMARY_DARK
        active_bg = self.PRIMARY_DARK if destaque else "#f3c9d9"
        return tk.Button(
            self.card,
            text=texto,
            command=comando,
            font=("Segoe UI", 11, "bold"),
            bg=bg,
            fg=fg,
            activebackground=active_bg,
            activeforeground=fg,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=18,
            pady=11,
        )

    def _mostrar_inicio(self):
        self._limpar_card()

        self._label("♡  PROJETO SECRETO  ♡", 11, True, self.PRIMARY, pady=(8, 14))
        self._label("Sistema de Compatibilidade Afetiva", 25, True, self.TEXT, pady=(0, 8))
        self._label(
            f"Release especial de {DATA_DO_NAMORO} • feito por {SEU_NOME}",
            11,
            False,
            self.MUTED,
            pady=(0, 26),
        )

        caixa = tk.Frame(self.card, bg="#fff8fb", padx=22, pady=18)
        caixa.pack(fill="x", padx=30, pady=(0, 24))
        tk.Label(
            caixa,
            text=(
                f"Olá, {NOME_DELA}.\n\n"
                "Antes de liberar seu presente, o sistema precisa executar "
                "alguns testes de compatibilidade.\n\n"
                "Aviso técnico: as perguntas podem conter níveis perigosos de fofura."
            ),
            font=("Segoe UI", 12),
            fg=self.TEXT,
            bg="#fff8fb",
            wraplength=600,
            justify="center",
        ).pack()

        botao = self._botao("INICIAR PIPELINE DO AMOR  →", self._iniciar_quiz, destaque=True)
        botao.pack(pady=8)
        self._label("status: aguardando a engenheira de dados mais linda clicar", 9, False, self.MUTED, pady=(12, 0))

    def _iniciar_quiz(self):
        self.indice = 0
        self.pontos = 0
        self._mostrar_questao()

    def _mostrar_questao(self):
        self._limpar_card()
        self.respondida = False
        self.botoes_resposta = []

        total = len(QUESTOES)
        q = QUESTOES[self.indice]

        cabecalho = tk.Frame(self.card, bg=self.CARD)
        cabecalho.pack(fill="x", pady=(2, 16))

        tk.Label(
            cabecalho,
            text=f"CHECK {self.indice + 1:02d}/{total:02d}",
            font=("Consolas", 10, "bold"),
            fg=self.PRIMARY,
            bg=self.CARD,
        ).pack(side="left")

        tk.Label(
            cabecalho,
            text="pipeline: relacionamento_em_producao",
            font=("Consolas", 9),
            fg=self.MUTED,
            bg=self.CARD,
        ).pack(side="right")

        progresso_bg = tk.Frame(self.card, bg="#f3e7ec", height=8)
        progresso_bg.pack(fill="x", pady=(0, 25))
        progresso_bg.pack_propagate(False)

        proporcao = (self.indice + 1) / total
        progresso = tk.Frame(progresso_bg, bg=self.PRIMARY)
        progresso.place(relx=0, rely=0, relwidth=proporcao, relheight=1)

        self._label(q["pergunta"], 17, True, self.TEXT, wrap=640, pady=(0, 20))

        respostas = tk.Frame(self.card, bg=self.CARD)
        respostas.pack(fill="both", expand=True, padx=18)

        for i, opcao in enumerate(q["opcoes"]):
            btn = tk.Button(
                respostas,
                text=opcao,
                command=lambda idx=i: self._responder(idx),
                font=("Segoe UI", 10),
                bg="#fff8fb",
                fg=self.TEXT,
                activebackground=self.SOFT,
                activeforeground=self.PRIMARY_DARK,
                relief="flat",
                bd=0,
                cursor="hand2",
                anchor="w",
                padx=16,
                pady=9,
            )
            btn.pack(fill="x", pady=4)
            self.botoes_resposta.append(btn)

        self.feedback = tk.Label(
            self.card,
            text="",
            font=("Segoe UI", 10, "bold"),
            fg=self.SUCCESS,
            bg=self.CARD,
            wraplength=620,
            justify="center",
        )
        self.feedback.pack(pady=(12, 4))

    def _responder(self, escolha):
        if self.respondida:
            return

        self.respondida = True
        q = QUESTOES[self.indice]
        correta = q["correta"]

        for btn in self.botoes_resposta:
            btn.configure(state="disabled")

        self.botoes_resposta[correta].configure(
            state="normal",
            bg=self.SOFT,
            fg=self.PRIMARY_DARK,
        )

        if escolha == correta:
            self.pontos += 1
            texto = "✓ " + q["feedback"]
        else:
            texto = "♡ Resposta aceita porque o sistema é completamente parcial a seu favor."

        self.feedback.configure(text=texto)

        texto_botao = "VER RESULTADO  →" if self.indice == len(QUESTOES) - 1 else "PRÓXIMO CHECK  →"
        btn_proximo = self._botao(texto_botao, self._proxima, destaque=True)
        btn_proximo.pack(pady=(8, 2))

    def _proxima(self):
        if self.indice < len(QUESTOES) - 1:
            self.indice += 1
            self._mostrar_questao()
        else:
            self._mostrar_resultado()

    def _mostrar_resultado(self):
        self._limpar_card()

        self._label("✓ PIPELINE FINALIZADO COM SUCESSO", 11, True, self.PRIMARY, pady=(8, 12))
        self._label("Compatibilidade afetiva: 100%", 27, True, self.TEXT, pady=(0, 8))
        self._label(
            f"Acertos técnicos: {self.pontos}/{len(QUESTOES)} • Resultado oficial: APROVADA PARA SEMPRE",
            10,
            False,
            self.MUTED,
            pady=(0, 22),
        )

        resultado = tk.Frame(self.card, bg="#fff8fb", padx=24, pady=20)
        resultado.pack(fill="x", padx=28, pady=(0, 22))
        tk.Label(
            resultado,
            text=(
                "Nenhuma anomalia encontrada.\n"
                "Nenhum rollback recomendado.\n"
                "Próxima janela de manutenção: nunca.\n\n"
                "Recomendação do sistema: continuar escolhendo uma à outra."
            ),
            font=("Consolas", 10),
            fg=self.TEXT,
            bg="#fff8fb",
            justify="center",
        ).pack()

        self._botao("ABRIR MENSAGEM FINAL  ♡", self._abrir_mensagem, destaque=True).pack(pady=5)
        self._label("build: amor.v∞ • ambiente: produção", 9, False, self.MUTED, pady=(15, 0))

        for _ in range(14):
            self.root.after(random.randint(0, 1500), self._soltar_coracao)

    def _abrir_mensagem(self):
        janela = tk.Toplevel(self.root)
        janela.title("Uma última coisa... ❤️")
        janela.geometry("650x500")
        janela.minsize(580, 450)
        janela.configure(bg=self.BG)
        janela.transient(self.root)
        janela.grab_set()

        tk.Label(
            janela,
            text=f"Para {NOME_DELA},",
            font=("Segoe UI", 20, "bold"),
            fg=self.PRIMARY_DARK,
            bg=self.BG,
        ).pack(pady=(36, 18))

        tk.Label(
            janela,
            text=MENSAGEM_FINAL,
            font=("Segoe UI", 12),
            fg=self.TEXT,
            bg=self.BG,
            wraplength=540,
            justify="center",
        ).pack(padx=40, pady=10, expand=True)

        tk.Label(
            janela,
            text=f"— {SEU_NOME} ♡",
            font=("Segoe UI", 12, "bold"),
            fg=self.PRIMARY,
            bg=self.BG,
        ).pack(pady=(8, 30))

    def _criar_coracoes(self):
        self.coracoes = []
        largura = max(self.root.winfo_width(), 900)
        altura = max(self.root.winfo_height(), 650)

        for _ in range(18):
            item = self.canvas.create_text(
                random.randint(20, largura - 20),
                random.randint(20, altura - 20),
                text=random.choice(["♡", "♥", "·"]),
                fill=random.choice(["#efbfd1", "#f5d4df", "#e8b1c6"]),
                font=("Segoe UI Symbol", random.randint(11, 20)),
            )
            self.canvas.tag_lower(item, self.card_window)
            self.coracoes.append((item, random.uniform(0.15, 0.45)))

    def _animar_coracoes(self):
        altura = max(self.canvas.winfo_height(), 650)
        largura = max(self.canvas.winfo_width(), 900)

        for item, velocidade in self.coracoes:
            x, y = self.canvas.coords(item)
            y -= velocidade
            if y < -20:
                y = altura + 20
                x = random.randint(20, max(21, largura - 20))
            self.canvas.coords(item, x, y)

        self.root.after(40, self._animar_coracoes)

    def _soltar_coracao(self):
        largura = max(self.canvas.winfo_width(), 900)
        item = self.canvas.create_text(
            random.randint(40, largura - 40),
            self.canvas.winfo_height() + 10,
            text="♥",
            fill="#d96891",
            font=("Segoe UI Symbol", random.randint(14, 24), "bold"),
        )
        self.canvas.tag_lower(item, self.card_window)
        self.coracoes.append((item, random.uniform(0.6, 1.2)))


def main():
    root = tk.Tk()
    app = LoveQuizApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
