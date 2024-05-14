# mypy: allow-untyped-defs

from ._abstract import AbstractScraper


class Foodbag(AbstractScraper):
    def __init__(self, url, proxies=None, timeout=None, *args, **kwargs):
        super().__init__(url=url, proxies=proxies, timeout=timeout, *args, **kwargs)
        print(self._extract_script_data())

    @classmethod
    def host(cls):
        return "foodbag.be"

    def author(self):
        return self.schema.author()

    def title(self):
        return self.schema.title()

    def category(self):
        return self.schema.category()

    def total_time(self):
        return self.schema.total_time()

    def yields(self):
        return self.schema.yields()

    def image(self):
        return self.schema.image()

    def ingredients(self):
        return self.schema.ingredients()

    def instructions(self):
        return self.schema.instructions()

    def ratings(self):
        return self.schema.ratings()

    def cuisine(self):
        return self.schema.cuisine()

    def description(self):
        return self.schema.description()

    def _extract_script_data(self):
        scripts = self.soup.find_all("script")
        next_script_strings = [
            script.string
            for script in scripts
            if script.string and script.string.startswith("self.__next_f.push")
        ]
        for next_script_string in next_script_strings:
            if "data" in next_script_string:
                pass
