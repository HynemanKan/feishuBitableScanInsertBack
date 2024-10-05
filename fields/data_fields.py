from flask_restful import fields
from . import base_fields

bitable_file_base_fields={
            "token":fields.String,
            "name":fields.String,
        }

bitable_fields={
    "data":fields.Nested({
        "hasMore":fields.Boolean(attribute="has_more"),
        "nextPageToken":fields.String(attribute="next_page_token"),
        "files":fields.List(fields.Nested(bitable_file_base_fields)),
    })
}
bitable_fields.update(base_fields)

bitable_table_base_field={
    "name":fields.String,
    "tableId":fields.String(attribute="table_id"),
}

bitable_tables_fields = {
"data":fields.Nested({
        "hasMore":fields.Boolean(attribute="has_more"),
        "nextPageToken":fields.String(attribute="next_page_token"),
        "tables":fields.List(fields.Nested(bitable_table_base_field)),
    })
}
bitable_tables_fields.update(base_fields)

bitable_fields_base_field={
    "fieldName":fields.String(attribute="field_name"),
    "fieldType":fields.String(attribute="field_type"),
    "uiType":fields.String(attribute="ui_type"),
    "isPrimary":fields.Boolean(attribute="is_primary")
}

bitable_table_fields_fields={
    "data":fields.Nested({
        "fields":fields.List(fields.Nested(bitable_fields_base_field),attribute="table_fields"),
    })
}
bitable_table_fields_fields.update(base_fields)