# Language Localization Implementation Guide

## Overview

The system now supports **Dutch and English** language selection. The language is selected in the Python GUI and sent to Unity via WebSocket.

## Python Side ✅ (Already Implemented)

### GUI Language Selector

Added to the participant data entry form:

```
Taal / Language:
( ) Nederlands (Dutch)  
(•) English
```

**Default:** Dutch

### WebSocket Message

The language is sent to Unity in the initial player data:

```json
{
  "type": "player",
  "playerValues": {
    "name": "TestChild",
    "height": 120,
    "gender": "M",
    "contingency": 80,
    "trial_block": "1",
    "trial_number": 0,
    "support_frequency": "frequent",
    "language": "dutch"  // ← NEW: "dutch" or "english"
  }
}
```

## Unity Side 🎯 (Needs Implementation)

### Recommended Approach: Localization System

Here's the best way to implement this in Unity:

### Step 1: Create Language Data Files

Create JSON files for each language:

**`Resources/Localization/dutch.json`**
```json
{
  "welcome_message": "Welkom!",
  "start_button": "Start",
  "continue_button": "Doorgaan",
  "trial_instruction": "Kies een deur",
  "support_request": "Wil je hulp?",
  "mama_name": "Mama",
  "alternative_name": "Vreemdeling",
  "rating_question": "Hoe voel je je?",
  "rating_very_happy": "Heel blij",
  "rating_happy": "Blij",
  "rating_neutral": "Neutraal",
  "rating_sad": "Verdrietig",
  "rating_very_sad": "Heel verdrietig",
  "thank_you": "Dank je wel!"
}
```

**`Resources/Localization/english.json`**
```json
{
  "welcome_message": "Welcome!",
  "start_button": "Start",
  "continue_button": "Continue",
  "trial_instruction": "Choose a door",
  "support_request": "Do you want help?",
  "mama_name": "Mom",
  "alternative_name": "Stranger",
  "rating_question": "How do you feel?",
  "rating_very_happy": "Very happy",
  "rating_happy": "Happy",
  "rating_neutral": "Neutral",
  "rating_sad": "Sad",
  "rating_very_sad": "Very sad",
  "thank_you": "Thank you!"
}
```

### Step 2: Create LocalizationManager Script

**`Scripts/LocalizationManager.cs`**
```csharp
using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public class LocalizationData
{
    public Dictionary<string, string> texts;
}

public class LocalizationManager : MonoBehaviour
{
    public static LocalizationManager Instance;
    
    private Dictionary<string, string> localizedText;
    private string currentLanguage = "dutch"; // default
    
    void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
            DontDestroyOnLoad(gameObject);
        }
        else
        {
            Destroy(gameObject);
        }
    }
    
    public void SetLanguage(string language)
    {
        currentLanguage = language.ToLower();
        LoadLocalizedText();
    }
    
    private void LoadLocalizedText()
    {
        string filePath = $"Localization/{currentLanguage}";
        TextAsset textAsset = Resources.Load<TextAsset>(filePath);
        
        if (textAsset != null)
        {
            localizedText = JsonUtility.FromJson<Dictionary<string, string>>(textAsset.text);
            Debug.Log($"Loaded {currentLanguage} localization with {localizedText.Count} entries");
        }
        else
        {
            Debug.LogError($"Cannot find localization file: {filePath}");
            // Fallback to Dutch
            if (currentLanguage != "dutch")
            {
                currentLanguage = "dutch";
                LoadLocalizedText();
            }
        }
    }
    
    public string GetLocalizedValue(string key)
    {
        if (localizedText == null)
        {
            LoadLocalizedText();
        }
        
        if (localizedText != null && localizedText.ContainsKey(key))
        {
            return localizedText[key];
        }
        else
        {
            Debug.LogWarning($"Localization key not found: {key}");
            return key; // Return the key itself as fallback
        }
    }
}
```

### Step 3: Update WsClient to Receive Language

**Modify `WsClient.cs`:**

```csharp
public class PlayerVals
{
    public string name;
    public int height;
    public string gender;
    public int contingency;
    public string trial_block;
    public int trial_number;
    public string support_frequency;
    public string language;  // ← ADD THIS
}
```

**In the message handling:**

```csharp
void HandlePlayerMessage(string jsonMessage)
{
    // ... existing parsing code ...
    
    PlayerVals playerVals = JsonUtility.FromJson<PlayerVals>(jsonMessage);
    
    // Set the language
    if (!string.IsNullOrEmpty(playerVals.language))
    {
        LocalizationManager.Instance.SetLanguage(playerVals.language);
        Debug.Log($"Language set to: {playerVals.language}");
    }
    
    // ... rest of player data handling ...
}
```

### Step 4: Create LocalizedText Component

**`Scripts/LocalizedText.cs`**
```csharp
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class LocalizedText : MonoBehaviour
{
    [SerializeField]
    private string localizationKey;
    
    private Text uiText;
    private TextMeshProUGUI tmpText;
    
    void Start()
    {
        // Try to get Text component
        uiText = GetComponent<Text>();
        if (uiText == null)
        {
            // Try to get TextMeshPro component
            tmpText = GetComponent<TextMeshProUGUI>();
        }
        
        UpdateText();
    }
    
    public void UpdateText()
    {
        string localizedValue = LocalizationManager.Instance.GetLocalizedValue(localizationKey);
        
        if (uiText != null)
        {
            uiText.text = localizedValue;
        }
        else if (tmpText != null)
        {
            tmpText.text = localizedValue;
        }
    }
    
    public void SetKey(string key)
    {
        localizationKey = key;
        UpdateText();
    }
}
```

### Step 5: Usage in Unity Scenes

#### For Static UI Text:

1. Add `LocalizedText` component to any Text/TextMeshPro object
2. Set the `Localization Key` in the inspector (e.g., "welcome_message")
3. The text will automatically update based on the selected language

#### For Dynamic Text in Scripts:

```csharp
// Example: Update a UI text dynamically
using UnityEngine;
using UnityEngine.UI;

public class TrialUIManager : MonoBehaviour
{
    public Text instructionText;
    
    void ShowInstruction()
    {
        string localizedInstruction = LocalizationManager.Instance.GetLocalizedValue("trial_instruction");
        instructionText.text = localizedInstruction;
    }
}
```

#### For Speech/Audio:

```csharp
// Example: Play localized audio clips
public AudioClip GetLocalizedAudio(string baseKey)
{
    string language = LocalizationManager.Instance.currentLanguage;
    string audioPath = $"Audio/{language}/{baseKey}";
    return Resources.Load<AudioClip>(audioPath);
}
```

## Text to Gather from Unity

You'll need to localize all player-facing text. Common areas:

### 1. UI Text
- ☐ Welcome screen
- ☐ Instructions
- ☐ Button labels
- ☐ Tutorial text
- ☐ Trial instructions
- ☐ Rating scales
- ☐ Thank you screen

### 2. Character Names
- ☐ "Mama" / "Mom"
- ☐ "Vreemdeling" / "Stranger" (or whatever you call the alternative figure)

### 3. Dialog/Prompts
- ☐ Support request questions
- ☐ Choice prompts
- ☐ Feedback messages

### 4. Audio Scripts
- ☐ Voiceover transcripts
- ☐ Character speech

## Quick Start Checklist

### In Unity:

1. ☐ Create `Resources/Localization/` folder
2. ☐ Create `dutch.json` with all Dutch text
3. ☐ Create `english.json` with all English text
4. ☐ Add `LocalizationManager.cs` script
5. ☐ Add `LocalizedText.cs` script
6. ☐ Add `LocalizationManager` to a persistent GameObject (e.g., GameManager)
7. ☐ Update `WsClient.cs` to receive and set language
8. ☐ Add `LocalizedText` components to all UI text objects
9. ☐ Update any dynamic text code to use `GetLocalizedValue()`

### Testing:

1. ☐ Run Python app, select Dutch → Unity shows Dutch text
2. ☐ Run Python app, select English → Unity shows English text
3. ☐ Test all UI screens in both languages
4. ☐ Test character names appear correctly
5. ☐ Test all instructions are readable

## Alternative: Simple Approach (Quick Start)

If you want a simpler approach for now:

```csharp
public class SimpleLocalization : MonoBehaviour
{
    public static string CurrentLanguage = "dutch";
    
    public static string GetText(string key)
    {
        if (CurrentLanguage == "english")
        {
            switch (key)
            {
                case "welcome": return "Welcome!";
                case "start": return "Start";
                case "continue": return "Continue";
                // ... add all keys
                default: return key;
            }
        }
        else // dutch
        {
            switch (key)
            {
                case "welcome": return "Welkom!";
                case "start": return "Start";
                case "continue": return "Doorgaan";
                // ... add all keys
                default: return key;
            }
        }
    }
}
```

Then use: `text.text = SimpleLocalization.GetText("welcome");`

## Benefits of JSON Approach

✅ **Easy to edit** - Non-programmers can update text files
✅ **Scalable** - Easy to add more languages later
✅ **Organized** - All text in one place per language
✅ **Version control friendly** - Easy to track changes
✅ **No recompilation** - Change text without rebuilding

## Example Translation Workflow

1. **Gather all text** → Create list of all English text in game
2. **Create keys** → Give each text a unique key (e.g., "trial_door_instruction")
3. **Translate** → Have translator create Dutch versions
4. **Create JSON files** → Put translations in dutch.json and english.json
5. **Implement** → Add LocalizedText components or use GetLocalizedValue()
6. **Test** → Verify all text appears correctly in both languages

## Summary

**Python ✅ Done:**
- Language selector added to GUI
- Language sent via WebSocket to Unity

**Unity 🎯 To Do:**
- Create language JSON files (dutch.json, english.json)
- Create LocalizationManager script
- Update WsClient to receive language setting
- Add LocalizedText components to UI
- Gather and translate all game text

This approach gives you a professional, maintainable localization system that's easy to expand in the future!
