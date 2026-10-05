# Contribuindo

Contribuições são bem-vindas por meio de problemas e solicitações pull.

## Escopo do projeto

MeshMill torna gerenciáveis arquivos de malha superdimensionados, densos ou difíceis para edição downstream e
fluxos de trabalho de produção. Contribuições devem melhorar inspeção de geometria, malha e densidade de pontos
gerenciamento, otimização, seleção, corte, limpeza, validação, intercâmbio STL, desempenho,
ou a coordenação dessas operações.

O projeto não inclui modelagem de uso geral, escultura, pintura, animação, renderização,
composição de cena, materiais, rigging ou outros sistemas de criação de conteúdo. Propostas que apresentam
esses recursos estão fora do escopo do projeto.

Novos recursos devem manter o foco da aplicação, preservar fluxos de trabalho diretos que se transformam em fonte
geometria em malhas gerenciáveis e evite transformar controles de suporte em uma edição geral
ambiente.

## Localização

O texto fonte da IU em inglês é armazenado em `locales/en-US.json`. Os metadados de localidade são armazenados em
`locales/manifest.json`. Os catálogos de UI traduzidos usam as mesmas chaves estáveis e o nome do arquivo
`<locale>.json`. A documentação traduzida usa o nome de arquivo raiz correspondente em
`docs/locales/<locale>/`.

As traduções são inicialmente produzidas com serviços externos de tradução automática e recebem
validação estrutural automatizada. Esse processo não pode garantir resultados naturais, tecnicamente precisos ou
linguagem contextualmente correta. Os falantes nativos são incentivados a revisar e corrigir a IU traduzida
texto e documentação. As correções de tradução devem preservar as chaves do catálogo, espaços reservados,
comandos, links, medidas, nomes de produtos e estrutura Markdown.

Depois de alterar rótulos, dicas de ferramentas, caixas de diálogo ou outros textos visíveis ao usuário, execute:

```powershell
python tools/localization/extract_ui_catalog.py
python tools/localization/validate_locales.py
```

Revise as alterações de origem e as chaves regeneradas juntas.

## Mudanças de geometria e algoritmo

Use a geometria da amostra agrupada ao alterar otimização, análise de densidade, seleção, corte,
manipulação de arquivos grandes ou comportamento de comparação de viewport. Contém intencionalmente camadas redundantes
e densidade irregular, portanto, um resultado útil deve melhorar a capacidade de gerenciamento sem esconder distorções,
descartando limites significativos ou removendo silenciosamente a geometria que outro algoritmo preserva.

Registre a entrada, algoritmo, configurações, contagem de triângulos, dimensões, desvio de dimensão, tempo decorrido,
e capturas de tela relevantes para comparações. Teste o fixture menor do Git normal e, quando o
a mudança diz respeito à geometria grande ou em camadas, o acessório Git LFS original. Não ajuste um algoritmo
apenas para este acessório. Adicione pequenos casos sintéticos para o invariante ou regressão específico que está sendo
testado.

Consulte [Teste e contribuição de algoritmo](docs/ALGORITHM_TESTING.md) para obter a lista de verificação de comparação.

## Configuração de desenvolvimento

1. Instale Python 3.12 de 64 bits em Windows.
2. Crie e ative um ambiente virtual.
3. Instale `requirements-dev.txt`.
4. Execute `python meshmill.py` para GUI ou `python meshmill.py --help` para uso CLI.
5. Execute `python -m py_compile meshmill.py` antes de enviar uma alteração.

Mantenha malhas privadas, executáveis gerados, capturas de tela contendo informações privadas e informações locais
construir diretórios a partir de commits. A geometria de teste redistribuível pertence a `samples/` com seu
fonte, licença, dimensões e método de geração documentados. Novos arquivos de origem devem usar o
Identificador SPDX `GPL-3.0-or-later`.

Corte todas as capturas de tela da documentação para o conteúdo do aplicativo MeshMill. Não inclua o
barra de tarefas, janela cromada não relacionada, notificações, detalhes da conta, caminhos privados ou plano de fundo
conteúdo da área de trabalho.
