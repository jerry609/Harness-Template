param(
    [Parameter(Mandatory = $true)]
    [string]$Slug,
    [string]$Title
)

if ($Title) {
    python scripts/init_task.py $Slug $Title
} else {
    python scripts/init_task.py $Slug
}