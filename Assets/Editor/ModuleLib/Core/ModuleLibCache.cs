using System;
using System.Collections.Generic;
using System.IO;
using System.Security.Cryptography;
using System.Text;
using UnityEngine;

namespace JiangJian
{
    /// <summary>
    /// 双层缓存管理器（内存字典 + 本地磁盘）
    /// 确保缩略图和原图在 Editor 会话中即时展示，无需重复消耗网络带宽
    /// 兼容 Unity 2018+
    /// </summary>
    public static class ModuleLibCache
    {
        private static readonly Dictionary<string, Texture2D> MemoryTextureCache = new Dictionary<string, Texture2D>();

        /// <summary>
        /// 从内存或磁盘获取已缓存的纹理，若未缓存则返回 null
        /// </summary>
        public static Texture2D GetTexture(string url)
        {
            if (string.IsNullOrEmpty(url)) return null;

            // 1. 检查内存缓存
            Texture2D tex;
            if (MemoryTextureCache.TryGetValue(url, out tex) && tex != null)
            {
                return tex;
            }

            // 2. 检查本地磁盘缓存
            string diskPath = GetDiskCachePath(url);
            if (File.Exists(diskPath))
            {
                try
                {
                    byte[] fileData = File.ReadAllBytes(diskPath);
                    var diskTex = new Texture2D(2, 2, TextureFormat.RGBA32, false);
                    diskTex.hideFlags = HideFlags.DontSave;
#if UNITY_2017_1_OR_NEWER
                    ImageConversion.LoadImage(diskTex, fileData);
#else
                    diskTex.LoadImage(fileData);
#endif
                    MemoryTextureCache[url] = diskTex;
                    return diskTex;
                }
                catch (Exception ex)
                {
                    Debug.LogWarning("[ModuleLibCache] 读取本地磁盘缓存图片失败: " + ex.Message);
                }
            }

            return null;
        }

        /// <summary>
        /// 将下载得到的纹理存入内存与磁盘缓存
        /// </summary>
        public static void SaveTexture(string url, Texture2D texture, byte[] rawBytes)
        {
            if (string.IsNullOrEmpty(url) || texture == null) return;

            texture.hideFlags = HideFlags.DontSave;
            MemoryTextureCache[url] = texture;

            // 保存到磁盘
            if (rawBytes != null && rawBytes.Length > 0)
            {
                try
                {
                    string diskPath = GetDiskCachePath(url);
                    File.WriteAllBytes(diskPath, rawBytes);
                }
                catch (Exception ex)
                {
                    Debug.LogWarning("[ModuleLibCache] 写入磁盘图片缓存失败: " + ex.Message);
                }
            }
        }

        /// <summary>
        /// 生成位于系统 Temp 目录的临时导入包路径（即用即删，工程目录 0 产生）
        /// </summary>
        public static string CreateTempPackagePath(string zipFile)
        {
            string fileName = string.IsNullOrEmpty(zipFile) ? "temp_module.unitypackage" : Path.GetFileName(zipFile);
            string safeName = Guid.NewGuid().ToString("N").Substring(0, 8) + "_" + fileName;
            return Path.Combine(ModuleLibConfig.TempPackageDirectory, safeName);
        }

        /// <summary>
        /// 清理系统临时目录中的残留暂存包
        /// </summary>
        public static void CleanAllTempPackages()
        {
            try
            {
                string dir = ModuleLibConfig.TempPackageDirectory;
                if (Directory.Exists(dir))
                {
                    string[] files = Directory.GetFiles(dir, "*", SearchOption.AllDirectories);
                    foreach (var f in files)
                    {
                        try { File.Delete(f); } catch {}
                    }
                    try { Directory.Delete(dir, true); } catch {}
                }
            }
            catch {}
        }

        /// <summary>
        /// 根据 URL 生成唯一的磁盘缓存文件名
        /// </summary>
        private static string GetDiskCachePath(string url)
        {
            using (var md5 = MD5.Create())
            {
                byte[] hash = md5.ComputeHash(Encoding.UTF8.GetBytes(url));
                var sb = new StringBuilder();
                for (int i = 0; i < hash.Length; i++)
                {
                    sb.Append(hash[i].ToString("x2"));
                }
                return Path.Combine(ModuleLibConfig.ThumbnailCacheDirectory, sb.ToString() + ".cache");
            }
        }

        /// <summary>
        /// 清理内存中的纹理缓存
        /// </summary>
        public static void ClearMemoryCache()
        {
            foreach (var kvp in MemoryTextureCache)
            {
                if (kvp.Value != null)
                {
                    UnityEngine.Object.DestroyImmediate(kvp.Value);
                }
            }
            MemoryTextureCache.Clear();
        }
    }
}
