from typing import List, Optional
from pydantic import UUID4, BaseModel, EmailStr
from schemas import rti

class SearchIn(BaseModel):
    query: str

class AdvancedSearchIn(BaseModel):
    title: Optional[str] = ""
    query: Optional[str] = ""
    topic: Optional[List[str]] = []
    start_date: Optional[int]
    end_date: Optional[int]
    ministry: Optional[int]
    public_authority: Optional[int]
    is_response_present: Optional[bool]
    is_file_present: Optional[bool]
    when_was_rti_filed: Optional[int]

class LoggedInAdvancedSearchIn(AdvancedSearchIn):
    email: Optional[EmailStr]
    id: Optional[UUID4]
