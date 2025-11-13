# Fix Git Authentication Error - Permission Denied

## Problem
You're getting: `Permission denied to Abhilesh-Vaka` when trying to push to `Jagadeeshwari-017/weather-app`

This means Git is using cached credentials from a different GitHub account.

---

## Solution: Clear Cached Credentials and Re-authenticate

### Step 1: Clear Windows Credential Manager

1. **Open Credential Manager**
   - Press `Windows Key + R`
   - Type: `control /name Microsoft.CredentialManager`
   - Press Enter

2. **Remove GitHub Credentials**
   - Click **"Windows Credentials"** tab
   - Look for entries containing:
     - `git:https://github.com`
     - `github.com`
   - Click on each one → **Remove**
   - Close Credential Manager

### Step 2: Use Personal Access Token (Recommended)

GitHub no longer accepts passwords. You need a **Personal Access Token**.

#### Create a Personal Access Token:

1. **Go to GitHub Settings**
   - Visit: https://github.com/settings/tokens
   - Or: GitHub → Your Profile → Settings → Developer settings → Personal access tokens → Tokens (classic)

2. **Generate New Token**
   - Click **"Generate new token"** → **"Generate new token (classic)"**
   - **Note**: "Weather App Push"
   - **Expiration**: Choose duration (90 days recommended)
   - **Scopes**: Check **`repo`** (this gives full repository access)
   - Scroll down and click **"Generate token"**

3. **Copy the Token**
   - **IMPORTANT**: Copy it immediately! It looks like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - You won't see it again!

### Step 3: Push with Token

Run these commands in PowerShell:

```powershell
# Make sure you're in the right directory
cd "C:\Users\NAGESWARARAO VAKA\Desktop\Weather App"

# Try pushing again
git push -u origin main
```

When prompted:
- **Username**: `Jagadeeshwari-017`
- **Password**: Paste your **Personal Access Token** (not your GitHub password!)

---

## Alternative: Use SSH Instead of HTTPS

If you prefer, you can use SSH keys instead:

### Step 1: Check if you have SSH keys

```powershell
ls ~/.ssh
```

If you see `id_rsa.pub` or `id_ed25519.pub`, you have SSH keys.

### Step 2: Add SSH key to GitHub

1. **Copy your public key**:
   ```powershell
   cat ~/.ssh/id_ed25519.pub
   ```
   (Or `cat ~/.ssh/id_rsa.pub` if that's what you have)

2. **Add to GitHub**:
   - Go to: https://github.com/settings/keys
   - Click **"New SSH key"**
   - Paste your public key
   - Save

### Step 3: Change remote URL to SSH

```powershell
git remote set-url origin git@github.com:Jagadeeshwari-017/weather-app.git
git push -u origin main
```

---

## Quick Fix Commands (HTTPS with Token)

```powershell
# Clear Git credential cache
git credential-manager-core erase
# When prompted, type: https://github.com
# Press Enter twice

# Or manually update remote URL (optional)
git remote set-url origin https://github.com/Jagadeeshwari-017/weather-app.git

# Push again (will prompt for credentials)
git push -u origin main
```

When prompted:
- **Username**: `Jagadeeshwari-017`
- **Password**: Your Personal Access Token

---

## Verify Your Setup

```powershell
# Check current remote URL
git remote -v

# Should show:
# origin  https://github.com/Jagadeeshwari-017/weather-app.git (fetch)
# origin  https://github.com/Jagadeeshwari-017/weather-app.git (push)
```

---

## Still Having Issues?

1. **Make sure you're logged into the correct GitHub account** in your browser
2. **Verify the repository exists** and you have access: https://github.com/Jagadeeshwari-017/weather-app
3. **Check if the repository is private** - make sure you have push access
4. **Try using GitHub CLI** instead:
   ```powershell
   # Install GitHub CLI
   winget install --id GitHub.cli
   
   # Authenticate
   gh auth login
   
   # Then push
   git push -u origin main
   ```

---

## Summary

The issue is that Git is using credentials from `Abhilesh-Vaka` account. You need to:
1. ✅ Clear cached credentials
2. ✅ Create a Personal Access Token for `Jagadeeshwari-017` account
3. ✅ Use the token when pushing

**Most Common Solution**: Use Personal Access Token (Step 2 above) - it's the easiest and most reliable method!

