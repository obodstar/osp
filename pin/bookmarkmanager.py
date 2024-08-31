class BookmarkManager:
    def __init__(self):
        self._bookmarkMap = {}
    
    def setBookmark(self, bookmark: str, primary: str, secondary: str|None = None):
        self._bookmarkMap[self._getKey(primary, secondary)] = bookmark

    def getBookmark(self, primary: str, secondary: str|None = None) -> str|None:
        return self._bookmarkMap.get(self._getKey(primary, secondary))
    
    def deleteBookmark(self, primary: str, secondary: str|None = None) -> str|None:
        key = self._getKey(primary, secondary)
        if key in list(self._bookmarkMap.keys()):
            del self._bookmarkMap[key]

    def _getKey(self, primary: str, secondary: str|None = None) -> str:
        return ":".join(
            list(
                filter(lambda x: isinstance(x, str), ["[{}]".format(primary), secondary])
            )
        )