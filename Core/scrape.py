from html.parser import HTMLParser

import requests


def request_item_data(item_id, sub_item_name=None):
    response = _query_website(item_id)
    parser = _parse_html(response)
    item_info = _get_fields(parser, sub_item_name)
    return item_info


def _get_fields(parser, sub_name):
    item_info = {}
    item_extra_info = []
    if sub_name:
        item_extra_info = _find_sub_item(parser.sub_items, sub_name)
        info = parser.info
        item_info = _set_base_data(item_info, item_extra_info)
    else:
        info = parser.sub_items[0]
        item_info = _set_base_data(item_info, info)
    extra_fields, info = _get_extra_fields(info)
    item_info.update(extra_fields)
    item_info["description"] = _combine_strings([_get_description(info), _get_description(item_extra_info)])
    return item_info


def _parse_html(response):
    parser = ItemParser()
    parser.feed(response.text)
    return parser


def _query_website(item_id):
    return requests.get(f"https://2e.aonprd.com/Equipment.aspx?ID={item_id}")


def _find_sub_item(sub_items, sub_name):
    for sub_item in sub_items:
        if sub_item[0] == sub_name:
            return sub_item
    raise ValueError("sub_name provided didn't exist")


def _set_base_data(item_info, info):
    item_info["name"] = info[0]
    item_info["item_level"] = _get_level(info)
    item_info["gp_cost"] = _get_price(info)
    return item_info


def _get_extra_fields(info):
    """
    Args:
        info (list):
    """
    extra_data = {}
    for field in ["Activate", "Frequency"]:
        if field in info:
            index = info.index(field)
            data = info[index + 1]
            del info[index + 1]
            del info[index]
            extra_data[field.lower()] = data.strip().replace(";", "")
    if "Effect" in info:
        index = info.index("Effect")
        extra_data["effect"] = "".join(info[index + 1:]).strip()
        info = info[:index]
    return extra_data, info


def _combine_strings(strings):
    return " ".join(filter(None, strings))


def _get_level(info):
    return int(info[1].split(" ")[1])


def _get_description(info):
    for previous_label in ["Bulk", "Usage", "Price"]:
        if previous_label in info:
            label = info.index(previous_label)
            break
    else:
        return ""
    description = "".join(info[label + 2:]).strip()
    return description


def _get_price(info):
    price_label = info.index("Price")
    total_price = info[price_label + 1].strip()
    price_denominated = total_price.split(",")
    cost = 0
    for price in price_denominated:
        price = price.strip()
        price_value = int(price.split(" ")[0])
        if "gp" in price:
            cost += price_value
        if "sp" in price:
            cost += price_value/10
    return cost


def get_item_names():
    response = requests.get("https://2e.aonprd.com/Sources.aspx?ID=1")
    parser = ItemListParser()
    parser.feed(response.text)
    return parser.items


class ItemParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.record = False
        self.info = []
        self.sub_items = []

    def handle_starttag(self, tag, attrs):
        if self._started(attrs):
            self.record = True
        if self.record and ('title', 'PFS Standard') in attrs:
            self.sub_items.append([])
        if self.record and self._finished(tag, attrs):
            self.record = False

    @staticmethod
    def _started(attrs):
        if ('id', 'ctl00_RadDrawer1_Content_MainContent_DetailedOutput') in attrs:
            return True
        return False

    @staticmethod
    def _finished(tag, attrs):
        if tag == "div" and ('class', 'clear') in attrs:
            return True
        return False

    def handle_data(self, data):
        if self.record:
            if self.sub_items:
                self.sub_items[len(self.sub_items) - 1].append(data)
            else:
                self.info.append(data)


class ItemListParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.equipment = False
        self.items = {}
        self.last_tag = ""
        self.last_link = ""

    def handle_starttag(self, tag, attrs):
        self.last_tag = tag
        if self.equipment:
            if attrs:
                self.last_link = attrs[0][1]

    def handle_data(self, data):
        if "Equipment" in data and self.last_tag == "h2":
            self.equipment = True
        if "Familiar Abilities" in data and self.last_tag == "h2":
            self.equipment = False
        elif self.equipment and self.last_link:
            self.items[data] = self.last_link.split("=")[1]
            self.last_link = None
