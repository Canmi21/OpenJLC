# config/Header.yaml
$headerFile = Join-Path -Path $PSScriptRoot -ChildPath "config/Header.yaml"
if (Test-Path $headerFile) {
    Remove-Item $headerFile -Force
    Write-Host "Removed: $headerFile"
}

# output
$outputDir = Join-Path -Path $PSScriptRoot -ChildPath "output"
if (Test-Path $outputDir) {
    Remove-Item $outputDir -Recurse -Force
    Write-Host "Removed: $outputDir"
}

Start-Sleep -Seconds 1

# Python
$pythonInstalled = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonInstalled) {
    $installPythonScript = Join-Path -Path $PSScriptRoot -ChildPath "python/install_python2.ps1"
    Write-Host "Python Not Found $installPythonScript"
    & $installPythonScript
    Exit
}

# pip
$pipInstalled = python -m pip --version 2>$null
if ($LASTEXITCODE -ne 0) {
    $installPipScript = Join-Path -Path $PSScriptRoot -ChildPath "pip/get-pip.ps1"
    Write-Host "Pip Not Found $installPipScript"
    & $installPipScript
    Exit
}

# init.py
$initScript = Join-Path -Path $PSScriptRoot -ChildPath "init.py"
Write-Host "Run: $initScript"
python $initScript

Start-Sleep -Seconds 3