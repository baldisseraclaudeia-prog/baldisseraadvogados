"""
Gera public/execucao-penal-revisao-completa.html — página "Revisão completa da execução penal" (v2, 08/10/2026).

Fonte única do conteúdo: os dados deste arquivo (os PDFs reaproveitam os mesmos dados). Nunca editar o HTML gerado
à mão: corrige-se aqui e gera-se de novo (python tools/gerar_revisao_execucao.py [A|B], B = contato sem botão, padrão).

Trilha (fora do git, ~/.claude/plans/site-execucao-penal/): v2/ROTEIRO-PAGINA.md (texto aprovado), v2/PARECER-ESPECIALISTA.md,
v2/PARECER-CONSELHO.md, v2/MATRIZ-AFIRMACOES.md, v2/SELAGEM-V2.md, pesquisa/D (dados oficiais) e pesquisa/E (fontes conferidas).
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
DESCRICAO = ("O que uma revisão da execução penal confere, documento por documento, como um erro de cálculo pode repercutir "
             "nos marcos seguintes e o que dizem os dados oficiais e os tribunais.")
PDF_GUIA = "assets/docs/guia-revisao-execucao-penal.pdf"
PDF_ESTUDO = "assets/docs/estudo-revisao-execucao-penal.pdf"
WORD_ESTUDO = "assets/docs/estudo-revisao-execucao-penal.docx"

# ---------------------------------------------------------------- 1. abertura
TESE = "Um erro no cálculo da pena pode repercutir em outros marcos da execução."
PREAMBULO = ("A pena fixada na sentença passa por sucessivos cálculos, lançamentos e decisões até o último dia de cumprimento. "
             "A revisão percorre esse caminho desde o início, documento por documento, e confere se a pena que está sendo cumprida "
             "corresponde à que a lei e as decisões do processo determinam.")
HONESTIDADE = "A revisão pode concluir que o cálculo está correto."
MOLDURA = ("Os dados oficiais não medem erros de cálculo: medem quanto do que o cálculo já indica ainda espera decisão ou "
           "cumprimento.")
NUMEROS = [
    ("75,4%",
     "dos 86.398 processos e incidentes de execução com incidente vencido (marco de progressão, livramento, extinção ou prescrição "
     "já atingido no sistema, sem decisão), levantados pelo CNJ fora de São Paulo no mutirão de 30/6 a 30/7/2025, ainda dependiam "
     "de análise judicial segundo o relatório final.",
     "Unidade: processos e incidentes, não pessoas. O CNJ registra que, em parte dos casos, o direito já estava implementado e "
     "apenas não fora lançado no sistema; em outros, a própria análise estava atrasada.",
     "CNJ, Relatório do I Mutirão Processual Penal — Pena Justa (2025), p. 28 a 30",
     "https://www.cnj.jus.br/wp-content/uploads/2025/11/relatorio-final-mutirao-2025-v5.pdf"),
    ("10.224",
     "pessoas presas em regime fechado que já haviam obtido a progressão e aguardavam transferência, em 31/12/2025.",
     "Número mínimo: 673 unidades declararam não controlar esse dado.",
     "SENAPPEN, Relatório de Informações Penais, 2º semestre de 2025, p. 36",
     "https://www.gov.br/senappen/pt-br/servicos/sisdepen/relatorios"),
]

# ---------------------------------------------------------------- 2. roteiro de leitura (o que conferir · onde está · por que importa)
ROTEIRO_ABERTURA = ("Na execução, o erro não aparece como erro: aparece como uma data. Os pontos abaixo mostram, documento por "
                    "documento, o que uma revisão confere. Servem para entender a execução; não substituem a análise do processo, "
                    "que depende do conjunto dos documentos.")
ROTEIRO = [
    ("Guias de recolhimento",
     "se há uma guia para cada condenação, sem duplicidade; se a pena lançada é a do último julgamento que a fixou; a natureza "
     "de cada crime e a data do fato.",
     "guias definitivas e provisórias, sentenças, acórdãos e certidões de trânsito em julgado.",
     "a pena total é a base de todos os benefícios. Uma guia em duplicidade ou uma pena desatualizada desloca cada prazo "
     "calculado sobre ela."),
    ("Registros de prisão e soltura",
     "a data da primeira prisão (flagrante ou preventiva), as solturas, as fugas e recapturas, as prisões em outros processos e o "
     "recolhimento domiciliar noturno imposto durante o processo.",
     "autos de prisão, mandados cumpridos, alvarás, decisões cautelares e os registros de prisões e solturas no sistema "
     "eletrônico de execução.",
     "essas datas definem a data-base e, quando presentes os pressupostos legais, o tempo a descontar da pena. Um período que "
     "não foi lançado não aparece como erro: simplesmente deixa de ser contado no cálculo."),
    ("Remição por trabalho e estudo",
     "os dias reconhecidos nas decisões em comparação com os dias lançados no cálculo; as certidões de todas as unidades por "
     "onde a pessoa passou; os saldos que não fecharam a proporção.",
     "certidões de trabalho e de estudo, decisões de remição e cálculo de pena.",
     "o tempo remido conta como pena cumprida para todos os efeitos. O que foi reconhecido e não foi lançado não aparece no "
     "cálculo, e as datas calculadas deixam de refleti-lo."),
    ("Procedimentos disciplinares",
     "se houve defesa técnica; a data do fato e a da decisão; o intervalo entre elas; quais efeitos foram lançados.",
     "procedimento disciplinar, decisão de homologação e cálculo de pena.",
     "a falta grave reinicia a contagem para a progressão, a partir da data em que foi cometida, e pode levar à regressão e à "
     "perda de até um terço dos dias remidos. Não reinicia o prazo do livramento condicional, embora pese na avaliação do "
     "comportamento exigida para ele, e, salvo previsão expressa no decreto, não reinicia o do indulto e da comutação. Se a "
     "falta for afastada, os efeitos lançados com base nela devem ser desfeitos."),
    ("Cálculo de pena e atestado de pena",
     "a fração aplicada a cada condenação, pela lei da data do fato ou pela posterior mais benéfica; a data-base depois de uma "
     "falta (a data da falta), depois de uma nova condenação (a soma, por si, não muda a data-base) e depois de uma progressão "
     "(a data em que o último requisito foi preenchido); a fração da progressão seguinte calculada sobre o saldo de pena.",
     "cálculo de pena e atestado de pena, que deve ser entregue ao preso todo ano.",
     "fração, data-base e pena total formam o requisito de tempo de cada benefício. Os demais requisitos são examinados à parte."),
    ("Decisões de progressão e de livramento",
     "se a decisão favorável foi efetivamente lançada; se o livramento tem data-base própria; se algum requisito de tempo já "
     "foi atingido sem pedido ou sem decisão.",
     "decisões, cálculo de pena e lista de incidentes pendentes.",
     "deferir e lançar são etapas distintas. O livramento corre em paralelo à progressão, com requisitos e data-base próprios."),
    ("Decretos de indulto e comutação",
     "cada decreto do período de cumprimento, na data prevista em cada um, hipótese por hipótese; se a comutação deferida foi "
     "lançada.",
     "decretos presidenciais, decisões de indulto e comutação e cálculo de pena.",
     "preenchidos os requisitos do decreto, a decisão apenas declara o direito. Decretos de anos anteriores podem continuar "
     "aplicáveis."),
    ("Certidões de trânsito e qualificação",
     "as datas de trânsito em julgado para cada uma das partes; a idade na data do fato e na data da sentença; os dados de "
     "identificação na guia.",
     "certidões, guias e documentos de identidade.",
     "essas datas entram na contagem da prescrição da pena, e a idade pode reduzir os prazos à metade (menos de 21 anos na data "
     "do fato ou mais de 70 na data da sentença), salvo crime que envolva violência sexual contra a mulher, nos fatos posteriores "
     "à Lei 15.160/2025. Dados de identificação errados podem vincular a pessoa a uma condenação de outra."),
]

# ---------------------------------------------------------------- 3. cascata (exemplo fictício)
CASCATA_TEXTO = ("Os marcos da execução se apoiam nos mesmos dados lançados no início: a pena e as datas. Por isso, um dado "
                 "errado na origem pode se refletir nas etapas seguintes. Um exemplo fictício:")
PREMISSAS = ("Pena de 8 anos (96 meses), em regime inicial fechado; prisão preventiva iniciada em maio de 2021, contínua desde "
             "então, lançada no cálculo como janeiro de 2022 (data do mandado definitivo); frações ilustrativas de um sexto para "
             "cada progressão, a segunda sobre o saldo, e de um terço para o livramento; contagem em meses inteiros a partir do "
             "primeiro dia do mês; sem remição, falta ou interrupção; requisitos não temporais pressupostos.")
CONTAS = "96 × 1/6 = 16 meses · saldo de 80 × 1/6 = 13 meses e 10 dias · 96 × 1/3 = 32 meses."
QUADRO = [
    ("Primeira progressão", "set/2022", "mai/2023"),
    ("Segunda progressão", "out/2023", "jun/2024"),
    ("Livramento condicional", "jan/2024", "set/2024"),
    ("Fim da pena", "mai/2029", "jan/2030"),
]
CABECALHOS = ("Etapa", "Data correta (premissas do exemplo)", "Data com o erro", "Diferença")
NOTA_FRACOES = ("Em caso real, a fração depende da data do fato, da natureza do crime, da reincidência e de lei posterior que "
                "seja mais benéfica. As frações do art. 112 da Lei de Execução Penal foram alteradas mais de uma vez, a última "
                "pelas Leis 15.358/2026 e 15.402/2026; a Lei 15.402/2026 é questionada no Supremo Tribunal Federal, sem "
                "julgamento até 8/10/2026. Na revisão, cada data é calculada com a conta exposta.")

# ---------------------------------------------------------------- 4. o que confere e entrega
CAPITULOS = [
    ("Leitura dos autos e linha do tempo",
     "A revisão começa pela leitura integral dos autos. Cada marco da execução é localizado no documento em que está.",
     [("Leitura de todas as folhas", "inclusive sentenças, denúncias e acórdãos antigos digitalizados como imagem; o que for ilegível é anotado no ponto exato."),
      ("Linha do tempo de marcos", "cada prisão, soltura, fuga, recaptura, falta e decisão de benefício, com data e folha."),
      ("Cadeia recursal até o trânsito", "a fundamentação que governa é a da última decisão, não a da sentença isolada."),
      ("Fato do caso e trecho citado", "o que é fato da condenação e o que é ementa transcrita pelo juiz não se confundem."),
      ("Situação dos corréus", "benefício de natureza objetiva concedido a corréu e nunca estendido."),
      ("Identificação e idade", "nome, filiação e data de nascimento: a idade altera prazos de prescrição.")]),
    ("Guias, condenações e soma das penas",
     "A pena total é a base de todos os benefícios. Se ela está errada, os prazos calculados sobre ela também estão.",
     [("Soma refeita", "cada condenação somada de novo e comparada ao total lançado, parcela a parcela."),
      ("Guia em duplicidade", "a mesma condenação cadastrada duas vezes, após mudança de vara ou de número."),
      ("Pena do último julgamento", "a pena fixada no último julgamento efetivamente lançada no lugar da anterior."),
      ("Soma ou unificação", "crimes da mesma espécie, em condições semelhantes de tempo, lugar e modo e com vínculo entre os fatos, somados quando deveriam ser tratados como crime continuado."),
      ("Natureza de cada crime", "comum ou hediondo, com ou sem violência, primário ou reincidente, conforme a lei da data do fato, ou a posterior mais benéfica, e não conforme o cadastro."),
      ("Pena já extinta", "condenação extinta antes do início das demais que continua pesando na base dos requisitos.")]),
    ("Prisão, detração e tempo cumprido",
     "O tempo de prisão provisória, e as restrições que a lei e a jurisprudência equiparam a ela, se descontam da pena. O que não é lançado deixa de ser contado no cálculo.",
     [("Prisão provisória do próprio processo", "flagrante e preventiva lançados com as datas reais, e não com a data do mandado definitivo."),
      ("Prisão em outro processo", "período de prisão em processo que terminou em absolvição ou arquivamento, quando presentes os pressupostos do desconto."),
      ("Recolhimento domiciliar noturno", "as horas de recolhimento convertidas em dias de pena cumprida."),
      ("Método do desconto", "a forma como o desconto incide sobre o requisito de cada benefício."),
      ("Suspensão e interrupção", "liberdade provisória e situações análogas não zeram o tempo já cumprido.")]),
    ("Remição por trabalho e estudo",
     "Os dias de trabalho e as horas de estudo só contam como pena cumprida depois de reconhecidos e lançados.",
     [("Atestado convertido em dias", "trabalho e estudo convertidos na proporção legal, com o saldo que sobra levado ao período seguinte."),
      ("Dias atestados e nunca homologados", "certidões juntadas sem pedido nem decisão."),
      ("Remição de outra unidade", "trabalho feito em estabelecimento anterior cujas certidões nunca chegaram."),
      ("Decisão lançada", "a remição reconhecida pelo juiz conferida contra o número efetivamente digitado no cálculo."),
      ("Perda por falta grave", "perda de até um terço, dependente de decisão que justifique a fração aplicada.")]),
    ("Progressão de regime e datas-base",
     "O requisito de tempo da progressão depende de três dados: a pena, a fração legal e a data-base. Um erro em qualquer deles desloca as etapas seguintes; os demais requisitos são avaliados à parte.",
     [("Fração da lei do fato", "a fração conferida no texto legal vigente na data de cada crime; lei posterior mais grave não alcança fato anterior, e a posterior mais benéfica alcança."),
      ("Duas leis, duas contas", "quando a lei mudou, as duas contas lado a lado, com a regra que decide qual se aplica."),
      ("Fração sobre o saldo", "a partir da segunda progressão, a fração incide sobre o que resta de pena."),
      ("Data-base após falta", "a data da falta, e não a data da decisão que a homologou."),
      ("Data-base após nova condenação", "a soma de condenação por fato anterior ao início do cumprimento não reinicia, por si, a contagem."),
      ("Requisito de tempo atingido e não pedido", "requisito temporal já atingido sem pedido nem decisão.")]),
    ("Faltas disciplinares e regressão",
     "A falta grave produz efeitos fortes: por isso é a primeira coisa a conferir, antes das datas.",
     [("Procedimento válido", "apuração com defesa técnica, oitiva e decisão fundamentada."),
      ("Prazo de apuração", "intervalo entre o fato e a homologação."),
      ("Efeitos limitados", "a falta interrompe a progressão, mas não reinicia o prazo do livramento, embora pese no comportamento exigido para ele, nem, por si, o de indulto e comutação."),
      ("Regressão cautelar", "regressão provisória que se prolonga sem decisão definitiva."),
      ("Falta afastada", "quando a falta é afastada, a data-base é restabelecida e os benefícios que ela impedia são reexaminados.")]),
    ("Livramento condicional",
     "O livramento corre em paralelo à progressão, com prazo e data-base próprios.",
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
     [("Termo inicial", "trânsito em julgado para cada parte, observada a modulação fixada pelo Supremo Tribunal Federal no Tema 788."),
      ("Prazo pela pena de cada crime", "sem o acréscimo do crime continuado."),
      ("Idade", "redução à metade para quem tinha menos de 21 anos na data do fato ou mais de 70 na data da sentença, salvo crime que envolva violência sexual contra a mulher praticado depois da Lei 15.160/2025."),
      ("Causas que impedem o curso", "prisão por outro processo e marcos de interrupção."),
      ("Parcela prescrita", "a pena extinta que continua na base do cálculo.")]),
    ("Incidentes, cadastro e direitos",
     "Parte dos erros não está na conta, mas no cadastro e na tramitação.",
     [("Incidente parado", "pedido em tramitação que não aparece como pendente."),
      ("Mandado de prisão", "mandado indevidamente vigente, que impede a soltura mesmo com direito reconhecido."),
      ("Advogado cadastrado", "defesa não intimada dos incidentes por cadastro desatualizado."),
      ("Lei posterior mais benéfica", "norma que reduziu a pena ou reclassificou a conduta, aplicável pelo juízo da execução."),
      ("Vícios da condenação", "reincidência fora do período legal ou antecedente que não subsiste, examinados pela via própria.")]),
    ("Providências indicadas",
     "A revisão indica, para cada divergência, a via e a ordem de urgência; a apresentação ao juízo é atuação distinta.",
     [("Posição processual", "o que já foi pedido, decidido e recorrido, para escolher a via (novo pedido, recurso ou habeas corpus) sem perder o prazo do recurso."),
      ("Ordem por urgência", "requisito já atingido primeiro; depois impugnação ao cálculo; depois as medidas de mais longo prazo."),
      ("Memória de cálculo", "a conta exposta, parcela a parcela, com o documento de cada número."),
      ("Retificação das datas", "desconto reconhecido sempre acompanhado do pedido de retificação do cálculo e das datas-base.")]),
]
ENTREGA = [
    ("Relatório escrito", "a situação da execução e as divergências encontradas, cada uma com o documento que a sustenta e o argumento que pode afastá-la."),
    ("Linha do tempo", "todos os marcos da execução, com data e folha."),
    ("Memória de cálculo", "a conta de cada benefício, refeita e comparada com o cálculo oficial."),
    ("Quadro de benefícios", "com requisito de tempo já atingido, próximos, dependentes de documento e não apurados."),
    ("Plano de providências", "as providências cabíveis, em ordem de urgência."),
]
LIMITES = ("A revisão é uma análise documental da execução. Pode concluir que o cálculo está correto ou que não há providência "
           "cabível. Pedidos, recursos e o acompanhamento da execução são atuação distinta, que não integra a revisão. Questões da "
           "própria condenação seguem outra via, avaliada separadamente; a aplicação de lei posterior mais benéfica, porém, cabe ao "
           "juízo da execução.")
METODO = [
    ("Leitura integral", "Todas as folhas, inclusive as digitalizadas como imagem."),
    ("Linha do tempo", "Cada fato ligado à folha ou ao evento em que está."),
    ("Conta refeita do zero", "Pela lei aplicável a cada fato (a da data do fato ou a posterior mais benéfica), com a conta exposta."),
    ("Confronto com o cálculo oficial e com o título", "Cada divergência é conferida antes de ser apontada, inclusive a que hoje beneficia o condenado e cuja correção o prejudicaria."),
    ("Revisão e assinatura", "Relatório revisado e assinado pelo advogado responsável antes da entrega; pedidos e recursos subscritos por advogado inscrito na seccional do processo."),
]

# ---------------------------------------------------------------- 5a. sistema penitenciário federal (Lei 11.671/2008, selada)
FEDERAL_TEXTO = ("Quando a pessoa está em estabelecimento penal federal de segurança máxima, a execução segue também as regras da "
                 "Lei 11.671/2008. Além dos pontos acima, a revisão confere:")
FEDERAL = [
    ("Competência", "durante a transferência, a execução da pena fica a cargo do juízo federal da localidade do estabelecimento (arts. 2º e 4º, § 1º)."),
    ("Fundamento da inclusão", "a admissão depende de decisão prévia e fundamentada do juízo federal, e a inclusão se justifica no interesse da segurança pública ou do próprio preso (arts. 3º e 4º)."),
    ("Quem pode requerer", "o processo de transferência pode ser requerido pela autoridade administrativa, pelo Ministério Público e pelo próprio preso (art. 5º)."),
    ("Prazo e renovação", "a inclusão é excepcional e por prazo determinado; a permanência é de até três anos, renovável por iguais períodos quando solicitado motivadamente pelo juízo de origem, observados os requisitos da transferência, e se persistirem os motivos que a determinaram (art. 10, caput e § 1º)."),
    ("Fim do prazo sem pedido de renovação", "decorrido o prazo sem pedido de renovação feito imediatamente após o seu decurso, o juízo de origem fica obrigado a receber o preso no estabelecimento sob sua jurisdição (art. 10, § 2º)."),
]
FEDERAL_FONTE = "Lei 11.671/2008, texto atualizado na compilação oficial do Senado Federal, consulta em 8/10/2026."

# ---------------------------------------------------------------- 5b. condições de cumprimento e direitos fundamentais
SV56 = ("A falta de estabelecimento penal adequado não autoriza a manutenção do condenado em regime prisional mais gravoso, "
        "devendo-se observar, nessa hipótese, os parâmetros fixados no RE 641.320/RS.")
SV56_EXPL = ("Obtida a progressão, a falta de vaga no regime adequado não justifica a permanência no anterior; a solução segue os "
             "parâmetros do RE 641.320/RS, aplicados pelo juízo caso a caso. Em 31/12/2025, havia ao menos 10.224 pessoas em "
             "regime fechado aguardando transferência depois de obter a progressão (SENAPPEN).")
ADPF = [
    "Em 4/10/2023, o Supremo Tribunal Federal reconheceu que <em>“Há um estado de coisas inconstitucional no sistema carcerário "
    "brasileiro, responsável pela violação massiva de direitos fundamentais dos presos”</em> e determinou um plano com diretrizes "
    "para reduzir, entre outros pontos, <em>“a permanência em regime mais severo ou por tempo superior ao da pena”</em> (notícia "
    "oficial do STF de 4/10/2023).",
    "Em dezembro de 2024, segundo a notícia oficial do STF, o Tribunal decidiu <em>“homologar com ressalvas o chamado Plano Pena "
    "Justa”</em>. O plano prevê, entre as metas, mutirões processuais penais semestrais (CNJ, Relatório do I Mutirão Processual "
    "Penal — Pena Justa, p. 7).",
    "É uma decisão estrutural, dirigida ao poder público. Não concede, por si, redução de pena ou soltura em caso individual, que "
    "depende da demonstração concreta.",
]

# ---------------------------------------------------------------- 6. julgados (orçamento: 5 blocos)
EP102_EMENTA = (
    "Ementa: Direito processual penal. Segundo agravo regimental na execução penal. PROGRESSÃO DE REGIME. UNIFICAÇÃO DE PENAS. "
    "CONCURSO DE CRIMES COM E SEM VIOLÊNCIA À PESSOA. CÁLCULO DO REQUISITO OBJETIVO. APLICAÇÃO DO PERCENTUAL MAIS GRAVOSO SOBRE "
    "A TOTALIDADE DA PENA. AGRAVO REGIMENTAL A QUE SE NEGA PROVIMENTO. I. Caso em exame 1. Trata-se de agravo regimental "
    "interposto contra decisão monocrática que, em sede de execução penal, determinou a retificação do cálculo de pena para "
    "aplicar o percentual de 25% (vinte e cinco por cento) para fins de progressão de regime, com base no artigo 112, inciso "
    "III, da Lei de Execução Penal, sobre a totalidade da pena unificada. O agravante, condenado por múltiplos crimes, sustenta "
    "que o percentual mais gravoso deveria incidir apenas sobre a pena do crime cometido com violência à pessoa, aplicando-se o "
    "percentual de 16% (dezesseis por cento) aos demais delitos. II. Questão em discussão 2. A controvérsia central consiste em "
    "definir se, no caso de concurso de crimes e consequente unificação das penas, o requisito objetivo para a progressão de "
    "regime deve ser calculado de forma isolada para cada delito ou se deve prevalecer o percentual mais rigoroso sobre o total "
    "da pena unificada, quando uma das condenações for por crime cometido com violência ou grave ameaça à pessoa. III. Razões de "
    "decidir 3. Em matéria de execução penal, as penas impostas em razão do concurso de crimes são unificadas, formando um "
    "montante único sobre o qual incidirão as regras para a concessão de benefícios, como a progressão de regime. 4. A "
    "existência de condenação por crime praticado com violência ou grave ameaça à pessoa, conforme previsto no artigo 112, "
    "inciso III, da Lei de Execução Penal, impõe a aplicação do percentual de 25% (vinte e cinco por cento) para a progressão. "
    "Este requisito mais gravoso se estende sobre a totalidade da pena unificada, sendo inviável a fragmentação do cálculo para "
    "aplicar percentuais distintos a cada crime. 5. A execução da pena é una e indivisível. A adoção de critério diverso, além "
    "de não encontrar amparo legal, criaria um sistema de execução complexo e impraticável, desvirtuando a finalidade da "
    "unificação das penas. IV. Dispositivo e tese 6. Agravo regimental a que se nega provimento. Tese de julgamento: “1. Havendo "
    "concurso de crimes, a unificação das penas para fins de execução penal impõe que o cálculo do requisito objetivo para a "
    "progressão de regime seja realizado sobre a <strong>totalidade da pena remanescente</strong>, observando-se o percentual "
    "mais gravoso previsto em lei. 2. A condenação simultânea por crimes comuns e por crime cometido com violência ou grave "
    "ameaça à pessoa (art. 112, III, da Lei de Execução Penal) atrai a incidência do percentual de 25% sobre a integralidade da "
    "pena unificada, não sendo cabível a aplicação de frações distintas para cada delito.” Dispositivos relevantes citados: Lei "
    "nº 7.210/1984 (Lei de Execução Penal), art. 112, III. Jurisprudência relevante citada: STF, HC nº 231.110 ED-AgR, Relator "
    "Ministro Gilmar Mendes, Segunda Turma, DJe 25/10/2023.")
TEMA_1161 = ("A valoração do requisito subjetivo para concessão do livramento condicional - bom comportamento durante da execução "
             "da pena (art. 83, inciso III, alínea \"a\", do Código Penal) - deve considerar todo o histórico prisional, não se "
             "limitando ao período de 12 meses referido na alínea \"b\" do mesmo inciso III do art. 83 do Código Penal.")
JULGADOS = [
    {"trib": "STJ · Tema Repetitivo 1.155",
     "tese": "O recolhimento domiciliar noturno durante o processo desconta da pena, com ou sem tornozeleira",
     "ponte": "Quem respondeu ao processo obrigado a ficar em casa à noite e nos dias de folga já teve a liberdade restringida. As "
              "horas de recolhimento são convertidas em dias e descontadas da pena. Esse período não aparece como prisão nos "
              "registros, e por isso é um dos pontos que o roteiro manda conferir.",
     "partes": [("Teses firmadas",
                 "1) <strong>O período de recolhimento obrigatório noturno e nos dias de folga, por comprometer o status libertatis "
                 "do acusado, deve ser reconhecido como período a ser detraído da pena privativa de liberdade</strong> e da medida "
                 "de segurança, em homenagem aos princípios da proporcionalidade e do non bis in idem. 2) <strong>O monitoramento "
                 "eletrônico associado, atribuição do Estado, não é condição indeclinável para a detração</strong> dos períodos de "
                 "submissão a essas medidas cautelares, não se justificando distinção de tratamento ao investigado ao qual não é "
                 "determinado e disponibilizado o aparelhamento. 3) As horas de recolhimento domiciliar noturno e nos dias de folga "
                 "devem ser convertidas em dias para contagem da detração da pena. Se no cômputo total remanescer período menor que "
                 "vinte e quatro horas, essa fração de dia deverá ser desprezada.",
                 "(REsp n. 1.977.135/SC, relator Ministro Joel Ilan Paciornik, Terceira Seção, julgado em 23/11/2022, DJe de 28/11/2022. Teses conferidas no portal de precedentes qualificados do STJ.)")],
     "publicacao": "publicacao-recolhimento-noturno-desconta-da-pena.html"},
    {"trib": "STJ · Tema Repetitivo 1.354 · STF · EP 102 AgR-segundo",
     "tese": "Cada condenação com a lei mais favorável ao seu fato; para crimes com e sem violência sob a mesma lei, o STF decidiu em sentido diverso",
     "ponte": "Quando a lei mudou entre um crime e outro, cada condenação recebe a fração de progressão da lei mais favorável ao seu "
              "fato: é uma questão de lei no tempo. Outra questão, a de crimes com e sem violência sob a mesma lei, foi decidida pelo "
              "Plenário do Supremo Tribunal Federal em sentido diverso, com a fração mais grave sobre toda a pena unificada. Por isso "
              "cada cálculo é conferido à luz dos dois entendimentos.",
     "partes": [("Tese firmada no Tema 1.354",
                 "<strong>É possível, para fins de cálculo para progressão de regime, a aplicação de percentuais distintos para cada "
                 "condenação isoladamente, em uma mesma execução</strong>, reconhecendo-se a retroatividade da Lei n. 13.964/2019 e a "
                 "ultratividade da redação anterior do art. 112 da Lei de Execução Penal, <strong>em respeito à norma mais favorável "
                 "ao executado</strong>.",
                 "(REsp n. 2.037.377/SC, relatora Ministra Maria Marluce Caldas, Terceira Seção, julgado em 18/6/2026, DJEN de 2/7/2026, trânsito em julgado em 2/9/2026.)"),
                ("Ementa do EP 102 AgR-segundo", EP102_EMENTA,
                 "(EP 102 AgR-segundo, relator Ministro Alexandre de Moraes, Tribunal Pleno, julgado em 14/4/2026, DJe de 8/5/2026.)")],
     "publicacao": "publicacao-tema-1354-e-a-progressao-por-condenacao.html"},
    {"trib": "STJ · Tema Repetitivo 1.165",
     "tese": "A contagem para a próxima progressão começa quando o último requisito foi preenchido, não quando o juiz decidiu",
     "ponte": "A decisão que concede a progressão apenas declara um direito. Se o cálculo adota como nova data-base o dia da decisão "
              "ou da transferência, o tempo de espera passa a ser cobrado de novo. A tese tem um limite que a revisão também confere: "
              "se o último requisito preenchido foi o subjetivo, é a data dele que serve de marco.",
     "partes": [("Tese firmada",
                 "<strong>A decisão que defere a progressão de regime não tem natureza constitutiva, senão declaratória. O termo "
                 "inicial para a progressão de regime deverá ser a data em que preenchidos os requisitos objetivo e subjetivo</strong> "
                 "descritos no art. 112 da Lei 7.210, de 11/07/1984 (Lei de Execução Penal), <strong>e não a data em que efetivamente "
                 "foi deferida a progressão</strong>. Essa data deverá ser definida de forma casuística, fixando-se como termo inicial "
                 "o momento em que preenchido o último requisito pendente, seja ele o objetivo ou o subjetivo. Se por último for "
                 "preenchido o requisito subjetivo, independentemente da anterior implementação do requisito objetivo, será aquele "
                 "(o subjetivo) o marco para fixação da data-base para efeito de nova progressão de regime.",
                 "(REsp n. 1.972.187/SP, relator Ministro Og Fernandes, Terceira Seção, julgado em 14/8/2024, DJe de 2/12/2024. Tese conferida no portal de precedentes qualificados do STJ.)")]},
    {"trib": "STJ · Tema Repetitivo 1.006",
     "tese": "A soma de uma nova condenação não altera, por si, a data-base dos benefícios",
     "ponte": "Quando chega uma condenação nova, as penas são somadas ou unificadas, mas a data-base dos benefícios não muda por "
              "causa disso. O cálculo que reinicia a contagem na data da nova guia desconsidera tempo já cumprido. A regra não se "
              "confunde com a falta grave, que interrompe a contagem da progressão.",
     "partes": [("Tese firmada",
                 "<strong>A unificação de penas não enseja a alteração da data-base para concessão de novos benefícios executórios.</strong>",
                 "(REsp n. 1.753.512/PR e REsp n. 1.753.509/PR, relator Ministro Rogerio Schietti Cruz, Terceira Seção, julgado em 18/12/2018, DJe de 11/3/2019.)")]},
    {"trib": "STJ · Súmulas 441 e 535 · Jurisprudência em Teses n. 7 · Tema Repetitivo 1.161",
     "tese": "A falta grave não reinicia o prazo do livramento, do indulto nem da comutação, mas pesa no comportamento",
     "ponte": "A falta grave interrompe a contagem para a progressão. O prazo do livramento continua correndo, mas a falta pesa no "
              "comportamento exigido para ele, avaliado em todo o histórico da execução. O prazo do indulto e da comutação também "
              "continua, salvo previsão expressa no decreto.",
     "partes": [("Enunciados e teses",
                 "Súmula 441: <strong>A falta grave não interrompe o prazo para obtenção de livramento condicional.</strong><br>"
                 "Súmula 535: <strong>A prática de falta grave não interrompe o prazo para fim de comutação de pena ou indulto.</strong><br>"
                 "Jurisprudência em Teses n. 7, tese 10: A prática de falta grave não interrompe o prazo para fim de comutação de pena "
                 "ou indulto, salvo se houver expressa previsão a respeito no decreto concessivo dos benefícios.<br>"
                 "Tema Repetitivo 1.161: " + TEMA_1161,
                 "(Súmula 441, Terceira Seção, julgada em 28/4/2010, DJe de 13/5/2010; Súmula 535, Terceira Seção, julgada em 10/6/2015, DJe de 15/6/2015; STJ, Jurisprudência em Teses n. 7, tese 10; REsp n. 1.970.217 e REsp n. 1.974.104, relator Ministro Ribeiro Dantas, Terceira Seção, Tema Repetitivo 1.161.)")]},
]

# ---------------------------------------------------------------- perguntas, aviso, contato
FAQ = [
    ("A revisão sempre encontra erro?",
     "Não. Há execuções corretamente calculadas, e não é possível antecipar o resultado antes de examinar os autos. A revisão "
     "pode concluir que o cálculo está correto."),
    ("Quem constitui o advogado na execução?",
     "O próprio condenado, em regra por procuração."),
    ("O advogado que já atua na execução pode solicitar a revisão?",
     "Sim. A revisão pode ser feita em apoio à defesa constituída, que continua responsável pelo processo."),
    ("Um erro antigo ainda pode ser apontado?",
     "Sim. O cálculo de pena acompanha toda a execução e é revisto a cada incidente: erro demonstrado pode ser levado ao juízo "
     "da execução enquanto houver pena a cumprir e, diante de ilegalidade flagrante, cabe habeas corpus a qualquer tempo. A via "
     "adequada depende do caso."),
    ("E se a revisão encontrar erro que hoje beneficia o condenado?",
     "Ele é registrado em seção própria do relatório, com a análise de seus riscos, para que a defesa conheça toda a situação "
     "da execução."),
]
AVISO = ("Conteúdo informativo, nos termos do Provimento CFOAB 205/2021. Os exemplos são fictícios e não se referem a casos do "
         "escritório. O resultado de cada execução depende dos documentos e das circunstâncias do caso. Dados oficiais com fonte e "
         "página indicadas; consulta em 8 de outubro de 2026.")
CONTATO_FRASE = "Atendimento virtual em todo o Brasil e atendimento presencial nas unidades de Cascavel, Porto Alegre, Foz do Iguaçu e Porto Belo, mediante agendamento prévio."
BIO = "Defesa criminal, habeas corpus e recursos perante o STJ e o STF, execução penal e sistema penitenciário federal."


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


MESES = {"jan": 0, "fev": 1, "mar": 2, "abr": 3, "mai": 4, "jun": 5, "jul": 6, "ago": 7, "set": 8, "out": 9, "nov": 10, "dez": 11}


def _ano(d: str) -> float:
    m, a = d.split("/")
    return int(a) + MESES[m] / 12


def grafico_svg() -> str:
    """Versão horizontal (computador e PDF)."""
    x0, x1, a0, a1 = 190, 690, 2022, 2030.5
    x = lambda d: round(x0 + (_ano(d) - a0) / (a1 - a0) * (x1 - x0), 1)  # noqa: E731
    p = ['<svg class="rv-grafico rv-grafico-h" viewBox="0 0 700 270" role="img" aria-labelledby="gh-tit gh-desc">',
         '<title id="gh-tit">Exemplo fictício: um erro na data da primeira prisão</title>',
         '<desc id="gh-desc">Para cada etapa, a data correta nas premissas do exemplo e a data com o erro. A mesma informação está '
         'no quadro logo abaixo.</desc>']
    for ano in range(2022, 2031):
        xa = x(f"jan/{ano}")
        p.append(f'<line class="g-fio" x1="{xa}" y1="20" x2="{xa}" y2="215"/><text class="g-rotulo" x="{xa}" y="234" text-anchor="middle">{ano}</text>')
    for i, (nome, rev, lan) in enumerate(QUADRO):
        y = 45 + i * 50
        xr, xl = x(rev), x(lan)
        p.append(f'<text class="g-titulo" x="0" y="{y + 5}">{nome}</text>')
        p.append(f'<rect class="g-ganho" x="{xr}" y="{y - 3}" width="{round(xl - xr, 1)}" height="6"/>')
        p.append(f'<circle class="g-revisto" cx="{xr}" cy="{y}" r="7"/><circle class="g-oficial" cx="{xl}" cy="{y}" r="7"/>')
    p.append('<circle class="g-revisto" cx="196" cy="258" r="6"/><text class="g-rotulo" x="208" y="262">data correta</text>')
    p.append('<circle class="g-oficial" cx="296" cy="258" r="6"/><text class="g-rotulo" x="308" y="262">data com o erro</text>')
    p.append('<rect class="g-ganho" x="420" y="255" width="22" height="6"/><text class="g-rotulo" x="450" y="262">diferença de 8 meses · exemplo fictício</text>')
    p.append("</svg>")
    return "\n".join(p)


def grafico_svg_vertical() -> str:
    """Versão vertical (celular): anos de cima para baixo, duas colunas."""
    y0, y1, a0, a1 = 40, 600, 2022, 2030.5
    y = lambda d: round(y0 + (_ano(d) - a0) / (a1 - a0) * (y1 - y0), 1)  # noqa: E731
    xc, xe = 150, 260
    p = ['<svg class="rv-grafico rv-grafico-v" viewBox="0 0 340 650" role="img" aria-labelledby="gv-tit gv-desc">',
         '<title id="gv-tit">Exemplo fictício: um erro na data da primeira prisão</title>',
         '<desc id="gv-desc">Duas colunas, data correta e data com o erro, de 2022 a 2030; cada etapa aparece oito meses depois na '
         'coluna com o erro. A mesma informação está no quadro logo abaixo.</desc>',
         f'<text class="g-titulo" x="{xc}" y="22" text-anchor="middle">Correta</text>',
         f'<text class="g-titulo" x="{xe}" y="22" text-anchor="middle">Com o erro</text>']
    for ano in range(2022, 2031):
        ya = y(f"jan/{ano}")
        p.append(f'<line class="g-fio" x1="60" y1="{ya}" x2="320" y2="{ya}"/><text class="g-rotulo" x="0" y="{ya + 4}">{ano}</text>')
    rot = ["1ª progressão", "2ª progressão", "Livramento", "Fim da pena"]
    for (nome, rev, lan), r in zip(QUADRO, rot):
        yr, yl = y(rev), y(lan)
        p.append(f'<line class="g-liga" x1="{xc}" y1="{yr}" x2="{xe}" y2="{yl}"/>')
        p.append(f'<circle class="g-revisto" cx="{xc}" cy="{yr}" r="7"/><circle class="g-oficial" cx="{xe}" cy="{yl}" r="7"/>')
        p.append(f'<text class="g-rotulo" x="{xc - 12}" y="{yr + 4}" text-anchor="end">{r}</text>')
    p.append("</svg>")
    return "\n".join(p)


def quadro_html() -> str:
    linhas = "\n".join(f'        <tr><th scope="row">{esc(n)}</th><td>{r}</td><td>{l}</td><td class="rv-dif">8 meses</td></tr>' for n, r, l in QUADRO)
    cab = "".join(f'<th scope="col">{esc(c)}</th>' for c in CABECALHOS)
    return f'''    <table class="rv-quadro">
      <caption>Exemplo fictício · frações ilustrativas</caption>
      <thead><tr>{cab}</tr></thead>
      <tbody>
{linhas}
      </tbody>
      <tfoot><tr><td colspan="4">{esc(CONTAS)}</td></tr></tfoot>
    </table>'''


def julgado_html(j: dict) -> str:
    partes = "\n".join(
        f'        <p class="rv-parte">{esc(r)}</p>\n        <blockquote>{txt}<span class="rv-ref">{esc(ref)}</span></blockquote>'
        for r, txt, ref in j["partes"])
    leia = f'\n      <p class="rv-leia"><a class="remissao" href="{j["publicacao"]}">Análise completa no site</a></p>' if j.get("publicacao") else ""
    return f'''    <article class="rv-julgado">
      <p class="rv-trib">{esc(j["trib"])}</p>
      <h3>{esc(j["tese"])}</h3>
      <p>{esc(j["ponte"])}</p>
      <details>
        <summary>Ler o texto oficial, na íntegra</summary>
{partes}
      </details>{leia}
    </article>'''


def corpo_html(contato: str = "B") -> str:
    s = []
    nums = "\n".join(
        f'        <li><span class="rv-num">{n}</span><span class="rv-num-rotulo">{esc(r)}</span>'
        f'<span class="rv-num-ressalva">{esc(rs)}</span>'
        f'<span class="rv-num-fonte"><a href="{u}" target="_blank" rel="noopener">{esc(f)}<span class="so-leitor"> (abre em nova aba)</span></a></span></li>'
        for n, r, rs, f, u in NUMEROS)
    s.append(f'''  <p class="trilha"><a href="areas-de-atuacao.html">Áreas de atuação</a> / <a href="area-execucao-penal.html">Execução Penal</a> / Revisão completa</p>

  <section class="rv-abertura" aria-labelledby="t-abertura">
    <div class="rv-abertura-interna">
      <p class="rv-sobre">Execução Penal</p>
      <h1 id="t-abertura">{TITULO}</h1>
      <p class="rv-tese-ab">{esc(TESE)}</p>
      <p class="rv-pre">{esc(PREAMBULO)}</p>
      <p class="rv-pre rv-honesto">{esc(HONESTIDADE)}</p>
      <p class="rv-moldura">{esc(MOLDURA)}</p>
      <ul class="rv-numeros">
{nums}
      </ul>
      <p class="rv-remissoes"><a href="#roteiro">Roteiro de leitura</a> <a href="#materiais">Guia em PDF</a></p>
    </div>
  </section>

  <div class="abertura abertura-area">
    <nav class="sumario" aria-label="Nesta página">
      <a href="#roteiro">Roteiro de leitura</a>
      <a href="#cascata">Efeito cascata</a>
      <a href="#conferencias">O que se confere</a>
      <a href="#federal">Execução federal</a>
      <a href="#direitos">Direitos fundamentais</a>
      <a href="#tribunais">Tribunais</a>
      <a href="#perguntas">Perguntas</a>
    </nav>
  </div>
''')
    # I — roteiro
    rt = []
    for i, (doc, oque, onde, porque) in enumerate(ROTEIRO, 1):
        rt.append(f'''    <details>
      <summary><span class="cap-num">{i}</span><span class="cap-titulo">{esc(doc)}</span></summary>
      <div class="cap-corpo">
        <dl class="rv-tres">
          <dt>O que conferir</dt><dd>{esc(oque[0].upper() + oque[1:])}</dd>
          <dt>Onde está</dt><dd>{esc(onde[0].upper() + onde[1:])}</dd>
          <dt>Por que importa</dt><dd>{esc(porque[0].upper() + porque[1:])}</dd>
        </dl>
      </div>
    </details>''')
    s.append(secao("roteiro", "I", "Roteiro de leitura dos documentos", f'''    <p class="rv-tese">{esc(ROTEIRO_ABERTURA.split(":")[0])}: {esc(ROTEIRO_ABERTURA.split(":", 1)[1].split(". ")[0].strip())}.</p>
    <div class="rv-coluna"><p class="abre">{esc(ROTEIRO_ABERTURA.split(". ", 1)[1])}</p></div>
    <div class="rv-capitulos rv-roteiro">
{chr(10).join(rt)}
    </div>
''', "Oito documentos, o que se confere em cada um e por que importa. Toque em cada documento para abrir."))
    # II — cascata
    s.append(secao("cascata", "II", "Do efeito cascata", f'''    <div class="rv-coluna">
      <p class="abre">{esc(CASCATA_TEXTO)}</p>
      <p class="rv-premissas"><span class="rotulo">Exemplo fictício · premissas</span>{esc(PREMISSAS)}</p>
    </div>
{grafico_svg()}
{grafico_svg_vertical()}
{quadro_html()}
    <p class="rv-aviso">{esc(NOTA_FRACOES)}</p>
''', "Como um dado errado na origem pode se refletir nas etapas seguintes."))
    # III — o que confere e entrega
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
    me = "\n".join(f'      <li><h3>{esc(t)}</h3><p>{esc(p)}</p></li>' for t, p in METODO)
    en = "\n".join(f'        <li><strong>{esc(a)}</strong>: {esc(b)}</li>' for a, b in ENTREGA)
    s.append(secao("conferencias", "III", "Do que a revisão confere e entrega", f'''    <div class="rv-capitulos">
{chr(10).join(caps)}
    </div>
    <div class="rv-duas">
      <div>
        <h3 class="sub-secao">O que a revisão entrega</h3>
        <ul class="rv-lista">
{en}
        </ul>
      </div>
      <div class="rv-limites">
        <h3 class="sub-secao">Os limites da revisão</h3>
        <p>{esc(LIMITES)}</p>
      </div>
    </div>
    <h3 class="sub-secao rv-centro">Método</h3>
    <ol class="rv-metodo">
{me}
    </ol>
''', f"{len(CAPITULOS)} capítulos, na ordem em que a execução é examinada. Toque em cada capítulo para abrir."))
    # IV — federal
    fe = "\n".join(f'      <li><strong>{esc(a)}</strong>: {esc(b)}</li>' for a, b in FEDERAL)
    s.append(secao("federal", "IV", "Da execução no sistema penitenciário federal", f'''    <div class="rv-coluna">
      <p class="abre">{esc(FEDERAL_TEXTO)}</p>
    </div>
    <ul class="rv-lista rv-coluna">
{fe}
    </ul>
    <p class="rv-aviso">{esc(FEDERAL_FONTE)}</p>
'''))
    # V — direitos fundamentais
    ad = "\n".join(f'      <p>{t}</p>' for t in ADPF)
    s.append(secao("direitos", "V", "Das condições de cumprimento e dos direitos fundamentais", f'''    <div class="rv-coluna">
      <h3 class="sub-secao">Súmula Vinculante 56</h3>
      <blockquote class="rv-enunciado">{esc(SV56)}<span class="rv-ref">(Súmula Vinculante 56, Supremo Tribunal Federal, aprovada na sessão plenária de 29/6/2016.)</span></blockquote>
      <p class="abre">{esc(SV56_EXPL)}</p>
      <h3 class="sub-secao">ADPF 347 e o Plano Pena Justa</h3>
{ad}
    </div>
'''))
    # VI — tribunais
    s.append(secao("tribunais", "VI", "Do que dizem os tribunais", f'''    <div class="rv-julgados">
{chr(10).join(julgado_html(j) for j in JULGADOS)}
    </div>
''', "Precedentes conferidos na fonte oficial. O texto oficial abre ao toque, sem cortes."))
    # VII — perguntas
    fq = "\n".join(f'    <details><summary>{esc(q)}</summary><p>{esc(r)}</p></details>' for q, r in FAQ)
    s.append(secao("perguntas", "VII", "Das perguntas frequentes", f'''    <div class="rv-faq">
{fq}
    </div>
'''))
    # VIII — materiais e contato
    ico = ('<svg viewBox="0 0 24 28" aria-hidden="true" focusable="false"><path d="M3 1h12l6 6v20H3z"/><path d="M15 1v6h6"/>'
           '<path d="M7 14h10M7 18h10M7 22h6"/></svg>')
    botao = '\n      <p><a class="botao" href="agendar.html">Agendar atendimento</a></p>' if contato == "A" else ""
    s.append(secao("materiais", "VIII", "Dos materiais", f'''    <ul class="rv-baixar">
      <li><a href="{PDF_GUIA}" download>{ico}<span class="b-titulo">Guia da revisão</span><span class="b-desc">Quatro páginas: o que a revisão confere, o efeito cascata, o roteiro de leitura e os documentos examinados.</span><span class="b-acao">Baixar PDF</span></a></li>
      <li><a href="{PDF_ESTUDO}" download>{ico}<span class="b-titulo">Estudo completo</span><span class="b-desc">O catálogo de erros, os exemplos com a conta, os dados oficiais, os precedentes e o que pesa contra.</span><span class="b-acao">Baixar PDF</span></a></li>
    </ul>
    <div class="atendimento rv-contato">
      <p>{esc(CONTATO_FRASE)}</p>{botao}
    </div>
    <p class="rv-aviso">{esc(AVISO)}</p>
'''))
    s.append(f'''  <section class="autor-bloco" aria-label="Responsável técnico">
    <img src="assets/images/luiz-henrique-baldissera.jpg" alt="Luiz Henrique Baldissera" width="600" height="750" loading="lazy">
    <div>
      <p class="rotulo">Responsável técnico</p>
      <h2>Luiz Henrique Baldissera</h2>
      <p class="cargo">Advogado criminalista · OAB/PR 55.717 · OAB/SC 78.938-A</p>
      <p class="bio">{esc(BIO)}</p>
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


def gerar(contato: str = "B", destino: Path = None) -> Path:
    destino = destino or (PUBLIC / f"{SLUG}.html")
    destino.write_text(molde.pagina(head_html(), corpo_html(contato), "Atuação"), encoding="utf-8", newline="\n")
    return destino


if __name__ == "__main__":
    c = sys.argv[1].upper() if len(sys.argv) > 1 else "B"
    print(gerar(c))
