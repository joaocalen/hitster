#set page(
  paper: "a4",
  margin: (x: 2cm, y: 2cm),
)

#set text(
  font: "New Computer Modern",
  size: 11pt,
  lang: "pt"
)

#let title(content) = {
  text(font: "Roboto", weight: "bold", size: 1.5em, content)
  v(0.5em)
}

#let section(content) = {
  v(1em)
  text(font: "Roboto", weight: "bold", size: 1.2em, content)
  v(0.5em)
}

#let subheader(content) = {
  v(0.5em)
  text(font: "Roboto", weight: "bold", size: 1.1em, content)
  v(0.3em)
}

// Title
#align(center)[
  #text(font: "Roboto", weight: "black", size: 24pt)[Regras Rápidas]
]

#v(1cm)

#columns(2)[
  #section[Preparação]
  Decidam se vocês estão jogando em equipes ou individualmente.
  
  Cada jogador/equipe recebe uma carta de música (virada para cima), que mostra o nome da música, o artista e o ano de lançamento. Este é o lado sem o QR code e inicia a linha do tempo.
  
  Você pode jogar uma partida mais simples sem usar fichas. No entanto, se quiser uma partida mais desafiadora, distribua 2 fichas de HITSTER para cada jogador/equipe. [Clique aqui para aprender como as fichas funcionam.]

  Um jogador aleatório escaneia a carta do topo do baralho. Aquele que escanear ainda poderá jogar. Mantenha um único jogador para escanear ou alterne os jogadores; a escolha é de vocês!

  #text(weight: "bold")[Importante:] Os jogadores que desempenham o papel de DJ não devem usar smartwatches (ex.: Apple Watch) durante a partida, pois eles podem revelar informações sobre a música na tela.

  #section[Preparação da Música]
  
  #subheader[Spotify Free]
  Há duas maneiras de iniciar a música (escolha no menu de regras e preparação):
  
  - *Sensor de Giro* 🔄 \ A faixa começa a tocar depois que você vira o seu celular para baixo.
  - *Contagem Regressiva* ⏳ \ A faixa começa a tocar depois de uma contagem regressiva de 3 segundos. Certifique-se de que o seu celular esteja virado para baixo antes que a contagem termine.

  #subheader[Spotify Premium]
  Há duas maneiras de jogar:

  - *Faixas Completas* 🎵 \ Ouça a música inteira desde o começo. Perfeito para uma experiência completa.
  - *Prévias de 30 segundos* ⚡ \ Modo rápido! Primeiro, vire o celular para iniciar a música, depois curta um teaser de 30 segundos.
  
  Opções de início: Sensor de Giro 🔄 ou Contagem Regressiva de 3 segundos ⏳ (assim como na versão Free).

  #section[Como Jogar]

  #subheader[Escanear]
  Um jogador escaneia uma carta usando o aplicativo do HITSTER, e uma música começa a tocar.

  #subheader[Colocar]
  O jogador à esquerda do DJ coloca a carta (virada para baixo) em sua linha do tempo, tentando adivinhar se ela foi lançada antes, depois ou entre as cartas que já estão ali.

  #subheader[Virar]
  Vire a carta para verificar se ela está na posição correta. Se estiver, o jogador ficará com a carta. Caso contrário, descarte-a. Se o ano corresponder ao de uma carta ali presente, você poderá colocá-la antes ou depois da carta, e isso ainda contará como um acerto.

  #subheader[Vitória]
  O primeiro jogador a adivinhar a posição de 10 cartas em sua linha do tempo será o vencedor.

  #colbreak()

  #section[Usando as Fichas]
  Para uma partida mais estratégica, vocês podem adicionar as fichas:

  - *No seu turno:* Gaste 1 ficha para pular a música da vez e comprar uma nova carta.
  - *No turno do oponente:* Grite “HITSTER” e coloque a sua ficha na linha do tempo do seu oponente se você achar que ele colocou a carta dele incorretamente. Se você estiver correto, roube a carta para a sua linha do tempo.
  - *A qualquer momento:* Troque 3 fichas para pegar uma carta do baralho e colocá-la diretamente na sua linha do tempo sem precisar adivinhar. Você não precisa esperar o seu turno para fazer isso.

  #subheader[Ganhando Fichas]
  Nomeie a música e o artista corretamente para ganhar 1 ficha (mesmo que coloque a carta no lugar errado). Máximo de 5 fichas por jogador.

  #section[Variantes]
  #subheader[Modos de Jogo Avançados]
  Se quiserem aumentar a dificuldade, cada jogador pode escolher seu próprio nível:

  - *Profissional:* Siga as regras originais, mas você deve nomear o artista e a música para adquirir ou roubar cartas. Cada jogador Profissional começa a partida com 5 fichas. Não é possível obter novas fichas.
  - *Especialista:* Siga as regras originais, mas você deve nomear o artista, a música e o ano de lançamento exato. Cada jogador Especialista começa a partida com 3 fichas. Não é possível obter novas fichas.
  - *Cooperativo:* Joguem juntos como uma única equipe. Comecem com 5 fichas e 1 carta de música em sua linha do tempo. Trabalhem juntos para colocar novas cartas nos lugares certos. Se errarem, percam uma ficha. Coletem 10 cartas antes de ficarem sem fichas para vencer.

  #section[Regras do Uso das Fichas]
  
  #subheader[Trocando 3 fichas de HITSTER]
  Se um jogador quiser trocar 3 fichas de HITSTER para colocar uma carta diretamente em sua linha do tempo, ele deverá fazê-lo antes de ouvir a música. Ele não pode ouvir a música e então decidir trocá-la pelas fichas.

  #subheader[Apostando na Colocação Correta]
  Se um jogador colocar uma ficha na linha do tempo de outro jogador, apostando que a carta foi colocada incorretamente, e a carta estiver correta (mesmo que ambas as cartas sejam do mesmo ano), o jogador que colocou a carta ficará com ela. O jogador que apostou a ficha perderá a ficha, já que o jogador da vez estava correto.
  
  Se vários jogadores apostarem fichas, apenas o jogador que colocou a carta ficará com ela se ele estiver correto. Todas as fichas apostadas são perdidas.

  #text(style: "italic")[Observação:] O primeiro a gritar “HITSTER” coloca sua ficha primeiro. No entanto, se o próximo jogador a gritar “HITSTER” também achar que a resposta está errada, ele poderá escolher um ponto diferente na linha do tempo do oponente para tentar roubar a carta. Duas fichas não podem ser colocadas no mesmo ponto da linha do tempo do oponente.
]
