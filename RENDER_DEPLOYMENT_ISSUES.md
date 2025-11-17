# CKICAS Drought Monitor - Render Deployment Issues Analysis

## Overview
This document details the persistent deployment failures encountered when deploying the CKICAS drought monitoring dashboard to Render.com. Both frontend (React/Vite) and backend (FastAPI/Python) services are failing to build despite multiple configuration attempts.

## Current Status
- **Date**: November 18, 2025
- **Latest Commit**: `b8404527` - "Add PYTHON_VERSION to backend render.yaml for Render deployment"
- **Frontend Status**: ❌ Failed
- **Backend Status**: ❌ Failed

## Service Configuration

### Frontend Service (Static Site)
- **Service Name**: `ckicas-frontend`
- **Service ID**: `srv-d4dpdcktvkls73co4ujg`
- **URL**: https://ckicas-frontend.onrender.com
- **Runtime**: Node.js 22.16.0
- **Build Command**: `npm install && npm run build`
- **Publish Directory**: `test-dashboard/dist`

### Backend Service (Web Service)
- **Service Name**: `ckicas-drought-monitor-1`
- **Service ID**: `srv-d4dpjmndiees73bp6fk0`
- **URL**: https://ckicas-drought-monitor-1.onrender.com
- **Runtime**: Python 3.13.4
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## Current Errors

### Frontend Build Failure
```
==> Running build command 'npm install && npm run build'...
npm error code ENOENT
npm error syscall open
npm error path /opt/render/project/src/package.json
npm error errno -2
npm error enoent Could not read package.json: Error: ENOENT: no such file or directory, open '/opt/render/project/src/package.json'
```

### Backend Build Failure
```
==> Running build command 'pip install -r requirements.txt'...
ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'requirements.txt'
```

## Root Cause Analysis

### Primary Issue: Incorrect Working Directory
Both services are executing build commands from the repository root (`/opt/render/project/src/`) instead of their respective service directories:

- **Frontend**: Should execute from `test-dashboard/` directory
- **Backend**: Should execute from `ckicas-deploy/` directory

### Secondary Issue: Multiple render.yaml Files
The repository contains conflicting render.yaml configurations:

1. **Root `/render.yaml`**: Contains correct `cd` commands
   ```yaml
   buildCommand: cd test-dashboard && npm install && npm run build  # Frontend
   buildCommand: cd ckicas-deploy && pip install -r requirements.txt  # Backend
   ```

2. **Backend `/ckicas-deploy/render.yaml`**: Contains service-specific config
   ```yaml
   buildCommand: pip install -r requirements.txt  # No cd needed if executed from ckicas-deploy/
   ```

3. **Legacy `/ckicas-deploy/frontend/render.yaml`**: Outdated configuration

## Attempted Solutions

### Attempt 1: Root render.yaml Configuration (Commit: 6ce5754e)
- **Action**: Modified root `render.yaml` to use `cd` commands
- **Frontend**: `cd test-dashboard && npm install && npm run build`
- **Backend**: `cd ckicas-deploy && pip install -r requirements.txt`
- **Result**: Frontend failed (commit 6ce5754), Backend not tested

### Attempt 2: Frontend Path Correction (Commit: 085521d4)
- **Action**: Corrected frontend build path from `ckicas-deploy/frontend` to `test-dashboard`
- **Result**: Frontend still failed with same error

### Attempt 3: Backend PYTHON_VERSION Addition (Commit: b8404527)
- **Action**: Added `PYTHON_VERSION: 3.11.0` to `ckicas-deploy/render.yaml`
- **Result**: Both services still failing with same directory issues

## Configuration Files Analysis

### Repository Structure
```
/
├── render.yaml                           # Root config (with cd commands)
├── test-dashboard/                       # Frontend code
│   ├── package.json
│   └── dist/
├── ckicas-deploy/                        # Backend code
│   ├── render.yaml                      # Backend-specific config
│   ├── requirements.txt
│   ├── main.py
│   └── weather_api.py
└── axiom-x/                             # Additional modules
```

### Render Service Detection Logic
Render appears to be using different render.yaml files for different services:
- **Frontend**: May be using root `render.yaml` but ignoring `cd` command
- **Backend**: Using `ckicas-deploy/render.yaml` but executing from wrong directory

## Likely Causes

### 1. Render Configuration Caching
- **Hypothesis**: Render cached the initial render.yaml configuration and isn't picking up updates
- **Evidence**: Same error patterns despite multiple configuration changes
- **Impact**: Build commands execute from `/opt/render/project/src/` instead of service directories

### 2. Service-Specific render.yaml Override
- **Hypothesis**: Render prioritizes `render.yaml` files in service subdirectories
- **Evidence**: Backend uses `ckicas-deploy/render.yaml`, Frontend may be using root but ignoring cd
- **Impact**: Inconsistent configuration application across services

### 3. Build Context Issues
- **Hypothesis**: Render's build process doesn't properly change directories for build commands
- **Evidence**: `cd` commands in buildCommand are being ignored
- **Impact**: All file operations occur from repository root

### 4. YAML Parsing Differences
- **Hypothesis**: Render parses different YAML structures differently
- **Evidence**: Root render.yaml uses `type: static/web`, subdirectory uses `env: static/python`
- **Impact**: Different parsing logic leads to different command execution

## Potential Solutions (Not Yet Implemented)

### Solution A: Unified Root Configuration
- Move all service configurations to root `render.yaml`
- Remove subdirectory `render.yaml` files
- Ensure consistent YAML structure

### Solution B: Explicit Directory Commands
- Use absolute paths instead of `cd` commands
- Example: `buildCommand: pip install -r ckicas-deploy/requirements.txt`

### Solution C: Service Re-creation
- Delete and recreate Render services
- Force fresh configuration reading

### Solution D: Build Script Approach
- Create build scripts in repository root
- Reference scripts in render.yaml instead of inline commands

### Solution E: Directory Structure Reorganization
- Move frontend code to root level
- Move backend code to root level
- Simplify directory structure

## Environment Variables Required
```
ANTHROPIC_API_KEY=your_claude_api_key
NIWA_API_KEY=your_niwa_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
```

## Testing Recommendations
1. Verify local build processes work in respective directories
2. Test render.yaml configurations locally before deployment
3. Monitor Render service logs for configuration loading messages
4. Consider using Render's support for complex deployment scenarios

## Next Steps
Await user decision on which solution approach to implement. Current state requires manual intervention to resolve the working directory issues preventing both services from building successfully.</content>
<parameter name="filePath">c:\Users\regan\ID SYSTEM\RENDER_DEPLOYMENT_ISSUES.md