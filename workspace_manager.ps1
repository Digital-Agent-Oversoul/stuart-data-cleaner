#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Multi-Project Workspace Manager for Stuart Projects
    
.DESCRIPTION
    This script manages multiple projects within the Stuart workspace,
    allowing easy switching between projects while maintaining clear boundaries.
    
.PARAMETER ProjectName
    Name of the project to activate (data_cleaner, lwrap_overlays, etc.)
    
.PARAMETER List
    List all available projects and their status
    
.PARAMETER Status
    Show current workspace status
    
.PARAMETER Cleanup
    Clean up Cursor workspace of misplaced files
    
.EXAMPLE
    .\workspace_manager.ps1 -ProjectName data_cleaner
    .\workspace_manager.ps1 -List
    .\workspace_manager.ps1 -Status
    .\workspace_manager.ps1 -Cleanup
#>

param(
    [Parameter(Position=0)]
    [string]$ProjectName,
    
    [switch]$List,
    
    [switch]$Status,
    
    [switch]$Cleanup
)

# Set strict error handling - keep consistent
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Define workspace paths dynamically
$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$WorkspaceRoot = $ScriptPath
$CursorWorkspace = "$env:USERPROFILE\.cursor"
$ConfigFile = "$WorkspaceRoot\workspace_config.json"

# Colors for output
$Colors = @{
    Info = "Cyan"
    Success = "Green"
    Warning = "Yellow"
    Error = "Red"
    Header = "Magenta"
}

function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Colors[$Color]
}

function Test-IsProjectFile {
    param([System.IO.FileSystemInfo]$File)
    
    # Define project file patterns
    $projectFilePatterns = @(
        "*.py", "*.md", "*.json", "*.ps1", "*.yml", "*.yaml", "*.txt", "*.cfg", "*.ini"
    )
    
    # Check if it's a project file type
    $isProjectFileType = $projectFilePatterns | Where-Object { $File.Name -like $_ }
    
    # Check if it's NOT in Cursor extension directories
    $notInExtensions = $File.FullName -notlike "*\extensions\*" -and 
                      $File.FullName -notlike "*\node_modules\*" -and
                      $File.FullName -notlike "*\\.git\*" -and
                      $File.FullName -notlike "*\\.vscode\*"
    
    # Check if it's in the root or immediate subdirectories of Cursor workspace
    $cursorDepth = $CursorWorkspace.Split('\').Count
    $fileDepth = $File.FullName.Split('\').Count
    $isNearRoot = $fileDepth -le ($cursorDepth + 2)
    
    return $isProjectFileType -and $notInExtensions -and $isNearRoot
}

function Get-MisplacedProjectFiles {
    Write-ColorOutput "🔍 Scanning Cursor workspace for misplaced project files..." "Info"
    
    try {
        # Get files in Cursor workspace root and immediate subdirectories only
        $cursorFiles = @()
        
        # Check root level
        $cursorFiles += Get-ChildItem $CursorWorkspace -File -ErrorAction SilentlyContinue
        
        # Check immediate subdirectories (but not deep nested ones)
        $immediateDirs = Get-ChildItem $CursorWorkspace -Directory -ErrorAction SilentlyContinue | 
            Where-Object { $_.Name -notin @("extensions", "node_modules", ".git", ".vscode") }
        
        foreach ($dir in $immediateDirs) {
            $cursorFiles += Get-ChildItem $dir -File -Recurse -ErrorAction SilentlyContinue
        }
        
        # Filter for actual project files
        $misplacedFiles = $cursorFiles | Where-Object {
            $_.Name -like "*stuart*" -or 
            $_.Name -like "*data_cleaner*" -or 
            $_.Name -like "*lwrap*" -or
            $_.Name -like "*broadly*" -or
            $_.Name -like "*unified*"
        } | Where-Object { Test-IsProjectFile $_ }
        
        return $misplacedFiles
    }
    catch {
        Write-ColorOutput "⚠️  Error scanning Cursor workspace: $($_.Exception.Message)" "Warning"
        return @()
    }
}

function Get-WorkspaceConfig {
    if (-not (Test-Path $ConfigFile)) {
        Write-ColorOutput "❌ Workspace configuration not found: $ConfigFile" "Error"
        return $null
    }
    
    try {
        $config = Get-Content $ConfigFile | ConvertFrom-Json
        return $config
    }
    catch {
        Write-ColorOutput "❌ Error reading workspace configuration: $($_.Exception.Message)" "Error"
        return $null
    }
}

function Show-ProjectList {
    $config = Get-WorkspaceConfig
    if (-not $config) { return }
    
    Write-ColorOutput "📋 Available Projects in Stuart Workspace" "Header"
    Write-Host "=" * 60 -ForegroundColor $Colors.Header
    
    foreach ($projectKey in $config.projects.PSObject.Properties.Name) {
        $project = $config.projects.$projectKey
        $status = if ($project.active) { "🟢 ACTIVE" } else { "⚪ INACTIVE" }
        $lastActive = if ($project.last_activated) { $project.last_activated } else { "Never" }
        
        Write-ColorOutput "📁 $($project.name)" "Info"
        Write-Host "   Key: $projectKey" -ForegroundColor White
        Write-Host "   Path: $($project.root_path)" -ForegroundColor White
        Write-Host "   Status: $status" -ForegroundColor White
        Write-Host "   Last Active: $lastActive" -ForegroundColor White
        Write-Host "   Description: $($project.description)" -ForegroundColor White
        Write-Host ""
    }
}

function Show-WorkspaceStatus {
    $config = Get-WorkspaceConfig
    if (-not $config) { return }
    
    Write-ColorOutput "📊 Current Workspace Status" "Header"
    Write-Host "=" * 60 -ForegroundColor $Colors.Header
    
    # Find active project
    $activeProject = $config.projects.PSObject.Properties | Where-Object { $_.Value.active -eq $true }
    
    if ($activeProject) {
        Write-ColorOutput "🎯 Active Project: $($activeProject.Value.name)" "Success"
        Write-Host "   Path: $($activeProject.Value.root_path)" -ForegroundColor White
        Write-Host "   Type: $($activeProject.Value.project_type)" -ForegroundColor White
    } else {
        Write-ColorOutput "⚠️  No active project" "Warning"
    }
    
    # Check Cursor workspace with improved detection
    Write-ColorOutput "🔍 Cursor Workspace Status:" "Info"
    $misplacedFiles = Get-MisplacedProjectFiles
    
    if ($misplacedFiles) {
        Write-ColorOutput "   ❌ Found potentially misplaced project files:" "Warning"
        foreach ($file in $misplacedFiles) {
            Write-Host "      $($file.FullName)" -ForegroundColor $Colors.Warning
        }
        Write-Host "   💡 These appear to be actual project files that shouldn't be in Cursor workspace" -ForegroundColor Yellow
    } else {
        Write-ColorOutput "   ✅ Cursor workspace is clean of project files" "Success"
    }
    
    # Current working directory
    Write-ColorOutput "📍 Current Working Directory:" "Info"
    $currentDir = Get-Location
    Write-Host "   $currentDir" -ForegroundColor White
}

function Remove-CursorWorkspaceFiles {
    Write-ColorOutput "🧹 Removing misplaced project files from Cursor workspace..." "Info"
    
    $misplacedFiles = Get-MisplacedProjectFiles
    
    if ($misplacedFiles) {
        Write-ColorOutput "Found $($misplacedFiles.Count) potentially misplaced project files:" "Warning"
        Write-Host ""
        
        foreach ($file in $misplacedFiles) {
            Write-Host "   📄 $($file.Name)" -ForegroundColor White
            Write-Host "      Location: $($file.FullName)" -ForegroundColor Gray
            Write-Host "      Size: $([math]::Round($file.Length / 1KB, 2)) KB" -ForegroundColor Gray
            Write-Host ""
        }
        
        Write-ColorOutput "⚠️  WARNING: These files will be permanently deleted!" "Error"
        Write-ColorOutput "💡 Consider backing up these files before proceeding." "Warning"
        
        $confirm = Read-Host "Do you want to remove these project files from Cursor workspace? (y/N)"
        if ($confirm -eq 'y' -or $confirm -eq 'Y') {
            $removedCount = 0
            $failedCount = 0
            
            foreach ($file in $misplacedFiles) {
                try {
                    Remove-Item $file.FullName -Force
                    Write-ColorOutput "   ✅ Removed: $($file.Name)" "Success"
                    $removedCount++
                }
                catch {
                    Write-ColorOutput "   ❌ Failed to remove: $($file.Name) - $($_.Exception.Message)" "Error"
                    $failedCount++
                }
            }
            
            Write-Host ""
            if ($removedCount -gt 0) {
                Write-ColorOutput "🎉 Cleanup completed! Removed $removedCount files." "Success"
            }
            if ($failedCount -gt 0) {
                Write-ColorOutput "⚠️  Failed to remove $failedCount files. Check permissions." "Warning"
            }
        } else {
            Write-ColorOutput "Cleanup cancelled by user" "Info"
        }
    } else {
        Write-ColorOutput "✅ Cursor workspace is already clean of project files" "Success"
    }
}

function Set-Project {
    param([string]$ProjectName)
    
    $config = Get-WorkspaceConfig
    if (-not $config) { return }
    
    # Check if project exists
    if (-not $config.projects.$ProjectName) {
        Write-ColorOutput "❌ Project '$ProjectName' not found in workspace configuration" "Error"
        Write-ColorOutput "Available projects:" "Info"
        Show-ProjectList
        return
    }
    
    $project = $config.projects.$ProjectName
    
    # Deactivate all projects first
    foreach ($projectKey in $config.projects.PSObject.Properties.Name) {
        $config.projects.$projectKey.active = $false
    }
    
    # Activate the requested project
    $config.projects.$ProjectName.active = $true
    $config.projects.$ProjectName.last_activated = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ssZ")
    
    # Save updated configuration
    try {
        $config | ConvertTo-Json -Depth 10 | Set-Content $ConfigFile
        Write-ColorOutput "✅ Project '$($project.name)' activated successfully!" "Success"
    }
    catch {
        Write-ColorOutput "❌ Failed to update workspace configuration: $($_.Exception.Message)" "Error"
        return
    }
    
    # Change to project directory
    if (Test-Path $project.root_path) {
        Set-Location $project.root_path
        Write-ColorOutput "📁 Changed to project directory: $($project.root_path)" "Info"
        
        # Run project-specific dev setup if available
        if ($project.dev_setup_script -and (Test-Path $project.dev_setup_script)) {
            Write-ColorOutput "🔧 Running project dev setup..." "Info"
            & ".\$($project.dev_setup_script)"
        }
    } else {
        Write-ColorOutput "❌ Project directory not found: $($project.root_path)" "Error"
    }
    
    # Show new status
    Write-Host ""
    Show-WorkspaceStatus
}

# Main execution logic
if ($List) {
    Show-ProjectList
}
elseif ($Status) {
    Show-WorkspaceStatus
}
elseif ($Cleanup) {
    Remove-CursorWorkspaceFiles
}
elseif ($ProjectName) {
    Set-Project -ProjectName $ProjectName
}
else {
    # Show help
    Write-ColorOutput "🚀 Stuart Multi-Project Workspace Manager" "Header"
    Write-Host "=" * 60 -ForegroundColor $Colors.Header
    Write-Host ""
    Write-ColorOutput "Usage:" "Info"
    Write-Host "  .\workspace_manager.ps1 -ProjectName <project>    # Activate a project" -ForegroundColor White
    Write-Host "  .\workspace_manager.ps1 -List                     # List all projects" -ForegroundColor White
    Write-Host "  .\workspace_manager.ps1 -Status                   # Show current status" -ForegroundColor White
    Write-Host "  .\workspace_manager.ps1 -Cleanup                  # Remove misplaced files from Cursor workspace" -ForegroundColor White
    Write-Host ""
    Write-ColorOutput "Examples:" "Info"
    Write-Host "  .\workspace_manager.ps1 -ProjectName data_cleaner" -ForegroundColor White
    Write-Host "  .\workspace_manager.ps1 -List" -ForegroundColor White
    Write-Host "  .\workspace_manager.ps1 -Status" -ForegroundColor White
    Write-Host ""
    
    # Show current status
    Show-WorkspaceStatus
}

