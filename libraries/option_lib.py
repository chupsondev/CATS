class Option:
    def __init__(self, description, tags, active=False):
        self.tags = tags
        self.description = description
        self.active = active

    def setTags(self, tags):
        self.tags = tags

    def setDescription(self, description):
        self.description = description

    def setActive(self, active):
        self.active = active

    def checkForTag(self, tag):
        if tag in self.tags:
            return True
        return False

    def __str__(self):
        return f"{self.tags} - {self.description}"


def getOption(tag, options):
    for option in options:
        if options[option].checkForTag(tag):
            return option
    return None
