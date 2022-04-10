@echo off

echo [*] Starting Rebuild Process

cd ..

cd ..

echo -------------------------------------

echo [*] Removing Migrations Directory

rmdir /S /Q migrations

echo [*] Migrations Directory Removed

echo -------------------------------------

echo [*] Remvoing pyproject.toml

del pyproject.toml

echo [*] pyproject.toml Removed

echo -------------------------------------

echo [*] Initializing TORTOISE_CONFIG

aerich init -t db.tortoise.config.tortoise_config.TORTOISE_CONFIG

echo [*] TORTOISE_CONFIG Intialized

echo -------------------------------------

echo [*] Monkeypatching Aerich Error

fart.exe pyproject.toml ./migrations migrations

echo [*] Aerich Error Monkeypatched

echo -------------------------------------

echo [*] Initializing Database

aerich init-db

echo [*] Database Intialized

echo -------------------------------------

PAUSE
EXIT
