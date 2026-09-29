using System;
using System.IO;
using System.Linq;
using System.Reflection;
using UnityEditor;
using UnityEditor.Compilation;
using UnityEngine;

namespace JiangJian
{
    /// <summary>
    /// 资源库独立 DLL 构建工具
    /// 支持一键将 Assets/Editor/ModuleLib 源码编译为标准 Editor DLL 及发布包
    /// </summary>
    public static class ModuleLibDllBuilder
    {
        private const string OutputDllName = "JiangJian.ModuleLib.Editor.dll";

        // 需要打包进 DLL 的 8 个核心源文件
        private static readonly string[] SourceFiles = new[]
        {
            "Assets/Editor/ModuleLib/Config/ModuleLibConfig.cs",
            "Assets/Editor/ModuleLib/Core/ModuleLibCache.cs",
            "Assets/Editor/ModuleLib/Core/ModuleLibData.cs",
            "Assets/Editor/ModuleLib/Core/ModuleLibHttp.cs",
            "Assets/Editor/ModuleLib/UI/ModuleLibDetailView.cs",
            "Assets/Editor/ModuleLib/UI/ModuleLibListView.cs",
            "Assets/Editor/ModuleLib/UI/ModuleLibStyles.cs",
            "Assets/Editor/ModuleLib/UI/ModuleLibWindow.cs"
        };

        [MenuItem("Tools/资源库/构建独立 DLL (Build DLL)", priority = 200)]
        public static void BuildDll()
        {
            BuildDllInternal(false);
        }

        [MenuItem("Tools/资源库/构建并导出 .unitypackage 发布包", priority = 201)]
        public static void BuildAndExportPackage()
        {
            BuildDllInternal(true);
        }

        [MenuItem("Tools/资源库/将已构建 DLL 打包为 .unitypackage", priority = 202)]
        public static void ExportExistingDllPackage()
        {
            string projectRoot = Path.GetDirectoryName(Application.dataPath);
            string dllPath = Path.Combine(projectRoot, "Build", "JiangJian.ModuleLib", "Editor", OutputDllName).Replace("\\", "/");
            if (!File.Exists(dllPath))
            {
                if (!Application.isBatchMode)
                {
                    EditorUtility.DisplayDialog("提示", "未找到已构建的 DLL，请先执行【构建独立 DLL】。", "确定");
                }
                return;
            }
            ExportUnityPackage(dllPath, projectRoot);
        }

        private static void BuildDllInternal(bool exportPackageAfterBuild)
        {
            // 1. 检查所有源文件是否存在
            foreach (var file in SourceFiles)
            {
                if (!File.Exists(file))
                {
                    EditorUtility.DisplayDialog("构建失败", $"找不到源文件:\n{file}", "确定");
                    return;
                }
            }

            // 2. 准备输出目录 (位于工程根目录下的 Build 目录，杜绝与 Assets 源码产生类冲突)
            string projectRoot = Path.GetDirectoryName(Application.dataPath);
            string buildDir = Path.Combine(projectRoot, "Build", "JiangJian.ModuleLib", "Editor");
            if (!Directory.Exists(buildDir))
            {
                Directory.CreateDirectory(buildDir);
            }

            string outputDllPath = Path.Combine(buildDir, OutputDllName).Replace("\\", "/");
            if (File.Exists(outputDllPath))
            {
                try { File.Delete(outputDllPath); } catch { }
            }

            Debug.Log($"[ModuleLibDllBuilder] 开始编译独立 DLL: {outputDllPath}");
            EditorUtility.DisplayProgressBar("构建 ModuleLib DLL", "正在编译核心源代码...", 0.3f);

            // 3. 配置 AssemblyBuilder
            var builder = new AssemblyBuilder(outputDllPath, SourceFiles);
            builder.flags = AssemblyBuilderFlags.EditorAssembly;
            builder.referencesOptions = ReferencesOptions.UseEngineModules;

            builder.buildStarted += delegate(string assemblyPath)
            {
                Debug.Log($"[ModuleLibDllBuilder] 编译进程已启动: {assemblyPath}");
            };

            builder.buildFinished += delegate(string assemblyPath, CompilerMessage[] messages)
            {
                EditorUtility.ClearProgressBar();

                int errorCount = messages != null ? messages.Count(m => m.type == CompilerMessageType.Error) : 0;
                int warningCount = messages != null ? messages.Count(m => m.type == CompilerMessageType.Warning) : 0;

                if (errorCount > 0)
                {
                    Debug.LogError($"[ModuleLibDllBuilder] 编译失败，出现 {errorCount} 个错误:");
                    foreach (var msg in messages.Where(m => m.type == CompilerMessageType.Error))
                    {
                        Debug.LogError($"  [{msg.file}:{msg.line}] {msg.message}");
                    }
                    EditorUtility.DisplayDialog("构建失败", $"编译出现 {errorCount} 个错误，请查看 Console 控制台日志。", "确定");
                    return;
                }

                if (warningCount > 0)
                {
                    foreach (var msg in messages.Where(m => m.type == CompilerMessageType.Warning))
                    {
                        Debug.LogWarning($"  [{msg.file}:{msg.line}] {msg.message}");
                    }
                }

                Debug.Log($"<color=#10B981>[ModuleLibDllBuilder] 编译成功！</color> 输出路径: {assemblyPath}");

                // 4. 生成配套的 README.md 与 Release 说明
                GenerateReleaseReadme(Path.GetDirectoryName(outputDllPath));

                // 5. 是否一键导出 .unitypackage
                if (exportPackageAfterBuild)
                {
                    ExportUnityPackage(outputDllPath, projectRoot);
                }
                else
                {
                    if (!Application.isBatchMode)
                    {
                        EditorUtility.RevealInFinder(outputDllPath);
                        EditorUtility.DisplayDialog("构建成功",
                            $"已成功生成独立 DLL 文件！\n\n文件: {OutputDllName}\n路径: {outputDllPath}\n\n可直接拷贝至任何项目的 Editor 目录下使用。", "确定");
                    }
                }
            };

            if (!builder.Build())
            {
                EditorUtility.ClearProgressBar();
                Debug.LogError("[ModuleLibDllBuilder] AssemblyBuilder 启动构建失败！");
                if (!Application.isBatchMode)
                {
                    EditorUtility.DisplayDialog("构建失败", "AssemblyBuilder 启动构建失败，请检查控制台输出。", "确定");
                }
            }
        }

        private static void GenerateReleaseReadme(string releaseDir)
        {
            string readmePath = Path.Combine(releaseDir, "README.md");
            string content = @"# JiangJian.ModuleLib.Editor.dll

## 简介
这是【资源库】前端资产管理器的独立预编译程序集（Editor-Only DLL）。
包含模块化资源浏览、筛选、多图预览、包体下载、断点解压与自动导入全套功能。

## 运行环境
- 兼容 Unity 2018.4+、Unity 2019.4+、Unity 2020.3+、Unity 2021.3+、Unity 2022.3+ 及 Unity 6
- 纯编辑器工具（Editor Assembly），零运行时开销

## 安装与使用方式
1. 将 `JiangJian.ModuleLib.Editor.dll` 放置于任何 Unity 项目的任意 `Editor` 目录下（例如 `Assets/Plugins/Editor/` 或 `Assets/Editor/`）。
2. 在 Unity 顶部菜单点击 `Window -> 资源库` (快捷键: `Ctrl+Shift+X` / `Cmd+Shift+X`) 或 `Tools -> 资源库 -> 打开资源库窗口` 即可立即使用。
3. DLL 模式下无需编译源码，完全免除 Domain Reload 等待时间。
";
            File.WriteAllText(readmePath, content, System.Text.Encoding.UTF8);
        }

        private static void ExportUnityPackage(string dllFilePath, string projectRoot)
        {
            try
            {
                // 临时暂存到 Assets 目录以调用 AssetDatabase.ExportPackage
                string tempDir = "Assets/JiangJianModuleLib_Staging/Editor";
                Directory.CreateDirectory(tempDir);
                string tempDllPath = Path.Combine(tempDir, OutputDllName).Replace("\\", "/");
                File.Copy(dllFilePath, tempDllPath, true);
                AssetDatabase.Refresh(ImportAssetOptions.ForceSynchronousImport);

                // 配置 meta 属性为仅限 Editor
                var importer = AssetImporter.GetAtPath(tempDllPath) as PluginImporter;
                if (importer != null)
                {
                    importer.SetCompatibleWithAnyPlatform(false);
                    importer.SetCompatibleWithEditor(true);
                    importer.SaveAndReimport();
                }

                string pkgDir = Path.Combine(projectRoot, "Build");
                Directory.CreateDirectory(pkgDir);
                string pkgPath = Path.Combine(pkgDir, "JiangJian.ModuleLib_v1.0.0.unitypackage").Replace("\\", "/");

                AssetDatabase.ExportPackage("Assets/JiangJianModuleLib_Staging", pkgPath, ExportPackageOptions.Recurse);
                Debug.Log($"<color=#10B981>[ModuleLibDllBuilder] UnityPackage 导出成功！</color> 路径: {pkgPath}");

                // 清理临时暂存目录
                AssetDatabase.DeleteAsset("Assets/JiangJianModuleLib_Staging");
                AssetDatabase.Refresh(ImportAssetOptions.ForceSynchronousImport);

                if (!Application.isBatchMode)
                {
                    EditorUtility.RevealInFinder(pkgPath);
                    EditorUtility.DisplayDialog("导出发布包成功",
                        $"已成功生成 .unitypackage 发布包！\n\n路径: {pkgPath}\n\n可以直接双击安装或分发给其他工程使用。", "确定");
                }
            }
            catch (Exception ex)
            {
                Debug.LogError("[ModuleLibDllBuilder] 导出 UnityPackage 失败: " + ex.Message);
                EditorUtility.DisplayDialog("导出失败", "导出 UnityPackage 时发生异常: " + ex.Message, "确定");
            }
        }
    }
}
