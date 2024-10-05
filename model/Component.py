class Component:
    self_id:str
    name:str
    supplier_name:str
    supplier_item_id:str
    qty:int
    supplier_detail_page_url:str
    datasheet_url:str
    category:list[str]
    description:str
    brand:str
    package:str
    img_url:str

    def __init__(self):
        self.self_id =""
        self.name= ""
        self.supplier_name = ""
        self.supplier_item_id = ""
        self.qty = 0
        self.supplier_detail_page_url = ""
        self.datasheet_url = ""
        self.category = []
        self.description = ""
        self.brand = ""
        self.package = ""
        self.img_url = ""
