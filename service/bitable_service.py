from libs.feishu.bitable.list_fields import list_fields
from libs.feishu.bitable.list_table import list_tables

class BitableTable:
    name:str
    table_id:str

    def __init__(self):
        self.table_id=""
        self.name=""

class ListBitableTableRes:
    tables:list[BitableTable]
    has_more:bool
    next_page_token:str

    def __init__(self):
        self.tables = []
        self.has_more = False
        self.next_page_token = ""

class TableField:
    field_name:str
    field_type:int
    ui_type:str
    is_primary:bool

    def __init__(self):
        self.field_name=""
        self.field_type=1
        self.ui_type=""
        self.is_primary=False

class ListBitableTableFieldRes:
    table_fields:list[TableField]

    def __init__(self):
        self.table_fields = []

class BitableService:
    @staticmethod
    def get_tables(user_token:str,app_id:str,page_token:str="")->ListBitableTableRes:
        response = list_tables(user_token,app_id,page_token=page_token)
        res = ListBitableTableRes()
        tables = []
        for item in response['items']:
            table = BitableTable()
            table.name = item['name']
            table.table_id = item['table_id']
            tables.append(table)
        res.tables = tables
        res.has_more = response['has_more']
        res.next_page_token = response['page_token']
        return res

    @staticmethod
    def get_table_fields(user_token:str, app_token:str,table_token:str)->ListBitableTableFieldRes:
        response = list_fields(user_token,app_token,table_token)
        res = ListBitableTableFieldRes()
        table_fields = []
        for item in response['items']:
            table_field = TableField()
            table_field.field_name = item['field_name']
            table_field.field_type = item['type']
            table_field.ui_type = item['ui_type']
            table_field.is_primary = item['is_primary']
            table_fields.append(table_field)
        res.table_fields = table_fields
        return res