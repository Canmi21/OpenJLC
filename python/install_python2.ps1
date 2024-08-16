# install_python2.ps1

# 检查是否有管理员权限
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)) {
    Write-Host "Requesting administrator permissions..."
    Start-Process PowerShell -ArgumentList "-File `"$PSCommandPath`"" -Verb RunAs
    exit
}

# 下载和安装Python
$pythonInstallerUrl = "https://www.python.org/ftp/python/2.7.18/python-2.7.18.amd64.msi"
$installerPath = "$PSScriptRoot\python-2.7.18.amd64.msi"

if (Test-Path $installerPath) {
    Write-Host "Found local installer: $installerPath"
} else {
    Write-Host "Local installer not found. Downloading Python 2.7.18..."
    Invoke-WebRequest -Uri $pythonInstallerUrl -OutFile $installerPath
}

Write-Host "Installing Python 2.7.18..."
Start-Process msiexec.exe -ArgumentList "/i `"$installerPath`" /quiet /norestart /l*v `"$PSScriptRoot\python_install.log`"" -Wait

Write-Host "Verifying installation..."
$pythonVersion = & python --version 2>&1
if ($pythonVersion -match "Python 2\.")
{
    Write-Host "Python 2 installed successfully: $pythonVersion"
}
else
{
    Write-Host "Installation failed. Please check the log file: $PSScriptRoot\python_install.log"
}

Start-Sleep -Seconds 3
