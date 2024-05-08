# mypy: allow-untyped-defs

import re

import requests

from ._abstract import AbstractScraper
from ._utils import url_path_to_dict


class Foodbag(AbstractScraper):
    def __init__(self, url, proxies=None, timeout=None, *args, **kwargs):
        super().__init__(url=url, *args, **kwargs)

        dish_id = self._get_dish_id()
        response = requests.get(
            "https://admin.foodbag.be/api/dishrecipe",
            {"dishId": dish_id, "language": "nl"},
        )

        self.data = response.json()
        self.recipe_data = self.data.get("dishRecipe")

    @classmethod
    def host(cls):
        return "foodbag.be"

    def author(self):
        return self.schema.author()

    def title(self):
        return self.recipe_data.get("name")

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

    def _get_dish_id(self):
        url_dict = url_path_to_dict(self.url)
        query = url_dict.get("query")
        match = re.search(r"dishId=([^&]+)", query)
        if not match:
            return None
        return match.group(1)
