# UnityModulesLib (Unity 团队私有资源库与插件商店)

[![Unity](https://img.shields.io/badge/Unity-2018.4%2B-blue.svg?logo=unity)](https://unity.com/)
[![Backend](https://img.shields.io/badge/Backend-PocketBase%200.23%2B-rgb(180%2C90%2C240).svg)](https://pocketbase.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE.md)

**UnityModulesLib** 是一套专为 Unity 研发团队打造的高效、轻量、无感集成的私有化资源商店与模块管理解决方案。

彻底解决游戏团队内部各类开源/商业插件、通用模块资产零散分发、版本难以同步、临时文件冗余以及工程体积极易膨胀的痛点。

---

## 🌟 核心特性

- 🚀 **0 本地冗余 · 即生即死导入架构**
  - 下载阶段采用全内存缓冲流传输，在系统临时目录生成毫秒级暂存包体。
  - 唤起 Unity 原生导入窗口后即刻挂载智能生命周期钩子，导入完毕或取消后立即物理粉碎临时包体，工程 Assets 目录 0 占位、0 冗余。
- ⚡ **高性能双层缓存体系**
  - **内存缓存**：高频卡片与大图基于内存字典即时呈现，无任何卡顿。
  - **磁盘缓存**：采用安全哈希映射持久化于本地缓存目录，避免重复网络开销；窗口关闭时支持一键彻底清理。
- 📊 **真实统计与即时交互**
  - **浏览量**：点击卡片进入详情界面时实时自增，界面无感刷新并后台异步持久化入库。
  - **下载量**：点击「📥 导入到当前工程」时实时自增并异步上报。
  - 支持按「最新发布」、「最多下载」、「最多浏览」多维实时排序。
- 🎨 **经典商业级卡片封面系统**
  - 深度定制的 16:9 商业级封面视觉规范，覆盖系统工具、着色特效、自然环境、动画物理等多种调色体系。
  - 清晰标注各插件支持的 **最低 Unity 版本徽标**（如 `Unity 2018.4+`、`Unity 2021.3+`）。
- 🔍 **多维检索与来源分离**
  - 支持 **模块库**（自研基础框架/工具）与 **插件库**（商业/第三方插件）来源切换。
  - 细分标签类型快速筛选（工具、视觉特效、3D、2D、动画、模板等），支持实时关键字模糊搜索。
- 🛡️ **超强全版本兼容**
  - 底层基于 `EditorApplication.update` 驱动非阻塞 HTTP 异步管线，全量兼容 **Unity 2018.4 至 Unity 2022+** 所有 LTS 版本。

---

## 🖥️ 客户端使用指南

### 1. 打开资源库界面
- **快捷键**：`Ctrl + Shift + X`
- **菜单入口**：点击 Unity 顶部菜单栏 **`Window` -> `资源库`**

### 2. 浏览与检索
- **顶部来源切换**：点击标签可在「全部」、「模块库」、「插件库」之间自由切换。
- **类型过滤条**：点击类型胶囊（如「工具」、「视觉特效」）即时筛选子类别。
- **实时搜索**：输入关键字即时过滤插件名称与作者信息。
- **排序切换**：右上角下拉框可按「最新发布」、「最多下载」、「最多浏览」自由排列。

### 3. 一键导入
1. 在列表中点击任意资源卡片进入详细介绍页。
2. 查阅插件功能介绍、核心特性与适用的 Unity 版本。
3. 点击绿色主操作按钮 **「📥 导入到当前工程」**。
4. 系统将自动拉取包体并在完成后弹出 Unity 官方的导入选择窗口（可自由勾选需要的文件）。

### 4. 自定义服务器配置
- 点击窗口右上角齿轮图标 ⚙ 打开设置面板。
- 可配置局域网或内网服务器地址（例如：`http://192.168.1.100:5050`），配置持久保存在 `EditorPrefs` 中。

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
│       └── ModuleLib/
│           ├── Core/                      # 核心数据模型与非阻塞网络层
│           │   ├── ModuleLibConfig.cs     # 全局配置、服务器地址与快捷键定义
│           │   ├── ModuleLibData.cs       # 强类型 DTO 实体与自增上报方法
│           │   ├── ModuleLibHttp.cs       # 基于 UnityWebRequest 的异步通信封装
│           │   └── ModuleLibCache.cs      # 双层缓存管理与临时包体清理安全防护
│           ├── UI/                        # IMGUI 高颜值界面与交互组件
│           │   ├── ModuleLibWindow.cs     # 主窗口框架、顶部导航与视图路由
│           │   ├── ModuleLibListView.cs   # 卡片瀑布流列表、搜索与类型筛选栏
│           │   ├── ModuleLibDetailView.cs # 资源详情页、轮播图与即生即死导入流
│           │   └── ModuleLibStyles.cs     # 暗色主题样式表、自定义按钮与徽标排版
│           └── Test/                      # 测试用例与自动化验证脚本
│               └── ModuleLibTest.cs
├── DataBase/                              # 服务端数据与管理运维脚本
│   ├── pb_data/                           # PocketBase 嵌入式 SQLite 数据文件与存储桶
│   ├── pb_migrations/                     # 数据库版本迁移定义 (Schema Migrations)
│   ├── pocketbase.exe                     # PocketBase 服务端引擎
│   ├── start.bat                          # 快捷启动服务脚本
│   ├── cover_engine.py                    # 经典商业级卡片封面生成渲染引擎
│   ├── batch_update_covers.py             # 批量封面重绘与更新脚本
│   ├── reset_counts.py                    # 统计数据一键归零重置脚本
│   └── upload_plugins.py                  # 资源包全量扫描入库同步脚本
├── README.md                              # 项目完整架构说明文档
└── LICENSE.md                             # 授权协议
```

---

## 🔧 运维与常见操作

### 1. 批量重置统计数据
如需将所有线上资源的查看次数与下载量重置为 0，直接运行：
```bash
python DataBase/reset_counts.py
```

### 2. 批量重新渲染卡片封面
如果调整了视觉规范或新增了插件类型，可一键执行：
```bash
python DataBase/batch_update_covers.py
```

---

## 📜 规范与约定
- **代码命名空间**：统一规范在 `JiangJian` 命名空间下。
- **零外部侵入**：编辑器功能纯放在 `Editor` 目录下，不打包进最终 Runtime 构建。
- **无感体验**：除导入到当前工程的具体资产外，资源商店本身不在 Unity 项目目录内堆积任何缓存。
