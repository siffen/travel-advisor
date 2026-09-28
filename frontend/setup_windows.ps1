$ErrorActionPreference = "Stop"

if (!(Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
}

npm install
Write-Host "Frontend setup complete. Run: npm run dev"
