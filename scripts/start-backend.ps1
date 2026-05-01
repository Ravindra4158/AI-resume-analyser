param()

$repoRoot = Split-Path -Parent $PSScriptRoot
$backendDir = Resolve-Path (Join-Path $repoRoot "backend")
$venvPython = Resolve-Path (Join-Path $backendDir ".venv\Scripts\python.exe")

Start-Process -FilePath $venvPython -ArgumentList @('-m','uvicorn','main:app','--host','127.0.0.1','--port','8000') -WorkingDirectory $backendDir
Write-Host "Backend started at http://127.0.0.1:8000"
