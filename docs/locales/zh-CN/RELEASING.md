# 释放MeshMill

稳定发布管道在 GitHub 托管的 Windows 运行器上构建 Windows 工件。一个单独的
手动工作流程在本机上构建未签名的 Linux x86-64 和 macOS Intel/Apple 芯片预览
GitHub 托管的运行器。最终用户不安装 Python、Node.js 或依赖项。

在构建之前，刷新并验证本地化源目录：

```powershell
python tools/localization/extract_ui_catalog.py
python tools/localization/validate_locales.py
python tools/release_privacy_check.py
```

## 在第一次公开发布之前

1. 完成并验证计划的应用程序和文档翻译。
2. 查看 GPL 和第三方声明。
3. 测试安装、启动、STL 加载、优化、导出和干净卸载
   Windows 帐户或虚拟机。
4. 针对 `samples/sample-scan.stl` 运行 CI。检查每个文档屏幕截图并裁剪
   任务栏、不属于 MeshMill 的窗口镶边、通知、私有路径、帐户
   发布前的详细信息和不相关的桌面内容。
5. 在之前配置存储库本地Git作者帐户的GitHub无回复地址
   首先提交。用`git config --local --get user.email`确认。
6. 配置可选的 Authenticode 签名密钥：
   - `WINDOWS_CERTIFICATE_BASE64`：Base64 编码的 PFX 证书。
   - `WINDOWS_CERTIFICATE_PASSWORD`：PFX密码。

如果没有签名证书，生成的文件仍然有效，但 Windows SmartScreen 可能会显示
无法识别的发布者警告。不要将未签名的版本描述为已签名或受信任的版本。

## 原件扫描件和Git LFS

`samples/original-scan.stl` 通过 Git LFS 进行跟踪，因为它超过了 GitHub 的正常 100 MiB
文件限制。在第一次提交之前，验证：

```powershell
git check-attr filter -- samples/original-scan.stl
git lfs pointer --file samples/original-scan.stl
```

过滤器必须是 `lfs`，并且指针对象 ID 必须匹配 `samples/SHA256SUMS.txt`。发布
工作流程检查 LFS 内容并将原始 STL 作为单独的发布资产发布。 CI 使用
较小的普通 Git 示例，并且不下载 LFS 对象。

## 测试发布版本而不发布

打开 **操作**，选择 **发布**，选择 **运行工作流程**，然后输入数字版本，例如
`0.1.0`。手动运行上传工作流工件以进行测试，但不会创建公共 GitHub
释放。

## 发布版本

来自干净、经过审查的 `main` 分支：

```powershell
git tag -a v0.1.0 -m "MeshMill 0.1.0"
git push origin v0.1.0
```

该标签启动发布工作流程。它：

1. 安装固定的构建依赖项；
2. 生成匹配的 Windows 版本元数据；
3. 构建独立的 GUI 和 CLI 可执行文件；
4. 配置签名机密时对可执行文件进行签名；
5. 构建每用户 Inno Setup 安装程序；
6. 配置时对安装程序进行签名；
7. 创建可移植的 ZIP 和 SHA-256 校验和文件；
8. 上传工作流程工件；
9. 为推送的标签创建 GitHub 版本。

在宣布发布之前，请在干净的 Windows 系统上验证安装程序和可移植存档。
保持与同一发布标签下可用的每个分布式二进制文件相对应的源代码。
在标记第一个之前，请确认 GitHub 按钮指向最终的公共存储库 URL
释放。

## 构建 Linux 和 macOS 预览

打开 **操作**，选择 **平台预览版本**，然后选择 **运行工作流程**。输入预览
版本如“0.2.0-preview.1”。

首次运行时关闭 **发布公共 GitHub 预发布**。工作流程构建和测试：

- Ubuntu 22.04 上的 Linux x86-64；
- Intel 运行器上的 macOS x86-64；
- Apple 芯片运行器上的 macOS arm64。

下载工作流程工件并检查其校验和和日志。再次运行工作流程
仅在每个构建作业通过后才启用发布。已发布的 macOS 预览版是临时签名的，
未经 Apple 公证。将它们描述为预览版本并将测试人员链接到
`docs/PLATFORM_TESTING.md` 和 **平台预览测试** 问题表单。
