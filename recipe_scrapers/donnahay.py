# mypy: allow-untyped-defs

from ._abstract import AbstractScraper


class DonnaHay(AbstractScraper):
    @classmethod
    def host(cls):
        return "donnahay.com.au"

    def title(self):
        return (
            self.soup.find("h1", class_="text-center recipe-title__mobile")
            .getText()
            .upper()
        )

    def yields(self):
        div = self.soup.find("div", class_="col-sm-6 method")
        instructions = div.findAll("li")
        last_instruction = instructions[len(instructions) - 1]
        if last_instruction.find("b") is not None:
            return last_instruction.find("b").getText()
        else:
            array = last_instruction.getText().split(".")
            for entry in array:
                if "Serves" in entry:
                    if entry[0] == " ":
                        yield_ = entry.replace(" ", "", 1)
                    return yield_

    def image(self):
        div = self.soup.find("div", class_="image-frame recipes")
        if not div:
            return
        image = div.find("img")
        return image["src"]

    def ingredients(self):
        return self.schema.ingredients()

    def instructions(self):
        div = self.soup.find("div", class_="col-sm-6 method")
        if not div:
            return
        instructions = div.find_all("li")
        for instruction in instructions:
            text = instruction.get_text(separator=" ", strip=True)
            if "Serves" in text:
                text = text.split("Serves", 1)[
                    0
                ].strip()  # Remove the sentence starting with Serves
            instruction.string = text
        return instructions

    def keywords(self):
        div = self.soup.find("div", class_="section text-left")
        tags = div.find_all("a")
        keywords = []
        for tag in tags:
            keywords.append(tag.getText())
        return keywords
