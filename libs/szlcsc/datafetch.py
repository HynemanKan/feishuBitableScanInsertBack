import requests
from bs4 import BeautifulSoup

from model.Component import Component

HEADERS = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
}

class DataFetch:
    @staticmethod
    def fetch_data(supplier_item_id:str)->Component:
        response = requests.get("https://so.szlcsc.com/global.html", params={
            "k": supplier_item_id
        }, headers=HEADERS)
        soup = BeautifulSoup(response.content, "lxml")
        table = soup.find("table", {"data-productcode": supplier_item_id.upper()})
        jlc_id = table.attrs['data-productid']
        component = Component()
        jlc_url = f"https://item.szlcsc.com/{jlc_id}.html"
        component.supplier_detail_page_url=jlc_url
        response = requests.get(jlc_url, headers=HEADERS)
        soup = BeautifulSoup(response.content, "lxml")
        datasheet_url_a = soup.find("a", {
            "id": "item-pdf-down"
        })
        if datasheet_url_a:
            datasheet_url = datasheet_url_a['href'].split("?")[0]
        else:
            datasheet_url = ""
        component.datasheet_url=datasheet_url
        category_block = soup.find("nav")
        category = list(
            filter(lambda x: x != "首页",
                map(lambda x: x.text.replace("\xa0", "").replace(">", ""),
                    category_block.find_all("a"))))
        component.category = category
        detail_block = soup.find("ul", {
            "class": "text-[14px] mb-[20px]"
        })
        description = detail_block.find('p').text
        component.description = description
        item_attrs_blocks = detail_block.find_all("li", {"class": "flex mt-[16px]"})
        attrs = {}
        for item in item_attrs_blocks:
            block = list(item.children)
            attrs[block[0].text] = block[1].text
        item_package = ""
        if "商品封装" in attrs:
            item_package = attrs["商品封装"]
        item_brand = ""
        if "品牌名称" in attrs:
            item_brand = attrs["品牌名称"]
        component.brand = item_brand
        component.package = item_package
        item_image = soup.find("img", {
            "width": "260"
        }).attrs["src"]
        component.img_url = item_image
        return component
