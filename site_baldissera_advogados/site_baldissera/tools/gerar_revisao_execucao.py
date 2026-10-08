"""
Gera public/execucao-penal-revisao-completa.html — página de serviço "Revisão completa da execução penal"
(pedido do Dr. Luiz, 08/10/2026).

Fonte única do conteúdo: os dicionários deste arquivo. Nunca editar o HTML gerado à mão: corrige-se aqui
e gera-se de novo (python tools/gerar_revisao_execucao.py).

Trilha das fontes (fora do git, ~/.claude/plans/site-execucao-penal/pesquisa/):
  A-inventario-crivo.md (o que a revisão confere) · B-catalogo-erros.md (erros e exemplos hipotéticos)
  C-julgados-selados.md (julgados já selados pela casa) · D-dados-oficiais-e-etica.md (CNJ/SENAPPEN/STF + Provimento 205)
  E-ficha-fontes.md (artigos e súmulas conferidos no portal oficial)
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import molde  # noqa: E402

PUBLIC = Path(__file__).resolve().parents[1] / "public"
SLUG = "execucao-penal-revisao-completa"
URL = f"https://www.baldisseraadvogados.com.br/{SLUG}"
TITULO = "Revisão completa da execução penal"
DESCRICAO = ("Como erros de cálculo, de lançamento e de decisão se propagam na execução penal, o que uma revisão "
             "completa confere, documento por documento, e o que dizem os dados oficiais e os tribunais.")
PDF_GUIA = "assets/docs/guia-revisao-execucao-penal.pdf"
PDF_ESTUDO = "assets/docs/estudo-revisao-execucao-penal.pdf"

# ---------------------------------------------------------------- I. números oficiais (D)
NUMEROS = [
    ("75,4%",
     "dos incidentes de execução com benefício vencido levantados em 2025 fora de São Paulo ainda dependiam de análise judicial",
     "CNJ, Relatório do I Mutirão Processual Penal — Pena Justa (2025), p. 28",
     "https://www.cnj.jus.br/wp-content/uploads/2025/11/relatorio-final-mutirao-2025-v5.pdf"),
    ("22.276",
     "pessoas cumpriam pena em estabelecimento de regime fechado embora sentenciadas a regime menos gravoso",
     "CNJ, Relatório do Mutirão Processual Penal (2023), p. 29",
     "https://www.cnj.jus.br/wp-content/uploads/2023/09/relatorio-mutirao-processual-penal.pdf"),
    ("10.224",
     "presos com progressão já deferida seguiam no regime fechado aguardando transferência em 31/12/2025, número mínimo: 673 unidades declararam não controlar o dado",
     "SENAPPEN, Relatório de Informações Penais, 2º semestre de 2025, p. 36",
     "https://www.gov.br/senappen/pt-br/servicos/sisdepen/relatorios"),
]

# ---------------------------------------------------------------- II. cascata (exemplo hipotético)
CASCATA = [
    ("A falta é reconhecida meses depois",
     "Uma falta grave ocorre em março; a decisão que a homologa sai em setembro. A lei manda recomeçar a contagem para a "
     "progressão a partir da data da falta.", "Origem do erro"),
    ("A nova data-base é lançada na data da decisão",
     "O cálculo adota setembro como novo início. Os seis meses entre a falta e a decisão deixam de contar.",
     "Seis meses de atraso na progressão seguinte"),
    ("A etapa seguinte herda o atraso",
     "Como cada progressão é contada a partir da anterior, o deslocamento tende a passar para as etapas seguintes e para "
     "o que delas depende.", "O atraso passa adiante"),
    ("O mesmo lançamento alcança o livramento",
     "A falta grave interrompe apenas a contagem da progressão. Se o cálculo reinicia também o prazo do livramento "
     "condicional, ou o tempo exigido para indulto e comutação, o erro passa a atingir benefícios que a lei preservou.",
     "Erro em dobro"),
    ("E a própria falta pode não se sustentar",
     "Falta reconhecida sem procedimento válido, sem defesa técnica ou fora do prazo não deveria produzir efeito algum. "
     "Afastada a falta, caem juntos a nova data-base, a eventual regressão e a perda de dias remidos.",
     "Três efeitos que caem juntos"),
]

# Quadro antes/depois — HIPOTÉTICO: pena de 8 anos; prisão preventiva em maio/2021 lançada como janeiro/2022
# (data do mandado definitivo). Frações ilustrativas: 1/6 para cada progressão (a segunda sobre o saldo de 80 meses),
# 1/3 para o livramento. Conta: 96 m × 1/6 = 16 m; 80 m × 1/6 = 13 m 10 d; 96 m × 1/3 = 32 m.
QUADRO = [
    ("Primeira progressão", "set/2022", "mai/2023"),
    ("Segunda progressão", "out/2023", "jun/2024"),
    ("Livramento condicional", "jan/2024", "set/2024"),
    ("Fim da pena", "mai/2029", "jan/2030"),
]

# ---------------------------------------------------------------- III. o que a revisão confere (A)
CAPITULOS = [
    ("Leitura dos autos e linha do tempo",
     "A revisão começa pela leitura integral, não por amostragem. Cada marco da execução é localizado no documento em que está.",
     [("Leitura de todas as folhas", "inclusive sentenças, denúncias e acórdãos antigos digitalizados como imagem; o que for ilegível é anotado no ponto exato."),
      ("Linha do tempo de marcos", "cada prisão, soltura, fuga, recaptura, falta e decisão de benefício, com data e folha."),
      ("Cadeia recursal até o trânsito", "a fundamentação que governa é a da última decisão, não a da sentença isolada."),
      ("Fato do caso e trecho citado", "o que é fato da condenação e o que é ementa transcrita pelo juiz não se confundem."),
      ("Situação dos corréus", "benefício de natureza objetiva concedido a corréu e nunca estendido."),
      ("Identificação e idade", "nome, filiação e data de nascimento: a idade na data do fato altera prazos de prescrição.")]),
    ("Guias, condenações e soma das penas",
     "A pena total é a base de todos os benefícios. Se ela está errada, todos os prazos estão errados.",
     [("Soma refeita", "cada condenação somada de novo e comparada ao total lançado, parcela a parcela."),
      ("Guia em duplicidade", "a mesma condenação cadastrada duas vezes, após mudança de vara ou de número."),
      ("Pena do acórdão", "a pena reduzida em recurso efetivamente lançada no lugar da pena da sentença."),
      ("Soma ou unificação", "crimes da mesma espécie, em condições semelhantes de tempo, lugar e modo, somados quando deveriam ser tratados como crime continuado."),
      ("Natureza de cada crime", "comum ou hediondo, com ou sem violência, primário ou reincidente, conforme a lei da data do fato e não conforme o cadastro."),
      ("Pena já cumprida", "condenação integralmente cumprida que continua pesando na base dos requisitos.")]),
    ("Prisão, detração e tempo cumprido",
     "O tempo de prisão provisória, e as restrições que a lei e a jurisprudência equiparam a ela, se descontam da pena. O que não é lançado simplesmente desaparece.",
     [("Prisão provisória do próprio processo", "flagrante e preventiva lançados com as datas reais, e não com a data do mandado definitivo."),
      ("Prisão em outro processo", "período de prisão em processo que terminou em absolvição ou arquivamento, quando cabe o desconto."),
      ("Recolhimento domiciliar noturno", "as horas de recolhimento convertidas em dias de pena cumprida."),
      ("Método do desconto", "a forma como o desconto incide sobre o requisito de cada benefício."),
      ("Suspensão e interrupção", "liberdade provisória e situações análogas não zeram o tempo já cumprido.")]),
    ("Remição por trabalho e estudo",
     "Cada dia trabalhado e cada hora estudada só reduzem a pena se forem reconhecidos e lançados.",
     [("Atestado convertido em dias", "trabalho e estudo convertidos na proporção legal, com o saldo que sobra levado ao período seguinte."),
      ("Dias atestados e nunca homologados", "certidões juntadas sem pedido nem decisão."),
      ("Remição de outra unidade", "trabalho feito em estabelecimento anterior cujas certidões nunca chegaram."),
      ("Decisão lançada", "a remição reconhecida pelo juiz conferida contra o número efetivamente digitado no cálculo."),
      ("Perda por falta grave", "perda limitada pela lei e dependente de decisão que justifique a fração aplicada.")]),
    ("Progressão de regime e datas-base",
     "O requisito de tempo da progressão depende de três dados: a pena, a fração legal e a data-base. Um erro em qualquer deles desloca as etapas seguintes; os demais requisitos são avaliados à parte.",
     [("Fração da lei do fato", "a fração conferida no texto legal vigente na data de cada crime; lei posterior mais grave não alcança fato anterior."),
      ("Duas leis, duas contas", "quando a lei mudou, as duas contas lado a lado, com a regra que decide qual se aplica."),
      ("Fração sobre o saldo", "a partir da segunda progressão, a fração incide sobre o que resta de pena."),
      ("Data-base após falta", "a data da falta, e não a data da decisão que a homologou."),
      ("Data-base após nova condenação", "condenação por fato anterior ao início do cumprimento não reinicia, por si, a contagem."),
      ("Benefício vencido e não pedido", "requisito temporal já atingido sem pedido nem decisão.")]),
    ("Faltas disciplinares e regressão",
     "A falta grave produz efeitos fortes: por isso é a primeira coisa a conferir, antes das datas.",
     [("Procedimento válido", "apuração com defesa técnica, oitiva e decisão fundamentada."),
      ("Prazo de apuração", "intervalo entre o fato e a homologação."),
      ("Efeitos limitados", "a falta interrompe a progressão, mas não reinicia o prazo do livramento nem, por si, o de indulto e comutação."),
      ("Regressão cautelar", "regressão provisória que se prolonga sem decisão definitiva."),
      ("Falta afastada", "quando a falta cai, a data-base volta e os benefícios que ela travava são reexaminados.")]),
    ("Livramento condicional",
     "O livramento corre em paralelo à progressão, com prazo e data-base próprios, e costuma ser esquecido.",
     [("Data-base própria", "conta-se da primeira prisão e não se altera por falta grave."),
      ("Primariedade e reincidência", "conferidas nas certidões e nas datas de cada condenação, e não apenas no cadastro do sistema."),
      ("Extinção que apaga a primeira prisão", "encerrar uma guia antiga pode deslocar o marco do livramento para uma prisão posterior."),
      ("Fim do período de prova", "suspensão ou revogação decretada depois de terminado o período de prova."),
      ("Revogação e tempo de prova", "situações em que o período em liberdade condicional conta como pena cumprida.")]),
    ("Indulto e comutação",
     "Os decretos presidenciais se examinam um a um, do mais antigo ao mais recente, pela situação na data de cada decreto.",
     [("Todos os decretos do período", "decretos antigos continuam aplicáveis, se os requisitos estavam presentes na data prevista."),
      ("Hipótese por hipótese", "vedação conferida inciso por inciso, nunca em bloco pelo tipo de crime."),
      ("Parcela não impeditiva", "a parte da pena por crime não impeditivo, que alguns decretos permitem alcançar."),
      ("Decisão que não chegou ao cálculo", "comutação deferida e nunca lançada."),
      ("Reexame após correção", "corrigida a pena ou afastada uma falta, os decretos dos anos afetados são revistos.")]),
    ("Prescrição na execução",
     "Quando o Estado demora a iniciar ou a retomar a execução, a pena pode deixar de ser exigível.",
     [("Prazo pela pena de cada crime", "sem o acréscimo do crime continuado."),
      ("Idade na data do fato", "a redução do prazo para quem tinha menos de 21 anos."),
      ("Causas que impedem o curso", "prisão por outro processo e marcos de interrupção."),
      ("Parcela prescrita", "a pena extinta que continua na base do cálculo.")]),
    ("Incidentes, cadastro e direitos",
     "Parte dos erros não está na conta, mas no cadastro e na tramitação.",
     [("Incidente parado", "pedido em tramitação que não aparece como pendente."),
      ("Mandado de prisão", "mandado indevidamente vigente, que impede a soltura mesmo com direito reconhecido."),
      ("Advogado cadastrado", "defesa não intimada dos incidentes por cadastro desatualizado."),
      ("Lei posterior mais benéfica", "norma que reduziu a pena ou reclassificou a conduta, aplicável na execução."),
      ("Vícios da condenação", "reincidência fora do período legal ou antecedente que não subsiste, quando indicam revisão criminal.")]),
    ("Pedidos e recursos",
     "Erro encontrado só produz efeito quando é levado ao juízo, na forma certa e na ordem certa.",
     [("Posição processual", "o que já foi pedido, decidido e recorrido, para não repetir pedido nem perder prazo."),
      ("Ordem por urgência", "direito vencido primeiro; depois impugnação ao cálculo; depois as medidas de mais longo prazo."),
      ("Memória de cálculo", "impugnação instruída com a conta exposta, parcela a parcela, e o documento de cada número."),
      ("Retificação das datas", "desconto reconhecido sempre acompanhado do pedido de retificação do cálculo e das datas-base."),
      ("Recurso", "agravo em execução e, diante de ilegalidade flagrante, habeas corpus.")]),
]

# ---------------------------------------------------------------- IV. erros frequentes (B; base legal conferida em E)
ERROS = [
    ("Remição reconhecida e lançada a menor",
     "O juiz reconhece trinta dias de desconto por trabalho ou estudo; no sistema, entram três. Ou remições antigas não são implantadas na migração dos autos para o meio eletrônico.",
     "como o tempo remido conta como pena cumprida, a diferença atrasa cada data ainda não alcançada: progressão, livramento e fim da pena.",
     "LEP, arts. 126 e 128."),
    ("Decisão favorável que não chega ao cálculo",
     "Comutação deferida, detração reconhecida ou data-base corrigida em recurso que nunca é lançada. Deferir e lançar são etapas distintas.",
     "o direito existe no papel, mas todas as datas continuam as mesmas.",
     "LEP, arts. 66, 106, § 2º, e 185."),
    ("A mesma condenação lançada duas vezes",
     "A guia é relançada após mudança de vara ou de número do processo, ou a guia provisória não é baixada quando chega a definitiva.",
     "pena total inflada; regime, progressão, livramento e término calculados sobre uma pena que não existe.",
     "LEP, arts. 106, § 2º, 111 e 185."),
    ("Crime cadastrado com natureza mais grave",
     "Tráfico privilegiado lançado como tráfico comum, crime sem violência marcado como violento, crime comum tratado como hediondo por lei posterior ao fato.",
     "fração maior em cada progressão e no livramento; o crime pode passar a impedir indulto.",
     "Constituição, art. 5º, XL; Código Penal, art. 2º, parágrafo único."),
    ("Primeira prisão com a data errada",
     "O cálculo adota a data do cumprimento do mandado definitivo, e não a do flagrante ou da preventiva.",
     "todas as datas, da primeira progressão ao fim da pena, deslocadas pelo mesmo intervalo.",
     "Código Penal, art. 42."),
    ("Fração de lei posterior aplicada a fato anterior",
     "A regra de tempo mais dura, criada depois do crime, é usada no cálculo, ou frações de épocas diferentes são misturadas.",
     "requisito maior em todas as progressões; o atraso se repete a cada etapa.",
     "Constituição, art. 5º, XL; LEP, art. 112."),
    ("Penas somadas quando o crime era continuado",
     "Crimes da mesma espécie, cometidos em condições semelhantes de tempo, lugar e modo, julgados em processos diferentes e simplesmente somados.",
     "pena total e regime mais graves do que a lei prevê para a unificação.",
     "Código Penal, art. 71; LEP, art. 111."),
    ("Detração não lançada",
     "Prisão provisória, prisão em outro processo encerrado sem condenação ou recolhimento domiciliar noturno que não entram no cálculo.",
     "dias que já foram cumpridos voltam a ser exigidos, em todas as datas.",
     "Código Penal, art. 42."),
    ("Falta grave reiniciando o que não reinicia",
     "A falta grave interrompe a contagem da progressão. O cálculo, porém, reinicia também o livramento ou o tempo exigido para indulto e comutação.",
     "benefícios preservados pela lei atrasados pelo tempo transcorrido desde a primeira prisão.",
     "Súmulas 441, 534 e 535 do STJ."),
    ("Falta reconhecida sem procedimento válido",
     "Apuração sem defesa técnica, sem oitiva do preso ou com autoria presumida, homologada mesmo assim.",
     "nova data-base, regressão e perda de dias remidos ao mesmo tempo.",
     "LEP, art. 118, § 2º; Súmula 533 do STJ."),
    ("Indulto e comutação nunca examinados",
     "Decretos de anos anteriores, que continuam aplicáveis, nunca são confrontados com a situação do condenado na data de cada um.",
     "redução ou extinção de pena que não chega a ser pedida; a pena a cumprir fica maior em todos os cálculos seguintes.",
     "LEP, arts. 192 e 193."),
    ("Livramento condicional esquecido",
     "O livramento corre em paralelo à progressão. Depois de progredir, ninguém confere que o prazo do livramento também chegou.",
     "anos de cumprimento em regime quando a lei já permitia a liberdade condicional.",
     "Código Penal, art. 83."),
]

# ---------------------------------------------------------------- V. exemplos hipotéticos (B: H-2, H-4, H-6, H-8)
EXEMPLOS = [
    ("Trinta dias que viraram três",
     "Um condenado estudou e trabalhou na unidade. O juiz reconheceu trinta dias de remição. Na digitação do cálculo, entraram três.",
     "A revisão compara a decisão com o número lançado e requer a retificação.",
     [("Remição reconhecida", "30 dias"), ("Remição lançada", "3 dias"), ("Diferença no fim da pena", "27 dias")]),
    ("A falta que reiniciou o prazo errado",
     "Pena de nove anos, cumprida desde janeiro de 2022. Com um terço (fração ilustrativa), o livramento caberia em janeiro de 2025. Em janeiro de 2024, uma falta grave. O cálculo reiniciou o livramento a partir da falta: um terço dos sete anos restantes.",
     "A falta grave não reinicia o prazo do livramento. A data do requisito de tempo continua sendo a original; o comportamento, avaliado em todo o histórico da execução, e os demais requisitos continuam a ser examinados à parte.",
     [("Data lançada", "maio de 2026"), ("Data do requisito temporal", "janeiro de 2025"), ("Diferença", "1 ano e 4 meses")]),
    ("Três furtos, uma só pena",
     "Três condenações em processos diferentes, por três furtos semelhantes, na mesma semana e no mesmo bairro, dois anos cada. Na execução, as penas foram somadas.",
     "Se presentes os requisitos da continuidade delitiva (crimes da mesma espécie, em condições semelhantes de tempo, lugar e modo de execução), aplica-se a pena de um dos crimes, aumentada de um quinto pelo número de crimes.",
     [("Penas somadas", "6 anos"), ("Pena unificada", "2 anos, 4 meses e 24 dias"), ("Diferença", "3 anos, 7 meses e 6 dias")]),
    ("O decreto que ninguém examinou",
     "Na data de um decreto antigo de comutação que reduzia um quinto da pena restante (fração ilustrativa), o condenado tinha cinco anos a cumprir e preenchia os requisitos. O pedido nunca foi feito.",
     "Decreto antigo continua aplicável se os requisitos estavam presentes na data prevista. Reconhecida a comutação, é preciso ainda conferir se ela foi lançada no cálculo.",
     [("Pena restante na data do decreto", "5 anos"), ("Comutação de um quinto", "1 ano"), ("Fim da pena", "1 ano antes")]),
]

# ---------------------------------------------------------------- VI. julgados (C) — preenchido com o que está selado
JULGADOS = [
    {"trib": "STJ · Tema Repetitivo 1.155",
     "tese": "O recolhimento domiciliar noturno durante o processo desconta da pena, com ou sem tornozeleira",
     "ponte": "Quem respondeu ao processo obrigado a ficar em casa à noite e nos dias de folga já cumpriu parte da pena. As horas "
              "de recolhimento são convertidas em dias e descontadas. É um dos períodos que mais ficam fora do cálculo, porque "
              "não aparecem como prisão. A matéria está também em exame no Supremo Tribunal Federal (Tema 1.454 de repercussão "
              "geral); até decisão em sentido contrário, a tese repetitiva do STJ é de observância obrigatória.",
     "rotulo_integral": "Ler as teses firmadas, na íntegra",
     "integral_html": "1) <strong>O período de recolhimento obrigatório noturno e nos dias de folga, por comprometer o status libertatis "
                      "do acusado, deve ser reconhecido como período a ser detraído da pena privativa de liberdade</strong> e da medida "
                      "de segurança, em homenagem aos princípios da proporcionalidade e do non bis in idem. 2) <strong>O monitoramento "
                      "eletrônico associado, atribuição do Estado, não é condição indeclinável para a detração</strong> dos períodos de "
                      "submissão a essas medidas cautelares, não se justificando distinção de tratamento ao investigado ao qual não é "
                      "determinado e disponibilizado o aparelhamento. 3) As horas de recolhimento domiciliar noturno e nos dias de folga "
                      "devem ser convertidas em dias para contagem da detração da pena. Se no cômputo total remanescer período menor que "
                      "vinte e quatro horas, essa fração de dia deverá ser desprezada.",
     "ref": "(REsp n. 1.977.135/SC, relator Ministro Joel Ilan Paciornik, Terceira Seção, julgado em 23/11/2022, DJe de 28/11/2022. Teses conferidas no portal de precedentes qualificados do STJ.)",
     "publicacao": "publicacao-recolhimento-noturno-desconta-da-pena.html"},
    {"trib": "STJ · Tema Repetitivo 1.354",
     "tese": "Cada condenação segue a lei do seu tempo: a fração mais dura da lei nova não alcança crime antigo",
     "ponte": "Quando a lei mudou entre um crime e outro, cada condenação recebe a fração de progressão da lei mais favorável ao seu "
              "fato: a fração mais dura da lei nova não alcança o crime anterior a ela. É uma questão de lei no tempo. Outra questão, a "
              "de crimes com e sem violência sob a mesma lei, foi decidida pelo Plenário do STF em sentido diverso, aplicando a fração "
              "mais grave sobre toda a pena (EP 102 AgR-segundo); por isso cada cálculo é conferido à luz dos dois entendimentos.",
     "rotulo_integral": "Ler a tese firmada, na íntegra",
     "integral_html": "<strong>É possível, para fins de cálculo para progressão de regime, a aplicação de percentuais distintos para cada "
                      "condenação isoladamente, em uma mesma execução</strong>, reconhecendo-se a retroatividade da Lei n. 13.964/2019 e a "
                      "ultratividade da redação anterior do art. 112 da Lei de Execução Penal, <strong>em respeito à norma mais favorável "
                      "ao executado</strong>.",
     "ref": "(REsp n. 2.037.377/SC, relatora Ministra Maria Marluce Caldas, Terceira Seção, julgado em 18/6/2026, DJEN de 2/7/2026, trânsito em julgado em 2/9/2026.)",
     "publicacao": "publicacao-tema-1354-e-a-progressao-por-condenacao.html"},
    {"trib": "STJ · Tema Repetitivo 1.165",
     "tese": "A contagem para a próxima progressão começa quando o direito nasceu, não quando o juiz decidiu",
     "ponte": "A decisão que concede a progressão apenas declara um direito que já existia. Se o cálculo adota como nova data-base "
              "o dia da decisão, ou da transferência, o tempo de espera vira pena. A tese tem um limite que a revisão também "
              "confere: se o último requisito a ser preenchido foi o subjetivo, é a data dele que serve de marco.",
     "rotulo_integral": "Ler a tese firmada, na íntegra",
     "integral_html": "<strong>A decisão que defere a progressão de regime não tem natureza constitutiva, senão declaratória. O termo "
                      "inicial para a progressão de regime deverá ser a data em que preenchidos os requisitos objetivo e subjetivo</strong> "
                      "descritos no art. 112 da Lei 7.210, de 11/07/1984 (Lei de Execução Penal), <strong>e não a data em que efetivamente "
                      "foi deferida a progressão</strong>. Essa data deverá ser definida de forma casuística, fixando-se como termo inicial "
                      "o momento em que preenchido o último requisito pendente, seja ele o objetivo ou o subjetivo. Se por último for "
                      "preenchido o requisito subjetivo, independentemente da anterior implementação do requisito objetivo, será aquele "
                      "(o subjetivo) o marco para fixação da data-base para efeito de nova progressão de regime.",
     "ref": "(REsp n. 1.972.187/SP, relator Ministro Og Fernandes, Terceira Seção, julgado em 14/8/2024, DJe de 2/12/2024. Tese conferida no portal de precedentes qualificados do STJ.)"},
    {"trib": "STJ · Tema Repetitivo 1.006",
     "tese": "Uma nova condenação somada às penas não zera o tempo já cumprido",
     "ponte": "Quando chega uma condenação nova, as penas são somadas ou unificadas, mas a data-base dos benefícios não muda por "
              "causa disso. O cálculo que reinicia a contagem na data da nova guia desconsidera tempo que já foi cumprido. "
              "A regra não se confunde com a falta grave, que interrompe a contagem da progressão.",
     "rotulo_integral": "Ler a tese firmada, na íntegra",
     "integral_html": "<strong>A unificação de penas não enseja a alteração da data-base para concessão de novos benefícios executórios.</strong>",
     "ref": "(REsp n. 1.753.512/PR e REsp n. 1.753.509/PR, relator Ministro Rogerio Schietti Cruz, Terceira Seção, julgado em 18/12/2018, DJe de 11/3/2019.)"},
    {"trib": "STJ · Súmulas 441 e 535 · Jurisprudência em Teses n. 7",
     "tese": "A falta grave não reinicia o prazo do livramento condicional, do indulto nem da comutação",
     "ponte": "A falta grave interrompe a contagem para a progressão de regime. Os demais prazos continuam correndo. A falta pode "
              "pesar na avaliação do comportamento para o livramento, e um decreto de indulto pode exigir expressamente a ausência "
              "de falta; o que não pode é o cálculo reiniciar esses prazos por conta própria.",
     "rotulo_integral": "Ler os enunciados, na íntegra",
     "integral_html": "Súmula 441: <strong>A falta grave não interrompe o prazo para obtenção de livramento condicional.</strong><br>"
                      "Súmula 535: <strong>A prática de falta grave não interrompe o prazo para fim de comutação de pena ou indulto.</strong><br>"
                      "Jurisprudência em Teses n. 7, tese 10: A prática de falta grave não interrompe o prazo para fim de comutação de pena ou "
                      "indulto, salvo se houver expressa previsão a respeito no decreto concessivo dos benefícios.",
     "ref": "(Súmula 441, Terceira Seção, julgada em 28/4/2010, DJe de 13/5/2010; Súmula 535, Terceira Seção, julgada em 10/6/2015, DJe de 15/6/2015; STJ, Jurisprudência em Teses n. 7, tese 10.)"},
    {"trib": "LEP, art. 127 · STJ, Jurisprudência em Teses, edição 7, tese 8",
     "tese": "A falta grave custa no máximo um terço dos dias remidos, e a fração precisa ser justificada",
     "ponte": "Os dias ganhos com trabalho e estudo não se perdem por inteiro. A lei fixa um teto, e o juiz deve dimensionar a "
              "perda conforme a natureza, os motivos, as circunstâncias e as consequências da falta. A perda de um terço lançada "
              "automaticamente, sem decisão que a fundamente, é erro que a revisão aponta.",
     "rotulo_integral": "Ler o dispositivo e a tese, na íntegra",
     "integral_html": "LEP, art. 127: Em caso de falta grave, <strong>o juiz poderá revogar até 1/3 (um terço) do tempo remido</strong>, "
                      "observado o disposto no art. 57, recomeçando a contagem a partir da data da infração disciplinar.<br>"
                      "Tese 8: Com o advento da Lei n. 12.433, de 29 de junho de 2011, <strong>o cometimento de falta grave não mais "
                      "enseja a perda da totalidade do tempo remido, mas limita-se ao patamar de 1/3, cabendo ao juízo das execuções "
                      "penais dimensionar o quantum, segundo os critérios do art. 57 da LEP</strong>.",
     "ref": "(Lei n. 7.210/1984, art. 127, conforme o texto compilado do Planalto; STJ, Jurisprudência em Teses n. 7, Falta Grave em Execução Penal, tese 8.)"},
]

# ---------------------------------------------------------------- VII. método (A, parte 3)
METODO = [
    ("Leitura integral", "Todas as folhas dos autos de execução e dos processos de origem são lidas, inclusive as digitalizadas como imagem. Nada é examinado por amostragem."),
    ("Cada fato com a sua folha", "Nenhuma afirmação entra no relatório sem a indicação do documento, da folha ou do evento em que está."),
    ("Conta refeita do zero", "Pena, detração, remição, fração e data de cada benefício recalculadas parcela a parcela, com a conta exposta. O total não é copiado: é somado de novo."),
    ("A lei de cada fato", "Cada fração é conferida no texto legal vigente na data de cada crime. Quando a lei mudou, as duas contas são apresentadas lado a lado."),
    ("Confronto com o cálculo oficial", "Cada número recalculado é comparado com o oficial. A divergência é confrontada com o título antes de ser apontada como erro."),
    ("Cenários quando falta documento", "Faltando um dado, a data aparece como hipótese declarada, nunca como certeza. O que não foi apurado não é tratado como inexistente."),
    ("Posição processual", "Antes de propor qualquer pedido, verifica-se o que já foi requerido, decidido e recorrido, para não repetir pedido nem perder prazo."),
    ("Divergências nos dois sentidos", "Divergência que favorece o condenado também é registrada, em seção própria, para que a defesa conheça a situação inteira da execução."),
    ("Revisão e responsabilidade", "O relatório passa por conferência independente antes de chegar ao cliente. Pedidos e recursos são assinados pelo advogado responsável."),
]

ENTREGA = [
    ("Relatório escrito", "a situação da execução, os erros e as divergências encontrados, cada um com o documento que o sustenta e o argumento que pode afastá-lo."),
    ("Linha do tempo", "todos os marcos da execução, com data e folha."),
    ("Memória de cálculo", "a conta de cada benefício, refeita e comparada com o cálculo oficial."),
    ("Quadro de benefícios", "o que já está vencido, o que vence em breve e o que depende de documento ainda não localizado."),
    ("Plano de pedidos", "as providências cabíveis, em ordem de urgência."),
]

# ---------------------------------------------------------------- VIII. documentos
DOCUMENTOS = [
    ("Número do processo de execução", "e, se houver, dos processos de origem."),
    ("Atestado de pena ou relatório da situação executória", "o mais recente."),
    ("Guias de recolhimento", "definitivas e provisórias."),
    ("Sentenças e acórdãos", "com as certidões de trânsito em julgado."),
    ("Decisões da execução", "progressão, remição, faltas, indulto, comutação, unificação."),
    ("Certidões de trabalho e de estudo", "de todas as unidades por onde passou."),
    ("Documentos de prisões anteriores", "auto de prisão em flagrante, mandados cumpridos, alvarás de soltura."),
    ("Procedimentos disciplinares", "se houve falta."),
    ("Documento de identidade", "com a data de nascimento."),
]

# ---------------------------------------------------------------- IX. perguntas frequentes (Provimento 205: informar, não convocar)
FAQ = [
    ("A revisão sempre encontra erro?",
     "Não. Há execuções corretamente calculadas, e não é possível antecipar o resultado antes de examinar os autos. Mesmo quando "
     "não há erro, a revisão entrega a linha do tempo, a memória de cálculo e o calendário dos benefícios, o que permite pedir "
     "cada um no momento em que se torna cabível."),
    ("Quem pode pedir a revisão?",
     "Para atuar no processo de execução, o advogado precisa ser constituído pelo condenado, em regra por procuração. Familiares "
     "costumam ajudar a reunir os documentos."),
    ("Já existe advogado no processo. A revisão é possível?",
     "Sim. A revisão pode ser feita em apoio à defesa já constituída, em diálogo com o colega responsável pelo processo."),
    ("Um erro antigo ainda pode ser apontado?",
     "O cálculo de pena acompanha toda a execução e é atualizado a cada incidente. Erro de cálculo demonstrado pode ser levado ao "
     "juízo da execução enquanto a pena é cumprida; a forma e o momento dependem do caso."),
    ("Quanto tempo leva?",
     "Depende do volume dos autos e do número de condenações. Execuções com várias guias, faltas e transferências exigem mais tempo "
     "de leitura e de conferência."),
    ("E se a divergência encontrada favorecer o condenado?",
     "Ela é registrada em seção própria do relatório, com a análise de seus riscos, para que a defesa conheça toda a situação da execução."),
]


# ================================================================= montagem
def esc(t: str) -> str:
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def secao(sid: str, numeral: str, titulo: str, corpo: str, nota: str = "") -> str:
    n = f'\n      <p class="nota-secao">{nota}</p>' if nota else ""
    return f'''  <section class="secao" id="{sid}" aria-labelledby="t-{sid}">
    <header>
      <span class="numeral" aria-hidden="true">{numeral}</span>
      <h2 id="t-{sid}">{titulo}</h2>{n}
    </header>
{corpo}
  </section>
'''


def grafico_svg() -> str:
    """Linha do tempo HIPOTÉTICA: o mesmo erro de data desloca todas as etapas (QUADRO)."""
    meses = {"jan": 0, "fev": 1, "mar": 2, "abr": 3, "mai": 4, "jun": 5, "jul": 6, "ago": 7, "set": 8, "out": 9, "nov": 10, "dez": 11}
    x0, x1, a0, a1 = 190, 690, 2022, 2030.5

    def x(d: str) -> float:
        m, a = d.split("/")
        v = int(a) + meses[m] / 12
        return round(x0 + (v - a0) / (a1 - a0) * (x1 - x0), 1)

    partes = ['<svg class="rv-grafico" viewBox="0 0 700 270" role="img" aria-labelledby="g-tit g-desc">',
              '<title id="g-tit">Exemplo hipotético: um erro na data da primeira prisão</title>',
              '<desc id="g-desc">Para cada etapa, a data revista e a data lançada com o erro. Primeira progressão: setembro de 2022 e '
              'maio de 2023. Segunda progressão: outubro de 2023 e junho de 2024. Livramento: janeiro de 2024 e setembro de 2024. '
              'Fim da pena: maio de 2029 e janeiro de 2030. Oito meses de diferença em cada etapa.</desc>']
    for ano in range(2022, 2031):
        xa = x(f"jan/{ano}")
        partes.append(f'<line class="g-fio" x1="{xa}" y1="20" x2="{xa}" y2="215"/>')
        partes.append(f'<text class="g-rotulo" x="{xa}" y="234" text-anchor="middle">{ano}</text>')
    for i, (nome, rev, lan) in enumerate(QUADRO):
        y = 45 + i * 50
        xr, xl = x(rev), x(lan)
        partes.append(f'<text class="g-titulo" x="0" y="{y + 5}">{nome}</text>')
        partes.append(f'<rect class="g-ganho" x="{xr}" y="{y - 3}" width="{round(xl - xr, 1)}" height="6"/>')
        partes.append(f'<circle class="g-revisto" cx="{xr}" cy="{y}" r="7"/><circle class="g-oficial" cx="{xl}" cy="{y}" r="7"/>')
    partes.append('<circle class="g-revisto" cx="196" cy="258" r="6"/><text class="g-rotulo" x="208" y="262">data revista</text>')
    partes.append('<circle class="g-oficial" cx="306" cy="258" r="6"/><text class="g-rotulo" x="318" y="262">data lançada com o erro</text>')
    partes.append('<rect class="g-ganho" x="476" y="255" width="22" height="6"/><text class="g-rotulo" x="506" y="262">8 meses de atraso</text>')
    partes.append("</svg>")
    return "\n".join(partes)


def corpo_html() -> str:
    s = []
    s.append(f'''  <p class="trilha"><a href="areas-de-atuacao.html">Áreas de atuação</a> / <a href="area-execucao-penal.html">Execução Penal</a> / Revisão completa</p>

  <section class="abertura-imagem abertura-imagem-area">
    <div class="abertura-texto">
      <h1>{TITULO}</h1>
      <p class="preambulo">A pena fixada na sentença atravessa anos de cálculos, lançamentos e decisões até o último dia de cumprimento. Um dado errado nesse percurso — uma data, uma fração, um período esquecido — não fica onde nasceu: segue para cada benefício seguinte. A revisão refaz a execução desde o início, documento por documento, e confere se a pena que está sendo cumprida é a pena que a lei manda cumprir.</p>
      <p class="remissoes"><a class="remissao" href="#conferencias">O que a revisão confere</a> <a class="remissao" href="#materiais">Guia em PDF</a></p>
    </div>
    <img class="abertura-foto" src="assets/images/conceito/area-execucao-penal-abertura.jpg" alt="" width="1600" height="629" fetchpriority="high">
  </section>

  <div class="abertura abertura-area">
    <nav class="sumario" aria-label="Nesta página">
      <a href="#problema">O problema</a>
      <a href="#cascata">O efeito cascata</a>
      <a href="#conferencias">O que se confere</a>
      <a href="#erros">Erros</a>
      <a href="#exemplos">Exemplos</a>
      <a href="#tribunais">Tribunais</a>
      <a href="#metodo">Método</a>
      <a href="#documentos">Documentos</a>
      <a href="#perguntas">Perguntas</a>
    </nav>
  </div>
''')
    # I — problema
    nums = "\n".join(
        f'      <li><span class="rv-num">{n}</span><span class="rv-num-rotulo">{esc(r)}</span>'
        f'<span class="rv-num-fonte"><a href="{u}" target="_blank" rel="noopener">{esc(f)}<span class="so-leitor"> (abre em nova aba)</span></a></span></li>'
        for n, r, f, u in NUMEROS)
    s.append(secao("problema", "I", "Da pena no papel e da pena na lei", f'''    <p class="rv-tese">Na execução penal, um erro raramente é um só.</p>
    <div class="rv-coluna">
      <p class="abre">A execução penal é uma conta longa, feita por muitas mãos. A sentença e o acórdão fixam a pena; a guia de recolhimento a transporta para a vara de execução; servidores a lançam no sistema eletrônico; a unidade prisional informa trabalho, estudo e ocorrências; o juízo decide incidentes ao longo de anos. Cada passagem é um ponto em que um número pode ser digitado errado, uma decisão pode não chegar ao cálculo, um período pode ficar de fora.</p>
      <p>A lei também muda. As frações exigidas para a progressão de regime foram reescritas mais de uma vez nos últimos anos, e cada condenação se rege pela lei vigente na data do fato, não pela do dia em que o cálculo é feito. Quem cumpre várias penas pode ter, no mesmo cálculo, regras de épocas diferentes, e é aí que a conta costuma falhar.</p>
      <p>O sistema eletrônico calcula o que recebe. Juntar um documento aos autos não é o mesmo que lançar o dado: a remição reconhecida, o período de prisão provisória, a comutação deferida só produzem efeito quando são lançados nos campos certos. Um cálculo pode estar aritmeticamente perfeito e, ainda assim, errado, porque partiu de um dado errado.</p>
      <p>Os levantamentos oficiais mostram a dimensão do problema. Nos mutirões nacionais, o Conselho Nacional de Justiça encontrou processos com benefício já vencido e sem decisão, e pessoas em regime mais rigoroso do que o fixado na condenação. O próprio CNJ ressalva que parte desses casos corresponde a atraso de lançamento no sistema, e não à perda de um direito; em ambos, a conferência é o que separa uma situação da outra.</p>
    </div>
    <ul class="rv-numeros">
{nums}
    </ul>
''', ""))
    # II — cascata
    casc = "\n".join(f'      <li><h3>{esc(t)}</h3><p>{esc(p)}</p><span class="rv-atraso">{esc(a)}</span></li>' for t, p, a in CASCATA)
    linhas = "\n".join(f'        <tr><th scope="row">{esc(n)}</th><td>{r}</td><td>{l}</td><td class="rv-dif">8 meses</td></tr>' for n, r, l in QUADRO)
    s.append(secao("cascata", "II", "Do efeito cascata", f'''    <div class="rv-coluna">
      <p class="abre">Na execução, os benefícios são encadeados. Cada um é contado a partir de uma pena e de uma data-base que dependem das etapas anteriores. Por isso o erro não permanece no ponto em que nasceu: ele se propaga. Um exemplo, em cinco passos:</p>
    </div>
    <ol class="rv-cascata">
{casc}
    </ol>
    <div class="rv-coluna">
      <p class="abre">O mesmo vale para uma única data errada. No exemplo hipotético abaixo, a pena é de oito anos e a prisão preventiva começou em maio de 2021; o cálculo lançou como início janeiro de 2022, a data do mandado definitivo. Oito meses de diferença na origem são oito meses de diferença em cada etapa.</p>
    </div>
{grafico_svg()}
    <table class="rv-quadro">
      <caption>Exemplo hipotético · frações ilustrativas</caption>
      <thead><tr><th scope="col">Etapa</th><th scope="col">Data revista</th><th scope="col">Data lançada</th><th scope="col">Atraso</th></tr></thead>
      <tbody>
{linhas}
      </tbody>
      <tfoot><tr><td colspan="4">Pena de 8 anos; um sexto para cada progressão (a segunda sobre o saldo) e um terço para o livramento, frações usadas só para ilustrar. Em caso real, a fração depende da data do fato, da natureza do crime e da reincidência, e cada data é calculada com a conta exposta.</td></tr></tfoot>
    </table>
''', "Como um erro em um ponto da execução repercute em todos os benefícios seguintes."))
    # III — conferências
    caps = []
    for i, (t, intro, itens) in enumerate(CAPITULOS, 1):
        li = "\n".join(f'          <li><strong>{esc(a)}</strong>: {esc(b)}</li>' for a, b in itens)
        caps.append(f'''    <details>
      <summary><span class="cap-num">{i}</span><span class="cap-titulo">{esc(t)}</span><span class="cap-qtd">{len(itens)} conferências</span></summary>
      <div class="cap-corpo">
        <p>{esc(intro)}</p>
        <ul>
{li}
        </ul>
      </div>
    </details>''')
    total = sum(len(c[2]) for c in CAPITULOS)
    s.append(secao("conferencias", "III", "Do que a revisão confere", f'''    <div class="rv-capitulos">
{chr(10).join(caps)}
    </div>
''', f"{len(CAPITULOS)} capítulos e {total} pontos de conferência, na ordem em que a execução é examinada. Toque em cada capítulo para abrir."))
    # IV — erros
    er = "\n".join(f'''      <li><h3>{esc(t)}</h3><p>{esc(c)}</p><p class="rv-efeito">{esc(e)}</p><p class="rv-base">{esc(b)}</p></li>''' for t, c, e, b in ERROS)
    s.append(secao("erros", "IV", "Dos erros que a revisão procura", f'''    <ul class="rv-erros">
{er}
    </ul>
''', "Doze erros, entre os mais de quarenta que a revisão procura, descritos de forma genérica. O estudo completo, em PDF, trata de todos."))
    # V — exemplos
    ex = []
    for t, cena, sol, conta in EXEMPLOS:
        dl = "\n".join(f'          <dt>{esc(a)}</dt><dd{" class=\"rv-saldo\"" if j == len(conta) - 1 else ""}>{esc(b)}</dd>' for j, (a, b) in enumerate(conta))
        ex.append(f'''      <article class="rv-exemplo">
        <p class="rotulo">Exemplo hipotético</p>
        <h3>{esc(t)}</h3>
        <p>{esc(cena)}</p>
        <p>{esc(sol)}</p>
        <dl>
{dl}
        </dl>
      </article>''')
    s.append(secao("exemplos", "V", "Dos exemplos", f'''    <div class="rv-exemplos">
{chr(10).join(ex)}
    </div>
''', "Situações fictícias, criadas para explicar; não se referem a casos do escritório. As frações são ilustrativas."))
    # VI — tribunais
    if JULGADOS:
        js = []
        for j in JULGADOS:
            leia = f'\n      <p class="rv-leia"><a class="remissao" href="{j["publicacao"]}">Análise completa no site</a></p>' if j.get("publicacao") else ""
            js.append(f'''    <article class="rv-julgado">
      <p class="rv-trib">{esc(j["trib"])}</p>
      <h3>{esc(j["tese"])}</h3>
      <p>{esc(j["ponte"])}</p>
      <details>
        <summary>{esc(j.get("rotulo_integral", "Ler a ementa integral"))}</summary>
        <blockquote>{j["integral_html"]}<span class="rv-ref">{esc(j["ref"])}</span></blockquote>
      </details>{leia}
    </article>''')
        s.append(secao("tribunais", "VI", "Do que dizem os tribunais", f'''    <div class="rv-julgados">
{chr(10).join(js)}
    </div>
''', "Precedentes conferidos na fonte oficial. O texto integral abre ao toque, sem cortes."))
    # VII — método
    me = "\n".join(f'      <li><h3>{esc(t)}</h3><p>{esc(p)}</p></li>' for t, p in METODO)
    en = "\n".join(f'          <li><strong>{esc(a)}</strong>: {esc(b)}</li>' for a, b in ENTREGA)
    s.append(secao("metodo", "VII", "Do método", f'''    <ol class="rv-metodo">
{me}
    </ol>
    <div class="rv-coluna">
      <h3 class="sub-secao">O que o cliente recebe</h3>
      <div class="rv-capitulos"><div class="cap-corpo">
        <ul>
{en}
        </ul>
      </div></div>
    </div>
''', "O trabalho é feito por advogados, folha a folha, com a conta exposta."))
    # VIII — documentos
    do = "\n".join(f'      <li><strong>{esc(a)}</strong>, {esc(b)}</li>' for a, b in DOCUMENTOS)
    s.append(secao("documentos", "VIII", "Dos documentos para começar", f'''    <ul class="rv-docs">
{do}
    </ul>
    <p class="rv-aviso">Não é preciso reunir tudo de início. Com a procuração, o advogado tem acesso aos autos eletrônicos da execução; os documentos da família servem para completar o que não estiver lá.</p>
''', "Quanto mais completo o conjunto, mais completa a revisão."))
    # IX — perguntas
    fq = "\n".join(f'    <details><summary>{esc(q)}</summary><p>{esc(r)}</p></details>' for q, r in FAQ)
    s.append(secao("perguntas", "IX", "Das perguntas frequentes", f'''    <div class="rv-faq">
{fq}
    </div>
'''))
    # X — materiais e atendimento
    ico = ('<svg viewBox="0 0 24 28" aria-hidden="true" focusable="false"><path d="M3 1h12l6 6v20H3z"/><path d="M15 1v6h6"/>'
           '<path d="M7 14h10M7 18h10M7 22h6"/></svg>')
    s.append(secao("materiais", "X", "Dos materiais e do atendimento", f'''    <ul class="rv-baixar">
      <li><a href="{PDF_GUIA}" download>{ico}<span class="b-titulo">Guia da revisão</span><span class="b-desc">Versão objetiva: o que é a revisão, por que importa, o que se confere e quais documentos reunir.</span><span class="b-acao">Baixar PDF</span></a></li>
      <li><a href="{PDF_ESTUDO}" download>{ico}<span class="b-titulo">Estudo completo</span><span class="b-desc">Versão aprofundada: o catálogo de erros, os exemplos com a conta, os dados oficiais e os precedentes.</span><span class="b-acao">Baixar PDF</span></a></li>
    </ul>
    <div class="atendimento">
      <p>Atendimento nas unidades de Cascavel, Porto Alegre e Foz do Iguaçu, com agendamento prévio.</p>
      <p><a class="botao" href="agendar.html">Agendar atendimento</a> <a class="remissao" href="area-execucao-penal.html">Execução Penal</a></p>
    </div>
    <p class="rv-aviso">Conteúdo informativo, nos termos do Provimento CFOAB 205/2021. Os exemplos são hipotéticos e não se referem a casos do escritório. O resultado de cada execução depende dos documentos e das circunstâncias do caso. Dados oficiais com fonte e página indicadas; consulta em 8 de outubro de 2026.</p>
'''))
    s.append('''  <section class="autor-bloco" aria-label="Responsável técnico">
    <img src="assets/images/luiz-henrique-baldissera.jpg" alt="Luiz Henrique Baldissera" width="600" height="750" loading="lazy">
    <div>
      <p class="rotulo">Responsável técnico</p>
      <h2>Luiz Henrique Baldissera</h2>
      <p class="cargo">Advogado criminalista · OAB/PR 55.717 · OAB/SC 78.938-A</p>
      <p class="bio">Defesa criminal em ações penais de alta complexidade, habeas corpus e recursos perante STJ e STF, execução penal e sistema penitenciário federal.</p>
      <a class="remissao" href="perfil-luiz.html">Ver perfil</a>
    </div>
  </section>
''')
    return "\n".join(s)


def head_html() -> str:
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in FAQ]}
    t = f"{TITULO} · Baldissera Advogados"
    return f'''<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{t}</title>
<link rel="canonical" href="{URL}">
<meta name="description" content="{DESCRICAO}">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Baldissera Advogados">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{DESCRICAO}">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://www.baldisseraadvogados.com.br/assets/images/og-default.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{DESCRICAO}">
<meta name="twitter:image" content="https://www.baldisseraadvogados.com.br/assets/images/og-default.png">
<script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
<script defer src="/_vercel/insights/script.js"></script>
'''


def gerar() -> Path:
    destino = PUBLIC / f"{SLUG}.html"
    destino.write_text(molde.pagina(head_html(), corpo_html(), "Atuação"), encoding="utf-8", newline="\n")
    return destino


if __name__ == "__main__":
    print(gerar())
