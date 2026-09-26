using System;
using System.IO;
using UnityEditor;
using UnityEngine;

namespace JiangJian
{
    /// <summary>
    /// 资源库配置管理类
    /// 管理服务器地址、网络超时和本地磁盘缓存路径
    /// 兼容 Unity 2018+
    /// </summary>
    public static class ModuleLibConfig
    {
        private const string PrefKeyServerUrl = "JiangJian_ModuleLib_ServerUrl";
        private const string DefaultServerUrl = "http://127.0.0.1:5050";

        private static string _serverUrl;

        /// <summary>
        /// 服务端基础地址（例如 http://127.0.0.1:5050）
        /// </summary>
        public static string ServerUrl
        {
            get
            {
                if (string.IsNullOrEmpty(_serverUrl))
                {
                    _serverUrl = EditorPrefs.GetString(PrefKeyServerUrl, DefaultServerUrl);
                    if (string.IsNullOrEmpty(_serverUrl))
                    {
                        _serverUrl = DefaultServerUrl;
                    }
                }
                return _serverUrl.TrimEnd('/');
            }
            set
            {
                _serverUrl = (value ?? DefaultServerUrl).TrimEnd('/');
                EditorPrefs.SetString(PrefKeyServerUrl, _serverUrl);
            }
        }

        /// <summary>
        /// 重置为默认服务器地址
        /// </summary>
        public static void ResetToDefaultServerUrl()
        {
            ServerUrl = DefaultServerUrl;
        }

        /// <summary>
        /// 本地缓存根目录（位于工程 Library 目录下，避免污染 Assets 并在 Git 中被自然隔离）
        /// </summary>
        public static string CacheRootDirectory
        {
            get
            {
                string projectRoot = Path.GetDirectoryName(Application.dataPath);
                string cacheDir = Path.Combine(projectRoot, "Library", "ModuleLibCache");
                if (!Directory.Exists(cacheDir))
                {
                    Directory.CreateDirectory(cacheDir);
                }
                return cacheDir;
            }
        }

        /// <summary>
        /// 图片缩略图磁盘缓存目录
        /// </summary>
        public static string ThumbnailCacheDirectory
        {
            get
            {
                string dir = Path.Combine(CacheRootDirectory, "Thumbnails");
                if (!Directory.Exists(dir))
                {
                    Directory.CreateDirectory(dir);
                }
                return dir;
            }
        }

        /// <summary>
        /// 临时导入管道目录（位于系统临时目录中，不在工程内生成任何文件，导入完成后即生即删）
        /// </summary>
        public static string TempPackageDirectory
        {
            get
            {
                string dir = Path.Combine(Path.GetTempPath(), "UnityModuleLib", "TempPackages");
                if (!Directory.Exists(dir))
                {
                    Directory.CreateDirectory(dir);
                }
                return dir;
            }
        }

        /// <summary>
        /// 清理所有本地磁盘图片缓存
        /// </summary>
        public static void ClearThumbnailCache()
        {
            try
            {
                string dir = ThumbnailCacheDirectory;
                if (Directory.Exists(dir))
                {
                    Directory.Delete(dir, true);
                    Directory.CreateDirectory(dir);
                }
            }
            catch (Exception ex)
            {
                Debug.LogWarning("[ModuleLibConfig] 清理图片缓存失败: " + ex.Message);
            }
        }
    }
}
