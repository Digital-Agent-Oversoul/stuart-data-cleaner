#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Development Environment Setup for Data Cleaner Project
    
.DESCRIPTION
    This script ensures the development environment is properly configured
    and sets the working directory to the correct project location.
    
.NOTES
    This script is designed to work with the Stuart Multi-Project Workspace Manager.
    Run this script before starting development work to prevent
    file location confusion between Cursor workspace and project folder.
#>

# Set strict error handling
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Define project paths
$ProjectRoot = "C:\LocalAI\!projects\Stuart\data_cleaner"
$WorkspaceRoot = "C:\LocalAI\!projects\Stuart"
$CursorWorkspace = "C:\Users\Oversoul\.cursor"

Write-Host "🔧 Setting up Data Cleaner Development Environment" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Green

# Check if we're in the right project context
$WorkspaceConfig = "$WorkspaceRoot\workspace_config.json"
if (Test-Path $WorkspaceConfig) {
    try {
        $config = Get-Content $WorkspaceConfig | ConvertFrom-Json
        $activeProject = $config.projects.PSObject.Properties | Where-Object { $_.Value.active -eq $true }
        
        if ($activeProject -and $activeProject.Name -eq "data_cleaner") {
            Write-Host "✅ Project context verified: Data Cleaner is active" -ForegroundColor Green
        } else {
            Write-Host "⚠️  Warning: Data Cleaner is not the active project" -ForegroundColor Yellow
            Write-Host "💡 Consider running: ..\workspace_manager.ps1 -ProjectName data_cleaner" -ForegroundColor Cyan
        }
    }
    catch {
        Write-Host "⚠️  Could not verify project context from workspace config" -ForegroundColor Yellow
    }
}

# Verify project root exists
if (-not (Test-Path $ProjectRoot)) {
    Write-Error "Project root not found: $ProjectRoot"
    exit 1
}

# Change to project directory
Write-Host "📁 Changing to project directory: $ProjectRoot" -ForegroundColor Yellow
Set-Location $ProjectRoot

# Verify we're in the right place
$CurrentLocation = Get-Location
Write-Host "📍 Current working directory: $CurrentLocation" -ForegroundColor Cyan

if ($CurrentLocation.Path -ne $ProjectRoot) {
    Write-Error "Failed to set working directory to project root"
    exit 1
}

# Check for project root marker
if (-not (Test-Path ".project_root")) {
    Write-Error "Project root marker not found. Are you in the correct directory?"
    exit 1
}

# Verify project structure
Write-Host "🏗️  Verifying project structure..." -ForegroundColor Yellow
$RequiredDirs = @("core", "config", "workflows", "tests", "project_docs")
$MissingDirs = @()

foreach ($dir in $RequiredDirs) {
    if (Test-Path $dir) {
        Write-Host "  ✅ $dir/" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $dir/ (MISSING)" -ForegroundColor Red
        $MissingDirs += $dir
    }
}

if ($MissingDirs.Count -gt 0) {
    Write-Warning "Missing required directories: $($MissingDirs -join ', ')"
}

# Check for misplaced files in Cursor workspace
Write-Host "🔍 Checking for misplaced files in Cursor workspace..." -ForegroundColor Yellow
$MisplacedFiles = Get-ChildItem $CursorWorkspace -Recurse -ErrorAction SilentlyContinue | 
    Where-Object {$_.Name -like "*data_cleaner*" -or $_.Name -like "*stuart*" -or $_.Name -like "*unified*"}

if ($MisplacedFiles) {
    Write-Warning "Found potentially misplaced files in Cursor workspace:"
    foreach ($file in $MisplacedFiles) {
        Write-Warning "  $($file.FullName)"
    }
    Write-Host "💡 Consider running: ..\workspace_manager.ps1 -Cleanup" -ForegroundColor Yellow
} else {
    Write-Host "  ✅ Cursor workspace is clean" -ForegroundColor Green
}

Write-Host "=" * 60 -ForegroundColor Green
Write-Host "🚀 Data Cleaner Development Environment Ready!" -ForegroundColor Green
Write-Host "📝 All file operations should now be contained within: $ProjectRoot" -ForegroundColor Cyan
Write-Host "🔗 Reference files available at: $WorkspaceRoot" -ForegroundColor Cyan

# Display current project status
Write-Host "📊 Current Project Status:" -ForegroundColor Magenta
Get-ChildItem -Directory | ForEach-Object {
    $itemCount = (Get-ChildItem $_.FullName -Recurse -File | Measure-Object).Count
    Write-Host "  📁 $($_.Name)/ ($itemCount files)" -ForegroundColor White
}

# Show workspace management options
Write-Host ""
Write-Host "🔄 Workspace Management Commands:" -ForegroundColor Magenta
Write-Host "  ..\workspace_manager.ps1 -Status                    # Show workspace status" -ForegroundColor White
Write-Host "  ..\workspace_manager.ps1 -List                      # List all projects" -ForegroundColor White
Write-Host "  ..\workspace_manager.ps1 -ProjectName lwrap_overlays # Switch to LWrap project" -ForegroundColor White
Write-Host "  ..\workspace_manager.ps1 -Cleanup                   # Clean up Cursor workspace" -ForegroundColor White
