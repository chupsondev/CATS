import os, json


def loadSettings(options):
    programFolder = os.path.dirname(os.path.realpath(__file__))
    settingsFile = programFolder + "\\settings.json"
    defaultSettings = {
        "themisUser": "",
        "themisPass": "",
        "themisGroup": "",
        "buildDefaultValue": True,
        "testDefaultValue": True,
    }
    for option in options:
        if option + "DefaultValue" not in defaultSettings:
            defaultSettings[option + "DefaultValue"] = False
    if not os.path.exists(settingsFile):
        open(settingsFile, "w").write(json.dumps(defaultSettings, indent=4))
    return json.load(open(settingsFile, "r"))
