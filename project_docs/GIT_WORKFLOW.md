# Git Workflow & Branching Strategy
## Stuart Data Cleaner Project

## 🌿 **Branch Structure**

```
main (production)
├── develop (integration)
├── feature/contact-export-improvements
├── feature/survey-workflow
├── feature/unified-logic
├── hotfix/critical-bug-fixes
└── release/v1.0.0
```

## 🎯 **Branch Purposes**

### **main**
- **Purpose**: Production-ready code
- **Protection**: No direct commits, only merges from develop
- **Deployment**: Automatic deployment to production

### **develop**
- **Purpose**: Integration branch for features
- **Protection**: No direct commits, only merges from feature branches
- **Testing**: Automated testing and integration

### **feature/***
- **Purpose**: New features and improvements
- **Naming**: `feature/descriptive-name`
- **Examples**: 
  - `feature/contact-export-improvements`
  - `feature/survey-workflow`
  - `feature/unified-logic`

### **hotfix/***
- **Purpose**: Critical production fixes
- **Naming**: `hotfix/issue-description`
- **Examples**: `hotfix/critical-data-loss`

### **release/***
- **Purpose**: Release preparation
- **Naming**: `release/version-number`
- **Examples**: `release/v1.0.0`

## 🔄 **Development Workflow**

### **1. Starting New Feature**
```bash
# Ensure develop is up to date
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "feat: implement your feature description"
```

### **2. Feature Development**
```bash
# Make incremental commits
git add .
git commit -m "feat: add specific functionality"

# Push feature branch
git push origin feature/your-feature-name
```

### **3. Completing Feature**
```bash
# Ensure all tests pass
python -m pytest tests/

# Update documentation
git add .
git commit -m "docs: update feature documentation"

# Push final changes
git push origin feature/your-feature-name
```

### **4. Merging to Develop**
```bash
# Create pull request from feature to develop
# Review code, run tests, approve

# Merge feature branch to develop
git checkout develop
git merge feature/your-feature-name

# Delete feature branch
git branch -d feature/your-feature-name
git push origin --delete feature/your-feature-name
```

### **5. Releasing to Production**
```bash
# Create release branch from develop
git checkout -b release/v1.0.0

# Final testing and documentation
git add .
git commit -m "chore: prepare release v1.0.0"

# Merge to main and develop
git checkout main
git merge release/v1.0.0
git tag v1.0.0

git checkout develop
git merge release/v1.0.0

# Delete release branch
git branch -d release/v1.0.0
```

## 📝 **Commit Message Convention**

### **Format**
```
type(scope): description

[optional body]

[optional footer]
```

### **Types**
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### **Examples**
```
feat(contact-export): implement proper sheet naming
fix(core): resolve LLM API key authentication issue
docs(api): update configuration documentation
refactor(unified-logic): extract common data cleaning functions
test(integration): add full dataset validation tests
chore(deps): update pandas to version 2.0
```

## 🧪 **Testing Requirements**

### **Before Merge to Develop**
- [ ] All unit tests pass
- [ ] Integration tests pass
- [ ] Code coverage maintained
- [ ] Documentation updated
- [ ] No linting errors

### **Before Release to Production**
- [ ] All tests pass on develop
- [ ] Performance benchmarks met
- [ ] Security review completed
- [ ] User acceptance testing passed

## 🚨 **Hotfix Process**

### **Critical Production Issues**
```bash
# Create hotfix branch from main
git checkout main
git checkout -b hotfix/critical-issue

# Fix the issue
git add .
git commit -m "fix(critical): resolve production data loss issue"

# Merge to main and develop
git checkout main
git merge hotfix/critical-issue
git tag v1.0.1

git checkout develop
git merge hotfix/critical-issue

# Delete hotfix branch
git branch -d hotfix/critical-issue
```

## 🔐 **Branch Protection Rules**

### **main Branch**
- Require pull request reviews
- Require status checks to pass
- Require branches to be up to date
- Restrict pushes

### **develop Branch**
- Require pull request reviews
- Require status checks to pass
- Restrict direct pushes

### **Feature Branches**
- No restrictions (developer freedom)
- Regular cleanup of stale branches

## 📊 **Code Review Process**

### **Review Checklist**
- [ ] Code follows project standards
- [ ] Tests are comprehensive
- [ ] Documentation is updated
- [ ] No security vulnerabilities
- [ ] Performance impact assessed
- [ ] Backward compatibility maintained

### **Reviewers**
- **Core Logic**: At least 2 reviewers
- **Workflow Changes**: At least 1 reviewer + workflow owner
- **Documentation**: At least 1 reviewer
- **Configuration**: At least 1 reviewer

## 🚀 **Deployment Process**

### **Automated Deployment**
- **develop**: Deploy to staging environment
- **main**: Deploy to production environment
- **feature branches**: Deploy to development environment

### **Manual Deployment**
- Tagged releases can be manually deployed
- Hotfixes require manual approval
- Production deployments require team lead approval

---

**Last Updated**: August 21, 2025  
**Version**: 1.0.0  
**Maintainer**: Development Team
