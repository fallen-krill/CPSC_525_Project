from function_tree import Function_tree

class Page:
    def __init__(self, name="Page"):
        self.name = name
        self.equations = [""]
        self.function_trees = [Function_tree("")]

    def add_equation(self):
        self.equations.append("")
        self.function_trees.append(Function_tree(""))

    def remove_equation(self, index: int):
        self.equations.pop(index)
        self.function_trees.pop(index)

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
