"""Script for crawling petfinder cats and dogs breeds info."""
import scrapy

from scrapy import Request
from ..items import PetFinderItem


class PetFinder(scrapy.Spider):
    """Class based on scrapy Spider for collect the data from petfinder website."""

    name = "pet_finder"

    custom_settings = {"ITEM_PIPELINES": {"pet_finder.pipelines.IntegrityPipeline": 100}}

    def start_requests(self):
        """Start the requests for both dogs and cats breeds page."""
        start_urls = [
            "https://www.petfinder.com/dog-breeds/",
            "https://www.petfinder.com/cat-breeds/",
        ]

        for url in start_urls:
            yield Request(url=url, callback=self.parse, cb_kwargs={"page": 1, "base_url": url})

    def parse(self, response, page, base_url):
        """Paginate the base_url and send all breeds links to parse_breeds function."""
        self.logger.debug(response.url)

        link_list = (
            response.css("li.grid-col").xpath(".//a[@class='contentCard-wrap']/@href").getall()
        )

        # Pagination logic
        if link_list:
            page = page + 1
            url = f"{base_url}?page={page}"
            yield Request(
                url=url, callback=self.parse, cb_kwargs={"page": page, "base_url": base_url}
            )

        for url in link_list:
            yield Request(url=url, callback=self.parse_breeds)

    def parse_breeds(self, response):
        """Collect all the information of a specific breeds webpage."""
        self.logger.debug(response.url)
        item = PetFinderItem()
        item["data"] = {}
        item["sections"] = {}
        item["url"] = response.url

        # Getting the breeds name
        item["breeds"] = response.xpath("//h1[@data-test='Breed_Details_Name']/text()").get()

        # Adding the breeds image to the item data
        item["data"]["img"] = response.css("div.grid>div.grid-col").xpath("./img/@src").get()

        # Getting the breeds traits
        attributes = {}
        traits_box = response.css("div.grid>div.grid-col")
        traits_path = zip(traits_box.xpath("./h3"), traits_box.xpath("./div[@class='meterBar']"))
        for attr_path, value_path in traits_path:
            attr = attr_path.xpath("./text()").get()
            value = value_path.xpath(".//span/text()").get().strip()
            attributes[attr] = value
        item["attributes"] = attributes

        # Getting the breeds description
        sections = {}
        sections["description"] = response.css("div.grid>div.grid-col>div.txt>p::text").getall()

        # Getting the text sections
        sections_box = response.xpath("//div[@class='card-section']")
        sections_path = zip(
            sections_box.xpath(".//h2[contains(' ' + @class + ' ',' txt ')]"),
            sections_box.xpath(".//div[@class='overflowAccordion']"),
        )
        for name_path, content_path in sections_path:
            section_name = name_path.xpath("./text()").get().strip()
            section_content = " ".join(
                [x.strip() for x in content_path.xpath(".//text()").getall() if len(x.strip()) > 0]
            )
            sections[section_name] = section_content

        # getting the attributes section
        sections["attributes"] = {}
        card_path = response.xpath("//div[@class='card-section']")
        attributes_path = zip(card_path.xpath(".//h3"), card_path.xpath(".//p"))
        for attr_path, value_path in attributes_path:
            attr = attr_path.xpath(".//text()").get().strip()
            value = value_path.xpath(".//text()").get().strip()
            sections["attributes"][attr] = value

        item["sections"] = sections
        yield item
