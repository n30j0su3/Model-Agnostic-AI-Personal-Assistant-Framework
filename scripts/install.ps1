param(
    [switch]$llm
)

$root = Resolve-Path (Join-Path $PSScriptRoot "..")

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command py -ErrorAction SilentlyContinue
    if (-not $python) {
        Write-Host "[ERROR] Python no encontrado. Instala Python 3.11+ y reintenta."
        exit 1
    }
    $pythonExe = "py"
    $pythonArgs = "-3"
} else {
    $pythonExe = "python"
    $pythonArgs = ""
}

$scriptPath = Join-Path $root "scripts\install.py"
$argsList = @()
if ($llm) { $argsList += "--llm" }

if ($pythonArgs) {
    & $pythonExe $pythonArgs $scriptPath @argsList
} else {
    & $pythonExe $scriptPath @argsList
}
