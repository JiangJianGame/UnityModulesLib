using System;
using System.Collections.Generic;
using System.IO;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

namespace JiangJian
{
    /// <summary>
    /// 编辑器专属非阻塞 HTTP 异步请求封装
    /// 由 EditorApplication.update 驱动，兼容 Unity 2018+
    /// </summary>
    public static class ModuleLibHttp
    {
        // 正在进行的纹理请求回调集合，防止对同一 URL 重复发起并发下载
        private static readonly Dictionary<string, List<Action<Texture2D>>> PendingTextureCallbacks = new Dictionary<string, List<Action<Texture2D>>>();

        /// <summary>
        /// 异步 GET 请求并反序列化为 JSON 对象
        /// </summary>
        public static void GetJson<T>(string url, Action<T> onSuccess, Action<string> onError = null, float timeoutSeconds = 10f) where T : class
        {
            var request = UnityWebRequest.Get(url);
            var asyncOp = request.SendWebRequest();
            var startTime = EditorApplication.timeSinceStartup;

            EditorApplication.CallbackFunction updateAction = null;
            updateAction = () =>
            {
                if (EditorApplication.timeSinceStartup - startTime > timeoutSeconds)
                {
                    EditorApplication.update -= updateAction;
                    request.Dispose();
                    string timeoutMsg = $"请求超时 ({timeoutSeconds:F1}s): {url}";
                    Debug.LogWarning("[ModuleLibHttp] " + timeoutMsg);
                    if (onError != null) onError(timeoutMsg);
                    return;
                }

                if (!asyncOp.isDone) return;

                EditorApplication.update -= updateAction;

                try
                {
                    if (HasError(request))
                    {
                        string err = $"HTTP 请求失败: {request.error} (Code {request.responseCode})";
                        if (onError != null) onError(err);
                        return;
                    }

                    string json = request.downloadHandler.text;
                    T data = JsonUtility.FromJson<T>(json);
                    if (data != null)
                    {
                        if (onSuccess != null) onSuccess(data);
                    }
                    else
                    {
                        string err = "JSON 解析结果为空: " + json;
                        if (onError != null) onError(err);
                    }
                }
                catch (Exception ex)
                {
                    string err = "处理响应异常: " + ex.Message;
                    if (onError != null) onError(err);
                }
                finally
                {
                    request.Dispose();
                }
            };

            EditorApplication.update += updateAction;
        }

        /// <summary>
        /// 异步加载纹理（集成 ModuleLibCache 双层缓存，带多重请求合并）
        /// </summary>
        public static void GetTexture(string url, Action<Texture2D> onSuccess, Action<string> onError = null)
        {
            if (string.IsNullOrEmpty(url))
            {
                if (onError != null) onError("URL 为空");
                return;
            }

            // 1. 尝试从缓存读取
            var cached = ModuleLibCache.GetTexture(url);
            if (cached != null)
            {
                if (onSuccess != null) onSuccess(cached);
                return;
            }

            // 2. 检查是否已有针对该 URL 的下载任务正在进行
            List<Action<Texture2D>> callbacks;
            if (PendingTextureCallbacks.TryGetValue(url, out callbacks))
            {
                if (onSuccess != null) callbacks.Add(onSuccess);
                return;
            }

            callbacks = new List<Action<Texture2D>>();
            if (onSuccess != null) callbacks.Add(onSuccess);
            PendingTextureCallbacks[url] = callbacks;

            // 3. 发起网络请求
            var request = UnityWebRequestTexture.GetTexture(url);
            var asyncOp = request.SendWebRequest();
            var startTime = EditorApplication.timeSinceStartup;

            EditorApplication.CallbackFunction updateAction = null;
            updateAction = () =>
            {
                if (EditorApplication.timeSinceStartup - startTime > 15f)
                {
                    EditorApplication.update -= updateAction;
                    request.Dispose();
                    PendingTextureCallbacks.Remove(url);
                    if (onError != null) onError("加载图片超时: " + url);
                    return;
                }

                if (!asyncOp.isDone) return;

                EditorApplication.update -= updateAction;

                try
                {
                    if (!HasError(request))
                    {
                        var tex = DownloadHandlerTexture.GetContent(request);
                        byte[] rawBytes = request.downloadHandler.data;
                        ModuleLibCache.SaveTexture(url, tex, rawBytes);

                        List<Action<Texture2D>> cbs;
                        if (PendingTextureCallbacks.TryGetValue(url, out cbs))
                        {
                            PendingTextureCallbacks.Remove(url);
                            for (int i = 0; i < cbs.Count; i++)
                            {
                                if (cbs[i] != null) cbs[i](tex);
                            }
                        }
                    }
                    else
                    {
                        PendingTextureCallbacks.Remove(url);
                        if (onError != null) onError(request.error);
                    }
                }
                catch (Exception ex)
                {
                    PendingTextureCallbacks.Remove(url);
                    if (onError != null) onError(ex.Message);
                }
                finally
                {
                    request.Dispose();
                }
            };

            EditorApplication.update += updateAction;
        }

        /// <summary>
        /// 异步下载文件（带平滑进度回调）
        /// </summary>
        public static void DownloadFile(string url, string savePath, Action<float> onProgress, Action<string> onComplete, Action<string> onError)
        {
            string dir = Path.GetDirectoryName(savePath);
            if (!string.IsNullOrEmpty(dir) && !Directory.Exists(dir))
            {
                Directory.CreateDirectory(dir);
            }

            var request = new UnityWebRequest(url, UnityWebRequest.kHttpVerbGET);
            var bufferHandler = new DownloadHandlerBuffer();
            request.downloadHandler = bufferHandler;
            var asyncOp = request.SendWebRequest();

            float lastProgressReportTime = 0f;

            EditorApplication.CallbackFunction updateAction = null;
            updateAction = () =>
            {
                // 限频上报进度（每 100ms 刷新一次）
                float now = (float)EditorApplication.timeSinceStartup;
                if (now - lastProgressReportTime > 0.1f)
                {
                    lastProgressReportTime = now;
                    if (onProgress != null) onProgress(request.downloadProgress);
                }

                if (!asyncOp.isDone) return;

                EditorApplication.update -= updateAction;

                try
                {
                    bool isError = HasError(request);
                    if (isError)
                    {
                        if (File.Exists(savePath)) File.Delete(savePath);
                        if (onError != null) onError(request.error);
                    }
                    else
                    {
                        // 全内存接收完成后原子写入目标路径，杜绝任何 0 字节磁盘占位 .tmp 文件
                        byte[] bytes = bufferHandler.data;
                        if (bytes != null && bytes.Length > 0)
                        {
                            File.WriteAllBytes(savePath, bytes);
                        }
                        if (onProgress != null) onProgress(1f);
                        if (onComplete != null) onComplete(savePath);
                    }
                }
                catch (Exception ex)
                {
                    if (onError != null) onError(ex.Message);
                }
                finally
                {
                    request.Dispose();
                    bufferHandler.Dispose();
                }
            };

            EditorApplication.update += updateAction;
        }

        /// <summary>
        /// 异步 PATCH 请求（用于更新记录统计信息等）
        /// </summary>
        public static void PatchJson(string url, string jsonBody, Action onSuccess = null, Action<string> onError = null, float timeoutSeconds = 10f)
        {
            var request = new UnityWebRequest(url, "PATCH");
            byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(jsonBody);
            request.uploadHandler = new UploadHandlerRaw(bodyRaw);
            request.downloadHandler = new DownloadHandlerBuffer();
            request.SetRequestHeader("Content-Type", "application/json");

            var asyncOp = request.SendWebRequest();
            var startTime = EditorApplication.timeSinceStartup;

            EditorApplication.CallbackFunction updateAction = null;
            updateAction = () =>
            {
                if (EditorApplication.timeSinceStartup - startTime > timeoutSeconds)
                {
                    EditorApplication.update -= updateAction;
                    request.Dispose();
                    if (onError != null) onError($"请求超时 ({timeoutSeconds:F1}s): {url}");
                    return;
                }

                if (!asyncOp.isDone) return;

                EditorApplication.update -= updateAction;

                try
                {
                    if (HasError(request))
                    {
                        string err = $"PATCH 请求失败: {request.error} (Code {request.responseCode})";
                        if (onError != null) onError(err);
                    }
                    else
                    {
                        if (onSuccess != null) onSuccess();
                    }
                }
                catch (Exception ex)
                {
                    string err = "处理响应异常: " + ex.Message;
                    if (onError != null) onError(err);
                }
                finally
                {
                    request.Dispose();
                }
            };

            EditorApplication.update += updateAction;
        }

        /// <summary>
        /// 跨版本安全判断 UnityWebRequest 是否发生错误
        /// 兼顾 Unity 2018.4 到 Unity 2022+ 及 Unity 6，防止编译为 DLL 后出现跨版本 MissingMethodException
        /// </summary>
        public static bool HasError(UnityWebRequest request)
        {
            if (request == null) return true;
            try
            {
                // Unity 2020.1+ 推荐属性 result
                var resultProp = typeof(UnityWebRequest).GetProperty("result");
                if (resultProp != null)
                {
                    var val = (int)resultProp.GetValue(request, null);
                    // UnityWebRequest.Result.Success == 1
                    return val != 1;
                }

                // Unity 2018 / 2019 属性 isNetworkError || isHttpError
                var isNetErr = typeof(UnityWebRequest).GetProperty("isNetworkError");
                var isHttpErr = typeof(UnityWebRequest).GetProperty("isHttpError");
                bool netErr = isNetErr != null && (bool)isNetErr.GetValue(request, null);
                bool httpErr = isHttpErr != null && (bool)isHttpErr.GetValue(request, null);
                return netErr || httpErr;
            }
            catch
            {
                return !string.IsNullOrEmpty(request.error);
            }
        }
    }
}
