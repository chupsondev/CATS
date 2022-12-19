class Option:
    def __init__(self, name, description, tags, defaultValue, value=None, valueType: type = bool):
        self.name = name
        self.tags = tags
        self.description = description
        self.defaultValue = defaultValue
        self.value = defaultValue if value is None else value
        self.valueType = valueType

    def setTags(self, tags):
        self.tags = tags

    def setDescription(self, description):
        self.description = description

    def setValue(self, value):
        self.value = value

    def getType(self):
        return self.valueType

    def setDefaultValue(self, defaultValue):
        self.defaultValue = defaultValue

    def getValue(self):
        return self.value

    def getType(self):
        return self.valueType

    def getName(self):
        return self.name

    def checkForTag(self, tag):
        if tag in self.tags:
            return True
        return False

    def __str__(self):
        return f"{self.tags} - {self.description}"


def getOption(tag, options):
    tag = tag.split("=")[0]
    tag = tag.lower()
    for option in options:
        if options[option].checkForTag(tag):
            return option
    return None
