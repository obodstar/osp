import os

class Form:
    imagePath: str
    title: str
    pinboard: str
    description: str | None
    link: str | None
    allowComment: bool
    showSimilarProduct: bool

    def __init__(self, image: str, title: str, pinboard: str):
        self.imagePath = image
        self.title = title
        self.pinboard = pinboard
        self.description = None
        self.link = None
        self.allowComment = True
        self.showSimilarProduct = True

    def setImagePath(self, value: str):
        self.imagePath = value
        return self

    def setTitle(self, value: str):
        self.title = value
        return self

    def setPinboard(self, value: str):
        self.pinboard = value
        return self

    def setDescription(self, value: str):
        self.description = value
        return self

    def setLink(self, value: str):
        self.link = value
        return self
    
    def setAllowCommentEnabled(self, value: bool):
        self.allowComment = value
        return self

    def setShowSimilarProductEnabled(self, value: bool):
        self.showSimilarProduct = value
        return self

    def validate(self):
        if not self.title.strip():
            raise ValueError("'title' is required")

        if not self.pinboard.strip():
            raise ValueError("'pinboard' is required")

        if not self.imagePath.strip():
            raise ValueError("'filePath' is required")

        if os.path.exists(self.imagePath) == False:
            raise ValueError("'filePath' '%s' doesn`t not exits"%(self.imagePath))

        if len(self.title) > 100:
            raise ValueError("'title' is too long (maximum 100 characters long)")
