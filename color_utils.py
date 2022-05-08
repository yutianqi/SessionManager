class ColorUtils():
    @staticmethod
    def getRedContent(content):
        return "\033[0;31;m{}\033[0m".format(content)

    @staticmethod
    def getGreenContent(content):
        return "\033[0;32;m{}\033[0m".format(content)

    @staticmethod
    def getYellowContent(content):
        return "\033[0;33;m{}\033[0m".format(content)