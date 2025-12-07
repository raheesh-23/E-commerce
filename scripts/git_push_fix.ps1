```powershell
param(
    [string]$ForkUser = "kabilanb29",   # change to your GitHub username if different
    [string]$Branch = "main",
    [switch]$UseSSH
)

Write-Host "1) Showing current git remotes..."
git remote -v

Write-Host "`n2) Current origin URL (if any):"
$origin = git remote get-url origin 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "No origin remote configured."
} else {
    Write-Host $origin
}

Write-Host "`n3) Common fixes:"
Write-Host " - If you don't have write access to the remote repo (403), either push to your fork or ask the repo owner to add you as collaborator."
Write-Host " - To push to your fork, the script can set origin to your fork and attempt the push."

if ($UseSSH) {
    $newUrl = "git@github.com:$ForkUser/E-commerce.git"
} else {
    $newUrl = "https://github.com/$ForkUser/E-commerce.git"
}

Write-Host "`nProposed origin for your fork: $newUrl"
$confirm = Read-Host "Set origin to this URL and push branch '$Branch'? (y/n)"
if ($confirm -ne 'y') {
    Write-Host "Aborted by user. Use the commands below manually if needed:"
    Write-Host "  git remote set-url origin $newUrl"
    Write-Host "  git push -u origin $Branch"
    return
}

# set origin (create if missing)
if ($origin) {
    git remote set-url origin $newUrl
} else {
    git remote add origin $newUrl
}

# configure credential helper (Windows)
Write-Host "Configuring Windows credential helper (manager-core) to store PAT if needed..."
git config --global credential.helper manager-core

Write-Host "Attempting to push..."
git push -u origin $Branch

if ($LASTEXITCODE -ne 0) {
    Write-Host "`nPush failed. Common reasons:"
    Write-Host " - You don't have a fork named 'E-commerce' under $ForkUser. Create a fork first and re-run."
    Write-Host " - For HTTPS, you need a Personal Access Token (PAT) instead of password. Visit https://github.com/settings/tokens to create one and re-run when prompted."
    Write-Host " - For SSH, ensure your public key is added to GitHub and use -UseSSH switch."
    Write-Host "`nUseful manual commands:"
    Write-Host "  git remote -v"
    Write-Host "  git remote set-url origin <your-fork-url>"
    Write-Host "  git push -u origin $Branch"
    Write-Host "  OR to push to the original repo (requires access): git push -u https://<username>:<PAT>@github.com/raheesh-23/E-commerce.git $Branch"
} else {
    Write-Host "Push succeeded."
}
```