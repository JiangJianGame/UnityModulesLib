using System;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;

namespace JiangJian
{
    /// <summary>
    /// 资源模块列表视图（自适应卡片网格、双重筛选、搜索与排序）
    /// 兼容 Unity 2018+
    /// </summary>
    public class ModuleLibListView
    {
        private readonly Action<ModelItemData> _onSelectModel;
        private readonly Action _onTriggerRefresh;

        private Vector2 _scrollPos;
        private string _searchText = "";
        private OriginFilterType _selectedOrigin = OriginFilterType.All;
        private string _selectedTypeName = "全部";
        private SortOption _selectedSort = SortOption.Newest;

        private readonly string[] _sortLabels = new string[] { "最新发布", "最多浏览", "最多下载", "名称升序" };
        private readonly string[] _fixedTypeNames = new string[] { "全部", "3D", "2D", "音频", "模板", "工具", "视觉特效" };

        public ModuleLibListView(Action<ModelItemData> onSelectModel, Action onTriggerRefresh)
        {
            _onSelectModel = onSelectModel;
            _onTriggerRefresh = onTriggerRefresh;
        }

        /// <summary>
        /// 绘制列表视图主界面
        /// </summary>
        public void Draw(Rect totalArea, List<ModelItemData> allModels, bool isLoading, EditorWindow parentWindow)
        {
            ModuleLibStyles.EnsureInitialized();

            GUILayout.BeginArea(totalArea);
            GUILayout.BeginVertical();

            // 1. 顶部工具栏（来源分类 Tab + 搜索框 + 排序下拉）
            DrawTopToolbar();

            // 2. 二级资源类型筛选胶囊行
            DrawTypeFilterBar();

            GUILayout.Space(4);

            // 3. 过滤与排序模型数据
            List<ModelItemData> filteredModels = FilterAndSortModels(allModels);

            // 4. 内容主体区域（网格卡片瀑布流）
            if (isLoading)
            {
                DrawLoadingState();
            }
            else if (filteredModels.Count == 0)
            {
                DrawEmptyState(allModels.Count == 0);
            }
            else
            {
                DrawModelGrid(filteredModels, parentWindow);
            }

            GUILayout.EndVertical();
            GUILayout.EndArea();
        }

        private void DrawTopToolbar()
        {
            GUILayout.BeginHorizontal(EditorStyles.toolbar, GUILayout.Height(30));

            // 来源分类切换 Tab（全部 / 模块库 / Unity商店）
            GUILayout.Space(4);
            bool isAll = _selectedOrigin == OriginFilterType.All;
            bool isInternal = _selectedOrigin == OriginFilterType.Internal;
            bool isStore = _selectedOrigin == OriginFilterType.Store;

            if (GUILayout.Toggle(isAll, "全部来源", ModuleLibStyles.TabButtonLeft, GUILayout.Width(76)))
            {
                _selectedOrigin = OriginFilterType.All;
            }
            if (GUILayout.Toggle(isInternal, "模块库 (自制)", ModuleLibStyles.TabButtonMid, GUILayout.Width(96)))
            {
                _selectedOrigin = OriginFilterType.Internal;
            }
            if (GUILayout.Toggle(isStore, "Unity 商店", ModuleLibStyles.TabButtonRight, GUILayout.Width(82)))
            {
                _selectedOrigin = OriginFilterType.Store;
            }

            GUILayout.Space(12);

            // 搜索输入框
            _searchText = EditorGUILayout.TextField(_searchText, ModuleLibStyles.SearchField, GUILayout.MinWidth(140), GUILayout.MaxWidth(280));
            if (!string.IsNullOrEmpty(_searchText))
            {
                if (GUILayout.Button("✕", EditorStyles.miniButton, GUILayout.Width(20)))
                {
                    _searchText = "";
                    GUI.FocusControl(null);
                }
            }

            GUILayout.FlexibleSpace();

            // 排序下拉框
            GUILayout.Label("排序:", EditorStyles.miniLabel, GUILayout.Width(32));
            _selectedSort = (SortOption)EditorGUILayout.Popup((int)_selectedSort, _sortLabels, EditorStyles.toolbarPopup, GUILayout.Width(90));

            GUILayout.Space(6);

            // 刷新按钮
            if (GUILayout.Button("刷新", EditorStyles.toolbarButton, GUILayout.Width(46)))
            {
                if (_onTriggerRefresh != null) _onTriggerRefresh();
            }

            GUILayout.Space(4);
            GUILayout.EndHorizontal();
        }

        private void DrawTypeFilterBar()
        {
            GUILayout.BeginHorizontal(EditorStyles.helpBox, GUILayout.Height(28));
            GUILayout.Space(4);
            GUILayout.Label("类型:", EditorStyles.miniBoldLabel, GUILayout.Width(36));

            for (int i = 0; i < _fixedTypeNames.Length; i++)
            {
                string tname = _fixedTypeNames[i];
                bool isSelected = _selectedTypeName == tname;
                GUIStyle style = isSelected ? ModuleLibStyles.PillButtonActive : ModuleLibStyles.PillButtonNormal;

                if (GUILayout.Button(tname, style))
                {
                    _selectedTypeName = tname;
                }
            }

            GUILayout.FlexibleSpace();
            GUILayout.EndHorizontal();
        }

        private List<ModelItemData> FilterAndSortModels(List<ModelItemData> source)
        {
            var result = new List<ModelItemData>();
            if (source == null) return result;

            string query = (_searchText ?? "").Trim().ToLower();

            for (int i = 0; i < source.Count; i++)
            {
                var item = source[i];

                // 来源过滤
                if (_selectedOrigin == OriginFilterType.Internal && !item.IsInternalModule()) continue;
                if (_selectedOrigin == OriginFilterType.Store && item.IsInternalModule()) continue;

                // 类型过滤
                if (_selectedTypeName != "全部")
                {
                    string itemType = item.GetTypeName();
                    if (!string.Equals(itemType, _selectedTypeName, StringComparison.OrdinalIgnoreCase)) continue;
                }

                // 搜索过滤
                if (!string.IsNullOrEmpty(query))
                {
                    bool matchTitle = (item.title ?? "").ToLower().Contains(query);
                    bool matchAuthor = (item.author ?? "").ToLower().Contains(query);
                    bool matchDesc = (item.description ?? "").ToLower().Contains(query);
                    if (!matchTitle && !matchAuthor && !matchDesc) continue;
                }

                result.Add(item);
            }

            // 排序处理
            switch (_selectedSort)
            {
                case SortOption.MostViews:
                    result.Sort((a, b) => b.GetViewCountInt().CompareTo(a.GetViewCountInt()));
                    break;
                case SortOption.MostDownloads:
                    result.Sort((a, b) => b.GetDownloadCountInt().CompareTo(a.GetDownloadCountInt()));
                    break;
                case SortOption.TitleAsc:
                    result.Sort((a, b) => string.Compare(a.title, b.title, StringComparison.Ordinal));
                    break;
                case SortOption.Newest:
                default:
                    // 默认按后端返回顺序（最新发布倒序）
                    break;
            }

            return result;
        }

        private void DrawModelGrid(List<ModelItemData> models, EditorWindow parentWindow)
        {
            _scrollPos = GUILayout.BeginScrollView(_scrollPos);

            float viewWidth = EditorGUIUtility.currentViewWidth - 26;
            float minCardWidth = 230f;
            int columns = Mathf.Max(1, Mathf.FloorToInt(viewWidth / minCardWidth));
            float cardWidth = (viewWidth - (columns - 1) * 8f) / columns;
            float cardHeight = 240f;

            int totalCount = models.Count;
            int rows = Mathf.CeilToInt((float)totalCount / columns);

            string baseUrl = ModuleLibConfig.ServerUrl;

            for (int r = 0; r < rows; r++)
            {
                GUILayout.BeginHorizontal();
                for (int c = 0; c < columns; c++)
                {
                    int index = r * columns + c;
                    if (index < totalCount)
                    {
                        var model = models[index];
                        DrawCardItem(model, cardWidth, cardHeight, baseUrl, parentWindow);
                    }
                    else
                    {
                        GUILayout.Space(cardWidth);
                    }
                    if (c < columns - 1) GUILayout.Space(8);
                }
                GUILayout.EndHorizontal();
                GUILayout.Space(8);
            }

            GUILayout.EndScrollView();
        }

        private void DrawCardItem(ModelItemData model, float width, float height, string baseUrl, EditorWindow parentWindow)
        {
            Rect cardRect = GUILayoutUtility.GetRect(width, height, GUILayout.Width(width), GUILayout.Height(height));
            Event evt = Event.current;

            // 悬停与点击事件检测
            EditorGUIUtility.AddCursorRect(cardRect, MouseCursor.Link);
            if (evt.type == EventType.MouseDown && evt.button == 0 && cardRect.Contains(evt.mousePosition))
            {
                evt.Use();
                if (_onSelectModel != null) _onSelectModel(model);
                return;
            }

            // 绘制卡片背景框
            GUI.Box(cardRect, GUIContent.none, ModuleLibStyles.CardBox);

            // 卡片内容布局
            float pad = 8f;
            float innerWidth = width - pad * 2;

            // 1. 缩略图区域 (16:9 比例)
            float imgHeight = innerWidth * 9f / 16f;
            Rect imgRect = new Rect(cardRect.x + pad, cardRect.y + pad, innerWidth, imgHeight);

            string thumbUrl = model.GetFirstThumbnailUrl(baseUrl);
            Texture2D tex = null;
            if (!string.IsNullOrEmpty(thumbUrl))
            {
                tex = ModuleLibCache.GetTexture(thumbUrl);
                if (tex == null)
                {
                    ModuleLibHttp.GetTexture(thumbUrl, loadedTex =>
                    {
                        if (parentWindow != null) parentWindow.Repaint();
                    });
                }
            }

            if (tex != null)
            {
                GUI.DrawTexture(imgRect, tex, ScaleMode.ScaleAndCrop);
            }
            else
            {
                // 占位背景
                var oldCol = GUI.color;
                GUI.color = new Color(0.2f, 0.22f, 0.26f, 1f);
                GUI.DrawTexture(imgRect, Texture2D.whiteTexture);
                GUI.color = oldCol;
                GUI.Label(imgRect, "加载预览中...", EditorStyles.centeredGreyMiniLabel);
            }

            // 2. 来源与类型徽章（叠在图片下方）
            float currentY = imgRect.yMax + 6f;
            float badgeHeight = 18f;

            // 来源徽章（自制 vs 商店）
            bool isInternal = model.IsInternalModule();
            string originText = isInternal ? "自制模块" : "Unity商店";
            Color originCol = isInternal ? ModuleLibStyles.ColorInternalBadge : ModuleLibStyles.ColorStoreBadge;
            float originBadgeWidth = 58f;
            ModuleLibStyles.DrawBadge(new Rect(cardRect.x + pad, currentY, originBadgeWidth, badgeHeight), originText, originCol);

            // 类型徽章（3D/2D/音频等）
            string typeText = model.GetTypeName();
            float typeBadgeWidth = Mathf.Max(36f, typeText.Length * 14f + 12f);
            ModuleLibStyles.DrawBadge(new Rect(cardRect.x + pad + originBadgeWidth + 4f, currentY, typeBadgeWidth, badgeHeight), typeText, ModuleLibStyles.ColorTypeBadge);

            // 版本徽章
            if (!string.IsNullOrEmpty(model.version))
            {
                string verText = "v" + model.version;
                float verWidth = Mathf.Max(42f, verText.Length * 7f + 10f);
                float verX = cardRect.xMax - pad - verWidth;
                ModuleLibStyles.DrawBadge(new Rect(verX, currentY, verWidth, badgeHeight), verText, ModuleLibStyles.ColorVersionBadge);
            }

            currentY += badgeHeight + 6f;

            // 3. 资源标题
            Rect titleRect = new Rect(cardRect.x + pad, currentY, innerWidth, 20f);
            GUI.Label(titleRect, new GUIContent(model.title, model.title), ModuleLibStyles.CardTitle);

            currentY += 20f;

            // 4. 作者与体积
            Rect authorRect = new Rect(cardRect.x + pad, currentY, innerWidth, 16f);
            string authorStr = $"作者: {model.author}  |  {model.size:F1} MB";
            GUI.Label(authorRect, authorStr, ModuleLibStyles.CardSub);

            currentY += 16f;

            // 5. 浏览与下载统计
            Rect statsRect = new Rect(cardRect.x + pad, currentY, innerWidth, 16f);
            string statsStr = $"👁 {model.view_Count}   ⬇ {model.download_count}";
            GUI.Label(statsRect, statsStr, ModuleLibStyles.CardSub);
        }

        private void DrawLoadingState()
        {
            GUILayout.FlexibleSpace();
            GUILayout.BeginHorizontal();
            GUILayout.FlexibleSpace();
            GUILayout.Label("正在从后端拉取资源数据，请稍候...", EditorStyles.boldLabel);
            GUILayout.FlexibleSpace();
            GUILayout.EndHorizontal();
            GUILayout.FlexibleSpace();
        }

        private void DrawEmptyState(bool noDataAtAll)
        {
            GUILayout.FlexibleSpace();
            GUILayout.BeginHorizontal();
            GUILayout.FlexibleSpace();
            GUILayout.BeginVertical();

            if (noDataAtAll)
            {
                GUILayout.Label("未获取到任何模块数据！", EditorStyles.boldLabel);
                GUILayout.Space(6);
                GUILayout.Label($"请确认 PocketBase 服务正在运行 ({ModuleLibConfig.ServerUrl})", EditorStyles.miniLabel);
                GUILayout.Space(10);
                if (GUILayout.Button("重新连接获取", GUILayout.Width(130), GUILayout.Height(28)))
                {
                    if (_onTriggerRefresh != null) _onTriggerRefresh();
                }
            }
            else
            {
                GUILayout.Label("未找到符合当前筛选条件的资源模块", EditorStyles.boldLabel);
                GUILayout.Space(6);
                if (GUILayout.Button("重置筛选条件", GUILayout.Width(110)))
                {
                    _searchText = "";
                    _selectedOrigin = OriginFilterType.All;
                    _selectedTypeName = "全部";
                }
            }

            GUILayout.EndVertical();
            GUILayout.FlexibleSpace();
            GUILayout.EndHorizontal();
            GUILayout.FlexibleSpace();
        }
    }
}
