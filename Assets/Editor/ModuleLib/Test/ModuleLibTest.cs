using System;
using System.Text;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

namespace JiangJian
{
    /// <summary>
    /// 测试脚本：从 PocketBase 获取并打印所有资源模块的数据列表信息
    /// 兼容 Unity 2018 及以上版本
    /// </summary>
    public static class ModuleLibTest
    {
        private static string ModelsUrl => ModuleLibConfig.ServerUrl + "/api/collections/models/records?perPage=50&sort=-created&expand=category,type";

        [MenuItem("Tools/资源库/测试获取模块列表", priority = 10)]
        public static void FetchAndPrintModelList()
        {
            Debug.Log("<color=#4EA8DE><b>[ModuleLibTest]</b> 开始请求资源模块数据列表: " + ModelsUrl + "</color>");

            ModuleLibHttp.GetJson<ModelListResponse>(ModelsUrl,
                response =>
                {
                    if (response == null || response.items == null)
                    {
                        Debug.LogWarning("<color=yellow><b>[ModuleLibTest]</b> 数据解析为空或格式不匹配！</color>");
                        return;
                    }

                    var sb = new StringBuilder();
                    sb.AppendLine($"<color=#52B788><b>[ModuleLibTest] 成功拉取到 {response.items.Length} 个资源模块！(总数: {response.totalItems})</b></color>");
                    sb.AppendLine("--------------------------------------------------------------------------------");

                    string baseUrl = ModuleLibConfig.ServerUrl;

                    for (int i = 0; i < response.items.Length; i++)
                    {
                        var item = response.items[i];
                        string originName = item.GetCategoryName();
                        string typeName = item.GetTypeName();
                        int previewCount = item.preview_images != null ? item.preview_images.Length : 0;
                        string firstPreviewUrl = item.GetFirstThumbnailUrl(baseUrl) ?? "无";
                        string packageUrl = item.GetPackageDownloadUrl(baseUrl) ?? "无";

                        sb.AppendLine($"<b>[{i + 1:D2}] {item.title}</b>");
                        sb.AppendLine($"   ├─ 来源分类: <color=#64B5F6>{originName}</color> | 资源类型: <color=#FFB74D>{typeName}</color>");
                        sb.AppendLine($"   ├─ 作者: <b>{item.author}</b> | 版本: v{item.version} | 大小: {item.size:F2} MB");
                        sb.AppendLine($"   ├─ 统计: 浏览量 {item.view_Count} 次 | 下载量 {item.download_count} 次");
                        sb.AppendLine($"   ├─ 预览图数量: {previewCount} 张 (缩略图: {firstPreviewUrl})");
                        sb.AppendLine($"   └─ 资源包体文件: {item.zip_file} (下载URL: {packageUrl})");
                    }

                    sb.AppendLine("--------------------------------------------------------------------------------");
                    Debug.Log(sb.ToString());
                },
                error =>
                {
                    Debug.LogError("<color=red><b>[ModuleLibTest]</b> 请求失败: " + error + "</color>");
                });
        }
    }
}
