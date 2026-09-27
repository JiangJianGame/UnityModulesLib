using System;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;

namespace JiangJian
{
    /// <summary>
    /// 资源库主编辑器可视化窗口
    /// 包含模块浏览、模块库/插件库与资源类型双重筛选、多图预览、包体下载与一键导入
    /// 兼容 Unity 2018+
    /// </summary>
    public class ModuleLibWindow : EditorWindow
    {
        private List<ModelItemData> _models = new List<ModelItemData>();
        private ModelItemData _selectedModel = null;
        private bool _isLoading = false;
        private string _errorMessage = null;
        private bool _showSettings = false;

        private ModuleLibListView _listView;
        private ModuleLibDetailView _detailView;

        [MenuItem("Tools/资源库/打开资源库窗口", priority = 0)]
        [MenuItem("Window/资源库 %#x", priority = 100)]
        public static void OpenWindow()
        {
            // 停靠在 Scene 场景视图面板（如同 Unity Asset Store 商店窗口，钉在主面板上而非独立悬浮）
            var window = GetWindow<ModuleLibWindow>("资源库", typeof(SceneView));
            window.minSize = new Vector2(680, 480);
            window.Show();
            window.Focus();
        }

        [InitializeOnLoadMethod]
        private static void RegisterQuittingCleanup()
        {
            EditorApplication.quitting -= OnEditorQuitting;
            EditorApplication.quitting += OnEditorQuitting;
        }

        private static void OnEditorQuitting()
        {
            // Unity 退出时彻底清除全部临时包体与本地缓存资源
            ModuleLibCache.ClearAllResources();
        }

        private void OnEnable()
        {
            titleContent = new GUIContent("资源库");

            // 每次打开或启用窗口时，主动清理任何残留的临时包体
            ModuleLibCache.CleanAllTempPackages();

            _listView = new ModuleLibListView(
                onSelectModel: model =>
                {
                    _selectedModel = model;
                    if (_detailView != null) _detailView.ResetState();
                    Repaint();
                },
                onTriggerRefresh: RefreshData
            );

            _detailView = new ModuleLibDetailView(
                onBackToList: () =>
                {
                    _selectedModel = null;
                    ModuleLibCache.CleanAllTempPackages();
                    Repaint();
                }
            );

            if (_models == null || _models.Count == 0)
            {
                RefreshData();
            }
        }

        private void OnDestroy()
        {
            // 关闭资源库界面时，清理掉全部资源（内存、临时包体、本地图片磁盘缓存）
            ModuleLibCache.ClearAllResources();
        }

        /// <summary>
        /// 从 PocketBase 刷新资源数据
        /// </summary>
        public void RefreshData()
        {
            _isLoading = true;
            _errorMessage = null;

            string url = $"{ModuleLibConfig.ServerUrl}/api/collections/models/records?perPage=50&sort=-created&expand=category,type";

            ModuleLibHttp.GetJson<ModelListResponse>(url,
                response =>
                {
                    _isLoading = false;
                    _errorMessage = null;
                    _models = new List<ModelItemData>();

                    if (response != null && response.items != null)
                    {
                        _models.AddRange(response.items);
                    }

                    // 若当前选中的模块存在更新，同步更新引用
                    if (_selectedModel != null)
                    {
                        var found = _models.Find(m => m.id == _selectedModel.id);
                        if (found != null) _selectedModel = found;
                    }

                    Repaint();
                },
                error =>
                {
                    _isLoading = false;
                    _errorMessage = error;
                    Repaint();
                });
        }

        private void OnGUI()
        {
            ModuleLibStyles.EnsureInitialized();

            // 1. 顶部全局功能条（服务器状态与设置入口）
            DrawWindowTopBar();

            // 2. 设置展开面板
            if (_showSettings)
            {
                DrawSettingsPanel();
            }

            // 3. 网络错误警报横幅
            if (!string.IsNullOrEmpty(_errorMessage))
            {
                DrawErrorBanner();
            }

            // 4. 主视图区域（列表视图 vs 详情视图）
            float topOffset = _showSettings ? 84f : 30f;
            if (!string.IsNullOrEmpty(_errorMessage)) topOffset += 38f;

            Rect mainArea = new Rect(0, topOffset, position.width, position.height - topOffset);

            if (_selectedModel != null)
            {
                _detailView.Draw(mainArea, _selectedModel, this);
            }
            else
            {
                _listView.Draw(mainArea, _models, _isLoading, this);
            }
        }

        private void DrawWindowTopBar()
        {
            GUILayout.BeginHorizontal(EditorStyles.toolbar, GUILayout.Height(26));

            GUILayout.Label(" 📦 资源库", EditorStyles.boldLabel, GUILayout.Width(80));

            // 显示连接的服务器地址
            string statusTip = $"已连接: {ModuleLibConfig.ServerUrl}";
            GUILayout.Label(statusTip, EditorStyles.miniLabel);

            GUILayout.FlexibleSpace();

            // 设置展开按钮
            string settingsText = _showSettings ? "隐藏设置 ▴" : "服务设置 ▾";
            if (GUILayout.Button(settingsText, EditorStyles.toolbarButton, GUILayout.Width(76)))
            {
                _showSettings = !_showSettings;
            }

            GUILayout.Space(4);
            GUILayout.EndHorizontal();
        }

        private void DrawSettingsPanel()
        {
            GUILayout.BeginVertical(EditorStyles.helpBox);
            GUILayout.BeginHorizontal();

            GUILayout.Label("服务器地址:", EditorStyles.miniLabel, GUILayout.Width(72));
            string curUrl = ModuleLibConfig.ServerUrl;
            string newUrl = EditorGUILayout.TextField(curUrl);
            if (newUrl != curUrl && !string.IsNullOrEmpty(newUrl))
            {
                ModuleLibConfig.ServerUrl = newUrl;
            }

            if (GUILayout.Button("恢复默认", EditorStyles.miniButton, GUILayout.Width(64)))
            {
                ModuleLibConfig.ResetToDefaultServerUrl();
                GUI.FocusControl(null);
            }

            if (GUILayout.Button("测试连接", EditorStyles.miniButton, GUILayout.Width(64)))
            {
                RefreshData();
            }

            if (GUILayout.Button("清理全部资源", EditorStyles.miniButton, GUILayout.Width(84)))
            {
                ModuleLibCache.ClearAllResources();
                EditorUtility.DisplayDialog("提示", "所有临时包体、图片缓存与内存资源已彻底清空！", "确定");
                Repaint();
            }

            GUILayout.EndHorizontal();
            GUILayout.EndVertical();
        }

        private void DrawErrorBanner()
        {
            EditorGUILayout.HelpBox($"连接错误: {_errorMessage}\n请检查后端 PocketBase (默认 http://127.0.0.1:5050) 是否启动。", MessageType.Error);
            GUILayout.BeginHorizontal();
            GUILayout.FlexibleSpace();
            if (GUILayout.Button("重试连接", GUILayout.Width(80)))
            {
                RefreshData();
            }
            GUILayout.Space(6);
            GUILayout.EndHorizontal();
        }
    }
}
