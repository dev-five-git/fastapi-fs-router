from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_users():
    return {"users": []}


@router.get("/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
