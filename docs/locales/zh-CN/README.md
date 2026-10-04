# MeshMill

![MeshMill 着色视图](../../images/meshmill-shaded.png)

MeshMill 是一款专用的桌面应用程序，旨在让处理超大、高密度或复杂的网格几何体
变得轻松可控。它提供快速检查、密度分析、区域选择、裁剪、删除、
以及受控的网格精简功能，且无需注册账户或上传几何数据。

GPU 加速的 OpenGL 渲染可保持视口导航、硬件拾取、密度可视化和交互检查的流畅响应。网格精简目前在独立的原生 CPU 工作进程中运行，因此耗时的几何计算不会阻塞界面。

MeshMill 支持处理来自 3D 扫描仪、CAD 和建模软件导出文件、重建流程、
生成的几何体以及其他 STL 来源的网格数据。它为下游编辑器、
制造工具及其他网格处理工作流准备几何数据。通用建模、雕刻、动画、
材质和场景创建均不在其功能范围内。

## 下载

从 [GitHub 发布页面](../../releases) 下载以下文件之一：

- `MeshMill-<version>-windows-x64-setup.exe`：针对单用户的安装程序，包含“开始”菜单项及可选的
  桌面快捷方式。
- `MeshMill-<version>-windows-x64-portable.zip`：便携式应用程序。解压整个压缩包，
  然后运行 ​​`MeshMill.exe`。

两个安装包均包含应用程序运行环境。最终用户无需安装 Python、Node.js 或
相关依赖项。初始版本支持 x64 硬件上的 Windows 10 和 Windows 11。计划推出 Linux 和
macOS 软件包；产品和文件格式并非专用于 Windows。

未签名的社区构建版本可能会显示 Windows SmartScreen 警告。版本校验和列于
`SHA256SUMS.txt` 中每个版本旁边。

## 快速入门

1. 打开 STL。
2. 在“着色”(Shaded)、“密度”(Density)、“线框”(Wireframe) 或“顶点”(Vertices) 显示模式下查看它。
3. 选择质量级别、算法和目标三角形数量。
4. 选择 **Optimize**（优化）以计算结果。
5. 比较原始网格与优化后的网格，然后选择 **Apply**（应用）以提交该处理步骤。
6. 选择 **Save current state**（保存当前状态）或按 `Ctrl+S`。

MeshMill 绝不会仅仅因为文件或设置发生更改而自动开始优化。

## 功能特性

- 支持二进制和 ASCII 格式的 STL 输入，以及二进制 STL 输出
- Fast QEM 简化：保持密度平衡、形状及拓扑结构
- 支持着色、密度、线框和顶点显示模式
- 基于几何特征而非固定三角形数量上限的自动简化目标设定
- 支持多边形选择，包括多区域累加选择功能
- 仅针对选定区域进行裁剪、删除或优化操作
- 缓存原始、上一版本与当前版本的网格对比
- 支持对已确认的几何更改进行撤销与重做
- 显示尺寸偏差、简化百分比及预计输出大小
- 支持毫米、厘米、米、英寸和英尺显示单位
- CPU、内存、GPU 及几何体活动状态指标
- 当二进制 STL 超出预设内存限额时，加载受限概览视图
- 提供图形用户界面 (GUI) 和命令行应用程序
- 本地处理，无需账户、遥测、上传或云端依赖

![MeshMill 密度显示](../../images/meshmill-density.png)

## 视图控制

| 输入 | 操作 |
| --- | --- |
| 鼠标中键拖动 | 环绕旋转 |
| Shift + 鼠标中键拖动 | 平移 |
| 鼠标滚轮 | 向指针位置缩放 |
| Ctrl + 鼠标滚轮 | 顺时针或逆时针旋转 |
| 方向键 | 绕视图中心旋转 |
| Ctrl + 方向键 | 平移 |
| Ctrl + Shift + 上/下键 | 缩放 |
| Ctrl + Shift + 左/右|卷|
| `F1` / `F2` / `F3` / `F4` |阴影/密度/线框/顶点|
|鼠标右键按住|放大镜|
| Shift + 左键单击 |添加或删除标尺点 |
| Ctrl + 左键拖动|绘制选择多边形 |
| `Ctrl+C` |将多边形添加到保存的选择|
| `Ctrl+X` |裁剪至选区|
| `Ctrl+Space` |优化选型|
| `Delete` |删除选择|
| `Escape` |清除活动选择或标尺 |
| `Ctrl+Z` / `Ctrl+Y` |撤消/重做 |
| `Ctrl+S` |保存当前网格状态 |

标准视图键遵循六键导航块：

|关键|查看 | Ctrl + 键 |
| --- | --- | --- |
| `Insert` |左|将当前方向设置为 Left |
| `Home` |前|将当前方向设置为前|
| `Page Up` |对|将当前方向设置为 Right |
| `Delete` |没有选择时置顶 |将当前方向设置为顶部|
| `End` |返回 |将当前方向设置为“后退”|
| `Page Down` |底部|将当前方向设置为底部|

保存视图也会更新其相反的视图。左、右、前、后、上、下
保持配对。在确认对话框中，**保存**是默认操作，因此 Enter 保存
方向。正面显示在顶视图和底视图的顶部。

可以在“设置”中更改或重置快捷方式。

## 选择工作流程

按住 Ctrl 并左键拖动以绘制多边形。拖动角以重塑形状，左键单击边缘以添加
点，或右键单击一条边以删除一条边。添加更多带有 `Ctrl+C` 的区域。移动相机隐藏
屏幕空间多边形，同时保留选定的几何图形。

使用活动选择进行的优化仅影响该选择。结果仍是临时的
直到选择**应用**。 **取消** 放弃临时结果并保留选择，以便
可以尝试另一种配置。裁剪和删除操作成为正常的可撤消网格编辑。

## 大网格

在分配二进制文件 STL 之前，MeshMill 会将其估计工作内存与配置的内存进行比较
内存预算。超出预算的文件将作为有限的只读概述打开。概览报告
完整的源三角形计数，但禁用编辑和导出，因为它是一个示例，而不是完整的
对象。索引的、依赖于缩放的核外处理计划在
[docs/OUT_OF_CORE.md](docs/OUT_OF_CORE.md)。

## 命令行

`MeshMillCLI.exe` 包含在两个发行包中：

```powershell
.\MeshMillCLI.exe "C:\path\mesh.stl" --preset balanced
.\MeshMillCLI.exe "C:\path\mesh.stl" --target 150000 --output "C:\path\mesh-reduced.stl"
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm density --target 150000
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm topology --overwrite
```

运行 `.\MeshMillCLI.exe --help` 以获取所有选项。 MeshMill 拒绝覆盖其输入文件。

## 样品几何形状

开发示例有两个版本可用。样本是一个复合网格
冗余几何形状和不同密度的有意层。它为没有扫描仪的人们提供了
用于比较算法、检查密度、练习区域操作的真实夹具，
并开发路线图功能。 MeshMill不需要扫描输入。

|文件 |三角形|尺寸|交货|最适合 |
| --- | ---: | ---: | --- | --- |
| [`sample-scan.stl`](../../../samples/sample-scan.stl) | 249,999 | 249,999 11.9 MiB | 11.9 MiB普通 Git |快速评估、CI 和学习控制 |
| [`original-scan.stl`](../../../samples/original-scan.stl) | 4,126,315 | 4,126,315 196.8 MiB | Git LFS |测试密集源几何体和大网格性能 |

每个正常克隆都会下载较小的样本。未动过的原件是可选的，并且
通过 Git LFS 进行管理，因此它不会增加普通存储库历史记录。 GitHub 桌面包括
Git LFS。命令行用户可以安装 Git LFS 并运行：

```powershell
git lfs pull --include="samples/original-scan.stl"
```

标记版本还发布原始 STL 作为不使用 Git 的人的直接下载。
请参阅 [`samples/README.md`](../../../samples/README.md) 了解出处、尺寸和校验和。

算法贡献者还应该阅读
[算法测试指南](docs/ALGORITHM_TESTING.md) 比较或更改还原之前
行为。

## STL 单位

STL 不编码单元。更改模型单位会更改标签和测量值，而无需缩放
保存的坐标。选择描述源几何的单位。

## 隐私

MeshMill 读写本地文件。它不包含帐户、遥测、上传、广告或
云处理功能。当前的 GPU 指标实现使用本地 Windows 性能
柜台。计划为 Linux 和 macOS 提供等效的本机指标提供程序。

对于诊断故障排除，开发人员可以使用以下命令启动 GUI
`--diagnostic-log <local-file.jsonl>`。日志记录本地的输入路由和摄像头状态，
正常使用期间禁用。

## 开发与发布

- [贡献](CONTRIBUTING.md)
- [发布流程](RELEASING.md)
- [路线图](ROADMAP.md)
- [故障排除](docs/TROUBLESHOOTING.md)
- [第三方通知](THIRD_PARTY_NOTICES.md)

## 支持MeshMill

MeshMill是自主开发和维护的。阅读
[为什么支持这项工作很重要](SUPPORT.md)，或通过以下方式支持持续开发
[请我喝杯咖啡](https://buymeacoffee.com/tednv)。

MeshMill 根据 GNU 通用公共许可证版本 3 或更高版本获得许可。参见
[`LICENSE`]（许可证）。
