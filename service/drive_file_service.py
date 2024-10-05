from libs.feishu.drive.list_file import list_file

class BitableFile:
    token:str
    name:str

    def __init__(self):
        self.token = ""
        self.name = ""

class ListBitableFileRes:
    files:list[BitableFile]
    has_more:bool
    next_page_token:str

    def __init__(self):
        self.files = []
        self.has_more = False
        self.next_page_token = ""

class DriveFileService:

    @staticmethod
    def list_bitable_files_in_root(access_token:str,page_token:str=""):
        response = list_file(access_token,page_token=page_token)
        files:list[BitableFile]=[]
        for  file in response["files"]:
            if file["type"]=="bitable":
                bitable_file = BitableFile()
                bitable_file.name = file["name"]
                bitable_file.token = file["token"]
                files.append(bitable_file)
        res = ListBitableFileRes()
        res.files = files
        res.has_more = response["has_more"]
        if res.has_more:
            res.next_page_token = response["next_page_token"]
        return res
