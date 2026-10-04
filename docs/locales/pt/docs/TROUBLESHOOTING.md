# Solução de problemas

## Windows bloqueia o download

Construções de comunidade não assinadas podem acionar o Microsoft Defender SmartScreen. Compare o baixado
hash SHA-256 do arquivo com `SHA256SUMS.txt` da mesma versão GitHub. Liberações assinadas identificam
seu editor nas propriedades do arquivo Windows.

## A compilação portátil não inicia

Extraia o ZIP completo antes de executar `MeshMill.exe`. O diretório `_internal` deve permanecer próximo
para ambos os executáveis. Não execute o executável de dentro do visualizador ZIP.

## Um grande STL abre como uma visão geral

O conjunto de trabalho estimado excede o orçamento de memória em Configurações. O modo de visão geral é intencionalmente
somente leitura. Aumente o orçamento somente quando a máquina tiver memória disponível suficiente ou reduza o
mesh antes de abri-lo para edição.

## Uma visualização padrão não foi salva

Pressione o atalho de visualização modificado por Ctrl e escolha **Salvar** ou pressione Enter na confirmação
diálogo. Salvar uma visualização também atualiza seu oposto. A linha de status informa a visualização salva.

## Os atalhos de navegação não respondem

Feche qualquer caixa de diálogo modal primeiro. Revise ou redefina os atalhos em Configurações, caso tenham sido personalizados. O
os atalhos de visualização padrão usam Inserir, Home, Page Up, Delete, End e Page Down.

## Crie um log de diagnóstico de orientação local

O log de diagnóstico está desabilitado por padrão. Para gravar o roteamento do teclado e o estado da câmera localmente:

```powershell
.\MeshMill.exe --diagnostic-log ".\orientation-session.jsonl" "C:\path\mesh.stl"
```

O log pode conter o caminho do arquivo aberto. Revise e edite antes de compartilhar. A geometria da malha não é
gravado no log.

## Informar um problema

Inclui a versão MeshMill, versão Windows, modelo GPU, contagem de triângulos de malha, ação exata
sequência e se o instalador ou pacote portátil foi usado. Use a amostra redistribuível
malha quando possível. Não anexe verificações privadas ou logs de diagnóstico sem revisá-los primeiro.
