using System;
using System.IO;
using System.Text.RegularExpressions;
using UnityEditor;
using UnityEngine;

namespace JiangJian
{
    /// <summary>
    /// 资源模块详情视图（多图轮播查看、元数据展示、Markdown 说明排版、一键下载导入）
    /// 兼容 Unity 2018+
    /// </summary>
    public class ModuleLibDetailView
    {
        private readonly Action _onBackToList;

        private Vector2 _scrollPos;
        private int _selectedImageIndex = 0;
        private bool _isDownloading = false;
        private float _downloadProgress = 0f;
        private string _statusMessage = "";

        public ModuleLibDetailView(Action onBackToList)
        {
            _onBackToList = onBackToList;
        }

        public void ResetState()
        {
            _selectedImageIndex = 0;
            _isDownloading = false;
            _downloadProgress = 0f;
            _statusMessage = "";
            _scrollPos = Vector2.zero;
            ModuleLibCache.CleanAllTempPackages();
        }

        public void Draw(Rect totalArea, ModelItemData model, EditorWindow parentWindow)
        {
            if (model == null) return;
            ModuleLibStyles.EnsureInitialized();

            GUILayout.BeginArea(totalArea);
            GUILayout.BeginVertical();

            // 1. 顶部操作导航栏
            DrawHeaderBar(model);

            GUILayout.Space(6);

            // 2. 详情滚动容器
            _scrollPos = GUILayout.BeginScrollView(_scrollPos);

            // 标题与基本标签
            DrawTitleAndMeta(model);

            GUILayout.Space(12);

            // 图片轮播查看器
            DrawImageGallery(model, parentWindow);

            GUILayout.Space(14);

            // 下载与导入操作区
            DrawActionSection(model, parentWindow);

            GUILayout.Space(16);

            // 资源描述（Markdown 解析展示）
            DrawDescriptionSection(model);

            GUILayout.Space(20);
            GUILayout.EndScrollView();

            GUILayout.EndVertical();
            GUILayout.EndArea();
        }

        private void DrawHeaderBar(ModelItemData model)
        {
            GUILayout.BeginHorizontal(EditorStyles.toolbar, GUILayout.Height(30));

            // 返回按钮
            if (GUILayout.Button("← 返回模块列表", EditorStyles.toolbarButton, GUILayout.Width(110)))
            {
                if (_onBackToList != null) _onBackToList();
            }

            GUILayout.FlexibleSpace();

            // 打开本地缓存目录
            if (GUILayout.Button("打开缓存目录", EditorStyles.toolbarButton, GUILayout.Width(90)))
            {
                EditorUtility.RevealInFinder(ModuleLibConfig.CacheRootDirectory);
            }

            GUILayout.Space(4);
            GUILayout.EndHorizontal();
        }

        private void DrawTitleAndMeta(ModelItemData model)
        {
            GUILayout.BeginVertical(EditorStyles.helpBox);

            // 资源大标题
            GUILayout.Label(model.title, ModuleLibStyles.DetailTitle);

            GUILayout.Space(8);

            // 徽章与元数据行
            GUILayout.BeginHorizontal();

            // 来源标签
            bool isInternal = model.IsInternalModule();
            string originText = isInternal ? "模块库" : "插件库";
            Color originCol = isInternal ? ModuleLibStyles.ColorInternalBadge : ModuleLibStyles.ColorPluginBadge;
            float originWidth = Mathf.Max(50f, originText.Length * 13f + 12f);
            Rect originRect = GUILayoutUtility.GetRect(originWidth, 20, GUILayout.Width(originWidth), GUILayout.Height(20));
            ModuleLibStyles.DrawBadge(originRect, originText, originCol);

            GUILayout.Space(6);

            // 类型标签
            string typeText = model.GetTypeName();
            float typeWidth = Mathf.Max(40, typeText.Length * 14 + 10);
            Rect typeRect = GUILayoutUtility.GetRect(typeWidth, 20, GUILayout.Width(typeWidth), GUILayout.Height(20));
            ModuleLibStyles.DrawBadge(typeRect, typeText, ModuleLibStyles.ColorTypeBadge);

            if (!string.IsNullOrEmpty(model.version))
            {
                GUILayout.Space(6);
                string verText = "v" + model.version;
                float verWidth = Mathf.Max(44, verText.Length * 7 + 12);
                Rect verRect = GUILayoutUtility.GetRect(verWidth, 20, GUILayout.Width(verWidth), GUILayout.Height(20));
                ModuleLibStyles.DrawBadge(verRect, verText, ModuleLibStyles.ColorVersionBadge);
            }

            GUILayout.Space(12);

            // 作者与大小信息
            string authorMeta = $"作者: {model.author}    体积: {model.size:F2} MB    浏览: {model.view_Count} 次    下载: {model.download_count} 次";
            GUILayout.Label(authorMeta, ModuleLibStyles.DetailMeta);

            GUILayout.FlexibleSpace();
            GUILayout.EndHorizontal();

            GUILayout.EndVertical();
        }

        private void DrawImageGallery(ModelItemData model, EditorWindow parentWindow)
        {
            string baseUrl = ModuleLibConfig.ServerUrl;
            int imgCount = model.preview_images != null ? model.preview_images.Length : 0;

            if (imgCount == 0) return;

            if (_selectedImageIndex >= imgCount) _selectedImageIndex = 0;

            GUILayout.BeginVertical(EditorStyles.helpBox);

            // 1. 主大图预览（宽度自适应，16:9）
            float viewWidth = EditorGUIUtility.currentViewWidth - 36;
            float maxImgWidth = Mathf.Min(viewWidth, 680f);
            float mainImgHeight = maxImgWidth * 9f / 16f;

            GUILayout.BeginHorizontal();
            GUILayout.FlexibleSpace();
            Rect mainImgRect = GUILayoutUtility.GetRect(maxImgWidth, mainImgHeight, GUILayout.Width(maxImgWidth), GUILayout.Height(mainImgHeight));

            string mainImgUrl = model.GetPreviewImageUrl(baseUrl, _selectedImageIndex);
            Texture2D mainTex = null;
            if (!string.IsNullOrEmpty(mainImgUrl))
            {
                mainTex = ModuleLibCache.GetTexture(mainImgUrl);
                if (mainTex == null)
                {
                    ModuleLibHttp.GetTexture(mainImgUrl, tex =>
                    {
                        if (parentWindow != null) parentWindow.Repaint();
                    });
                }
            }

            if (mainTex != null)
            {
                GUI.DrawTexture(mainImgRect, mainTex, ScaleMode.ScaleToFit);
            }
            else
            {
                var oldCol = GUI.color;
                GUI.color = new Color(0.18f, 0.2f, 0.24f, 1f);
                GUI.DrawTexture(mainImgRect, Texture2D.whiteTexture);
                GUI.color = oldCol;
                GUI.Label(mainImgRect, "正在加载高清预览大图...", EditorStyles.centeredGreyMiniLabel);
            }

            GUILayout.FlexibleSpace();
            GUILayout.EndHorizontal();

            // 2. 缩略图横向切换栏（有多张图时展示）
            if (imgCount > 1)
            {
                GUILayout.Space(8);
                GUILayout.BeginHorizontal();
                GUILayout.FlexibleSpace();

                for (int i = 0; i < imgCount; i++)
                {
                    bool isCur = i == _selectedImageIndex;
                    float thumbW = 80f;
                    float thumbH = 45f;
                    Rect thumbRect = GUILayoutUtility.GetRect(thumbW, thumbH, GUILayout.Width(thumbW), GUILayout.Height(thumbH));

                    string tUrl = model.GetPreviewImageUrl(baseUrl, i);
                    Texture2D tTex = ModuleLibCache.GetTexture(tUrl);
                    if (tTex == null)
                    {
                        ModuleLibHttp.GetTexture(tUrl, tex =>
                        {
                            if (parentWindow != null) parentWindow.Repaint();
                        });
                    }

                    if (tTex != null)
                    {
                        GUI.DrawTexture(thumbRect, tTex, ScaleMode.ScaleAndCrop);
                    }
                    else
                    {
                        GUI.Box(thumbRect, $"{i + 1}");
                    }

                    // 选中边框高亮
                    if (isCur)
                    {
                        var oldC = GUI.color;
                        GUI.color = new Color(0.2f, 0.65f, 1f, 1f);
                        GUI.Box(new Rect(thumbRect.x - 2, thumbRect.y - 2, thumbW + 4, thumbH + 4), GUIContent.none);
                        GUI.color = oldC;
                    }

                    EditorGUIUtility.AddCursorRect(thumbRect, MouseCursor.Link);
                    if (Event.current.type == EventType.MouseDown && thumbRect.Contains(Event.current.mousePosition))
                    {
                        _selectedImageIndex = i;
                        Event.current.Use();
                    }

                    if (i < imgCount - 1) GUILayout.Space(6);
                }

                GUILayout.FlexibleSpace();
                GUILayout.EndHorizontal();
            }

            GUILayout.EndVertical();
        }

        private void DrawActionSection(ModelItemData model, EditorWindow parentWindow)
        {
            GUILayout.BeginVertical(EditorStyles.helpBox);

            string downloadUrl = model.GetPackageDownloadUrl(ModuleLibConfig.ServerUrl);

            if (_isDownloading)
            {
                // 下载与准备导入进度
                GUILayout.Label($"正在传输包体数据... {(_downloadProgress * 100f):F0}%", EditorStyles.boldLabel);
                Rect progRect = GUILayoutUtility.GetRect(EditorGUIUtility.currentViewWidth - 40, 20);
                EditorGUI.ProgressBar(progRect, _downloadProgress, $"{(_downloadProgress * 100f):F0}%");
                if (!string.IsNullOrEmpty(_statusMessage))
                {
                    GUILayout.Label(_statusMessage, EditorStyles.miniLabel);
                }
            }
            else
            {
                if (string.IsNullOrEmpty(downloadUrl))
                {
                    GUILayout.Label("该资源当前暂无附带包体文件", EditorStyles.centeredGreyMiniLabel);
                }
                else
                {
                    var oldCol = GUI.backgroundColor;
                    GUI.backgroundColor = new Color(0.2f, 0.75f, 0.4f, 1f);

                    string btnText = $" 📥 导入到当前工程 ({model.size:F1} MB)";
                    if (GUILayout.Button(btnText, ModuleLibStyles.BigActionButton))
                    {
                        StartEphemeralImportFlow(model, downloadUrl, parentWindow);
                    }

                    GUI.backgroundColor = oldCol;
                    GUILayout.Label("💡 提示：点击后将直接拉取并唤起 Unity 官方导入选择窗口，不产生任何本地冗余包体文件。", EditorStyles.centeredGreyMiniLabel);
                }
            }

            GUILayout.EndVertical();
        }

        private void StartEphemeralImportFlow(ModelItemData model, string downloadUrl, EditorWindow parentWindow)
        {
            if (string.IsNullOrEmpty(downloadUrl)) return;

            // 增加下载量并即时异步同步至服务端数据库
            model.IncrementDownloadCount(ModuleLibConfig.ServerUrl);

            // 每次下载前先清理可能存在的残留临时包
            ModuleLibCache.CleanAllTempPackages();

            // 在系统 Temp 临时目录创建毫秒级暂存文件（不在工程内，工程体积 0 增加）
            string tempPackagePath = ModuleLibCache.CreateTempPackagePath(model.zip_file);
            _isDownloading = true;
            _downloadProgress = 0f;
            _statusMessage = "连接服务器并传输数据中...";

            ModuleLibHttp.DownloadFile(downloadUrl, tempPackagePath,
                progress =>
                {
                    _downloadProgress = progress;
                    if (parentWindow != null) parentWindow.Repaint();
                },
                completedPath =>
                {
                    _isDownloading = false;
                    _downloadProgress = 1f;
                    _statusMessage = "";
                    if (parentWindow != null) parentWindow.Repaint();

                    // 启动 Unity 原生导入并挂载即生即死清理钩子
                    ExecuteInteractiveImportAndCleanup(completedPath);
                },
                error =>
                {
                    _isDownloading = false;
                    _statusMessage = "传输失败: " + error;
                    Debug.LogError("[ModuleLibDetailView] 获取包体失败: " + error);
                    DeleteTempFileWithRetry(tempPackagePath, 0);
                    if (parentWindow != null) parentWindow.Repaint();
                });
        }

        private void ExecuteInteractiveImportAndCleanup(string tempPackagePath)
        {
            if (!File.Exists(tempPackagePath))
            {
                EditorUtility.DisplayDialog("提示", "未找到包体临时数据！", "确定");
                return;
            }

            // 状态标记
            bool importStarted = false;
            bool cleanedUp = false;
            bool windowEverDetected = false;
            double windowClosedTime = 0;
            double startTime = EditorApplication.timeSinceStartup;

            Action cleanup = null;
            EditorApplication.CallbackFunction updateWatcher = null;
            AssetDatabase.ImportPackageCallback onStarted = null;
            AssetDatabase.ImportPackageCallback onCompleted = null;
            AssetDatabase.ImportPackageCallback onCancelled = null;
            AssetDatabase.ImportPackageFailedCallback onFailed = null;

            cleanup = () =>
            {
                if (cleanedUp) return;
                cleanedUp = true;

                if (updateWatcher != null)
                {
                    EditorApplication.update -= updateWatcher;
                    updateWatcher = null;
                }

                AssetDatabase.importPackageStarted -= onStarted;
                AssetDatabase.importPackageCompleted -= onCompleted;
                AssetDatabase.importPackageCancelled -= onCancelled;
                AssetDatabase.importPackageFailed -= onFailed;

                // 异步重试删除临时包体（防止 Unity 关闭窗口瞬间仍占用文件句柄）
                DeleteTempFileWithRetry(tempPackagePath, 0);
            };

            onStarted = packageName =>
            {
                importStarted = true;
            };

            onCompleted = packageName =>
            {
                cleanup();
            };

            onCancelled = packageName =>
            {
                cleanup();
            };

            onFailed = (packageName, errorMsg) =>
            {
                cleanup();
            };

            AssetDatabase.importPackageStarted += onStarted;
            AssetDatabase.importPackageCompleted += onCompleted;
            AssetDatabase.importPackageCancelled += onCancelled;
            AssetDatabase.importPackageFailed += onFailed;

            // 唤起 Unity 官方原生导入窗口（interactive: true 会展示勾选确认弹窗）
            AssetDatabase.ImportPackage(tempPackagePath, true);

            // 启动 Update 监听器：侦测 Unity PackageImport 弹窗生命周期
            // 如果用户点击取消或点击右上角 X 关闭窗口，Unity 并不会可靠派发 importPackageCancelled 事件，
            // 此时通过侦测弹窗关闭且未触发 importPackageStarted，精准判定取消并即时销毁临时文件！
            updateWatcher = () =>
            {
                if (cleanedUp) return;

                bool isWindowOpen = IsPackageImportWindowOpen();

                if (isWindowOpen)
                {
                    windowEverDetected = true;
                    windowClosedTime = 0;
                }
                else
                {
                    if (windowEverDetected)
                    {
                        // 弹窗曾打开，现在已关闭
                        if (windowClosedTime <= 0)
                        {
                            windowClosedTime = EditorApplication.timeSinceStartup;
                        }
                        else if (EditorApplication.timeSinceStartup - windowClosedTime >= 0.4)
                        {
                            // 窗口关闭超过 0.4 秒，且未触发开始导入
                            if (!importStarted)
                            {
                                // 用户点击了取消或右上角 X 叉掉弹窗，立即销毁临时文件
                                cleanup();
                                return;
                            }
                        }
                    }
                    else
                    {
                        // 超过 10 秒弹窗仍未出现且未开始导入，执行安全兜底清理
                        if (EditorApplication.timeSinceStartup - startTime > 10.0)
                        {
                            cleanup();
                            return;
                        }
                    }
                }

                // 安全兜底：导入耗时保护（若超过 300 秒，解绑并尝试清理）
                if (importStarted && EditorApplication.timeSinceStartup - startTime > 300.0)
                {
                    cleanup();
                }
            };

            EditorApplication.update += updateWatcher;
        }

        private static bool IsPackageImportWindowOpen()
        {
            try
            {
                var windows = Resources.FindObjectsOfTypeAll<EditorWindow>();
                if (windows != null)
                {
                    for (int i = 0; i < windows.Length; i++)
                    {
                        var w = windows[i];
                        if (w != null && w.GetType().Name.IndexOf("PackageImport", StringComparison.OrdinalIgnoreCase) >= 0)
                        {
                            return true;
                        }
                    }
                }
            }
            catch {}
            return false;
        }

        private static void DeleteTempFileWithRetry(string filePath, int retryCount)
        {
            if (string.IsNullOrEmpty(filePath) || !File.Exists(filePath)) return;

            try
            {
                File.Delete(filePath);
                string dir = Path.GetDirectoryName(filePath);
                if (Directory.Exists(dir) && Directory.GetFiles(dir).Length == 0 && Directory.GetDirectories(dir).Length == 0)
                {
                    try { Directory.Delete(dir); } catch {}
                }
            }
            catch (IOException)
            {
                // Unity 可能短暂占用文件句柄，200ms 后重试（最多 10 次）
                if (retryCount < 10)
                {
                    double nextTry = EditorApplication.timeSinceStartup + 0.2;
                    EditorApplication.CallbackFunction retryFn = null;
                    retryFn = () =>
                    {
                        if (EditorApplication.timeSinceStartup >= nextTry)
                        {
                            EditorApplication.update -= retryFn;
                            DeleteTempFileWithRetry(filePath, retryCount + 1);
                        }
                    };
                    EditorApplication.update += retryFn;
                }
            }
            catch (Exception ex)
            {
                Debug.LogWarning("[ModuleLibDetailView] 清理临时包体异常: " + ex.Message);
            }
        }

        private void DrawDescriptionSection(ModelItemData model)
        {
            GUILayout.BeginVertical(ModuleLibStyles.MarkdownBox);
            GUILayout.Label("资源介绍与使用指南", ModuleLibStyles.SectionHeader);
            GUILayout.Space(8);

            string desc = model.description ?? "";
            if (string.IsNullOrEmpty(desc))
            {
                GUILayout.Label("暂无详细介绍说明。", EditorStyles.centeredGreyMiniLabel);
            }
            else
            {
                RenderMarkdownContent(desc);
            }

            GUILayout.EndVertical();
        }

        /// <summary>
        /// 简易高效的 Markdown 文本流渲染器（支持标题、列表、粗体与超链接）
        /// </summary>
        private void RenderMarkdownContent(string markdown)
        {
            string[] lines = markdown.Split(new char[] { '\r', '\n' }, StringSplitOptions.RemoveEmptyEntries);

            for (int i = 0; i < lines.Length; i++)
            {
                string line = lines[i].Trim();
                if (string.IsNullOrEmpty(line)) continue;

                if (line.StartsWith("### "))
                {
                    GUILayout.Space(4);
                    GUILayout.Label(line.Substring(4), EditorStyles.boldLabel);
                }
                else if (line.StartsWith("## "))
                {
                    GUILayout.Space(6);
                    GUILayout.Label(line.Substring(3), EditorStyles.boldLabel);
                }
                else if (line.StartsWith("# "))
                {
                    GUILayout.Space(8);
                    GUILayout.Label(line.Substring(2), EditorStyles.boldLabel);
                }
                else if (line.StartsWith("- ") || line.StartsWith("* "))
                {
                    GUILayout.BeginHorizontal();
                    GUILayout.Space(12);
                    GUILayout.Label("• " + line.Substring(2), EditorStyles.wordWrappedLabel);
                    GUILayout.EndHorizontal();
                }
                else if (line.StartsWith("[") && line.Contains("](") && line.EndsWith(")"))
                {
                    // 超链接模式 [文本](URL)
                    Match match = Regex.Match(line, @"\[(.*?)\]\((.*?)\)");
                    if (match.Success)
                    {
                        string linkText = match.Groups[1].Value;
                        string linkUrl = match.Groups[2].Value;

                        GUILayout.BeginHorizontal();
                        GUILayout.Label("🔗 相关链接: ", EditorStyles.miniLabel, GUILayout.Width(64));
                        if (GUILayout.Button(linkText, EditorStyles.linkLabel))
                        {
                            Application.OpenURL(linkUrl);
                        }
                        GUILayout.FlexibleSpace();
                        GUILayout.EndHorizontal();
                    }
                    else
                    {
                        GUILayout.Label(line, EditorStyles.wordWrappedLabel);
                    }
                }
                else
                {
                    GUILayout.Label(line, EditorStyles.wordWrappedLabel);
                }
            }
        }
    }
}
