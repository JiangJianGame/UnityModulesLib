using UnityEditor;
using UnityEngine;

namespace JiangJian
{
    /// <summary>
    /// 资源库 UI 视觉规范与全局样式表
    /// 支持 Unity ProSkin（深色）与 Personal（浅色）双主题自适应
    /// 兼容 Unity 2018+
    /// </summary>
    public static class ModuleLibStyles
    {
        private static bool _initialized;

        // 调色板
        public static readonly Color ColorInternalBadge = new Color(0.18f, 0.55f, 0.34f, 1f);  // 绿色：自制模块
        public static readonly Color ColorPluginBadge = new Color(0.15f, 0.45f, 0.82f, 1f);    // 蓝色：插件库
        public static readonly Color ColorStoreBadge = ColorPluginBadge;                        // 兼容别名
        public static readonly Color ColorTypeBadge = new Color(0.85f, 0.52f, 0.12f, 1f);      // 橙色：资源类型
        public static readonly Color ColorVersionBadge = new Color(0.35f, 0.40f, 0.48f, 1f);   // 灰蓝：版本
        public static readonly Color ColorCardBorder = new Color(0.3f, 0.33f, 0.38f, 0.6f);

        // 纯色背景纹理缓存
        private static Texture2D _texCardBg;
        private static Texture2D _texCardHoverBg;
        private static Texture2D _texBadgeBg;
        private static Texture2D _texHeaderBg;

        // GUIStyles
        public static GUIStyle CardBox;
        public static GUIStyle CardTitle;
        public static GUIStyle CardSub;
        public static GUIStyle CardBadge;
        public static GUIStyle TabButtonLeft;
        public static GUIStyle TabButtonMid;
        public static GUIStyle TabButtonRight;
        public static GUIStyle PillButtonNormal;
        public static GUIStyle PillButtonActive;
        public static GUIStyle SearchField;
        public static GUIStyle BigActionButton;
        public static GUIStyle DetailTitle;
        public static GUIStyle DetailMeta;
        public static GUIStyle SectionHeader;
        public static GUIStyle MarkdownBox;

        /// <summary>
        /// 初始化样式表（在 OnGUI 中安全延迟加载）
        /// </summary>
        public static void EnsureInitialized()
        {
            if (_initialized) return;
            _initialized = true;

            bool isDark = EditorGUIUtility.isProSkin;

            _texCardBg = CreateSolidTexture(2, 2, isDark ? new Color(0.19f, 0.21f, 0.24f, 1f) : new Color(0.92f, 0.92f, 0.93f, 1f));
            _texCardHoverBg = CreateSolidTexture(2, 2, isDark ? new Color(0.24f, 0.27f, 0.32f, 1f) : new Color(0.86f, 0.88f, 0.92f, 1f));
            _texBadgeBg = CreateSolidTexture(2, 2, Color.white);
            _texHeaderBg = CreateSolidTexture(2, 2, isDark ? new Color(0.15f, 0.16f, 0.18f, 1f) : new Color(0.82f, 0.83f, 0.85f, 1f));

            // 卡片容器样式
            CardBox = new GUIStyle(GUI.skin.box)
            {
                margin = new RectOffset(6, 6, 6, 6),
                padding = new RectOffset(8, 8, 8, 8),
                normal = { background = _texCardBg },
                hover = { background = _texCardHoverBg },
                border = new RectOffset(1, 1, 1, 1)
            };

            // 卡片标题
            CardTitle = new GUIStyle(EditorStyles.boldLabel)
            {
                fontSize = 13,
                wordWrap = false,
                clipping = TextClipping.Clip,
                normal = { textColor = isDark ? new Color(0.95f, 0.96f, 0.98f) : new Color(0.1f, 0.12f, 0.15f) }
            };

            // 副标题与统计信息
            CardSub = new GUIStyle(EditorStyles.miniLabel)
            {
                fontSize = 11,
                normal = { textColor = isDark ? new Color(0.68f, 0.72f, 0.78f) : new Color(0.35f, 0.38f, 0.42f) }
            };

            // 徽章文字样式
            CardBadge = new GUIStyle(EditorStyles.miniLabel)
            {
                fontSize = 10,
                fontStyle = FontStyle.Bold,
                alignment = TextAnchor.MiddleCenter,
                normal = { textColor = Color.white }
            };

            // 选项卡按钮
            TabButtonLeft = new GUIStyle(EditorStyles.miniButtonLeft)
            {
                fontSize = 12,
                fixedHeight = 28,
                fontStyle = FontStyle.Bold
            };
            TabButtonMid = new GUIStyle(EditorStyles.miniButtonMid)
            {
                fontSize = 12,
                fixedHeight = 28,
                fontStyle = FontStyle.Bold
            };
            TabButtonRight = new GUIStyle(EditorStyles.miniButtonRight)
            {
                fontSize = 12,
                fixedHeight = 28,
                fontStyle = FontStyle.Bold
            };

            // 胶囊筛选按钮
            PillButtonNormal = new GUIStyle(EditorStyles.miniButton)
            {
                fontSize = 11,
                fixedHeight = 22,
                margin = new RectOffset(2, 2, 2, 2),
                padding = new RectOffset(8, 8, 2, 2)
            };

            PillButtonActive = new GUIStyle(EditorStyles.miniButton)
            {
                fontSize = 11,
                fontStyle = FontStyle.Bold,
                fixedHeight = 22,
                margin = new RectOffset(2, 2, 2, 2),
                padding = new RectOffset(8, 8, 2, 2),
                normal = { textColor = isDark ? new Color(0.35f, 0.75f, 1f) : new Color(0.1f, 0.45f, 0.9f) }
            };

            // 搜索框
#if UNITY_2018_1_OR_NEWER
            SearchField = new GUIStyle(EditorStyles.toolbarSearchField)
            {
                fontSize = 12,
                fixedHeight = 24
            };
#else
            SearchField = new GUIStyle(EditorStyles.textField)
            {
                fontSize = 12,
                fixedHeight = 24
            };
#endif

            // 大动作按钮（下载/导入）
            BigActionButton = new GUIStyle(GUI.skin.button)
            {
                fontSize = 14,
                fontStyle = FontStyle.Bold,
                fixedHeight = 36,
                normal = { textColor = isDark ? Color.white : new Color(0.05f, 0.1f, 0.2f) }
            };

            // 详情标题
            DetailTitle = new GUIStyle(EditorStyles.boldLabel)
            {
                fontSize = 18,
                wordWrap = true,
                normal = { textColor = isDark ? Color.white : Color.black }
            };

            DetailMeta = new GUIStyle(EditorStyles.label)
            {
                fontSize = 12,
                wordWrap = true,
                normal = { textColor = isDark ? new Color(0.8f, 0.82f, 0.85f) : new Color(0.2f, 0.22f, 0.25f) }
            };

            SectionHeader = new GUIStyle(EditorStyles.boldLabel)
            {
                fontSize = 14,
                normal = { textColor = isDark ? new Color(0.4f, 0.75f, 1f) : new Color(0.1f, 0.45f, 0.85f) }
            };

            MarkdownBox = new GUIStyle(EditorStyles.helpBox)
            {
                padding = new RectOffset(12, 12, 10, 10),
                fontSize = 12
            };
        }

        /// <summary>
        /// 绘制彩色胶囊徽章
        /// </summary>
        public static void DrawBadge(Rect rect, string text, Color bgColor)
        {
            var oldColor = GUI.color;
            GUI.color = bgColor;
            GUI.DrawTexture(rect, _texBadgeBg ?? Texture2D.whiteTexture, ScaleMode.StretchToFill, true, 0, bgColor, 0, 3);
            GUI.color = oldColor;

            GUI.Label(rect, text, CardBadge);
        }

        /// <summary>
        /// 生成纯色单色 Texture2D
        /// </summary>
        public static Texture2D CreateSolidTexture(int width, int height, Color color)
        {
            var tex = new Texture2D(width, height, TextureFormat.RGBA32, false);
            tex.hideFlags = HideFlags.DontSave;
            var pixels = new Color[width * height];
            for (int i = 0; i < pixels.Length; i++) pixels[i] = color;
            tex.SetPixels(pixels);
            tex.Apply();
            return tex;
        }
    }
}
