param(
    [string]$ProjectDir = (Get-Location).Path,
    [string]$AdminUser = "Admin",
    [string]$AdminEmail = "admin@example.com",
    [string]$ServerHost = "127.0.0.1",
    [int]$Port = 8000,
    [switch]$UseEnvPassword
)

Set-Location $ProjectDir

if (-Not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python not found in PATH. Install Python and add to PATH."
    exit 1
}

$venvPath = Join-Path $ProjectDir "venv"
if (-Not (Test-Path $venvPath)) {
    Write-Host "Creating virtual environment at $venvPath..."
    python -m venv $venvPath
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create venv."
        exit 1
    }
}

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force | Out-Null

$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"
if (-Not (Test-Path $activateScript)) {
    Write-Error "Activation script not found: $activateScript"
    exit 1
}
. $activateScript

$venvPip = Join-Path $venvPath "Scripts\pip.exe"
if (-Not (Test-Path $venvPip)) {
    Write-Error "pip not found in venv: $venvPip"
    exit 1
}
& $venvPip install --upgrade pip setuptools wheel
if ($LASTEXITCODE -ne 0) {
    Write-Warning "Failed to upgrade pip; continuing."
}

$req = Join-Path $ProjectDir "requirements.txt"
if (Test-Path $req) {
    Write-Host "Installing dependencies from requirements.txt..."
    & $venvPip install -r $req
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Error installing dependencies."
        exit 1
    }
} else {
    Write-Host "requirements.txt not found — skipping dependency installation."
}

Write-Host "Applying migrations..."
& python manage.py migrate --noinput
if ($LASTEXITCODE -ne 0) {
    Write-Error "Error applying migrations."
    exit 1
}

if ($UseEnvPassword) {
    $envPassword = [Environment]::GetEnvironmentVariable("DJANGO_SUPERUSER_PASSWORD", "Process")
    if ([string]::IsNullOrEmpty($envPassword)) {
        Write-Error "Environment variable DJANGO_SUPERUSER_PASSWORD is not set."
        exit 1
    }
    $AdminPassword = $envPassword
} else {
    Write-Host "Enter password for superuser $AdminUser (input hidden):"
    $secure = Read-Host -AsSecureString
    if ($null -eq $secure) {
        Write-Error "Password not entered."
        exit 1
    }
    $bstr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    try {
        $AdminPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($bstr)
    } finally {
        [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
    }
    if ([string]::IsNullOrEmpty($AdminPassword)) {
        Write-Error "Password is empty."
        exit 1
    }
}

$tempPy = Join-Path $env:TEMP "create_or_update_superuser.py"
$pyCode = @"
from django.contrib.auth import get_user_model
import sys

User = get_user_model()
username = r'''$AdminUser'''
email = r'''$AdminEmail'''
password = r'''$AdminPassword'''

try:
    u, created = User.objects.get_or_create(username=username, defaults={'email': email, 'is_staff': True, 'is_superuser': True})
    u.email = email
    u.is_staff = True
    u.is_superuser = True
    u.set_password(password)
    u.save()
    if created:
        print('Superuser created')
    else:
        print('Superuser updated')
except Exception as e:
    print('ERROR:', e, file=sys.stderr)
    sys.exit(1)
"@
Set-Content -Path $tempPy -Value $pyCode -Encoding UTF8

Write-Host "Creating/updating superuser $AdminUser..."
& python $tempPy
$createExit = $LASTEXITCODE

Remove-Item $tempPy -ErrorAction SilentlyContinue

if ($createExit -ne 0) {
    Write-Error "Failed to create/update superuser."
    exit 1
}

$addr = "$ServerHost`:$Port"
Write-Host "Starting development server on $addr ..."
Write-Host "Stop server — Ctrl+C"
& python manage.py runserver $addr
