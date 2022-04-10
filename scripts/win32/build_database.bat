@echo off

echo [*] Starting Build Process

cd ..

cd ..

echo -------------------------------------

echo [*] Initializing TORTOISE_CONFIG

aerich init -t db.tortoise.config.tortoise_config.TORTOISE_CONFIG

echo [*] TORTOISE_CONFIG Initialized

echo -------------------------------------

echo [*] Monkeypatching Aerich Error

fart.exe pyproject.toml ./migrations migrations

echo [*] Aerich Error Monkeypatched

echo -------------------------------------

echo [*] Initializing Database

aerich init-db

echo [*] Database Initialized

echo -------------------------------------

PAUSE
EXIT
