const SOUND_URLS = {
  dexter: "https://www.myinstants.com/media/sounds/dexter-meme.mp3",
  fahh: "https://www.myinstants.com/media/sounds/fahhhh-loud.mp3",
  xp: "https://www.myinstants.com/media/sounds/preview_4.mp3"
};

const PHASES = {
  programming: {
    label: "PROGRAMAÇÃO",
    path: "validation/programming",
    questions: [
      {
        tag:"PYTHON / CLOSURES",
        q:"Qual é a saída deste código?\n\nfuncs = [lambda: i for i in range(3)]\nprint([f() for f in funcs])",
        o:["[0, 1, 2]","[2, 2, 2]","[0, 0, 0]","NameError"], c:1,
        a:"[2, 2, 2]",
        why:"As lambdas capturam i por referência; quando executam, o loop já terminou em 2."
      },
      {
        tag:"SQL / WINDOW FUNCTION",
        q:"Você precisa manter apenas o pedido mais recente de cada cliente sem perder as outras colunas. Qual abordagem é a mais adequada?",
        o:["GROUP BY cliente_id e MAX(data)","DISTINCT cliente_id, *","ROW_NUMBER() OVER (PARTITION BY cliente_id ORDER BY data DESC) e filtrar rn = 1","ORDER BY data DESC LIMIT 1"], c:2,
        a:"ROW_NUMBER() ... rn = 1",
        why:"A window function escolhe a linha inteira mais recente dentro de cada cliente."
      },
      {
        tag:"DATA ENGINEERING / IDEMPOTÊNCIA",
        q:"Um pipeline pode reprocessar o mesmo lote depois de falhar. Qual desenho reduz melhor o risco de duplicar dados?",
        o:["INSERT puro em toda execução","Chave determinística + UPSERT/MERGE + checkpoint","Apagar a tabela inteira antes de cada carga","Aumentar o timeout do job"], c:1,
        a:"Chave determinística + UPSERT/MERGE + checkpoint",
        why:"Assim o mesmo lote pode ser repetido sem mudar o resultado final."
      },
      {
        tag:"GIT / HISTÓRICO COMPARTILHADO",
        q:"Um commit ruim já foi enviado para a main e outras pessoas já puxaram. Qual opção costuma ser mais segura para desfazer sem reescrever o histórico?",
        o:["git reset --hard HEAD~1","git revert <sha>","git clean -fd","git rebase -i --root"], c:1,
        a:"git revert <sha>",
        why:"Revert cria um novo commit inverso e preserva o histórico compartilhado."
      }
    ]
  },
  us: {
    label:"NÓS DUAS", path:"validation/us",
    questions:[
      {q:"Qual data está salva no banco oficial como nosso primeiro encontro?",o:["31 de março","2 de abril","4 de abril","10 de abril"],c:1,a:"2 de abril",right:"Mais que sua obrigação, macaquinha. 02/04 está versionado.",panic:true},
      {q:"Se eu rodar SELECT nossa_musica FROM memorias LIMIT 1, o que volta?",o:["Me Chamando de Paixão — Jorge Ben Jor","Meu — Djavan","Deusa do Amor — Caetano Veloso","Ensaio Sobre Ela — Cícero"],c:1,a:"Meu — Djavan"},
      {q:"Em qual mês aconteceu o primeiro 'eu te amo'?",o:["Abril","Maio","Junho","Julho"],c:1,a:"Maio"},
      {q:"Qual desses programas eu excluiria de um dia perfeito com você?",o:["Jogar","Ficar quietinhas","Sair","Nenhum deles"],c:3,a:"Nenhum deles",right:"Exato. Eu gosto de fazer tudo com você — inclusive absolutamente nada."}
    ]
  },
  me: {
    label:"LUANA", path:"validation/luana",
    questions:[
      {q:"Qual dessas alternativas descreve melhor minha relação com comida?",o:["Estrogonofe acima de tudo","Japonês e acabou","Salmão é sempre a primeira escolha","A pergunta é inválida porque eu gosto de praticamente tudo"],c:3,a:"Eu gosto de praticamente tudo"},
      {q:"Qual jogo fica no topo do meu ranking pessoal?",o:["Red Dead Redemption 2","Valorant","League of Legends","Detroit: Become Human"],c:3,a:"Detroit: Become Human"},
      {q:"Sem pegadinha desta vez: qual é minha cor preferida?",o:["Marsala","Marrom","Roxo","Preto"],c:1,a:"Marrom"},
      {q:"Qual seria, de verdade, o melhor cenário para um dia perfeito meu?",o:["Praia com sol","Restaurante caro","Festa até tarde","Um dia com você"],c:3,a:"Um dia com você",right:"Acertou a mais importante. Te amo."}
    ]
  },
  dexter: {
    label:"DEXTER", path:"validation/dexter",
    questions:[
      {q:"Quem é revelado como o Ice Truck Killer?",o:["Arthur Mitchell","Brian Moser","Miguel Prado","James Doakes"],c:1,a:"Brian Moser"},
      {q:"Qual é o nome do barco do Dexter?",o:["Sea Escape","Slice of Life","Dark Passenger","Bay Harbor"],c:1,a:"Slice of Life"},
      {q:"Quem acaba sendo responsabilizado publicamente como o Bay Harbor Butcher?",o:["Angel Batista","James Doakes","Frank Lundy","Miguel Prado"],c:1,a:"James Doakes"},
      {q:"Quem mata Rita no final da quarta temporada?",o:["Brian Moser","Travis Marshall","Arthur Mitchell / Trinity","Jordan Chase"],c:2,a:"Arthur Mitchell / Trinity"}
    ]
  }
};

let soundEnabled = true;
let activeAudio = null;
let currentPhase = "programming";
let questionIndex = 0;
let locked = false;
let lives = 4;
let xpCooldown = 0;
const scores = {programming:0, us:0, me:0, dexter:0};

function toggleSound(){
  soundEnabled=!soundEnabled;
  document.getElementById("soundToggle").textContent=soundEnabled?"SOM: ON":"SOM: OFF";
  if(!soundEnabled && activeAudio){activeAudio.pause();activeAudio=null;}
}
function playSound(name){
  if(!soundEnabled) return;
  if(name==="xp"){
    const now=Date.now();
    if(now-xpCooldown<900) return;
    xpCooldown=now;
  }
  try{
    if(activeAudio){activeAudio.pause();}
    activeAudio=new Audio(SOUND_URLS[name]);
    activeAudio.volume=name==="fahh"?.58:.7;
    activeAudio.play().catch(()=>{});
  }catch(e){}
}
function show(id,path,status="ONLINE"){
  document.querySelectorAll(".screen").forEach(s=>s.classList.remove("active"));
  document.getElementById(id).classList.add("active");
  document.getElementById("path").innerHTML="&nbsp;/ "+path;
  document.getElementById("status").textContent=status;
  window.scrollTo({top:0,behavior:"smooth"});
}
function showDashboard(){show("dashboard","relationship_health","ONLINE")}

const bootLines=[
  "[OK] carregando memórias compartilhadas...",
  "[OK] conectando ao cluster: coracao_da_yasmin",
  "[OK] validando credenciais do meu bichinho...",
  "[OK] identidade detectada: Meu amor",
  "[OK] procurando motivos para continuar juntas...",
  "[WARN] resultado excedeu o limite máximo de linhas",
  "[OK] inicializando meu aplicativozinho ∞",
  "SYSTEM READY."
];
let bootIndex=0;
const terminal=document.getElementById("terminal");
function boot(){
  if(bootIndex<bootLines.length){
    terminal.textContent+=bootLines[bootIndex++]+"\n";
    setTimeout(boot,bootIndex===bootLines.length?260:310);
  }else{
    terminal.innerHTML+='<span class="cursor"></span>';
    document.getElementById("openBtn").style.display="inline-block";
    document.getElementById("status").textContent="READY";
  }
}
boot();

function startPhase(name){
  currentPhase=name;
  questionIndex=0;
  scores[name]=0;
  if(name==="us") lives=4;
  renderQuestion();
  show("quiz",PHASES[name].path,name==="dexter"?"CASE OPEN":"TESTING");
}
function renderQuestion(){
  locked=false;
  const phase=PHASES[currentPhase], q=phase.questions[questionIndex];
  const cat=document.getElementById("quizCat");
  cat.textContent=q.tag||phase.label;
  cat.classList.toggle("red",currentPhase==="dexter");
  document.getElementById("quizCounter").textContent=`CHECK ${String(questionIndex+1).padStart(2,"0")}/${String(phase.questions.length).padStart(2,"0")}`;
  const bar=document.getElementById("quizBar");
  bar.style.width=((questionIndex+1)/phase.questions.length*100)+"%";
  bar.classList.toggle("dexter",currentPhase==="dexter");
  document.getElementById("question").textContent=q.q;
  document.getElementById("feedback").textContent="";
  document.getElementById("feedback").className="feedback";
  document.getElementById("nextBtn").style.display="none";
  renderHearts();

  const choices=document.getElementById("choices");
  choices.innerHTML="";
  q.o.forEach((option,i)=>{
    const b=document.createElement("button");
    b.className="choice";
    b.textContent=`  ${String.fromCharCode(65+i)}   ${option}`;
    b.onclick=()=>answer(i);
    choices.appendChild(b);
  });
}
function renderHearts(){
  const box=document.getElementById("hearts");
  if(currentPhase!=="us"){box.style.display="none";return;}
  box.style.display="flex";
  box.innerHTML='<span class="hearts-label">VIDAS</span>';
  for(let i=0;i<4;i++){
    const h=document.createElement("span");
    h.className="life-heart"+(i<lives?"":" dead");
    h.textContent=i<lives?"♥":"💔";
    box.appendChild(h);
  }
}
function answer(selected){
  if(locked) return;
  locked=true;
  const q=PHASES[currentPhase].questions[questionIndex];
  const buttons=[...document.querySelectorAll("#choices .choice")];
  buttons.forEach(b=>b.disabled=true);
  buttons[q.c].classList.add("good");
  const feedback=document.getElementById("feedback");

  if(selected===q.c){
    scores[currentPhase]++;
    feedback.textContent=q.right||("[PASS] "+(q.why||"Resposta validada."));
  }else{
    buttons[selected].classList.add("bad");
    feedback.classList.add("bad");
    feedback.textContent=`[ERRO] A resposta correta era ${q.a}. ${q.why||""}`;
    playSound("fahh");
    document.getElementById("app").classList.remove("shake");
    void document.getElementById("app").offsetWidth;
    document.getElementById("app").classList.add("shake");
    if(currentPhase==="us"){
      lives=Math.max(0,lives-1);
      renderHearts();
      breakHeart();
      if(lives===0) playSound("xp");
    }
    if(q.panic) panic02();
  }
  const next=document.getElementById("nextBtn");
  next.textContent=questionIndex===PHASES[currentPhase].questions.length-1?"FINALIZAR FASE →":"PRÓXIMA →";
  next.style.display="inline-block";
}
function nextQuestion(){
  const total=PHASES[currentPhase].questions.length;
  if(questionIndex<total-1){questionIndex++;renderQuestion();return;}
  if(currentPhase==="programming"){show("usIntro","phase/us","HEARTS ARMED");return;}
  if(currentPhase==="us"){show("meIntro","phase/luana","PERSONAL DATA");return;}
  if(currentPhase==="me"){showDexterIntro();return;}
  showScore();
}
function showDexterIntro(){
  show("dexterIntro","phase/dexter","MIAMI METRO");
  playSound("dexter");
}
function breakHeart(){
  const overlay=document.createElement("div");
  overlay.className="heart-break-overlay";
  const heart=document.createElement("div");
  heart.className="broken-heart";
  heart.textContent="💔";
  overlay.appendChild(heart);
  for(let i=0;i<18;i++){
    const s=document.createElement("span");
    s.className="shard";
    s.style.left=(45+Math.random()*10)+"%";
    s.style.top=(42+Math.random()*12)+"%";
    s.style.setProperty("--dx",(Math.random()*260-130)+"px");
    s.style.setProperty("--dy",(90+Math.random()*180)+"px");
    overlay.appendChild(s);
  }
  document.body.appendChild(overlay);
  setTimeout(()=>overlay.remove(),980);
}
function panic02(){
  const toast=document.createElement("div");
  toast.className="xp-flash";
  toast.textContent="SYSTEM ERROR • 02/04 NÃO ENCONTRADO • macaquinha sob investigação";
  document.body.appendChild(toast);
  setTimeout(()=>toast.remove(),950);
}
function showScore(){
  show("score","final_report","COMPLETE");
  const data=[
    ["PROGRAMAÇÃO",`${scores.programming}/4`],
    ["NÓS DUAS",`${scores.us}/4`],
    ["LUANA",`${scores.me}/4`],
    ["DEXTER",`${scores.dexter}/4`],
    ["COMPATIBILIDADE","100%"]
  ];
  document.getElementById("scoreGrid").innerHTML=data.map(([k,v])=>`<div class="score-box"><small>${k}</small><strong>${v}</strong></div>`).join("");
}
function showForever(){
  show("forever","decision/forever","DECISION REQUIRED");
  wireRunaway("foreverNo","foreverRunway",showUno);
}
function showUno(){
  show("uno","decision/uno","NEGOTIATION OPEN");
  wireRunaway("unoNo","unoRunway",showLetter);
}
function wireRunaway(noId,runwayId,yesFn){
  const no=document.getElementById(noId);
  const field=document.getElementById(runwayId);
  no.onmouseenter=()=>dodgeNo(no,field,yesFn);
  no.onclick=e=>{e.preventDefault();dodgeNo(no,field,yesFn)};
}
function dodgeNo(no,field,yesFn){
  playSound("xp");
  no.style.left=(10+Math.random()*78)+"%";
  no.style.top=(12+Math.random()*76)+"%";
  showXpToast();
  const labels=["SIM","SIM ♡","ÓBVIO","SIM, LUANA","CLARO QUE SIM"];
  for(let i=0;i<3;i++){
    const b=document.createElement("button");
    b.className="btn primary tiny-yes";
    b.textContent=labels[Math.floor(Math.random()*labels.length)];
    b.style.left=(6+Math.random()*86)+"%";
    b.style.top=(8+Math.random()*84)+"%";
    b.onclick=yesFn;
    field.appendChild(b);
  }
}
function showXpToast(){
  const toast=document.createElement("div");
  toast.className="xp-flash";
  toast.textContent="Windows XP: opção NÃO está sendo encerrada...";
  document.body.appendChild(toast);
  setTimeout(()=>toast.remove(),920);
}
function showLetter(){
  show("letterScreen","release_notes","DEPLOYED");
  celebrate();
}
function celebrate(){
  for(let i=0;i<44;i++){
    const e=document.createElement("div");
    e.className="shard";
    e.style.position="fixed";
    e.style.zIndex="50";
    e.style.left=(10+Math.random()*80)+"vw";
    e.style.top=(70+Math.random()*20)+"vh";
    e.style.background=[getComputedStyle(document.documentElement).getPropertyValue("--pink"),getComputedStyle(document.documentElement).getPropertyValue("--purple"),getComputedStyle(document.documentElement).getPropertyValue("--green")][Math.floor(Math.random()*3)];
    e.style.setProperty("--dx",(Math.random()*400-200)+"px");
    e.style.setProperty("--dy",(-220-Math.random()*440)+"px");
    document.body.appendChild(e);
    setTimeout(()=>e.remove(),1000);
  }
}
for(let i=0;i<28;i++){
  const e=document.createElement("div");
  e.className="float";
  e.textContent=["♡","·","✦"][Math.floor(Math.random()*3)];
  e.style.left=Math.random()*100+"vw";
  e.style.fontSize=(10+Math.random()*18)+"px";
  e.style.animationDuration=(12+Math.random()*16)+"s";
  e.style.animationDelay=(-Math.random()*20)+"s";
  document.getElementById("bg").appendChild(e);
}
