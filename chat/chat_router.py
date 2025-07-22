from fastapi import APIRouter

router = APIRouter()


@router.get("/response")
async def content_generator():
    return {"message": "Test Complete"}
