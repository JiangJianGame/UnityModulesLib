# UnityModulesLib (Unity 团队私有资源库与插件商店)

[![Unity](https://img.shields.io/badge/Unity-2018.4%2B-blue.svg?logo=unity)](https://unity.com/)
[![Backend](https://img.shields.io/badge/Backend-PocketBase%200.23%2B-rgb(180%2C90%2C240).svg)](https://pocketbase.io/)
[![Precompiled DLL](https://img.shields.io/badge/DLL-Ready-10b981.svg)](Build/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE.md)

**UnityModulesLib** 是一套专为 Unity 研发团队打造的高效、轻量、无感集成的私有化资源商店与模块管理解决方案。

彻底解决游戏团队内部各类开源/商业插件、自研通用模块资产零散分发、版本难以同步、临时文件冗余以及工程体积极易膨胀的痛点。支持**纯源码模式**与**独立预编译 DLL 模式**双轨运行。

---

## 🌟 核心特性

- 🚀 **0 本地冗余 · 即生即死导入架构**
  - 下载阶段采用全内存缓冲流传输，在系统临时目录生成毫秒级暂存包体。
  - 唤起 Unity 原生导入窗口后即刻挂载智能生命周期钩子，导入完毕或取消后立即物理粉碎临时包体，工程 Assets 目录 0 占位、0 冗余。
- 📦 **支持一键构建独立 DLL（零编译耗时 · 源码保护）**
  - 内置 `ModuleLibDllBuilder` 工具，一键将前端资源库编译为 `JiangJian.ModuleLib.Editor.dll`。
  - 接入项目的其他成员无需承担资源库源码的 Domain Reload 编译时间，同时保护源码逻辑不被意外修改。
  - 跨版本二进制安全设计，单个 DLL 无缝兼容 **Unity 2018.4 至 Unity 2022+ 及 Unity 6**。
- 🖼️ **官方高清多图画廊与智能去重体系**
  - **突出主题第一封面**：46 款收录插件均配备 16:9（800x450）高清主题大横幅或官方 Hero 海报，突出大号粗体标题与 Unity 兼容胶囊徽章。
  - **实机多图导轨**：支持 1~4 张真实实机截图/编辑器操作面板/性能对比图，带横向导轨无缝异步切换查看。
  - **智能感知去重**：同款或重复截图智能合并，杜绝冗余重复图。
- ⚡ **高性能双层缓存体系**
  - **内存缓存**：高频卡片与大图基于内存字典即时呈现，无任何卡顿。
  - **磁盘缓存**：采用安全哈希映射持久化于本地缓存目录，避免重复网络开销；窗口关闭时支持一键彻底清理。
- 📊 **真实统计与即时交互**
  - **浏览量**：点击卡片进入详情界面时实时自增，界面无感刷新并后台异步持久化入库。
  - **下载量**：点击「📥 导入到当前工程」时实时自增并异步上报。
  - 支持按「最新发布」、「最多下载」、「最多浏览」多维实时排序。
- 🔍 **多维检索与来源分离**
  - 支持 **模块库**（自研基础框架/工具）与 **插件库**（商业/第三方插件）双库一键切换。
  - 细分标签类型快速筛选（工具、视觉特效、3D、2D、动画、模板等），支持实时关键字模糊搜索。

---

## 🖥️ 前端资源库使用指南

### 1. 界面打开方式
- **快捷键**：`Ctrl + Shift + X`（macOS 上为 `Cmd + Shift + X`）
- **顶部菜单入口**：
  - 点击 Unity 菜单栏 **`Window` -> `资源库`**
  - 或点击 **`Tools` -> `资源库` -> `打开资源库窗口`**
- 窗口默认停靠在 Scene 场景视口面板（如同 Unity Asset Store 原生体验），支持自由拖拽与分屏停靠。

### 2. 资源浏览与多维筛选
- **顶部来源库切换**：在顶部工具栏点击「全部」、「模块库」（团队自研组件）、「插件库」（第三方商业工具）快速切库。
- **分类标签胶囊**：点击「工具」、「视觉特效」、「3D」、「2D」、「动画」等胶囊标签即时过滤。
- **实时搜索**：在搜索栏输入插件名称、作者或功能关键字，实时模糊过滤。
- **多维排序**：右上角下拉框支持按「最新发布」、「最多下载」、「最多浏览」即时排序。

### 3. 多图预览与功能详情
- 点击列表中的任意卡片进入**详细介绍面板**。
- **第一张封面**：突出展示该插件的主题名称、官方认证标识及 Unity 最低兼容版本（如 `Unity 2019.4+`）。
- **画廊切换**：主大图下方显示横向缩略图导轨，点击任意缩略图即可无缝切换查看实机界面、配置面板与效果演示图。
- **详细描述**：查阅该插件的使用文档、版本变更与功能特性。

### 4. 一键极速导入（即生即死安全流）
1. 在详情页中点击绿色主操作按钮 **「📥 导入到当前工程」**。
2. 系统将在后台全内存流式拉取包体，界面实时显示下载进度百分比。
3. 下载完成后自动弹出 Unity 原生的 Package 导入窗口，您可以自由勾选需要的文件。
4. 无论您点击「Import」完成导入还是点击「Cancel」取消，底层生命周期钩子都会**在第一时间自动粉碎并清理临时包体**，不留任何磁盘垃圾。

### 5. 自定义网络与服务器配置
- 点击窗口右上角齿轮图标 **⚙** 展开设置面板。
- 可随时更改服务端地址（例如部署在局域网服务器上的 `http://192.168.1.100:5050`）。
- 配置自动持久化保存于本地 `EditorPrefs`，团队换机或更新工程无需重复输入。

---

## 📦 独立 DLL 构建与分发指南

为了方便将资源管理器分发给团队其他项目使用，同时**杜绝源码带来的编译开销（Domain Reload）并保护核心代码**，本项目提供了全自动独立 DLL 构建工具。

### 1. 在 Unity 中一键构建 DLL
点击 Unity 顶部菜单：
- **`Tools` -> `资源库` -> `构建独立 DLL (Build DLL)`**
  - 自动调用原生 `AssemblyBuilder` 编译 8 个核心类文件。
  - 编译产物自动生成至工程根目录下的 `Build/JiangJian.ModuleLib/Editor/`。
  - 产物目录位于 `Assets/` 外，**彻底避免与当前工程内的 `.cs` 源码产生同名类冲突**。
- **`Tools` -> `资源库` -> `将已构建 DLL 打包为 .unitypackage`**
  - 自动将生成的 DLL 打包为标准的 `.unitypackage`，方便双击快速导入。

### 2. 构建产物结构
执行构建后，在根目录 `Build/` 下将生成如下完整交付物：
```
Build/
├── JiangJian.ModuleLib_v1.0.0.zip        # 完整独立分发压缩包
└── JiangJian.ModuleLib/
    └── Editor/
        ├── JiangJian.ModuleLib.Editor.dll      # 预编译独立类库 (仅限 Editor 平台)
        ├── JiangJian.ModuleLib.Editor.dll.meta # 自动预设的 Editor 平台隔离配置
        ├── JiangJian.ModuleLib.Editor.pdb      # 调试符号文件
        └── README.md                           # 独立接入说明
```

### 3. 在其他 Unity 工程中接入 DLL
1. **直接复制法**：
   将 `Build/JiangJian.ModuleLib/Editor/` 文件夹直接拷贝到目标 Unity 工程的任意 `Assets/` 或 `Plugins/` 目录下（例如 `Assets/Plugins/Editor/JiangJian.ModuleLib/`）。
2. **UnityPackage 导入法**：
   双击生成的 `JiangJian.ModuleLib_v1.0.0.unitypackage` 直接导入即可。
3. **即刻使用**：
   导入后无需等待任何源码编译，直接按下 `Ctrl+Shift+X` 即可弹出完整的资源库面板。

---

## 🛠️ 服务端架构与部署

本项目服务端基于现代化轻量级单文件后端 [PocketBase](https://pocketbase.io/) 构建，内存占用极低（< 30MB），支持万级并发与秒级响应。

### 1. 服务启动方式
- **批处理一键启动**：
  双击运行 `DataBase/start.bat`。
- **命令行启动**：
  ```bash
  cd DataBase
  pocketbase.exe serve --http="0.0.0.0:5050"
  ```

### 2. 管理后台访问
- **管理后台 URL**：`http://127.0.0.1:5050/_/`
- **默认管理员账号**：`admin@modules.local`
- **默认管理员密码**：`Admin12345678`

### 3. 数据表集合架构 (Collections)

| 集合名称 | 类型 | 说明 | 核心字段 |
| :--- | :--- | :--- | :--- |
| `models` | Base | 资源模块核心数据表 | `title`, `author`, `version`, `size`, `zip_file`, `preview_images`, `category`, `type`, `description`, `download_count`, `view_Count` |
| `categories` | Base | 来源分类库 | `name` (模块库 / 插件库) |
| `resource_types` | Base | 资源类型分类 | `name` (工具 / 视觉特效 / 3D / 2D / 模板 等) |
| `banners` | Base | 首页轮播推荐 | `model` (关联 models 记录) |

> 💡 **大文件上传支持**：服务端的 `models` 集合已动态配置 `zip_file.maxSize = 3GB`，全面支持千兆级巨型资源包（如大型海洋模拟、地形环境包）的流畅上传与高速分发。

---

## 📂 项目工程结构

```
UnityModulesLib/
├── Assets/
│   └── Editor/
│       ├── ModuleLib/                             # 前端核心业务源码
│       │   ├── Config/
│       │   │   └── ModuleLibConfig.cs             # 全局配置、服务器地址与快捷键定义
│       │   ├── Core/                              # 核心数据模型与非阻塞网络层
│       │   │   ├── ModuleLibData.cs               # 强类型 DTO 实体与统计自增上报方法
│       │   │   ├── ModuleLibHttp.cs               # 跨版本安全异步 HTTP 通信（Unity 2018~6 兼容）
│       │   │   └── ModuleLibCache.cs              # 双层缓存管理与临时包体清理安全防护
│       │   ├── UI/                                # IMGUI 高颜值界面与交互组件
│       │   │   ├── ModuleLibWindow.cs             # 主窗口框架、顶部导航与视图路由
│       │   │   ├── ModuleLibListView.cs           # 卡片瀑布流列表、搜索与类型筛选栏
│       │   │   ├── ModuleLibDetailView.cs         # 资源详情页、多图导轨与即生即死导入流
│       │   │   └── ModuleLibStyles.cs             # 暗色主题样式表、自定义按钮与徽标排版
│       │   └── Test/                              # 测试用例与自动化验证脚本
│       │       └── ModuleLibTest.cs
│       └── ModuleLibBuilder/                      # 独立预编译类库构建工具
│           └── ModuleLibDllBuilder.cs             # 一键构建独立 DLL 与发布包工具
├── Build/                                         # 预编译发布产物目录 (受 .gitignore 保护)
│   ├── JiangJian.ModuleLib_v1.0.0.zip             # 独立分发压缩包
│   └── JiangJian.ModuleLib/Editor/                # 可直接拷入任何项目的纯 DLL 模块
│       ├── JiangJian.ModuleLib.Editor.dll
│       ├── JiangJian.ModuleLib.Editor.dll.meta
│       ├── JiangJian.ModuleLib.Editor.pdb
│       └── README.md
├── DataBase/                                      # 服务端数据与管理运维脚本
│   ├── pb_data/                                   # PocketBase 嵌入式 SQLite 数据文件与存储桶
│   ├── pb_migrations/                             # 数据库版本迁移定义 (Schema Migrations)
│   ├── pocketbase.exe                             # PocketBase 服务端引擎
│   ├── start.bat                                  # 快捷启动服务脚本
│   ├── optimize_previews.py                       # 主题大横幅渲染、画廊去重与数据库同步管线
│   ├── theme_configs.py                           # 14 款核心工具主题设计参数与文案定义
│   ├── verify_all_clean.py                        # 全库感知哈希与画廊质量校验工具
│   ├── sync_official_covers.py                    # 官方封面同步脚本
│   ├── sync_multi_previews.py                     # 多图画廊数据抓取与同步脚本
│   ├── reset_counts.py                            # 统计数据一键归零重置脚本
│   └── upload_plugins.py                          # 资源包全量扫描入库同步脚本
├── README.md                                      # 项目完整架构说明文档
└── LICENSE.md                                     # 授权协议
```

---

## 🔧 运维与常见操作

### 1. 批量重置统计数据
如需将所有线上资源的查看次数与下载量重置为 0，直接运行：
```bash
python DataBase/reset_counts.py
```

### 2. 自动化画廊优化与去重同步
如需重新生成 14 款工具主题大横幅、对全库所有预览图进行智能去重并同步到 PocketBase：
```bash
python DataBase/optimize_previews.py
```

### 3. 全库画廊完整度校验
校验 46 款插件是否存在任何重复预览图或异常封面：
```bash
python DataBase/verify_all_clean.py
```

---

## 📜 规范与约定
- **代码命名空间**：统一规范在 `JiangJian` 命名空间下。
- **全版本兼顾**：全套源码与预编译 DLL 严格兼容 **Unity 2018.4+** 至 **Unity 2022+** 及 **Unity 6**。
- **零外部侵入**：编辑器功能纯放在 `Editor` 目录下，不打包进最终 Runtime 构建。
- **无感体验**：除导入到当前工程的具体资产外，资源商店本身不在 Unity 项目目录内堆积任何缓存。
