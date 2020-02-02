# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem


class IntegrityPipeline:
    def process_item(self, item, spider):
        if item["url"] and item["breeds"] and item["attributes"]:
            return item
        else:
            raise DropItem("Item failled on integrity pipeline %s" % item)
