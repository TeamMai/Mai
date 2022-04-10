@echo off

echo [*] Starting Upgrade Process

cd ..

cd ..

echo -------------------------------------

echo [*] Starting Migrate Process

aerich migrate

echo [*] Migrating Done

echo -------------------------------------

echo [*] Starting Upgrade Process

aerich upgrade

echo [*] Upgrade Done

echo -------------------------------------

echo [*] Database Upgraded

PAUSE
EXIT
