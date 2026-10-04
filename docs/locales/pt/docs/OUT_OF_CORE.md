# Arquitetura de malha fora do núcleo

A proteção atual de arquivos grandes do MeshMill estima a memória de trabalho antes de alocar um arquivo completo
malha. Os arquivos que excedem o orçamento configurado podem ser abertos como visões gerais de navegação limitadas. Um
a visão geral é uma amostra de geometria, é visivelmente identificada como tal e não pode ser editada ou exportada como
embora fosse a fonte completa.

Os verdadeiros detalhes dependentes do zoom requerem um índice espacial persistente. O design abaixo define que
próxima fase de implementação.

## Formato do índice

Cada malha de origem recebe um diretório `.meshmill-index` versionado contendo:

- `manifest.json`, com o tamanho da fonte, hora da modificação, hashes de conteúdo amostrado, limites,
  contagem de triângulos, versão do índice, precisão das coordenadas e descrições de níveis;
- blocos espaciais endereçados por nível octree e código Morton;
- uma malha de exibição grosseira para cada bloco pai ocupado;
- registros triangulares de resolução total em blocos de folhas; e
- propriedade de limites e metadados de sobreposição usados durante operações e montagem regionais.

A criação do índice lê a origem sequencialmente em blocos limitados. Ele grava execuções temporárias de blocos e
publica atomicamente o manifesto depois que cada arquivo necessário passa na validação. Uma interrupção ou
o índice obsoleto é detectado em seu manifesto e pode ser retomado ou reconstruído sem abrir o arquivo completo
malha na memória.

## Streaming de janela de visualização

A viewport seleciona blocos usando o tronco da câmera e o erro de espaço na tela. Os blocos principais grossos são
mostrado primeiro. Blocos filhos visíveis os substituem conforme a câmera se aproxima, enquanto fora da tela e
ladrilhos de baixo impacto permanecem ásperos. RAM e VRAM têm orçamentos independentes e orçamentos usados menos recentemente
caches. Liberar detalhes nunca libera a representação grosseira do objeto inteiro.

O agendador registra estes estados de bloco: enfileirado, leitura, processamento, upload, residente, falhado,
e cancelado. A viewport pode colorir cubos por estado e preencher cada cubo proporcionalmente ao seu
progresso. O cancelamento remove resultados parciais e deixa ativa a última representação completa.

## Processamento e capacidade

Uma unidade de trabalho local é um bloco mais a sobreposição determinística exigida pela sua operação. Simultaneidade
é limitado pelo RAM atualmente disponível, porcentagem de memória configurada, contagem de processador lógico e
tamanho medido da unidade de trabalho. O upload e a exibição de GPU têm um orçamento VRAM separado. Paralelo relatado
a capacidade é uma estimativa até que os ladrilhos representativos sejam medidos.

As operações mantêm um proprietário para cada elemento de fronteira. A montagem valida limites compartilhados,
remove duplicatas, verifica contagens e limites e registra os parâmetros exatos usados. O mesmo trabalho
a unidade e o formato do resultado podem ser posteriormente agendados em nós de síntese distribuída.

## Regras de segurança

- Uma amostra global é rotulada como uma visão geral, e não como detalhe da janela de visualização de resolução total.
- Uma visão geral não pode substituir ou exportar como a malha de origem completa.
- As solicitações de carga total que excedem o orçamento atual exigem uma escolha explícita.
- A geração de índice, o processamento de blocos e a montagem permanecem canceláveis e preservam o anterior
  estado completo.
- Os valores de capacidade são estimativas e identificam se descrevem o motor atual ou planejado
  execução de blocos paralelos.
