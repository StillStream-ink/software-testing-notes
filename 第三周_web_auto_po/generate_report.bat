@echo off
chcp 65001 >nul

echo [1/3] 复制历史数据...
if exist "allure-report\history" (
    xcopy "allure-report\history" "allure-results\history" /I /Y /Q
    echo 历史数据已复制
) else (
    echo 首次运行，无历史数据
)

echo [2/3] 复制 Categories 配置...
if exist "config\categories.json" (
    copy "config\categories.json" "allure-results\categories.json" /Y >nul
)

echo [3/3] 生成 Allure 报告...
allure generate allure-results -o allure-report --clean

echo.
echo 报告生成完成！正在打开...
start allure-report\index.html
allure open allure-report