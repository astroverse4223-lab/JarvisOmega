# Quick Git Push - Simple version

# Get commit message from user or use default
$message = Read-Host "Commit message (or press Enter for default)"
if ([string]::IsNullOrWhiteSpace($message)) {
    $message = "Update JARVIS Omega - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
}

# Run the full script
& "$PSScriptRoot\git-push.ps1" -CommitMessage $message
