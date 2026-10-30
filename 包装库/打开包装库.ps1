$ErrorActionPreference = 'Stop'
$taskLibraryRoot = Split-Path -Parent $PSCommandPath
$taskGalleryUrl = 'http://127.0.0.1:8769/index.html'

function Test-TaskGallery {
    try {
        $taskResponse = Invoke-WebRequest -Uri $taskGalleryUrl -UseBasicParsing -TimeoutSec 2
        return ($taskResponse.StatusCode -eq 200 -and $taskResponse.Content -match 'packaging-review-v1')
    } catch { return $false }
}

if (-not (Test-TaskGallery)) {
    $taskPythonCommand = Get-Command pythonw.exe, python.exe, py.exe -ErrorAction SilentlyContinue | Where-Object { $_.Source -notlike '*\WindowsApps\*' } | Select-Object -First 1
    if (-not $taskPythonCommand) { throw '请先安装 Python 3，并将 python 或 py 添加到 PATH。' }
    $taskPython = $taskPythonCommand.Source
    $taskServerScript = Join-Path $taskLibraryRoot 'tools\serve_gallery.py'
    Start-Process -FilePath $taskPython -ArgumentList ('"' + $taskServerScript + '"') -WorkingDirectory $taskLibraryRoot -WindowStyle Hidden
    $taskReady = $false
    for ($taskAttempt = 0; $taskAttempt -lt 20; $taskAttempt++) {
        if (Test-TaskGallery) { $taskReady = $true; break }
        Start-Sleep -Milliseconds 250
    }
    if (-not $taskReady) { throw '预览服务未启动，请检查8769端口是否被其他程序占用。' }
}

$taskChrome = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
if (Test-Path -LiteralPath $taskChrome -PathType Leaf) {
    Start-Process -FilePath $taskChrome -ArgumentList $taskGalleryUrl
} else {
    Start-Process $taskGalleryUrl
}
