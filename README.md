# Nosso Quiz ❤️

Um quiz romântico em Python/Tkinter feito para virar um executável do Windows.

## Personalizar

Abra `main.py` e altere no topo:

```python
SEU_NOME = "Yasmin"
NOME_DELA = "Meu amor"
DATA_DO_NAMORO = "10/09"
```

Você também pode editar `MENSAGEM_FINAL` e as perguntas em `QUESTOES`.

## Rodar localmente

No PowerShell, dentro da pasta do projeto:

```powershell
python main.py
```

## Gerar o executável no Windows

### Opção mais fácil

Dê dois cliques em:

```text
build.bat
```

Ao terminar, o arquivo ficará em:

```text
dist\NossoQuiz.exe
```

### Pelo GitHub Actions

O repositório também possui o workflow `Build Windows EXE`.

1. Abra a aba **Actions** no GitHub.
2. Abra **Build Windows EXE**.
3. Clique em **Run workflow**.
4. Ao finalizar, baixe o artifact **NossoQuiz-Windows**.

## Tecnologia

- Python
- Tkinter
- PyInstaller

O aplicativo funciona offline e não envia nenhum dado para a internet.
