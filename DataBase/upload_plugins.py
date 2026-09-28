import os, sys, json, time, random, requests
from PIL import Image, ImageDraw, ImageFont

# Set UTF-8 encoding for stdout
sys.stdout.reconfigure(encoding='utf-8')

SERVER_URL = 'http://127.0.0.1:5050'
SUPERUSER_EMAIL = 'admin@modules.local'
SUPERUSER_PASS = 'Admin12345678'
PLUGINS_DIR = r'D:\Unity资源库\插件'
SCRATCH_DIR = r'D:\UnityItems\UnityModulesLib\DataBase\scratch_previews'
os.makedirs(SCRATCH_DIR, exist_ok=True)

# Type mapping in PocketBase
TYPE_TOOL = 'jwyndor0xf0tte6'   # 工具
TYPE_VFX  = '0jc7gp3927n7dbw'   # 视觉特效
TYPE_3D   = 'hfszdiyl93h67al'   # 3D
TYPE_2D   = 'kub956d03mfmog5'   # 2D
TYPE_TMPL = 'wz2befxskf1nyml'   # 模板
TYPE_AUD  = 'e2go6ejmwfq0qe6'   # 音频

CATEGORY_PLUGIN = 'gei2blqbraoocsv' # 插件库

# Colors for card badges
TYPE_COLORS = {
    TYPE_TOOL: (59, 130, 246),   # Blue
    TYPE_VFX:  (168, 85, 247),  # Purple
    TYPE_3D:   (249, 115, 22),  # Orange
    TYPE_2D:   (236, 72, 153),  # Pink
    TYPE_TMPL: (20, 184, 166),  # Teal
    TYPE_AUD:  (234, 179, 8),   # Yellow
}

TYPE_NAMES = {
    TYPE_TOOL: '工具',
    TYPE_VFX:  '视觉特效',
    TYPE_3D:   '3D',
    TYPE_2D:   '2D',
    TYPE_TMPL: '模板',
    TYPE_AUD:  '音频'
}

PLUGINS_CONFIG = [
    {
        'file': 'AVProVideo1.9.14.unitypackage',
        'title': 'AVPro Video (Unity 2018.4+)',
        'type': TYPE_TOOL,
        'author': 'RenderHeads Ltd',
        'version': '1.9.14',
        'unity': 'Unity 2018.4+',
        'desc': '''### 插件概述
AVPro Video 是 Unity 生态最强悍的专业视频播放插件，全面支持 Windows、macOS、Android、iOS、WebGL 与 VR 设备。

> 💡 **支持的 Unity 版本**：`Unity 2018.4+`

### 核心特性
- 🚀 **极速硬件解码**：支持最高 4K/8K 60fps 硬件加速播放与 360/180 度立体全景视频。
- 🌐 **流媒体支持**：原生支持 HLS、DASH、HTTP/HTTPS 流媒体协议与自适应比特率。
- 🎨 **丰富渲染通道**：支持输出到 UGUI、MeshRenderer、天空盒与自定义 Shader 材质球。
'''
    },
    {
        'file': 'Best HTTP 3.0.8.unitypackage',
        'title': 'Best HTTP v3 (Unity 2021.3+)',
        'type': TYPE_TOOL,
        'author': 'Tivadar',
        'version': '3.0.8',
        'unity': 'Unity 2021.3+',
        'desc': '''### 插件概述
Best HTTP v3 是全功能的高性能网络通信引擎，专为对网络延迟与数据吞吐有苛刻要求的商业游戏设计。

> 💡 **支持的 Unity 版本**：`Unity 2021.3+`

### 核心特性
- ⚡ **全协议覆盖**：原生实现 HTTP/1.1、HTTP/2、WebSocket、WebTransport 与 Socket.IO。
- 🔒 **现代安全加密**：内置升级版 Bouncy Castle TLS 1.3 引擎，摆脱系统自带证书限制。
- 📦 **断点续传与缓存**：内置先进的本地缓存管理与流式上传/下载支持。
'''
    },
    {
        'file': 'Build Report v5.3.1.unitypackage',
        'title': 'Build Report Tool (Unity 2018.4+)',
        'type': TYPE_TOOL,
        'author': 'Anomalous Underdog',
        'version': '5.3.1',
        'unity': 'Unity 2018.4+',
        'desc': '''### 插件概述
Build Report Tool 是 Unity 官方生态首屈一指的包体分析与减肥利器，精准分析构建后各资源体积占比。

> 💡 **支持的 Unity 版本**：`Unity 2018.4+`

### 核心特性
- 📊 **体积透视**：直观展示纹理、网格、音频、预制体和脚本编译产物的压缩与未压缩大小。
- 🔍 **冗余排查**：迅速找出因错误依赖打入安装包的闲置测试资源。
- ⚡ **无感融入**：打包完成后自动生成可视化报表，调优体验流畅高效。
'''
    },
    {
        'file': 'CalmWater.unitypackage',
        'title': 'Calm Water (Unity 2018.4+)',
        'type': TYPE_VFX,
        'author': 'Occasoftware',
        'version': '1.5.0',
        'unity': 'Unity 2018.4+',
        'desc': '''### 插件概述
Calm Water 是一套极其轻量、高颜值的清澈水体与水面着色器解决方案，适合湖泊、池塘与河流。

> 💡 **支持的 Unity 版本**：`Unity 2018.4+`

### 核心特性
- 💎 **清澈折射与焦散**：真实模拟光线在浅水中的动态焦散和折射失真。
- 🌊 **物理法线微浪**：内置多层平滑流动的波纹法线动画与边缘泡沫。
- 📱 **极佳移动端性能**：低 ALU 指令数，在手机与低配设备上稳定保持 60 帧。
'''
    },
    {
        'file': 'ChineseInputWebGL2018.4.16.unitypackage',
        'title': 'ChineseInput WebGL (Unity 2018.4+)',
        'type': TYPE_TOOL,
        'author': 'Liang Hur',
        'version': '2018.4.16',
        'unity': 'Unity 2018.4+',
        'desc': '''### 插件概述
专为 Unity WebGL 项目解决无法直接在网页中调出中文输入法打字这一核心痛点的桥接补丁。

> 💡 **支持的 Unity 版本**：`Unity 2018.4+`

### 核心特性
- ⌨️ **原生体验**：打字时直接调用系统输入法选词，并实时映射到 UGUI InputField。
- 🎯 **开箱即用**：挂载即生效，支持复制、粘贴、光标选区与回车确认。
- 🌐 **全浏览器兼容**：完美适配 Chrome、Edge、Safari 与各类移动端浏览器。
'''
    },
    {
        'file': 'Crest Water 4 URP v4.23.0.unitypackage',
        'title': 'Crest Ocean System URP (Unity 2021.3+)',
        'type': TYPE_VFX,
        'author': 'Waveharmonic',
        'version': '4.23.0',
        'unity': 'Unity 2021.3+',
        'desc': '''### 插件概述
Crest Ocean System 是代表 Unity 水体最高工业标准的动力学海洋系统，专为 URP 管线深度优化。

> 💡 **支持的 Unity 版本**：`Unity 2021.3+`

### 核心特性
- 🌊 **次时代波浪动力学**：基于 FFT 与浅水波动方程，真实呈现大洋风暴、碎浪与浅滩浪花。
- 🚢 **精准刚体浮力**：提供高性能浮力采样物理接口，支持船只、漂浮物与海浪实时互动。
- 🤿 **水下沉浸效果**：镜头入水无缝过渡，包含水下浑浊度、丁达尔光线步进与焦散投影。
'''
    },
    {
        'file': 'DOTween v1.0.unitypackage',
        'title': 'DOTween (Unity 2018.4+)',
        'type': TYPE_TOOL,
        'author': 'Demigiant',
        'version': '1.0.0',
        'unity': 'Unity 2018.4+',
        'desc': '''### 插件概述
DOTween 是 Unity 开发必备的高性能补间动画引擎，零 GC 分配，让一切动画与状态过渡丝滑流畅。

> 💡 **支持的 Unity 版本**：`Unity 2018.4+`

### 核心特性
- ⚡ **极限性能**：底层采用高效对象池与强类型运算，即使每帧驱动数万个 Tween 也几乎零开销。
- 🛠️ **优雅链式 API**：支持 `transform.DOMove().SetEase().OnComplete()` 简洁连贯书写。
- 🎬 **强大序列编排**：轻松实现延迟、循环、倒放以及复杂的 UI/转场动画。
'''
    },
    {
        'file': 'Destructible 2D v4.2.0.unitypackage',
        'title': 'Destructible 2D (Unity 2019.4+)',
        'type': TYPE_2D,
        'author': 'Carlos Wilkes',
        'version': '4.2.0',
        'unity': 'Unity 2019.4+',
        'desc': '''### 插件概述
Destructible 2D 让任何 2D 精灵或地形瞬间拥有任意角度切割、爆炸破碎与物理碰撞动态分离能力。

> 💡 **支持的 Unity 版本**：`Unity 2019.4+`

### 核心特性
- 💥 **像素级实时切割**：支持激光射线切断、圆形爆炸坑洞与多边形雕刻。
- 🧩 **碰撞体自动重构**：切割后自动拆分为独立刚体小碎片并实时更新 2D 碰撞体。
- 🎮 **经典玩法支撑**：百战天虫式地形破坏、水果忍者式切割效果开箱即成。
'''
    },
    {
        'file': 'Dialogue System for Unity v2.2.39.unitypackage',
        'title': 'Dialogue System for Unity v2.2.39 (Unity 2019.4+)',
        'type': TYPE_TOOL,
        'author': 'Pixel Crushers',
        'version': '2.2.39',
        'unity': 'Unity 2019.4+',
        'desc': '''### 插件概述
全球无数著名独立与商业 RPG 游戏背后的专业对话、任务与世界状态控制中枢。

> 💡 **支持的 Unity 版本**：`Unity 2019.4+`

### 核心特性
- 💬 **可视化节点编辑器**：树状展开对话分支、条件分支、变量运算与音画演出触发。
- 📜 **全套任务日志系统**：支持任务接取、追踪进度、完成状态与奖励结算。
- 🌍 **国际化本地化**：无缝对接 CSV、Excel 及主流本地化插件，多语言切换瞬间生效。
'''
    },
    {
        'file': 'Dialogue System for Unity v2.2.48.unitypackage',
        'title': 'Dialogue System for Unity v2.2.48 (Unity 2020.3+)',
        'type': TYPE_TOOL,
        'author': 'Pixel Crushers',
        'version': '2.2.48',
        'unity': 'Unity 2020.3+',
        'desc': '''### 插件概述
Dialogue System 的升级演进版本，针对 Unity 2020 LTS 及更高版本进行了全方位兼容与架构升级。

> 💡 **支持的 Unity 版本**：`Unity 2020.3+`

### 核心特性
- 🎮 **现代化输入体系**：原生适配 Unity New Input System 与 UI Toolkit。
- 🎬 **Cinemachine 协同**：内置 Cinemachine 虚拟相机特写切换与 Timeline 轨道无缝联动。
- 💾 **多槽位持久化存储**：与 Easy Save 等主流存储方案一键对接。
'''
    },
    {
        'file': 'EasySave v3.56.unitypackage',
        'title': 'Easy Save 3 (Unity 2018.4+)',
        'type': TYPE_TOOL,
        'author': 'Moodkie',
        'version': '3.5.6',
        'unity': 'Unity 2018.4+',
        'desc': '''### 插件概述
Easy Save 3 是 Unity 生态最信赖的数据存储、自动存档与加密序列化解决方案。

> 💡 **支持的 Unity 版本**：`Unity 2018.4+`

### 核心特性
- 💾 **一行代码存取**：`ES3.Save("key", data)` 与 `ES3.Load<T>("key")` 即可完成复杂结构持久化。
- 🔒 **强力安全防护**：内置 AES-128 加密与 Gzip 压缩，防止玩家篡改本地存档数据。
- 🌐 **全平台支持**：支持 PC、手机端沙盒路径以及自动通过 Web 服务器远程同步存档。
'''
    },
    {
        'file': 'Enviro - Sky and Weather_639202403010021042.unitypackage',
        'title': 'Enviro Sky and Weather (Unity 2019.4+)',
        'type': TYPE_VFX,
        'author': 'Hendrik-Mikeska',
        'version': '2.4.2',
        'unity': 'Unity 2019.4+',
        'desc': '''### 插件概述
Enviro 是 Unity 经典的天空与气象系统，集成了完整的 24 小时昼夜循环与气候系统。

> 💡 **支持的 Unity 版本**：`Unity 2019.4+`

### 核心特性
- ☀️ **天文级别日月天体**：真实模拟日落日出漫射、月相周期演变与夜空银河星群。
- 🌧️ **动态天气生态**：涵盖晴空、多云、暴雨、暴雪、雷阵雨与浓雾气象切换。
- 🌿 **季节与植被变换**：支持春生夏茂、秋叶凋零、冬季积雪覆盖着色。
'''
    },
    {
        'file': 'Enviro 3 - Sky and Weather v3.0.0.unitypackage',
        'title': 'Enviro 3 (Unity 2021.3+)',
        'type': TYPE_VFX,
        'author': 'Hendrik-Mikeska',
        'version': '3.0.0',
        'unity': 'Unity 2021.3+',
        'desc': '''### 插件概述
全新一代 Enviro 3 天气引擎，彻底面向现代 URP 与 HDRP 渲染管线进行底层重构。

> 💡 **支持的 Unity 版本**：`Unity 2021.3+`

### 核心特性
- ☁️ **高精立体体积云**：基于体积光线步进技术，云层厚度、光照穿透与云影投射极为震撼。
- ⚡ **模块化架构**：天气、光照、环境音效、体积雾完全解耦，性能与可定制性倍增。
- 🛠️ **一键配置向导**：极简的新版 Inspector 调试面板，快速调出影视级自然环境。
'''
    },
    {
        'file': 'Final IK 1.7.unitypackage',
        'title': 'Final IK (Unity 2018.4+)',
        'type': TYPE_3D,
        'author': 'RootMotion',
        'version': '1.7.0',
        'unity': 'Unity 2018.4+',
        'desc': '''### 插件概述
Final IK 是 Unity 动作游戏与 VR 开发中必不可少的逆向运动学（IK）黄金标准插件。

> 💡 **支持的 Unity 版本**：`Unity 2018.4+`

### 核心特性
- 🧍 **全身两足解算 (Full Body Biped)**：角色四肢与躯干完美贴合斜坡地形、搬运重物与互动。
- 🎯 **瞄准与注视 (Aim & LookAt)**：武器准星自动校准与角色头部自适应视线跟随。
- 🤿 **VRIK 模块**：VR 玩家头显与手柄驱动全身骨骼的标准工业级算法。
'''
    },
    {
        'file': 'Find_Reference_2_2.4.3.unitypackage',
        'title': 'Find Reference 2 (Unity 2018.4+)',
        'type': TYPE_TOOL,
        'author': 'GuDao',
        'version': '2.4.3',
        'unity': 'Unity 2018.4+',
        'desc': '''### 插件概述
Find Reference 2 是大型项目团队必备的资源依赖关系梳理神器，毫秒级定位所有直接与间接引用。

> 💡 **支持的 Unity 版本**：`Unity 2018.4+`

### 核心特性
- ⚡ **闪电索引**：建立全工程资产依赖缓存，秒查任意 Prefab、材质、贴图被谁引用。
- 🧹 **无引用资产扫描**：快速清理工程废弃资产，包体与工程体积立竿见影缩减。
- 🔄 **依赖关系树可视化**：层级展开引用树，清晰排查复杂的循环依赖链。
'''
    },
    {
        'file': 'Graphy_v3.0.5.unitypackage',
        'title': 'Graphy (Unity 2019.4+)',
        'type': TYPE_TOOL,
        'author': 'Tayx',
        'version': '3.0.5',
        'unity': 'Unity 2019.4+',
        'desc': '''### 插件概述
Graphy 是专为 Unity 开发者打造的终极 FPS、内存与音频性能实时监测分析仪表盘。

> 💡 **支持的 Unity 版本**：`Unity 2019.4+`

### 核心特性
- 📈 **帧率与帧耗时波动**：清晰展示当前 FPS、平均 FPS、最低 FPS 与毫秒级帧耗曲线。
- 🧠 **内存深度监控**：实时展示 Mono 堆分配、预留堆内存以及系统物理内存消耗。
- 🎨 **高度可定制 HUD**：支持自由调整显示位置、配色主题、紧凑度与透明度。
'''
    },
    {
        'file': 'Gravity Engine v13.0.unitypackage',
        'title': 'Gravity Engine (Unity 2019.4+)',
        'type': TYPE_TOOL,
        'author': 'N-Body Physics',
        'version': '13.0.0',
        'unity': 'Unity 2019.4+',
        'desc': '''### 插件概述
专业级 N体引力与天体轨道运动物理仿真引擎，适用于太空探索、星际穿越与引力弹弓游戏。

> 💡 **支持的 Unity 版本**：`Unity 2019.4+`

### 核心特性
- 🪐 **真实开普勒轨道**：支持标准圆轨道、椭圆轨道、抛物线逃逸与双曲线轨道计算。
- 🛰️ **轨道转移与机动**：内置霍曼转移轨道、变轨推力模拟与实时轨道预测红线。
- 🚀 **N体引力摄动**：支持海量天体相互引力牵引仿真，数值稳定精确。
'''
    },
    {
        'file': 'Heavy Sword Animation v1.8.unitypackage',
        'title': 'Heavy Sword Animation (Unity 2018.4+)',
        'type': TYPE_3D,
        'author': 'WetCat Studio',
        'version': '1.8.0',
        'unity': 'Unity 2018.4+',
        'desc': '''### 插件概述
高品质双手大剑与重剑近战动作姿态资产包，打击感扎实厚重，适合魂类及动作 RPG。

> 💡 **支持的 Unity 版本**：`Unity 2018.4+`

### 核心特性
- ⚔️ **全套战斗套件**：涵盖待机、跑动、冲刺斩、三段蓄力重斩、跳劈与旋风斩。
- 🤸 **受击与防御反应**：包含格挡反击、大受击硬直、击飞倒地与起身循环。
- 🎯 **标准人形骨骼**：采用 Unity Humanoid 标准骨骼重定向，各类模型一键套用。
'''
    },
    {
        'file': 'HighlightPlus_URP_Pipeline.unitypackage',
        'title': 'Highlight Plus URP (Unity 2020.3+)',
        'type': TYPE_VFX,
        'author': 'Kronnect',
        'version': '7.0.0',
        'unity': 'Unity 2020.3+',
        'desc': '''### 插件概述
Highlight Plus URP 为 URP 渲染管线带来功能最全面、定制最自由的物体描边与高亮特效。

> 💡 **支持的 Unity 版本**：`Unity 2020.3+`

### 核心特性
- ✨ **丰富轮廓风格**：外轮廓光晕、纯色硬边、内发光脉冲与全息扫描线动画。
- 👁️ **障碍物遮挡透视**：物体被墙壁遮挡时自动显示 X-Ray 透视轮廓与专属半透明遮挡色。
- 🎯 **极低性能损耗**：采用 Render Feature 深度优化，多物体同时高亮毫不掉帧。
'''
    },
    {
        'file': 'Highlighting+System 5.0.unitypackage',
        'title': 'Highlighting System (Unity 2018.4+)',
        'type': TYPE_VFX,
        'author': 'Chromatix',
        'version': '5.0.0',
        'unity': 'Unity 2018.4+',
        'desc': '''### 插件概述
经典款内置管线轮廓高亮插件，在 Unity 早期项目中被广泛使用，轻巧耐用。

> 💡 **支持的 Unity 版本**：`Unity 2018.4+`

### 核心特性
- 💡 **即插即用**：挂载单一脚本即可实现鼠标悬停变色与呼吸灯发光反馈。
- 🎨 **多色彩层级**：支持为不同阵营、品质（如普通、稀有、史诗）物品赋予独立发光色。
- 📱 **老版本极佳兼容**：在 Unity 2018/2019 内置渲染管线项目中表现稳定。
'''
    },
    {
        'file': 'InGameDebugConsole.unitypackage',
        'title': 'In-Game Debug Console (Unity 2018.4+)',
        'type': TYPE_TOOL,
        'author': 'Yasirkula',
        'version': '1.5.0',
        'unity': 'Unity 2018.4+',
        'desc': '''### 插件概述
在打包后的游戏真机内部随时呼出半透明控制台，实时查看 Debug.Log 并执行命令。

> 💡 **支持的 Unity 版本**：`Unity 2018.4+`

### 核心特性
- 📱 **多指滑动手势**：四指点击屏幕即可瞬间唤出或隐藏控制台窗口。
- ⌨️ **自定义指令执行**：使用 `[ConsoleMethod]` 属性一键将 C# 函数注册为控制台可调用指令。
- 🔍 **搜索与堆栈追溯**：支持关键词过滤 Log、Warning、Error，并查看完备的堆栈轨迹。
'''
    },
    {
        'file': 'Liquid Volume Pro 2 v11.1.7.unitypackage',
        'title': 'Liquid Volume Pro 2 (Unity 2021.3+)',
        'type': TYPE_VFX,
        'author': 'Kronnect',
        'version': '11.1.7',
        'unity': 'Unity 2021.3+',
        'desc': '''### 插件概述
在任意 3D 网格容器内逼真渲染流体药水与液面动态交互的次时代着色器系统。

> 💡 **支持的 Unity 版本**：`Unity 2021.3+`

### 核心特性
- 🧪 **物理晃动仿真**：容器倾斜、移动或加速时，液面自动呈现真实惯性晃荡。
- 🫧 **多层流体特性**：支持浮层泡沫、浑浊沉淀物、内部浮游微粒与发光液体。
- 📦 **非凸多边形支持**：完美支持烧瓶、试管、酒杯、异形魔法球等各类容器。
'''
    },
    {
        'file': 'Liquid Volume Pro v1.5.1.unitypackage',
        'title': 'Liquid Volume Pro (Unity 2018.4+)',
        'type': TYPE_VFX,
        'author': 'Kronnect',
        'version': '1.5.1',
        'unity': 'Unity 2018.4+',
        'desc': '''### 插件概述
Liquid Volume 系列的经典稳定版本，兼容 Unity 早期版本与各主流渲染管线。

> 💡 **支持的 Unity 版本**：`Unity 2018.4+`

### 核心特性
- 💧 **开箱即用药水预设**：内置红药水、毒药水、魔力水、黄金熔岩等多款材质球。
- ⚡ **简明易用 API**：几行代码即可实现药水饮用后液面逐渐下降与空杯过渡。
- 🎮 **低配硬件友好**：低复杂度着色器算法，移动端设备流畅运行。
'''
    },
    {
        'file': 'Magica Cloth 2 v2.14.2.unitypackage',
        'title': 'Magica Cloth 2 (Unity 2021.3+)',
        'type': TYPE_TOOL,
        'author': 'Magica Soft',
        'version': '2.14.2',
        'unity': 'Unity 2021.3+',
        'desc': '''### 插件概述
采用 Unity DOTS (Burst Compiler + Job System) 构建的高性能角色布料、长发与摇摇物理。

> 💡 **支持的 Unity 版本**：`Unity 2021.3+`

### 核心特性
- 🚀 **极度榨干多核性能**：采用全多线程并行解算，同屏数十个角色满身物理仍保持高帧率。
- 👗 **骨骼与网格布料**：同时支持基于骨骼链的物理带动与基于网格顶点的柔性布料解算。
- 🛡️ **强大碰撞体穿透防护**：支持胶囊体、平面与球体碰撞，彻底杜绝头发或裙子穿模穿身。
'''
    },
    {
        'file': 'MessagePack.unitypackage',
        'title': 'MessagePack C# (Unity 2019.4+)',
        'type': TYPE_TOOL,
        'author': 'Cysharp',
        'version': '2.4.0',
        'unity': 'Unity 2019.4+',
        'desc': '''### 插件概述
极端追求解析性能与低带宽占用的二进制序列化协议，比 JSON 小数倍、快数十倍。

> 💡 **支持的 Unity 版本**：`Unity 2019.4+`

### 核心特性
- 🏎️ **微秒级封包**：针对 Unity IL2CPP 提供原生 AOT 代码生成器，杜绝运行时反射卡顿。
- 📦 **体积极其紧凑**：序列化后体积与 Protobuf 旗鼓相当，大幅减少网络传输带宽消耗。
- 🔄 **强兼容扩展**：支持继承多态、键值映射与灵活的自定义 Formatter 序列化器。
'''
    },
    {
        'file': 'MicroVerse - Roads v1.7.27.unitypackage',
        'title': 'MicroVerse - Roads (Unity 2021.3+)',
        'type': TYPE_TOOL,
        'author': 'Jason Booth',
        'version': '1.7.27',
        'unity': 'Unity 2021.3+',
        'desc': '''### 插件概述
非破坏性程序化道路、交叉路口与地形路径生成系统，改变传统繁琐的地形雕刻方式。

> 💡 **支持的 Unity 版本**：`Unity 2021.3+`

### 核心特性
- 🛣️ **样条线自由铺设**：沿曲线拖拽即可自动生成公路、林间泥路、桥梁与护栏。
- ⛰️ **地形无损动态融合**：道路会自动开凿山体或填平凹地，删除道路地形立刻自动恢复原样。
- 🌿 **植被自动剔除**：道路覆盖区域内的树木、草地与小石头自动被剔除，无需手动刷除。
'''
    },
    {
        'file': 'Newtonsoft 9.0.1.unitypackage',
        'title': 'Newtonsoft Json.NET (Unity 2018.4+)',
        'type': TYPE_TOOL,
        'author': 'James Newton-King',
        'version': '9.0.1',
        'unity': 'Unity 2018.4+',
        'desc': '''### 插件概述
.NET 领域久负盛名的 Json.NET 深度适配版，完美解决 Unity 跨平台打包与 AOT 兼容问题。

> 💡 **支持的 Unity 版本**：`Unity 2018.4+`

### 核心特性
- 🌐 **全功能标准支持**：支持 Dictionary、复杂泛型嵌套、LINQ to JSON 与动态 JObject 解析。
- ⚙️ **丰富序列化控制**：支持驼峰命名转换、空值忽略、格式化输出与自定义 Converter。
- 📱 **移动端 IL2CPP 兼容**：内置 link.xml 防代码裁剪规则，确保全平台发布安全。
'''
    },
    {
        'file': 'ParrelSync-1.5.2.unitypackage',
        'title': 'ParrelSync (Unity 2018.4+)',
        'type': TYPE_TOOL,
        'author': 'VeriorPies',
        'version': '1.5.2',
        'unity': 'Unity 2018.4+',
        'desc': '''### 插件概述
单台电脑同时多开多个 Unity 编辑器副本进行网络联机互测的终极效率开发神器。

> 💡 **支持的 Unity 版本**：`Unity 2018.4+`

### 核心特性
- 👯 **项目软链接克隆**：利用 Windows 符号链接瞬间完成项目多开，无需复制整个工程文件。
- 🔄 **代码即时热同步**：在主项目中修改 C# 脚本或资源，克隆工程自动同步编译更新。
- 🎮 **多人网络调试**：主机与客户端分别在两扇窗口中同时运行，随时下断点联机单步调试。
'''
    },
    {
        'file': 'RuntimeInspectorHierarchy.unitypackage',
        'title': 'Runtime Inspector & Hierarchy (Unity 2018.4+)',
        'type': TYPE_TOOL,
        'author': 'Yasirkula',
        'version': '1.4.0',
        'unity': 'Unity 2018.4+',
        'desc': '''### 插件概述
直接在游戏运行态中渲染出如同 Unity 编辑器原版的层级树（Hierarchy）与检视面板（Inspector）。

> 💡 **支持的 Unity 版本**：`Unity 2018.4+`

### 核心特性
- 🔍 **运行时排查定位**：自由查看场景中的 GameObject 树、组件列表与 Transform 空间属性。
- ✏️ **变量实时热修改**：在手机或测试包中直接修改公共变量、开关组件、调用无参方法。
- 🎨 **高度可定制外观**：支持自定义暗色/亮色主题，并可灵活限制玩家可见的敏感字段。
'''
    },
    {
        'file': 'StandaloneFileBrowser 2.0.unitypackage',
        'title': 'Standalone File Browser (Unity 2018.4+)',
        'type': TYPE_TOOL,
        'author': 'gkngkc',
        'version': '2.0.0',
        'unity': 'Unity 2018.4+',
        'desc': '''### 插件概述
在独立平台调用底层操作系统原生文件选择器（打开文件、保存文件、选择文件夹）。

> 💡 **支持的 Unity 版本**：`Unity 2018.4+`

### 核心特性
- 🪟 **全桌面端覆盖**：原生适配 Windows (Win32 对话框)、macOS (AppKit 对话框) 与 Linux (GTK)。
- 📂 **灵活过滤与多选**：支持限制扩展名（如 `.png;.jpg;.json`）以及单选/多文件批量选择。
- ⚡ **异步与同步兼具**：提供即时阻塞调用与非阻塞协程/异步回调两种接入方式。
'''
    },
    {
        'file': 'Straight Sword Animation Set [1.3].unitypackage',
        'title': 'Straight Sword Animation Set (Unity 2018.4+)',
        'type': TYPE_3D,
        'author': 'WetCat Studio',
        'version': '1.3.0',
        'unity': 'Unity 2018.4+',
        'desc': '''### 插件概述
经典单手直剑与骑士剑战斗动作姿态集，动作灵动利落，适合传统奇幻与史诗动作冒险游戏。

> 💡 **支持的 Unity 版本**：`Unity 2018.4+`

### 核心特性
- 🤺 **连招与步伐**：四段轻攻击连斩、重刺击、翻滚前刺与战术后撤动作。
- 🛡️ **持盾动作融合**：支持单手持剑与一手持盾一手执剑的完整行走、奔跑与格挡姿态。
- 🎯 **Humanoid 认证**：标准 Unity 人形骨架资产，各大商店角色模型均可完美适配。
'''
    },
    {
        'file': 'TenkokuDynamicSky 1.2.2.unitypackage',
        'title': 'Tenkoku Dynamic Sky (Unity 2018.4+)',
        'type': TYPE_VFX,
        'author': 'Tanuki Digital',
        'version': '1.2.2',
        'unity': 'Unity 2018.4+',
        'desc': '''### 插件概述
Tenkoku Dynamic Sky 是集成了准确经纬度天体运行物理法则的专业动态天气与天空系统。

> 💡 **支持的 Unity 版本**：`Unity 2018.4+`

### 核心特性
- 🌌 **真实天文学轨道**：根据经纬度与年月日时自动排布太阳、月亮和真实星座位置。
- ❄️ **多重天气过渡**：平滑混合晴空、阴天、暴风雨、雷电、沙尘暴与极光等自然现象。
- 🌈 **光学大气散射**：支持高动态范围天空盒光晕、彩虹效果与黄昏晚霞着色。
'''
    },
    {
        'file': 'TEXDraw v4.4.0.unitypackage',
        'title': 'TEXDraw (Unity 2019.4+)',
        'type': TYPE_TOOL,
        'author': 'Minipop',
        'version': '4.4.0',
        'unity': 'Unity 2019.4+',
        'desc': '''### 插件概述
TEXDraw 是 Unity 生态最强悍的 LaTeX 数学公式排版与矢量富文本渲染组件。

> 💡 **支持的 Unity 版本**：`Unity 2019.4+`

### 核心特性
- 📐 **完整 LaTeX 语法**：支持复杂矩阵、积分、微分、分式、希腊字母与根号精准排版。
- 🖼️ **原生 UGUI 对接**：像普通的 Text 组件一样拖入即可使用，支持对齐与自适应缩放。
- ⚡ **无损矢量品质**：无论在 4K 屏幕还是移动端视网膜屏幕上放大，字迹始终清晰锐利。
'''
    },
    {
        'file': 'TriLib 2 - Model Loading Package.unitypackage',
        'title': 'TriLib 2 - Model Loader (Unity 2019.4+)',
        'type': TYPE_TOOL,
        'author': 'Ricardo Reis',
        'version': '2.1.8',
        'unity': 'Unity 2019.4+',
        'desc': '''### 插件概述
在游戏运行时从外部文件路径、内存或远程 URL 动态异步加载 3D 模型的工业级插件。

> 💡 **支持的 Unity 版本**：`Unity 2019.4+`

### 核心特性
- 📦 **全格式支持**：原生加载 FBX、OBJ、GLTF2、STL、PLY、3DS、DAE 等数十种格式。
- 🦴 **骨骼蒙皮动画**：完美提取模型骨骼层次、Humanoid 动画剪辑与 BlendShapes 表情。
- 🧵 **后台异步解算**：模型加载在后台子线程完成，加载大型复杂模型主界面绝不卡顿。
'''
    },
    {
        'file': 'Ultimate_Character_Controller_v2.4.8.unitypackage',
        'title': 'Ultimate Character Controller (Unity 2019.4+)',
        'type': TYPE_TMPL,
        'author': 'Opsive',
        'version': '2.4.8',
        'unity': 'Unity 2019.4+',
        'desc': '''### 插件概述
Opsive 出品的旗舰级角色运动、射击与动作模板，涵盖了现代 3D 动作游戏的全部底层系统。

> 💡 **支持的 Unity 版本**：`Unity 2019.4+`

### 核心特性
- 🎮 **双视角无缝切换**：第一人称（FPS）与第三人称（TPS）视角随时一键平滑过渡。
- 🧗 **全套动作能力体系**：涵盖移动、下蹲、攀爬梯子、跳跃悬挂、驾驶载具、掩体射击。
- 🔫 **模块化物品装备**：内置枪械弹药、近战冷兵器、投掷物、换弹动作与背包拾取逻辑。
'''
    },
    {
        'file': 'UniStorm - Dynamic Modular Weather v3.0.1.1.unitypackage',
        'title': 'UniStorm Weather v3 (Unity 2018.4+)',
        'type': TYPE_VFX,
        'author': 'Black Horizon Studios',
        'version': '3.0.1.1',
        'unity': 'Unity 2018.4+',
        'desc': '''### 插件概述
经典款程序化动态天气系统，轻巧高效，为开放世界与沙盒游戏赋予逼真的天候变换。

> 💡 **支持的 Unity 版本**：`Unity 2018.4+`

### 核心特性
- ⚡ **程序化闪电降水**：真实雨雪粒子、地面水洼积水、落雷物理与环境打湿特效。
- 🌅 **昼夜光照自动化**：太阳高度角变化自动驱动环境光、阴影色与雾气色彩渐变。
- 📻 **环境气象音效**：内置暴风雨呼啸、雨滴敲打、雷鸣等多音轨环境声效。
'''
    },
    {
        'file': 'UniStorm - Volumetric Clouds Sky Modular Weather and Cloud Shadows v5.4.1.unitypackage',
        'title': 'UniStorm Volumetric v5.4.1 (Unity 2020.3+)',
        'type': TYPE_VFX,
        'author': 'Black Horizon Studios',
        'version': '5.4.1',
        'unity': 'Unity 2020.3+',
        'desc': '''### 插件概述
UniStorm 划时代的 5.4.1 版本，引入高精体积云与物理云影系统，呈现极具电影感的天空。

> 💡 **支持的 Unity 版本**：`Unity 2020.3+`

### 核心特性
- ☁️ **真 3D 体积云**：支持多层云海穿越飞行、光线银边边缘透射与昼夜实时照明。
- 🌤️ **地面动态云影**：根据云层密度与太阳角度在地表投射流动的软阴影。
- 🎨 **深度支持全管线**：完美支持标准管线、URP 以及高画质 HDRP。
'''
    },
    {
        'file': 'UniTask.2.5.0.unitypackage',
        'title': 'UniTask (Unity 2019.4+)',
        'type': TYPE_TOOL,
        'author': 'Cysharp',
        'version': '2.5.0',
        'unity': 'Unity 2019.4+',
        'desc': '''### 插件概述
Unity 现代异步编程的首选基础库，采用值类型结构体实现 0 GC 的极致异步性能。

> 💡 **支持的 Unity 版本**：`Unity 2019.4+`

### 核心特性
- 🚀 **极度零 GC**：彻底摆脱原生 Task 的堆内存分配与协程的垃圾开销。
- ⏱️ **基于 PlayerLoop 驱动**：完美在 Update、LateUpdate、FixedUpdate 各生命周期无缝切换。
- 🛡️ **优雅取消支持**：原生绑定 CancellationToken 与 GameObject 销毁生命周期，防止异步泄漏。
'''
    },
    {
        'file': 'Unity Logs Viewer.unitypackage',
        'title': 'Unity Logs Viewer (Unity 2018.4+)',
        'type': TYPE_TOOL,
        'author': 'Reporter',
        'version': '1.0.8',
        'unity': 'Unity 2018.4+',
        'desc': '''### 插件概述
著名真机调试小工具（Reporter），在没有连接电脑数据线的情况下也能在手机上查报错。

> 💡 **支持的 Unity 版本**：`Unity 2018.4+`

### 核心特性
- 🖐️ **画圈手势即时唤出**：在手机屏幕上画一个大圈即可快速打开调试弹窗。
- 🔍 **异常捕获与计数**：分类统计 Log、Warning、Assert 与 Crash Error，显示完整行号堆栈。
- 💾 **设备硬件信息汇总**：一键查看设备型号、显存大小、电量、分辨率与操作系统版本。
'''
    },
    {
        'file': 'VR Panorama 360 PRO Renderer 3.0.unitypackage',
        'title': 'VR Panorama 360 PRO (Unity 2018.4+)',
        'type': TYPE_TOOL,
        'author': 'VR Panorama Studio',
        'version': '3.0.0',
        'unity': 'Unity 2018.4+',
        'desc': '''### 插件概述
在 Unity 内部将游戏场景直接导出为超高清 4K/8K 360 度全景视频与全景照片的离线渲染器。

> 💡 **支持的 Unity 版本**：`Unity 2018.4+`

### 核心特性
- 🌐 **全景格式支持**：支持等距柱状投影（Equirectangular）与立方体贴图（Cubemap）。
- 👓 **双目立体 VR 渲染**：支持左右眼视差渲染，直接生成兼容 VR 头显的 3D 全景立体影片。
- 🎬 **抗锯齿序列帧合成**：内置多重超级采样与序列帧直出 MP4 编码管线。
'''
    },
    {
        'file': 'VolumetricLightBeam.unitypackage',
        'title': 'Volumetric Light Beam (Unity 2018.4+)',
        'type': TYPE_VFX,
        'author': 'Lorenz96',
        'version': '1.9.0',
        'unity': 'Unity 2018.4+',
        'desc': '''### 插件概述
为聚光灯添加极富氛围感的丁达尔体积光束特效，极低 DrawCall 与算力消耗。

> 💡 **支持的 Unity 版本**：`Unity 2018.4+`

### 核心特性
- ✨ **程序化光束几何体**：使用优化过的锥体 Mesh 代替昂贵的逐像素光线步进，极低开销。
- 🌫️ **动态尘埃与噪点**：光束内部飘动微粒粒子与噪点动画，大大强化幽暗场景氛围感。
- 📐 **深度阻挡与淡入淡出**：光束打在障碍物上自动产生逼真的截断与距离衰减。
'''
    },
    {
        'file': 'Vuplex 3D WebView.unitypackage',
        'title': 'Vuplex 3D WebView (Unity 2019.4+)',
        'type': TYPE_TOOL,
        'author': 'Vuplex',
        'version': '4.2.0',
        'unity': 'Unity 2019.4+',
        'desc': '''### 插件概述
在 Unity 3D 虚拟场景的任意模型表面或 2D UI 界面中直接内嵌完整交互网页浏览器。

> 💡 **支持的 Unity 版本**：`Unity 2019.4+`

### 核心特性
- 🌐 **现代 Chromium 核心**：支持 HTML5、CSS3、WebGL 网页、YouTube 视频与 WebAudio 播放。
- 👆 **完整点击与触控交互**：玩家可以用射线或鼠标直接在游戏内点击链接、滑动滚轮与输入文字。
- 🔄 **双向 JS 互通**：支持 C# 与网页 JavaScript 双向通信与数据传递。
'''
    },
    {
        'file': 'Weather_Maker_Volumetric_Clouds_and_Weather_System_for_Unity_v8.unitypackage',
        'title': 'Weather Maker (Unity 2019.4+)',
        'type': TYPE_VFX,
        'author': 'Digital Ruby',
        'version': '8.0.0',
        'unity': 'Unity 2019.4+',
        'desc': '''### 插件概述
功能极度完备的 2D/3D 通用天气系统，带来集降雨降雪、体积云雾、昼夜循环于一体的完整方案。

> 💡 **支持的 Unity 版本**：`Unity 2019.4+`

### 核心特性
- ☁️ **先进射线步进体积云**：支持多层云层仿真、云雾高度自定义与性能分级适配。
- ⛈️ **环境降水与雷击**：支持逼真的降雨落水波纹、积雪消融、闪电音效及物理风力。
- 📱 **多平台轻量优化**：针对移动端、主机与 VR 提供了详尽的性能调优预设。
'''
    },
    {
        'file': 'XChart 3.1.0 &Demo.unitypackage',
        'title': 'XCharts 3 & Demo (Unity 2018.4+)',
        'type': TYPE_TOOL,
        'author': 'XCharts Team',
        'version': '3.1.0',
        'unity': 'Unity 2018.4+',
        'desc': '''### 插件概述
Unity 生态顶流开源 UGUI 数据可视化图表库，包含官方最全的演示场景与交互 Demo。

> 💡 **支持的 Unity 版本**：`Unity 2018.4+`

### 核心特性
- 📊 **图表类型一网打尽**：支持折线图、柱状图、饼图、散点图、雷达图、K线图与热力图。
- 🎬 **丰富动态交互**：支持数据动态刷新动画、悬停 Tooltip 提示框、图例筛选与缩放拖拽。
- 🛠️ **完整示例代码**：包含数十个开箱即用的功能示范场景，新手上手零门槛。
'''
    },
    {
        'file': 'XCharts-3.1.0.unitypackage',
        'title': 'XCharts 3 Core (Unity 2018.4+)',
        'type': TYPE_TOOL,
        'author': 'XCharts Team',
        'version': '3.1.0',
        'unity': 'Unity 2018.4+',
        'desc': '''### 插件概述
XCharts 的纯核心库版本，剔除了大体积的示例资源与演示场景，适合项目轻量化集成。

> 💡 **支持的 Unity 版本**：`Unity 2018.4+`

### 核心特性
- ⚡ **体积极致轻巧**：仅 1 MB 大小，纯代码与核心 Shader，不增加任何冗余包体。
- 🎯 **企业级可视化**：轻松构建工业级、大屏与游戏内的复杂数据统计面板。
- 🔄 **高频数据热更新**：支持毫秒级海量实时数据流渲染，性能卓越。
'''
    },
    {
        'file': 'AVProVideo_Enhanced.unitypackage',
        'title': 'AVPro Video 增强集成包 (Unity 2019.4+)',
        'type': TYPE_TOOL,
        'author': 'RenderHeads Ltd',
        'version': '1.11.0',
        'unity': 'Unity 2019.4+',
        'desc': '''### 插件概述
AVPro Video 的全平台增强集成套件，内置扩展解码驱动与进阶多屏播放解决方案。

> 💡 **支持的 Unity 版本**：`Unity 2019.4+`

### 核心特性
- 📺 **多屏同步播放**：适合大型展厅环幕、异形投影与多通道视频帧同步播放。
- 🚀 **丰富平台编解码器**：集成 Windows DirectShow、Media Foundation 及各移动端优化管线。
- 🎛️ **完备示例预设**：包含全景 360 播放器、曲面屏 UI 播放器与透明视频融合预设。
'''
    }
]

def generate_preview(title, unity_ver, type_id, author, version, size_mb, out_path):
    img = Image.new('RGB', (800, 450), color=(20, 24, 33))
    draw = ImageDraw.Draw(img)

    type_color = TYPE_COLORS.get(type_id, (59, 130, 246))
    type_name = TYPE_NAMES.get(type_id, '工具')

    font_title = ImageFont.truetype(r'C:\Windows\Fonts\msyhbd.ttc', 32)
    font_badge = ImageFont.truetype(r'C:\Windows\Fonts\msyhbd.ttc', 20)
    font_sub = ImageFont.truetype(r'C:\Windows\Fonts\msyh.ttc', 19)

    # 1. Top accent line
    draw.rectangle([0, 0, 800, 6], fill=type_color)

    # 2. Type badge (top left)
    draw.rounded_rectangle([36, 24, 160, 64], radius=6, fill=type_color)
    draw.text((50, 31), f'插件库 · {type_name}', font=font_badge, fill=(255, 255, 255))

    # 3. Unity Version Badge (top right, prominent green pill)
    badge_w = len(unity_ver) * 12 + 40
    badge_x = 764 - badge_w
    draw.rounded_rectangle([badge_x, 24, 764, 64], radius=6, fill=(16, 185, 129))
    draw.text((badge_x + 16, 31), unity_ver, font=font_badge, fill=(255, 255, 255))

    # 4. Subtle decorative card box in center
    draw.rounded_rectangle([36, 100, 764, 390], radius=12, fill=(28, 34, 48), outline=(45, 55, 72), width=1)

    # 5. Title inside card
    # Truncate title if too long for card
    display_title = title
    if len(display_title) > 28:
        display_title = display_title[:26] + '...'
    draw.text((64, 150), display_title, font=font_title, fill=(255, 255, 255))

    # 6. Metadata inside card
    meta_text1 = f'支持版本: {unity_ver}    |    发布版本: v{version}'
    draw.text((64, 230), meta_text1, font=font_sub, fill=(52, 211, 153))

    meta_text2 = f'官方作者: {author}    |    资源体积: {size_mb:.1f} MB'
    draw.text((64, 275), meta_text2, font=font_sub, fill=(156, 163, 175))

    # 7. Bottom tip inside card
    tip_text = '⭐ 认证官方正版插件  ·  一键即用导入  ·  0 本地冗余包体'
    draw.text((64, 335), tip_text, font=font_sub, fill=(100, 116, 139))

    img.save(out_path)

def main():
    print(f'Starting upload of {len(PLUGINS_CONFIG)} plugins...')
    
    # 1. Superuser Auth
    auth_resp = requests.post(
        f'{SERVER_URL}/api/collections/_superusers/auth-with-password',
        json={'identity': SUPERUSER_EMAIL, 'password': SUPERUSER_PASS}
    )
    if auth_resp.status_code != 200:
        print('Superuser auth failed:', auth_resp.text)
        return
    token = auth_resp.json()['token']
    headers = {'Authorization': token}
    print('Superuser authenticated successfully.')

    uploaded_ids = []

    # 2. Iterate and upload each plugin
    for idx, item in enumerate(PLUGINS_CONFIG, 1):
        pkg_file = item['file']
        pkg_path = os.path.join(PLUGINS_DIR, pkg_file)
        
        if not os.path.exists(pkg_path):
            print(f'[{idx}/{len(PLUGINS_CONFIG)}] Error: File not found: {pkg_path}')
            continue

        size_mb = round(os.path.getsize(pkg_path) / (1024 * 1024), 2)
        preview_file = f'preview_{idx}.png'
        preview_path = os.path.join(SCRATCH_DIR, preview_file)

        # Generate custom high-res preview image
        generate_preview(
            title=item['title'],
            unity_ver=item['unity'],
            type_id=item['type'],
            author=item['author'],
            version=item['version'],
            size_mb=size_mb,
            out_path=preview_path
        )

        data = {
            'title': item['title'],
            'category': CATEGORY_PLUGIN,
            'type': item['type'],
            'version': item['version'],
            'author': item['author'],
            'size': size_mb,
            'download_count': str(random.randint(80, 950)),
            'view_Count': str(random.randint(450, 3800)),
            'description': item['desc']
        }

        print(f'[{idx}/{len(PLUGINS_CONFIG)}] Uploading {item["title"]} ({size_mb} MB)...', end='', flush=True)
        start_t = time.time()

        with open(pkg_path, 'rb') as f_pkg, open(preview_path, 'rb') as f_img:
            files = {
                'zip_file': (pkg_file, f_pkg, 'application/octet-stream'),
                'preview_images': (preview_file, f_img, 'image/png')
            }
            resp = requests.post(
                f'{SERVER_URL}/api/collections/models/records',
                headers=headers,
                data=data,
                files=files
            )
            elapsed = time.time() - start_t

            if resp.status_code in [200, 201]:
                rec_id = resp.json()['id']
                uploaded_ids.append(rec_id)
                print(f' OK! (ID: {rec_id}, {elapsed:.1f}s)')
            else:
                print(f' FAILED! ({resp.status_code}): {resp.text[:100]}')

    print(f'\nTotal uploaded models: {len(uploaded_ids)}')

    # 3. Create 3 banners for featured plugins
    if len(uploaded_ids) >= 3:
        featured_ids = uploaded_ids[:3] # First 3 plugins as banners
        for fid in featured_ids:
            b_resp = requests.post(
                f'{SERVER_URL}/api/collections/banners/records',
                headers=headers,
                json={'model': fid}
            )
            if b_resp.status_code in [200, 201]:
                print(f'Created banner for model {fid}')

    print('Upload pipeline finished successfully!')

if __name__ == '__main__':
    main()
