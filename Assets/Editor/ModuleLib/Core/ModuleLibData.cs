using System;
using UnityEngine;

namespace JiangJian
{
    #region Data Transfer Objects (DTO) for JsonUtility

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
        public string created;
        public string updated;
        public ModelExpandData expand;

        /// <summary>
        /// 获取来源名称（如：模块库 / 插件库）
        /// </summary>
        public string GetCategoryName()
        {
            if (expand != null && expand.category != null && !string.IsNullOrEmpty(expand.category.name))
            {
                return expand.category.name;
            }
            return !string.IsNullOrEmpty(category) ? category : "未知来源";
        }

        /// <summary>
        /// 获取资源类型名称（如：3D / 2D / 音频 / 模板 / 工具 / 视觉特效）
        /// </summary>
        public string GetTypeName()
        {
            if (expand != null && expand.type != null && !string.IsNullOrEmpty(expand.type.name))
            {
                return expand.type.name;
            }
            return !string.IsNullOrEmpty(type) ? type : "通用";
        }

        /// <summary>
        /// 是否为内部自制模块库
        /// </summary>
        public bool IsInternalModule()
        {
            string catName = GetCategoryName();
            return catName.Contains("模块") || category == "5q010nwkhziyuby";
        }

        /// <summary>
        /// 是否为外部导入插件库
        /// </summary>
        public bool IsPluginModule()
        {
            string catName = GetCategoryName();
            return catName.Contains("插件") || catName.Contains("商店") || category == "gei2blqbraoocsv";
        }

        /// <summary>
        /// 格式化浏览量为整型数值（用于排序）
        /// </summary>
        public int GetViewCountInt()
        {
            int val;
            if (int.TryParse(view_Count, out val)) return val;
            return 0;
        }

        /// <summary>
        /// 格式化下载量为整型数值（用于排序）
        /// </summary>
        public int GetDownloadCountInt()
        {
            int val;
            if (int.TryParse(download_count, out val)) return val;
            return 0;
        }

        /// <summary>
        /// 获取首张缩略图的下载 URL
        /// </summary>
        public string GetFirstThumbnailUrl(string baseUrl)
        {
            if (preview_images != null && preview_images.Length > 0 && !string.IsNullOrEmpty(preview_images[0]))
            {
                return $"{baseUrl}/api/files/models/{id}/{preview_images[0]}?thumb=400x225";
            }
            return null;
        }

        /// <summary>
        /// 获取指定索引的完整预览图 URL
        /// </summary>
        public string GetPreviewImageUrl(string baseUrl, int index)
        {
            if (preview_images != null && index >= 0 && index < preview_images.Length && !string.IsNullOrEmpty(preview_images[index]))
            {
                return $"{baseUrl}/api/files/models/{id}/{preview_images[index]}";
            }
            return null;
        }

        /// <summary>
        /// 获取资源包体文件的完整下载 URL
        /// </summary>
        public string GetPackageDownloadUrl(string baseUrl)
        {
            if (!string.IsNullOrEmpty(zip_file))
            {
                return $"{baseUrl}/api/files/models/{id}/{zip_file}";
            }
            return null;
        }
    }

    [Serializable]
    public class ModelExpandData
    {
        public CategoryData category;
        public TypeData type;
    }

    [Serializable]
    public class CategoryListResponse
    {
        public int page;
        public int perPage;
        public int totalItems;
        public CategoryData[] items;
    }

    [Serializable]
    public class CategoryData
    {
        public string id;
        public string name;
    }

    [Serializable]
    public class TypeListResponse
    {
        public int page;
        public int perPage;
        public int totalItems;
        public TypeData[] items;
    }

    [Serializable]
    public class TypeData
    {
        public string id;
        public string name;
        public int sort_order;
    }

    [Serializable]
    public class BannerListResponse
    {
        public int page;
        public int perPage;
        public int totalItems;
        public BannerData[] items;
    }

    [Serializable]
    public class BannerData
    {
        public string id;
        public string model;
        public BannerExpandData expand;
    }

    [Serializable]
    public class BannerExpandData
    {
        public ModelItemData model;
    }

    #endregion

    #region Filtering & Sorting Enums

    /// <summary>
    /// 来源分类筛选
    /// </summary>
    public enum OriginFilterType
    {
        All = 0,            // 全部
        Internal = 1,       // 模块库（自制模块）
        Plugin = 2,         // 插件库
        Store = 2           // 兼容别名
    }

    /// <summary>
    /// 排序方式
    /// </summary>
    public enum SortOption
    {
        Newest = 0,         // 最新发布
        MostViews = 1,      // 最多浏览
        MostDownloads = 2,  // 最多下载
        TitleAsc = 3        // 名称升序
    }

    #endregion
}
