# PowerShell script to update README.md via GitHub API
# This bypasses the large repository push timeout issue

$repo = "reichert-sentinel-ai/guardian-fraud-analytics"
$filePath = "README.md"

# Read the current README
$readmeContent = Get-Content "README.md" -Raw -Encoding UTF8
$contentBytes = [System.Text.Encoding]::UTF8.GetBytes($readmeContent)
$base64Content = [System.Convert]::ToBase64String($contentBytes)

# Get the current file SHA from GitHub
Write-Host "Fetching current file SHA from GitHub..."
$currentFile = gh api "repos/$repo/contents/$filePath" | ConvertFrom-Json
$sha = $currentFile.sha

Write-Host "Current SHA: $sha"
Write-Host "File size: $($readmeContent.Length) characters"

# Create the update payload
$payload = @{
    message = "Fix code block formatting in README.md - replace malformed markers"
    content = $base64Content
    sha = $sha
} | ConvertTo-Json

# Update the file via API
Write-Host "Updating README.md via GitHub API..."
try {
    $result = gh api -X PUT "repos/$repo/contents/$filePath" --input - <<< $payload
    Write-Host "Success! README.md updated on GitHub."
    Write-Host $result
} catch {
    Write-Host "Error updating file: $_"
    Write-Host "You may need to update the file manually via GitHub web interface"
}

