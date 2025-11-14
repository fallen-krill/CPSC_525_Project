class Page:
    def __init__(self, name="Page"):
        self.name = name
        self.equations = [""]

    def add_equation(self):
        self.equations.append("")

    def remove_equation(self, index: int):
        self.equations.pop(index)

class Project:
    def __init__(self):
        self.pages = []

    def add_page(self):
        page = Page(f"Page {len(self.pages)}")
        self.pages.append(page)
        return page
    
    def remove_page(self, index: int):
        self.pages.pop(index)

    def rename_page(self, index: int, name: str):
        self.pages[index].name = name