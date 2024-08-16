# get-pip.ps1
# 检查是否有管理员权限
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)) {
    Write-Host "Requesting administrator permissions..."
    Start-Process PowerShell -ArgumentList "-File `"$PSCommandPath`"" -Verb RunAs
    exit
}

# 定义脚本路径和文件名
$scriptRoot = $PSScriptRoot
$getPipScript = "$scriptRoot\get-pip.py"
$pipWheel = "$scriptRoot\pip-24.2-py3-none-any.whl"

# 检查Python是否安装
$pythonVersion = & python --version 2>&1
if ($pythonVersion -notmatch "Python 2\.|Python 3\.")
{
    Write-Host "Python is not installed or not found in PATH."
    exit
}
Write-Host "Found Python: $pythonVersion"

# 检查get-pip.py是否存在
if (-Not (Test-Path $getPipScript)) {
    Write-Host "get-pip.py not found in $scriptRoot. Please ensure the script is in the same directory."
    exit
}

# 安装pip并指定镜像源
Write-Host "Installing pip using get-pip.py..."
& python $getPipScript $pipWheel --index-url https://pypi.tuna.tsinghua.edu.cn/simple --no-warn-script-location

# 检查pip是否成功安装
$pipVersion = & python -m pip --version 2>&1
if ($pipVersion -match "pip")
{
    Write-Host "Pip installed successfully: $pipVersion"
}
else
{
    Write-Host "Pip installation failed."
    exit
}

# 更新pip数据库并指定镜像源
Write-Host "Updating pip package database..."
& python -m pip install --upgrade pip --index-url https://pypi.tuna.tsinghua.edu.cn/simple

Write-Host "Pip database updated successfully."

Start-Sleep -Seconds 3
