# MeshMillの解放

安定版リリース パイプラインは、GitHub でホストされている Windows ランナー上に Windows アーティファクトを構築します。別個の
手動ワークフローは、未署名の Linux x86-64 および macOS Intel/Apple シリコン プレビューをネイティブでビルドします
GitHub でホストされているランナー。エンド ユーザーは、Python、Node.js、または依存関係をインストールしません。

構築する前に、ローカリゼーション ソース カタログを更新して検証します。

```powershell
python tools/localization/extract_ui_catalog.py
python tools/localization/validate_locales.py
python tools/release_privacy_check.py
```

## 初公開前に

1. 計画されているアプリケーションとドキュメントの翻訳を完了し、検証します。
2. GPL とサードパーティの通知を確認してください。
3. クリーンな環境でのインストール、起動、STL の読み込み、最適化、エクスポート、およびアンインストールのテスト
   Windows アカウントまたは仮想マシン。
4. `samples/sample-scan.stl` に対して CI を実行します。すべてのドキュメントのスクリーンショットを検査し、切り取る
   タスクバー、MeshMill の一部ではないウィンドウ クロム、通知、プライベート パス、アカウント
   詳細と無関係なデスクトップ コンテンツを公開前に確認します。
5. リポジトリ ローカルの Git 作成者を、アカウントの前に GitHub 応答不可アドレスを使用して構成します。
   最初のコミット。 `git config --local --get user.email`で確認してください。
6. オプションの Authenticode 署名シークレットを構成します。
   - `WINDOWS_CERTIFICATE_BASE64`: Base64 でエンコードされた PFX 証明書。
   - `WINDOWS_CERTIFICATE_PASSWORD`: PFX パスワード。

署名証明書がなくても、生成されたファイルは引き続き機能しますが、Windows SmartScreen に次のようなメッセージが表示される場合があります。
認識されない発行元の警告。署名されていないビルドを署名付きまたは信頼できるビルドとして記述しないでください。

## オリジナルスキャンとGit LFS

`samples/original-scan.stl` は、GitHub の通常の 100 MiB を超えているため、Git LFS を通じて追跡されます。
ファイル制限。最初のコミットの前に、以下を確認してください。

```powershell
git check-attr filter -- samples/original-scan.stl
git lfs pointer --file samples/original-scan.stl
```

フィルターは `lfs` である必要があり、ポインター オブジェクト ID は `samples/SHA256SUMS.txt` と一致する必要があります。リリース
ワークフローは LFS コンテンツをチェックアウトし、元の STL を別のリリース アセットとして公開します。 CI の使用
より小さい通常の Git サンプルであり、LFS オブジェクトはダウンロードされません。

## 公開せずにリリース ビルドをテストする

**アクション**を開き、**リリース**を選択し、**ワークフローの実行**を選択して、次のような数値バージョンを入力します。
`0.1.0`。手動実行では、テスト用のワークフロー アーティファクトがアップロードされますが、パブリック GitHub は作成されません
リリースします。

## リリースを発行する

クリーンでレビュー済みの `main` ブランチから:

```powershell
git tag -a v0.1.0 -m "MeshMill 0.1.0"
git push origin v0.1.0
```

タグはリリース ワークフローを開始します。それ:

1. 固定されたビルドの依存関係をインストールします。
2. 一致する Windows バージョンのメタデータを生成します。
3. 自己完結型の GUI および CLI 実行可能ファイルを構築します。
4. 署名シークレットが設定されている場合、実行可能ファイルに署名します。
5. ユーザーごとの Inno Setup インストーラーを構築します。
6. 構成時にインストーラーに署名します。
7. ポータブルな ZIP および SHA-256 チェックサム ファイルを作成します。
8. ワークフロー成果物をアップロードします。
9. プッシュされたタグの GitHub リリースを作成します。

リリースを発表する前に、クリーンな Windows システムでインストーラーとポータブル アーカイブを確認してください。
同じリリース タグで利用可能なすべての配布バイナリに対応するソースを保持します。
最初のパブリック リポジトリ URL にタグを付ける前に、GitHub ボタンが最後のパブリック リポジトリ URL を指していることを確認します。
解放する。

## Build Linux and macOS previews

**アクション**を開き、**プラットフォーム プレビュー ビルド**を選択し、**ワークフローの実行**を選択します。プレビューを入力してください
version such as `0.2.0-preview.1`.

最初の実行では、**パブリック GitHub プレリリースを公開** はオフのままにしておきます。 The workflow builds and tests:

- Linux x86-64 on Ubuntu 22.04;
- macOS x86-64 on an Intel runner;
- Apple シリコン ランナー上の macOS arm64。

ワークフロー アーティファクトをダウンロードし、そのチェックサムとログを検査します。 Run the workflow again with
パブリッシュは、すべてのビルド ジョブが成功した後にのみ有効になります。 Published macOS previews are ad-hoc signed,
Apple の公証を受けていません。それらをプレビュー ビルドとして説明し、テスターをリンクします。
`docs/PLATFORM_TESTING.md` と **プラットフォーム プレビュー テスト** 発行フォーム。
