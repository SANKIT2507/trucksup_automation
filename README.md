

## Troubleshooting: Activity Not Found Error

### Error:
```
Error: Activity class {com.logistics.trucksup/com.logistics.trucksup/.activities.WLcomeScreen} does not exist.
```

### Solution:
**APP_ACTIVITY mein package name mat daalo!**

```python
# ❌ GALAT:
APP_ACTIVITY = "com.logistics.trucksup/.activities.WLcomeScreen"

# ✅ SAHI:
APP_ACTIVITY = ".activities.WLcomeScreen"
```

### Activity Verify Karne Ka Tarika:
```bash
# Phone mein app open karo, phir terminal mein:
adb shell dumpsys window | findstr "mCurrentFocus"

# Output kuch aisa hoga:
mCurrentFocus=Window{... com.logistics.trucksup/.activities.WLcomeScreen}

# config.py mein daalo:
APP_PACKAGE = "com.logistics.trucksup"
APP_ACTIVITY = ".activities.WLcomeScreen"
```

### Ya phir script run karo:
```bash
python activity_verifier.py
```


## IMPORTANT: App Not Opening?

### Run Diagnostic First:
```bash
python diagnose.py
```

Yeh batayega:
- Kya app installed hai?
- Kya driver connect ho raha hai?
- Screenshot lega current screen ka
- Page source save karega

### Check Activity Name:
```bash
# Phone mein app manually open karo, phir:
python activity_verifier.py
```

### Common Issues:
1. **App not installed** → Install from Play Store
2. **Wrong activity** → Run activity_verifier.py
3. **Splash screen** → Add `time.sleep(5)` after driver creation


## SCREEN-BY-SCREEN XML CAPTURE GUIDE

### Step 1: Capture Login Screen XML
```bash
# Terminal 1: Start Appium
appium

# Terminal 2: Run helper
python xml_capture.py

# Phone mein:
# 1. App open karo
# 2. Google popup dismiss karo
# 3. Mobile number screen par jao
# 4. Terminal mein type karo: login_screen
# 5. Press Enter
```

### Step 2: Share XML with me
```
xml_screenshots/login_screen.xml  ← Mujhe yeh file bhejo
```

### Step 3: Repeat for all screens
- `otp_screen`
- `location_screen`  
- `profile_screen`

Main har screen ke exact locators update kar dunga!
