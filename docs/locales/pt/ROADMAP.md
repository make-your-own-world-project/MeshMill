# Roteiro MeshMill

## Suporte de plataforma

Windows é a plataforma empacotada inicial. A arquitetura do aplicativo e os formatos de malha são
multiplataforma e versões futuras devem adicionar pacotes nativos Linux e macOS. Trabalho de plataforma
inclui empacotamento, integração de aplicativos, métricas de hardware, comportamento do sistema de arquivos e automação
teste de lançamento preservando o mesmo projeto e fluxos de trabalho STL em todos os sistemas suportados.

- Adicione pacotes Linux x86-64 e cobertura CI.
- Adicione pacotes macOS Apple Silicon e x86-64, assinatura, reconhecimento de firma e cobertura de CI.
- Adicione provedores de métricas CPU, memória e GPU nativos da plataforma por trás de uma interface compartilhada.
- Mantenha as configurações salvas, os mapeamentos de teclado, o comportamento da linha de comando e os dados do projeto portáteis.

Este roteiro registra o trabalho planejado. Ele não descreve os recursos da versão atual.

## Escopo

MeshMill gerencia geometria, densidade de malha, densidade de pontos, otimização, limpeza, validação e STL
intercâmbio de arquivos de malha tão grandes ou pesados que permanecem úteis em fluxos de trabalho de edição posteriores.

Modelagem de uso geral, escultura, pintura, animação, renderização, composição de cena, materiais,
rigging e outros sistemas de criação de conteúdo estão fora deste roteiro. A síntese distribuída se aplica
às operações de gerenciamento de malha do MeshMill e não expande o produto para um editor geral.

## Geometria de referência

A malha composta agrupada é o acessório de desenvolvimento comum para algoritmos e roteiros atuais
trabalho. Suas camadas intencionalmente redundantes e densidade desigual suportam comparações repetíveis de
qualidade de redução, análise de densidade, tratamento de sobreposição, operações regionais, processamento fora do núcleo,
e síntese futura. As implementações do roteiro devem relatar resultados em relação a este equipamento e pequenas
malhas de regressão criadas especificamente, em vez de otimizar o comportamento apenas para um modelo.

## Espaços de trabalho Multi-STL e síntese estatística

Um espaço de trabalho deve aceitar várias entradas STL como objetos de origem separados e visíveis de forma independente.
MeshMill deve alinhar essas fontes, medir sua concordância geométrica e sintetizar uma fonte utilizável
malha sem reter superfícies internas duplicadas ou geometria de sobreposição repetida.

Comportamento planejado:

- adicione, remova, oculte, isole, reordene e inspecione várias fontes STL em um espaço de trabalho;
- reter identidade de origem, unidades, transformações, limites, resolução e histórico de operação;
- fornecer registro automático com controles de alinhamento manual e qualidade de ajuste mensurável;
- particionar as fontes em regiões espaciais antes da comparação, para que grandes entradas permaneçam limitadas;
- analisar ocupação, distância da superfície mais próxima, concordância normal, densidade local, variância e
  contagem de observações em regiões sobrepostas;
- classificar superfícies correspondentes, superfícies conflitantes, ruído de varredura, lacunas e geometria exclusiva;
- consolidar superfícies estatisticamente concordantes em uma superfície representativa com registros
  confiança em vez de empilhar triângulos duplicados;
- remover geometria fechada, coincidente e compartilhada que não contribui com detalhes de forma externa;
- retém a geometria de origem não sobreposta e expõe regiões ambíguas para revisão visual;
- permitir ponderação por origem e por região quando uma varredura é mais limpa ou mais detalhada;
- validar estanqueidade, limites, normais, dimensões e topologia após síntese;
- registrar a origem da fonte e os parâmetros de síntese para que a malha combinada seja reproduzível;
- visualizar a contagem esperada de triângulos, limites, sobreposição removida e distribuição de confiança antes
  comprometendo o resultado sintetizado.

Este fluxo de trabalho deve usar o mesmo índice espacial fora do núcleo e modelo de unidade de trabalho planejado para grandes
malhas. A comparação estatística e a consolidação de sobreposições também devem ser distribuíveis entre países locais.
ou nós MeshMill remotos.

## Síntese distribuída

Um cluster MeshMill deve coordenar vários nós operando em paralelo em vários
estações de trabalho. Um nó pode inspecionar, selecionar, reduzir, validar, reparar ou combinar uma região ou região atribuída.
unidade de trabalho. As contribuições permanecem com versões independentes até serem revisadas e incorporadas
em uma versão de objeto compartilhado.

O sistema deve suportar:

- contribuições simultâneas de múltiplos operadores e nós automatizados;
- entradas, parâmetros, dependências e saídas determinísticas de unidades de trabalho;
- agendamento com reconhecimento de capacidade baseado em CPU, GPU, memória, algoritmos e carga atual;
- particionamento de malhas, regiões, passagens de validação e estágios de síntese com reconhecimento de dependência;
- filas duráveis com pausa, retomada, cancelamento, nova tentativa, reatribuição e recuperação de falhas;
- artefatos endereçados por conteúdo e verificações de integridade entre nós;
- síntese reproduzível de um conjunto gravado de versões de contribuições aceitas;
- estações de trabalho off-line ou conectadas de forma intermitente que podem ser sincronizadas posteriormente;
- operação local com controle explícito sobre os nós participantes e dados compartilhados do projeto.

## Colaboração versionada

Cada contribuição deve registrar a versão do objeto pai, região selecionada ou unidade de trabalho, operação,
parâmetros, identidade do nó, carimbos de data/hora, dependências, resultados de validação e soma de verificação de saída.

Comportamento de colaboração planejado:

- os projetos contêm objetos, ramificações, pontos de verificação, contribuições e versões sintetizadas;
- os contribuidores podem trabalhar a partir da mesma versão pai sem substituir uns aos outros;
- contribuições não sobrepostas podem ser mescladas automaticamente após validação;
- geometria sobreposta ou dependências incompatíveis criam um conflito explícito;
- os conflitos fornecem comparação visual, escolha em nível de região, rebase, nova execução e resolução manual;
- os estados de revisão incluem pendente, aceito, rejeitado, substituído, conflitante e incorporado;
- o manifesto de síntese final identifica todas as contribuições e dependências incorporadas.

## IU de coordenação

O aplicativo de desktop deve gerenciar o trabalho distribuído sem exigir uma linha de comando separada
ou fluxo de trabalho de administração de servidor. As visualizações planejadas incluem:

- **Projetos:** objetos, ramificações, versões, contribuidores e status de síntese.
- **Cluster:** estações de trabalho e nós conectados, recursos, integridade, carga e atribuição atual.
- **Fila:** unidades de trabalho pendentes, ativas, pausadas, bloqueadas, com falha e concluídas.
- **Contribuições:** autor, nó, versão pai, região afetada, parâmetros, verificações e estado de revisão.
- **Comparar:** visualizações 3D sincronizadas, diferenças geométricas, métricas e inspeção de limites.
- **Conflitos:** regiões sobrepostas, conflitos de dependência, opções de resolução e resultados de validação.
- **Síntese:** gráfico de dependências, progresso agregado, versões de contribuição selecionadas e resultado final.
- **Histórico:** gráfico de ramificação, pontos de verificação, mesclagens, versões sintetizadas e manifestos de reprodutibilidade.

A janela de visualização deve mostrar propriedade, regiões atribuídas, trabalho concluído, alterações pendentes, conflitos,
e diferenças de versão sem alterar a malha subjacente.

## Coordenação e transporte

A primeira fase de projeto deve definir os limites do protocolo antes de selecionar um transporte. O protocolo
deve separar os metadados de coordenação de grandes artefatos de malha, apoiar a transferência recuperável e
permanecem utilizáveis em uma rede local sem uma conta externa ou serviço hospedado.

Conceitos de coordenação necessários:

- eleição do coordenador ou de um coordenador explicitamente selecionado;
- descoberta de nós e registro manual de nós;
- sessões autenticadas e autorização no escopo do projeto;
- arrendamentos e batimentos cardíacos para propriedade de trabalho;
- submissão de trabalho idempotente e aceitação de resultados;
- negociação de versões entre diferentes releases do MeshMill;
- eventos estruturados para progresso, logs, validação, falhas e novas tentativas;
- recuperação após interrupção do coordenador, estação de trabalho, rede ou nó.

## Fases de entrega

### Fase 0: processamento de malha grande fora do núcleo

O contrato de índice, streaming, cache, unidade de trabalho e segurança está documentado em
[`docs/OUT_OF_CORE.md`](docs/OUT_OF_CORE.md).

- Estime a contagem de triângulos e a memória de trabalho antes de alocar a malha completa.
- Abra arquivos STL binários grandes como visões gerais de navegação limitadas e com amostragem uniforme.
- Divida a geometria de resolução total em cubos espaciais com limites de sobreposição determinísticos.
- Leia, analise e otimize cubos independentes simultaneamente dentro de CPU e limites de memória.
- Transmita níveis de viewport grossos a finos em vez de exigir a malha completa na memória.
- Desenhe o estado do cubo diretamente na viewport: enfileirado, lendo, processando, concluído e com falha.
- Mostre o progresso por cubo preenchendo cada cubo e mantenha uma visualização de alto nível do objeto inteiro.
- Monte cubos processados com validação de limites, remoção de duplicatas e configurações reproduzíveis.
- Estenda o planejador de cubo local para unidades de trabalho de síntese distribuída em fases posteriores.

### Fase 1: fundação local versionada

- Defina formatos de objeto, operação, contribuição, ramificação e manifesto.
- Adicione espaços de trabalho multi-STL com visibilidade, transformações, metadados e procedência por origem.
- Adicione métricas de qualidade de registro e classificação de sobreposição espacial.
- Sintetize superfícies estatisticamente concordantes enquanto remove geometria duplicada e fechada.
- Adicione revisão visual de conflitos, lacunas, confiança e geometria exclusiva de uma fonte.
- Persista o histórico local nas sessões do aplicativo.
- Adicione malha visual e comparações de região.
- Torne as operações determinísticas e reproduzíveis de forma independente.

### Fase 2: nós locais coordenados

- Execute nós do trabalhador em uma estação de trabalho.
- Adicione filas, relatórios de capacidade, atribuição de trabalho e cancelamento.
- Exibir o estado do nó e da unidade de trabalho na UI MeshMill.
- Valide o particionamento e a montagem de resultados localmente.

### Fase 3: síntese de múltiplas estações de trabalho

- Adicione descoberta e registro de LAN autenticados.
- Transfira entradas de trabalho e resultados endereçados por conteúdo com suporte de currículo.
- Coordene o trabalho simultâneo em várias estações de trabalho.
- Recuperar atribuições após falha de nó ou rede.

### Fase 4: versionamento colaborativo

- Adicione colaboradores, filiais, estados de revisão e permissões.
- Mesclar contribuições não sobrepostas.
- Detecte e resolva conflitos de sobreposição ou dependência.
- Sintetize as contribuições selecionadas em uma versão reproduzível do objeto.

### Fase 5: endurecimento de produção

- Adicione testes de compatibilidade de protocolo e manipulação de versões mistas.
- Adicione testes de auditoria, integridade, corrupção, interrupção e recuperação.
- Desempenho de agendamento, particionamento, transferência, mesclagem e síntese de referência.
- Implantação de documentos, backup, migração e recuperação de incidentes.
