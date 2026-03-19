# test_api.ps1
# Interactive PowerShell script to test /api/movies endpoints

$baseUrl = "http://localhost:8000/api/movies"

function Show-Menu {
    Write-Host "`n=== Movie API Tester ==="
    Write-Host "1. GET all movies"
    Write-Host "2. POST (add) a movie"
    Write-Host "3. PUT (update) a movie"
    Write-Host "4. DELETE a movie"
    Write-Host "5. Exit"
}

function Get-Movies {
    $movies = Invoke-RestMethod -Uri $baseUrl -Method Get
    Write-Host "`nMovies in DB:"
    $movies | Format-Table
}

function Post-Movie {
    $title = Read-Host "Enter movie title"
    $genre = Read-Host "Enter movie genre"
    $rating = Read-Host "Enter movie rating (number)"
    $body = @{
        title = $title
        genre = $genre
        rating = [float]$rating
    } | ConvertTo-Json
    $response = Invoke-RestMethod -Uri $baseUrl -Method Post -Body $body -ContentType "application/json"
    Write-Host "`nMovie added:"
    $response | Format-Table
}

function Put-Movie {
    $id = Read-Host "Enter movie ID to update"
    if (-not ($id -match '^\d+$')) {
        Write-Host "Invalid ID. Please enter a number." -ForegroundColor Yellow
        return
    }
    $title = Read-Host "Enter new movie title"
    $genre = Read-Host "Enter new movie genre"
    $rating = Read-Host "Enter new movie rating (number)"
    $body = @{
        title = $title
        genre = $genre
        rating = [float]$rating
    } | ConvertTo-Json
    $response = Invoke-RestMethod -Uri "$baseUrl/$id" -Method Put -Body $body -ContentType "application/json"
    Write-Host "`nMovie updated:"
    $response | Format-Table
}

function Delete-Movie {
    $id = Read-Host "Enter movie ID to delete"
    if (-not ($id -match '^\d+$')) {
        Write-Host "Invalid ID. Please enter a number." -ForegroundColor Yellow
        return
    }
    Invoke-RestMethod -Uri "$baseUrl/$id" -Method Delete
    Write-Host "`nMovie deleted successfully."
}

# Main loop
$running = $true
while ($running) {
    Show-Menu
    $choice = Read-Host "Choose an option (1-5)"
    switch ($choice) {
        "1" { Get-Movies }
        "2" { Post-Movie }
        "3" { Put-Movie }
        "4" { Delete-Movie }
        "5" { 
            Write-Host "`nExiting tester..."
            $running = $false 
        }
        default { Write-Host "Invalid option. Choose 1-5." }
    }
}
