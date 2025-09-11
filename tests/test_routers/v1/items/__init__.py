from fastapi import APIRouter

router = APIRouter()
# duplicate router test
router1 = router


@router.get("/")
def get_items():
    return {"items": []}


@router.get("/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}
