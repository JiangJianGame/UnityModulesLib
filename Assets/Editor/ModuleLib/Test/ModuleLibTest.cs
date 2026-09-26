using System;
using System.Text;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

namespace JiangJian
{
    [Serializable]
    public class ModelListResponse
    {
        public int page;
        public int perPage;
        public int totalItems;
        public int totalPages;
        public ModelItemData[] items;
    }

    [Serializable]
    public class ModelItemData
    {
        public string id;
        public string title;
        public string author;
        public float size;
        public string view_Count;
        public string download_count;
        public string version;
        public string category;
        public string type;
        public string[] preview_images;
        public string zip_file;
        public string description;
        public ModelExpandData expand;
    }

    [Serializable]
    public class ModelExpandData
    {
        public CategoryData category;
        public TypeData type;
    }

    [Serializable]
    public class CategoryData
    {
        public string id;
        public string name;
    }

    [Serializable]
    public class TypeData
    {
        public string id;
        public string name;
        public int sort_order;
    }

    /// <summary>
    /// 测试脚本：从 PocketBase 获取并打印所有资源模块的数据列表信息
    /// 兼容 Unity 2018 及以上版本
    /// </summary>
    public static class ModuleLibTest
    {
        private const string BaseUrl = "http://127.0.0.1:5050";
        private const string ModelsUrl = BaseUrl + "/api/collections/models/records?perPage=50&sort=-created&expand=category,type";

        [MenuItem("Tools/资源商店/测试获取模块列表", priority = 1)]
        public static void FetchAndPrintModelList()
        {
            Debug.Log("<color=#4EA8DE><b>[ModuleLibTest]</b> 开始请求资源模块数据列表: " + ModelsUrl + "</color>");

            var request = UnityWebRequest.Get(ModelsUrl);
            var asyncOp = request.SendWebRequest();
            var startTime = EditorApplication.timeSinceStartup;

            EditorApplication.CallbackFunction updateAction = null;
            updateAction = () =>
            {
                // 超时处理（10秒）
                if (EditorApplication.timeSinceStartup - startTime > 10.0)
                {
                    EditorApplication.update -= updateAction;
                    request.Dispose();
                    Debug.LogError("<color=red><b>[ModuleLibTest]</b> 请求超时（10秒），请检查 PocketBase 服务是否已启动于 5050 端口！</color>");
                    return;
                }

                if (!asyncOp.isDone) return;

                EditorApplication.update -= updateAction;

                try
                {
#if UNITY_2020_1_OR_NEWER
                    bool isError = request.result != UnityWebRequest.Result.Success;
#else
                    bool isError = request.isNetworkError || request.isHttpError;
#endif

                    if (isError)
                    {
                        Debug.LogError("<color=red><b>[ModuleLibTest]</b> 请求失败: " + request.error + " (HTTP " + request.responseCode + ")</color>\n" + request.downloadHandler.text);
                        return;
                    }

                    string jsonText = request.downloadHandler.text;
                    var response = JsonUtility.FromJson<ModelListResponse>(jsonText);

                    if (response == null || response.items == null)
                    {
                        Debug.LogWarning("<color=yellow><b>[ModuleLibTest]</b> 数据解析为空或格式不匹配！原始 JSON：</color>\n" + jsonText);
                        return;
                    }

                    var sb = new StringBuilder();
                    sb.AppendLine($"<color=#52B788><b>[ModuleLibTest] 成功拉取到 {response.items.Length} 个资源模块！(总数: {response.totalItems})</b></color>");
                    sb.AppendLine("--------------------------------------------------------------------------------");

                    for (int i = 0; i < response.items.Length; i++)
                    {
                        var item = response.items[i];
                        string originName = item.expand != null && item.expand.category != null ? item.expand.category.name : item.category;
                        string typeName = item.expand != null && item.expand.type != null ? item.expand.type.name : item.type;
                        int previewCount = item.preview_images != null ? item.preview_images.Length : 0;

                        // 组装第一张预览图的访问 URL
                        string firstPreviewUrl = "无";
                        if (previewCount > 0)
                        {
                            firstPreviewUrl = $"{BaseUrl}/api/files/models/{item.id}/{item.preview_images[0]}?thumb=400x225";
                        }

                        // 包体下载 URL
                        string packageUrl = string.IsNullOrEmpty(item.zip_file) 
                            ? "无" 
                            : $"{BaseUrl}/api/files/models/{item.id}/{item.zip_file}";

                        sb.AppendLine($"<b>[{i + 1:D2}] {item.title}</b>");
                        sb.AppendLine($"   ├─ 来源分类: <color=#64B5F6>{originName}</color> | 资源类型: <color=#FFB74D>{typeName}</color>");
                        sb.AppendLine($"   ├─ 作者: <b>{item.author}</b> | 版本: v{item.version} | 大小: {item.size:F2} MB");
                        sb.AppendLine($"   ├─ 统计: 浏览量 {item.view_Count} 次 | 下载量 {item.download_count} 次");
                        sb.AppendLine($"   ├─ 预览图数量: {previewCount} 张 (缩略图: {firstPreviewUrl})");
                        sb.AppendLine($"   └─ 资源包体文件: {item.zip_file} (下载URL: {packageUrl})");
                    }

                    sb.AppendLine("--------------------------------------------------------------------------------");
                    Debug.Log(sb.ToString());
                }
                catch (Exception ex)
                {
                    Debug.LogError("<color=red><b>[ModuleLibTest]</b> 处理异常: " + ex.Message + "\n" + ex.StackTrace + "</color>");
                }
                finally
                {
                    request.Dispose();
                }
            };

            EditorApplication.update += updateAction;
        }
    }
}
