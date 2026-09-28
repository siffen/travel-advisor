$ErrorActionPreference = "Stop"

Write-Host "Creating Python virtual environment..."
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1

Write-Host "Installing backend dependencies..."
pip install -r requirements.txt

if (!(Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example. Update PostgreSQL credentials before continuing."
}

Write-Host "Running migrations..."
python manage.py makemigrations travel
python manage.py migrate

Write-Host "Loading Travel Advisor destinations..."
python manage.py seed_data

Write-Host "Backend setup complete. Run: python manage.py runserver"
