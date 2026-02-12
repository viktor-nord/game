dialogs = {
    "jon": "hej",
    "bob": "tjo",
    "jim": "Def"
}

class Dialog:
    def __init__(self, id):
        self.id = id
        try:
            self.text = dialogs[id]
        except:
            self.text = "don't talk to me"