
class DefaultList(list):
    def __init__(self, default_value=None):
        super().__init__()
        self.default = default_value

    def __getitem__(self, index):
        if 0 <= index < len(self):
            return super().__getitem__(index)
        return self.default