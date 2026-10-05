# Liberando MeshMill

O pipeline de lançamento estável cria artefatos do Windows em executores do Windows hospedados no GitHub. Um separado
fluxo de trabalho manual cria visualizações não assinadas de Linux x86-64 e macOS Intel/Apple Silicon em nativo
Corredores hospedados no GitHub. Os usuários finais não instalam Python, Node.js ou dependências.

Antes de criar, atualize e valide os catálogos de origem de localização:

```powershell
python tools/localization/extract_ui_catalog.py
python tools/localization/validate_locales.py
python tools/release_privacy_check.py
```

## Antes do primeiro lançamento público

1. Concluir e validar as traduções planejadas de aplicação e documentação.
2. Revise os avisos da GPL e de terceiros.
3. Teste a instalação, inicialização, carregamento do STL, otimização, exportação e desinstalação em um ambiente limpo
   Conta Windows ou máquina virtual.
4. Execute o CI em `samples/sample-scan.stl`. Inspecione todas as capturas de tela da documentação e recorte
   a barra de tarefas, janela cromada que não faz parte de MeshMill, notificações, caminhos privados, conta
   detalhes e conteúdo de desktop não relacionado antes da publicação.
5. Configure o autor Git local do repositório com o endereço sem resposta GitHub da conta antes do
   primeiro confirme. Confirme com `git config --local --get user.email`.
6. Configure segredos opcionais de assinatura do Authenticode:
   - `WINDOWS_CERTIFICATE_BASE64`: Certificado PFX codificado em Base64.
   - `WINDOWS_CERTIFICATE_PASSWORD`: senha PFX.

Sem um certificado de assinatura, os arquivos gerados ainda funcionam, mas o Windows SmartScreen pode mostrar
um aviso de editor não reconhecido. Não descreva compilações não assinadas como assinadas ou confiáveis.

## Digitalização original e Git LFS

`samples/original-scan.stl` é rastreado por meio de Git LFS porque excede os 100 MiB normais de GitHub
limite de arquivo. Antes do primeiro commit, verifique:

```powershell
git check-attr filter -- samples/original-scan.stl
git lfs pointer --file samples/original-scan.stl
```

O filtro deve ser `lfs` e o ID do objeto ponteiro deve corresponder a `samples/SHA256SUMS.txt`. O lançamento
O fluxo de trabalho verifica o conteúdo do LFS e publica o STL original como um ativo de lançamento separado. CI usa
a amostra menor do Git normal e não baixa o objeto LFS.

## Testar uma versão de lançamento sem publicar

Abra **Ações**, selecione **Liberar**, escolha **Executar fluxo de trabalho** e insira uma versão numérica, como
`0.1.0`. Uma execução manual carrega artefatos de fluxo de trabalho para teste, mas não cria um GitHub público
Liberar.

## Publicar um lançamento

De uma ramificação `main` limpa e revisada:

```powershell
git tag -a v0.1.0 -m "MeshMill 0.1.0"
git push origin v0.1.0
```

A tag inicia o fluxo de trabalho de lançamento. Isto:

1. instala as dependências de construção fixadas;
2. gera metadados de versão Windows correspondentes;
3. constrói os executáveis GUI e CLI independentes;
4. assina os executáveis quando os segredos de assinatura são configurados;
5. cria o instalador Inno Setup por usuário;
6. assina o instalador quando configurado;
7. cria o arquivo de soma de verificação ZIP e SHA-256 portátil;
8. carrega artefatos de fluxo de trabalho;
9. cria a versão GitHub para a tag enviada.

Verifique o instalador e o arquivo portátil em um sistema Windows limpo antes de anunciar o lançamento.
Mantenha a fonte correspondente a cada binário distribuído disponível sob a mesma tag de lançamento.
Confirme se o botão GitHub aponta para o URL final do repositório público antes de marcar o primeiro
lançamento.

## Crie visualizações do Linux e do macOS

Abra **Ações**, selecione **Compilações de visualização da plataforma** e escolha **Executar fluxo de trabalho**. Insira uma visualização
versão como `0.2.0-preview.1`.

Deixe a opção **Publicar um pré-lançamento público do GitHub** desativada na primeira execução. O fluxo de trabalho cria e testa:

- Linux x86-64 no Ubuntu 22.04;
- macOS x86-64 em um processador Intel;
- macOS arm64 em um executor de silício da Apple.

Baixe os artefatos de fluxo de trabalho e inspecione suas somas de verificação e logs. Execute o fluxo de trabalho novamente com
publicação habilitada somente após cada trabalho de construção ser aprovado. As visualizações publicadas do macOS são assinadas ad hoc,
não autenticado pela Apple. Descreva-os como versões de visualização e vincule testadores a
`docs/PLATFORM_TESTING.md` e o formulário de emissão **Teste de visualização da plataforma**.
