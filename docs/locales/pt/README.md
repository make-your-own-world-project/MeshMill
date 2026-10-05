<p align="center">
  <img src="assets/meshmill-logo.svg" width="620" alt="MeshMill: Dirty geometry? Clean it up!">
</p>

O MeshMill é um aplicativo de desktop especializado na manipulação de geometrias de malha
grandes, densas ou complexas, tornando-as gerenciáveis. Ele oferece inspeção rápida, análise de densidade, seleção regional, recorte, exclusão
e redução controlada da malha, sem exigir criação de conta ou upload da geometria.

A renderização OpenGL acelerada por GPU mantém a navegação na janela de visualização, seleção de hardware, visualização de densidade,
e inspeção interativa responsiva. A redução de malha atualmente é executada em trabalhadores de CPU nativos separados,
mantendo longos cálculos de geometria longe da interface.

O MeshMill trabalha com malhas provenientes de scanners 3D, exportações de CAD e modelagem, pipelines de reconstrução,
geometria gerada e outras fontes compatíveis com o STL. Ele prepara a geometria para editores subsequentes,
ferramentas de manufatura e outros fluxos de trabalho com malhas. Modelagem de uso geral, escultura, animação,
materiais e criação de cenas estão fora do seu escopo.

## Download

Escolha seu sistema operacional. Cada pacote é independente. Python, Node.js e outros
dependências de desenvolvimento não são necessárias.

| Sistema | Download recomendado | Estado |
| --- | --- | --- |
| **Windows x64** | **[Baixe o instalador do Windows][windows-installer]** | Versão suportada |
| Windows x64, sem instalação | [Baixe o ZIP portátil][windows-portable] | Versão suportada |
| Linux x86-64 | [Baixar a visualização do Linux][linux-preview] | Pré-visualização dos testes iniciais |
| macOS Apple silício | [Baixe a visualização do Apple Silicon][mac-arm-preview] | Pré-visualização dos testes iniciais |
| MacOS Intel | [Baixe a visualização do Intel Mac][mac-intel-preview] | Pré-visualização dos testes iniciais | <!-- macOS -->

**A maioria dos usuários do Windows deve escolher o instalador do Windows.** Use o ZIP portátil somente quando fizer isso.
não deseja MeshMill instalado ou não tem permissão para instalar aplicativos.

Os pacotes Linux e macOS são pré-visualizações não assinadas. Eles passam compilações nativas automatizadas e
testes de fumaça empacotados, mas ainda precisam de testes de hardware real. Leia o
[Notas de visualização do Linux e macOS](../../PLATFORM_TESTING.md) antes de instalá-los.

O Windows SmartScreen ou o macOS Gatekeeper podem alertar sobre pacotes não assinados. Somas de verificação e o
optional [sample mesh][sample-mesh] are available with the releases. [Browse all releases and
checksums][all-releases] only if you need an older version or want to verify a download.

[windows-installer]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.1.1/MeshMill-0.1.1-windows-x64-setup.exe
[windows-portable]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.1.1/MeshMill-0.1.1-windows-x64-portable.zip
[linux-preview]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.2.0-preview.2/MeshMill-0.2.0-preview.2-linux-x86_64.tar.gz
[mac-arm-preview]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.2.0-preview.2/MeshMill-0.2.0-preview.2-macos-arm64.zip
[mac-intel-preview]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.2.0-preview.2/MeshMill-0.2.0-preview.2-macos-x86_64.zip
[sample-mesh]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.1.1/MeshMill-sample-scan-original.stl
[all-releases]: https://github.com/make-your-own-world-project/MeshMill/releases

## Início rápido

1. Abra um STL.
2. Inspecione-o nos modos de exibição Sombreado, Densidade, Aramado ou Vértices.
3. Escolha um nível de qualidade, um algoritmo e uma contagem de triângulos desejada.
4. Selecione **Otimizar** para calcular um resultado.
5. Compare as malhas original e otimizada e, em seguida, selecione **Aplicar** para confirmar a operação.
6. Selecione **Salvar estado atual** ou pressione `Ctrl+S`.

O MeshMill nunca inicia a otimização apenas porque um arquivo ou configuração foi alterado.

## Recursos

- Entrada STL em formatos binário e ASCII; saída STL em formato binário
- Fast QEM, redução com densidade balanceada, preservação de forma e preservação de topologia
- Janela de visualização OpenGL acelerada por GPU, seleção de hardware e visualização de densidade
- Trabalhadores de geometria de fundo nativos para redução de malha
- Modos de visualização: sombreado, densidade, estrutura de arame (wireframe) e vértices
- Metas automáticas derivadas da geometria, em vez de um limite fixo de triângulos
- Seleção de polígonos com seleção aditiva de múltiplas regiões
- Recortar, excluir ou otimizar apenas a região selecionada
- Comparação em cache entre as malhas original, anterior e atual
- Desfazer e refazer para alterações de geometria confirmadas
- Desvio dimensional, porcentagem de redução e tamanho estimado da saída
- Unidades de exibição: milímetro, centímetro, metro, polegada e pé
- Métricas de CPU, memória, GPU e atividade geométrica
- Carregamento de visão geral limitada quando um arquivo STL binário excede o limite de memória configurado
- Aplicativos com interface gráfica (GUI) e linha de comando
- Processamento local sem dependência de conta, telemetria, upload ou nuvem

## Inspecione a geometria antes de reduzi-la

A tela sombreada fornece uma visão nítida da superfície e da silhueta. É útil para comparar
preservação da forma antes de aplicar uma passagem de otimização.

![Visualização sombreada do MeshMill mostrando a malha de amostra agrupada](../../images/meshmill-shaded.png)

A exibição Vértices expõe a distribuição real dos pontos. Regiões de varredura densas, áreas esparsas e
mudanças abruptas na amostragem são visíveis sem alterar a geometria. O painel de métricas expandido
rastreia atividades de CPU, memória, GPU e processamento de geometria enquanto trabalha com a malha.

![Exibição de vértices do MeshMill com métricas de desempenho expandidas](../../images/meshmill-vertices.png)

A exibição Wireframe mostra a estrutura triangular diretamente. Ajuda a identificar densidade desnecessária,
triangulação irregular e regiões onde a simplificação pode remover geometria substancial.

![Exibição do MeshMill Wireframe mostrando variação na densidade do triângulo](../../images/meshmill-wireframe.png)

## Analisar densidade de malha

A exibição Densidade mapeia a densidade local relativa em todo o modelo. Regiões esparsas permanecem frias enquanto
regiões cada vez mais densas movem-se através de cores mais brilhantes, tornando a amostragem irregular visível à primeira vista.

![Exibição da densidade do MeshMill mostrando a densidade relativa da malha](../../images/meshmill-density.png)

A densidade permanece disponível durante a avaliação de uma otimização provisória. A caixa de ferramentas informa o
algoritmo, alvo, contagens de triângulos e vértices resultantes, porcentagem de redução, dimensões e
tamanho de saída estimado antes da aplicação da passagem.

![Exibição de densidade do MeshMill mostrando uma otimização provisória](../../images/meshmill-density-overview.png)

Segure o botão direito do mouse para inspecionar uma região através da lupa circular. A visão ampliada
permanece centralizado no ponteiro e revela a densidade local sem alterar a posição da câmera principal.

![Exibição da densidade do MeshMill com o ampliador da janela de visualização](../../images/meshmill-density-zoom.png)

## Controles de visualização

| Entrada | Ação |
| --- | --- |
| Arrastar com o botão do meio | Orbitar |
| Shift + arrastar com o botão do meio | Panorâmica |
| Roda do mouse | Zoom em direção ao ponteiro |
| Ctrl + roda do mouse | Girar no sentido horário ou anti-horário |
| Teclas de seta | Orbitar em torno do centro da vista |
| Ctrl + teclas de seta | Panorâmica |
| Ctrl + Shift + Cima/Baixo | Zoom |
| Ctrl + Shift + Esquerda/Direita | Rolo |
| `F1`/`F2`/`F3`/`F4` | Sombreado / Densidade / Wireframe / Vértices |
| Segure o botão direito do mouse | Lupa |
| Shift + clique com o botão esquerdo | Adicionar ou remover pontos de régua |
| Ctrl + arrastar para a esquerda | Desenhe um polígono de seleção |
| `Ctrl+C` | Adicione o polígono à seleção salva |
| `Ctrl+X` | Cortar para a seleção |
| `Ctrl+Space` | Otimizar a seleção |
| `Delete` | Exclua a seleção |
| `Escape` | Limpar a seleção ou régua ativa |
| `Ctrl+Z`/`Ctrl+Y` | Desfazer/refazer |
| `Ctrl+S` | Salvar o estado atual da malha |

As teclas de visualização padrão seguem o bloco de navegação de seis teclas:

| Chave | Ver | Ctrl + tecla |
| --- | --- | --- |
| `Insert` | Esquerda | Defina a orientação atual como Esquerda |
| `Home` | Frente | Defina a orientação atual como Frontal |
| `Page Up` | Certo | Defina a orientação atual como Direita |
| `Delete` | Topo quando não existe seleção | Defina a orientação atual como Superior |
| `End` | Voltar | Defina a orientação atual como Voltar |
| `Page Down` | Parte inferior | Defina a orientação atual como Inferior |

Salvar uma visualização também atualiza sua visualização oposta. Esquerda e Direita, Frente e Trás, e Superior e Inferior
permanecer emparelhado. Na caixa de diálogo de confirmação, **Salvar** é a ação padrão, então Enter salva o
orientação. A frente aparece na parte superior das visualizações Superior e Inferior.

Os atalhos podem ser alterados ou redefinidos em Configurações.

## Fluxo de trabalho de seleção

Segure Ctrl e arraste para a esquerda para desenhar um polígono. Arraste os cantos para remodelá-la, clique com o botão esquerdo em uma aresta para adicionar uma
ponto ou clique com o botão direito em uma aresta para removê-la. Adicione mais regiões com `Ctrl+C`. Mover a câmera esconde
o polígono do espaço da tela, mantendo a geometria selecionada.

A otimização com uma seleção ativa afeta apenas essa seleção. O resultado permanece provisório
até que **Aplicar** seja selecionado. **Cancelar** descarta o resultado provisório e mantém a seleção para
outra configuração pode ser tentada. As operações de corte e exclusão tornam-se edições normais de malha que podem ser revertidas.

O painel de seleção informa os vértices selecionados cumulativamente, triângulos, participação de malha, estimativa
tamanho e dimensões. Suas ações cortam, adicionam, otimizam, excluem, recuam ou limpam os dados retidos.
seleção sem ocultar a geometria circundante.

![MeshMill mostrando uma seleção regional retida e suas estatísticas de geometria](../../images/meshmill-crop-selection.png)

## Malhas grandes

Antes de alocar um STL binário, MeshMill compara sua memória de trabalho estimada com a configurada
orçamento de memória. Um arquivo acima do orçamento é aberto como uma visão geral limitada e somente leitura. Os relatórios de visão geral
a contagem completa de triângulos de origem, mas desativa a edição e a exportação porque é uma amostra, não a completa
objeto. O processamento fora do núcleo indexado e dependente de zoom é planejado em
[docs/OUT_OF_CORE.md](docs/OUT_OF_CORE.md).

## Linha de comando

`MeshMillCLI.exe` está incluído em ambos os pacotes de lançamento:

```powershell
.\MeshMillCLI.exe "C:\path\mesh.stl" --preset balanced
.\MeshMillCLI.exe "C:\path\mesh.stl" --target 150000 --output "C:\path\mesh-reduced.stl"
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm density --target 150000
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm topology --overwrite
```

Execute `.\MeshMillCLI.exe --help` para todas as opções. MeshMill se recusa a substituir seu arquivo de entrada.

## Geometria de amostra

Duas versões do exemplo de desenvolvimento estão disponíveis. A amostra é uma malha composta com
camadas intencionais de geometria redundante e densidade variada. Dá às pessoas sem scanner uma
acessório realista para comparar algoritmos, inspecionar densidade, exercer operações regionais,
e desenvolvimento de recursos de roteiro. MeshMill não requer entrada digitalizada.

| Arquivo | Triângulos | Tamanho | Entrega | Melhor para |
| --- | ---: | ---: | --- | --- |
| [`sample-scan.stl`](../../../samples/sample-scan.stl) | 249.999 | 11,9 MiB | Git normal | Avaliação rápida, CI e aprendizado dos controles |
| [`original-scan.stl`](../../../samples/original-scan.stl) | 4.126.315 | 196,8 MiB | Git LFS | Testando geometria de fonte densa e desempenho de malha grande |

A amostra menor é baixada com cada clone normal. O original intocado é opcional e
gerenciado por meio de Git LFS para que não aumente o histórico comum do repositório. O desktop GitHub inclui
Git LFS. Usuários de linha de comando podem instalar Git LFS e executar:

```powershell
git lfs pull --include="samples/original-scan.stl"
```

Os lançamentos marcados também publicam o STL original como um download direto para pessoas que não usam Git.
Consulte [`samples/README.md`](../../../samples/README.md) para procedência, dimensões e somas de verificação.

Os contribuidores do algoritmo também devem ler o
[guia de teste de algoritmo](docs/ALGORITHM_TESTING.md) antes de comparar ou alterar a redução
comportamento.

## Unidades STL

STL não codifica uma unidade. Alterar unidades do modelo altera rótulos e medidas sem dimensionamento
as coordenadas salvas. Selecione a unidade que descreve a geometria de origem.

## Privacidade

MeshMill lê e grava arquivos locais. Ele não contém conta, telemetria, upload, publicidade ou
recurso de processamento em nuvem. A implementação atual das métricas GPU usa desempenho Windows local
contadores. Provedores de métricas nativas equivalentes estão planejados para Linux e macOS.

Para solução de problemas de diagnóstico, os desenvolvedores podem iniciar a GUI com
`--diagnostic-log <local-file.jsonl>`. O log registra o roteamento de entrada e o estado da câmera localmente e é
desativado durante o uso normal.

## Desenvolvimento e lançamento

O texto e a documentação da interface do usuário localizados são inicialmente produzidos com tradução automática externa
serviços e verificado automaticamente quanto a danos estruturais. A tradução automática ainda pode ser
não natural ou incorreto. Os falantes nativos são incentivados a revisar e corrigir as traduções por meio de
o processo de contribuição.

- [Contribuindo](CONTRIBUTING.md)
- [Processo de liberação](RELEASING.md)
- [Roteiro](ROADMAP.md)
- [Solução de problemas](docs/TROUBLESHOOTING.md)
- [Avisos de terceiros](THIRD_PARTY_NOTICES.md)

## Suporte MeshMill

MeshMill é desenvolvido e mantido de forma independente. Leia
[por que apoiar este trabalho é importante](SUPPORT.md), ou apoiar o desenvolvimento contínuo por meio de
[Compre um café para mim](https://buymeacoffee.com/tednv).

MeshMill está licenciado sob a Licença Pública Geral GNU, versão 3 ou posterior. Veja
[`LICENSE`](../../../LICENSE).
