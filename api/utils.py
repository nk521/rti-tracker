from typing import Dict, Any, List

def remove_meta_rti(obj: Dict[str, Any], fields: List[str] = None):
    if fields == None:
        fields = []

    pop_list = ["updated_on", "created_on"]
    pop_list.extend(fields)
    
    for _pop in pop_list:
        obj.pop(_pop)
    
    return obj