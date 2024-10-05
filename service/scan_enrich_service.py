from enum import Enum

from libs.szlcsc.datafetch import DataFetch as SzlcscDataFetch
from model.Component import Component


class SourceType(Enum):
    SZLCSC = "szlcsc"


class ScanEnrichService:
    @staticmethod
    def enrich(scan_result:str,source:SourceType)->Component:
        if source == SourceType.SZLCSC:
            return ScanEnrichService.szlcsc_enrich(scan_result)


    @staticmethod
    def szlcsc_enrich(scan_result:str)->Component:
        scan_data = list(map(lambda x:x.split(":"),scan_result[1:-1].split(",")))
        scan_dict = {}
        for item in scan_data:
            scan_dict[item[0]] = item[1]
        supplier_item_id = scan_dict["pc"]
        qty = scan_dict["qty"]
        name = scan_dict["pm"]
        component = SzlcscDataFetch.fetch_data(supplier_item_id)
        component.name = name
        component.qty = qty
        component.supplier_item_id = supplier_item_id
        component.self_id = f"SZLCSC_{component.supplier_item_id}"
        component.supplier_name="立创商城/szlcsc"
        return component

