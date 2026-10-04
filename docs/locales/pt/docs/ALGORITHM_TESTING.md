# Teste de algoritmo e contribuição

Os algoritmos MeshMill devem tornar a geometria difícil gerenciável, mantendo seus efeitos visíveis,
mensurável e reversível antes que um resultado seja aplicado.

## Jogos de referência

Use ambas as versões agrupadas da geometria da amostra composta:

- `samples/sample-scan.stl` é o acessório Git normal menor para desenvolvimento de rotina, automatizado
  verificações e aprendendo os controles.
- `samples/original-scan.stl` é o acessório Git LFS completo para comportamento de arquivos grandes, camadas redundantes,
  densidade irregular, sobreposição e trabalho de desempenho.

As regiões redundantes e densas são características de teste intencionais. Um teste pode direcioná-los, mas
não deve assumir que todas as superfícies sobrepostas são descartáveis. Adicione malhas sintéticas compactas quando um
a mudança precisa de um limite conhecido, curvatura, topologia, densidade ou invariante de sobreposição.

## Lista de verificação de comparação

Para uma alteração de algoritmo ou parâmetro, registre:

- Versão ou commit MeshMill;
- acessório de entrada e soma de verificação;
- algoritmo, predefinição de qualidade, alvo e configurações avançadas;
- contagens de triângulos e vértices originais e resultantes;
- porcentagem de redução, dimensões e desvio de dimensão;
- tempo decorrido e pico de memória quando o desempenho é relevante;
- capturas de tela das mesmas visualizações e modos de exibição salvos;
- limites visíveis, buracos, auto-intersecção, sobreposição ou alterações de distorção;
- se o resultado veio de uma operação de malha inteira ou somente de seleção.

Compare com o comportamento atual no mesmo alvo, não apenas com outra predefinição com um
contagem de saída diferente. Inspecione exibições sombreadas, de densidade, de estrutura de arame e de vértices, quando aplicável.

## Orientação de aceitação

Uma alteração de otimização deve evitar alterações dimensionais inesperadas, inversão óbvia da superfície,
rachaduras entre regiões processadas, perda de limites significativos e grandes regressões de qualidade em um
contagem de saída semelhante. Mudanças orientadas para a densidade devem demonstrar que a concentração removida não
não carrega curvatura ou topologia útil.

Os resultados de desempenho devem identificar o processador, capacidade de memória, hardware gráfico, operação
sistema, tamanho da entrada e se os dados já estavam armazenados em cache. Validação estrutural e capturas de tela
apoiam a revisão, mas não substituem a inspeção por colaboradores familiarizados com a geometria de origem.

## Testes de regressão

Prefira testes determinísticos com tolerâncias explícitas. Mantenha os novos fixtures pequenos o suficiente para o Git normal,
documentar sua origem e licença e usar geometria sintética quando dados de origem reais forem desnecessários.
Os testes devem abranger o cancelamento e a restauração do estado quando uma operação pode modificar a geometria.
