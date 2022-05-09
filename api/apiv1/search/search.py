from typing import Any, Dict, List, Union
from api import deps
from fastapi import APIRouter, HTTPException, status
from api.utils import ready_rti_obj
from schemas import search, rti
from models import Rti
from tortoise.queryset import Q

router = APIRouter()


@router.get("/search", response_model=List[rti.RtiOut])
async def simple_search(query: str) -> List[Rti]:
    allRtiObjList = []

    async for RtiObj in Rti.filter(
        Q(query__icontains=query) | Q(title__icontains=query)
    ):
        allRtiObjList.append(await ready_rti_obj(RtiObj))

    return allRtiObjList


@router.post("/advsearch", response_model=List[rti.RtiOut])
async def advanced_search(content: search.AdvancedSearchIn) -> List[Rti]:
    # _kwargs_for_filters: Dict[str, Union[str, int]]
    _args_for_filters: List[Q] = []
    
    if content.query:
        _args_for_filters.append(Q(query__icontains=content.query))
    
    if content.title:
        _args_for_filters.append(Q(title__icontains=content.title))
    
    if (not(bool(content.start_date) ^ bool(content.end_date))) and (bool(content.start_date) or bool(content.end_date)):
        # _args_for_filters.append(Q(Q(rti_send_date__gte=content.start_date) & Q(rti_send_date__lte=content.end_date)))
        _args_for_filters.append(Q(rti_send_date__range=(content.start_date, content.end_date)))

    if content.ministry:
        _args_for_filters.append(Q(ministry=content.ministry))
    
    if content.public_authority:
        _args_for_filters.append(Q(public_authority=content.public_authority))
    
    print(content)
    if content.is_file_present:
        _args_for_filters.append(Q(file_id__not_isnull=True))
    # else:
    #     _args_for_filters.append(Q(file__not_isnull=True))

    if not _args_for_filters:
        return []

    allRtiObjList: List[Rti] = []

    async for RtiObj in Rti.filter(
        Q(*_args_for_filters, join_type="AND")
    ):
        allRtiObjList.append(await ready_rti_obj(RtiObj))

    return allRtiObjList
