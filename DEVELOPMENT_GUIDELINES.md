# Development Guidelines

## 🚨 **CRITICAL: File Location Rules**

### **Project Boundaries**
- **ONLY** create/modify files within `C:\LocalAI\!projects\Stuart\data_cleaner\`
- **NEVER** create project files in `C:\Users\Oversoul\.cursor\`
- **ALWAYS** verify working directory before file operations

### **Working Directory Protocol**
1. **Start each session** by running `.\dev_setup.ps1`
2. **Verify location** with `Get-Location` - should show project root
3. **Check for `.project_root` marker** file to confirm correct location
4. **Use absolute paths** when in doubt: `C:\LocalAI\!projects\Stuart\data_cleaner\`

### **File Creation Rules**
- **Core modules**: `core\` directory
- **Configuration**: `config\` directory  
- **Workflows**: `workflows\` directory
- **Tests**: `tests\` directory
- **Documentation**: `project_docs\` directory

### **Reference Access**
- **Source data**: `C:\LocalAI\!projects\Stuart\Broadly Report\`
- **Business docs**: `C:\LocalAI\!projects\Stuart\docs\`
- **Legacy code**: `C:\LocalAI\!projects\Stuart\broadly_app\`

## 🔧 **Development Workflow**

### **Session Start Checklist**
- [ ] Run `.\dev_setup.ps1`
- [ ] Verify working directory is project root
- [ ] Check for `.project_root` marker
- [ ] Review project structure

### **File Operation Checklist**
- [ ] Confirm working directory is correct
- [ ] Use project-relative paths when possible
- [ ] Verify file is created in intended location
- [ ] Check for duplicate files in wrong locations

### **Session End Checklist**
- [ ] Verify all new files are in correct locations
- [ ] Check Cursor workspace for misplaced files
- [ ] Update project documentation if needed

## 🚨 **Common Mistakes to Avoid**

1. **Creating files in Cursor workspace** instead of project folder
2. **Using relative paths** without confirming working directory
3. **Assuming file location** without verification
4. **Forgetting to run dev_setup.ps1** at session start

## 🆘 **Troubleshooting**

### **If files are created in wrong location:**
1. **STOP** development work immediately
2. **Run** `.\dev_setup.ps1` to reset environment
3. **Move** misplaced files to correct location
4. **Delete** duplicate files from wrong location
5. **Verify** project structure integrity

### **If working directory is unclear:**
1. **Check** `Get-Location` output
2. **Look for** `.project_root` marker file
3. **Run** `.\dev_setup.ps1` to reset
4. **Use absolute paths** until location is confirmed

## 📋 **Project Structure Reference**

```
C:\LocalAI\!projects\Stuart\data_cleaner\
├── .project_root              # 🎯 Project boundary marker
├── dev_setup.ps1             # 🔧 Development environment setup
├── DEVELOPMENT_GUIDELINES.md  # 📖 This file
├── core\                      # 🧠 Core engine modules
├── config\                    # ⚙️ Configuration management
├── workflows\                 # 🔄 Workflow implementations
│   ├── broadly_survey\       # 📊 Survey workflow
│   └── contact_export\       # 📧 Export workflow
├── tests\                     # 🧪 Test scripts
├── project_docs\              # 📚 Project documentation
├── cli\                       # 💻 Command line interface
└── processors\                # 🔧 Process modules
```

## 🎯 **Success Metrics**

- ✅ **Zero files** created in Cursor workspace
- ✅ **All development** contained within project boundaries
- ✅ **Clear separation** between project and reference files
- ✅ **Consistent** working directory across sessions
