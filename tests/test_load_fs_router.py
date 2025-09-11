"""fastapi_fs_router module test"""

import pytest
from pathlib import Path
from fastapi import FastAPI
from fastapi_fs_router import load_fs_router


def test_load_fs_router_basic():
    """basic load_fs_router function test"""
    app = FastAPI()

    # test with nonexistent directory (os.walk does not raise an exception)
    load_fs_router(app, "nonexistent_dir")
    # no exception should be raised


@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("[id]", "{id}"),
        ("[user_id]", "{user_id}"),
        ("[item_id]", "{item_id}"),
        ("[category_id]", "{category_id}"),
        ("users", "users"),
        ("api", "api"),
        ("v1", "v1"),
        ("", ""),
        ("[", "["),
        ("]", "]"),
        ("[incomplete", "[incomplete"),
        ("incomplete]", "incomplete]"),
        ("hello_world", "hello-world"),
        ("wow_wow_wow", "wow-wow-wow"),
        ("{hello}", "{hello}"),
        ("{hello_world}", "{hello_world}"),
        ("{wow_wow_wow}", "{wow_wow_wow}"),
    ],
)
def test_change_seg_function(input_str, expected):
    """_change_seg function parameter test"""
    from fastapi_fs_router.load_fs_router import _change_seg

    assert _change_seg(input_str) == expected


@pytest.mark.parametrize(
    "route_dir,prefix,file_path,expected",
    [
        # basic cases
        ("routers", "", "routers/users", "/users"),
        ("routers", "", "routers/api/users", "/api/users"),
        ("routers", "", "routers/api/v1/users", "/api/v1/users"),
        # custom prefix cases
        ("routers", "/api", "routers/users", "/api/users"),
        ("routers", "/api", "routers/api/users", "/api/api/users"),
        ("routers", "/api", "routers/api/v1/users", "/api/api/v1/users"),
        # slash handling cases
        ("routers", "api", "routers/users", "/api/users"),
        ("routers", "api/", "routers/users", "/api/users"),
        ("routers", "/api/", "routers/users", "/api/users"),
        ("routers", "api", "./routers/users", "/api/users"),
        ("routers", "api/", "./routers", "/api"),
        # root directory cases
        ("routers", "", "routers/", ""),
        ("routers", "", "routers/index", "/index"),
        # nested directory cases
        ("routers", "", "routers/admin/users", "/admin/users"),
        ("routers", "/v1", "routers/admin/users", "/v1/admin/users"),
        ("routers", "/v1/(empty)", "routers/admin/users", "/v1/admin/users"),
        ("routers", "/v1/(empty)/", "routers/admin/users", "/v1/admin/users"),
        ("routers", "/v1/(empty)/", "routers/admin/users/(empty)", "/v1/admin/users"),
        ("routers", "/v1/(empty)/", "routers/admin/users/(empty)/", "/v1/admin/users"),
        ("routers", "/v1/", "routers/admin/users/(empty)/", "/v1/admin/users"),
        ("routers", "/v1", "routers/admin/users/(empty)/", "/v1/admin/users"),
    ],
)
def test_get_api_prefix_function(route_dir, prefix, file_path, expected):
    """_get_api_prefix function parameter test"""
    from fastapi_fs_router.load_fs_router import _get_api_prefix

    route_dir_path = Path(route_dir)
    file_path_obj = Path(file_path)
    result = _get_api_prefix(route_dir_path, prefix, file_path_obj)
    assert result == expected


@pytest.mark.parametrize(
    "route_dir,prefix",
    [
        ("routers", ""),
        ("routers", "/api"),
        ("src/routes", "/v1"),
        ("app/routers", "/api/v1"),
    ],
)
def test_load_fs_router_with_different_params(route_dir, prefix):
    """load_fs_router function different parameters test"""
    app = FastAPI()

    # nonexistent directory should not raise an exception
    load_fs_router(app, route_dir, prefix=prefix)

    # check if app is created normally
    assert app is not None
    assert isinstance(app, FastAPI)


@pytest.mark.parametrize(
    "path_segments",
    [
        ["users"],
        ["api", "users"],
        ["api", "v1", "users"],
        ["admin", "users"],
        ["api", "admin", "users"],
        ["v1", "api", "users"],
    ],
)
def test_path_segment_handling(path_segments):
    """path segment handling test"""
    from fastapi_fs_router.load_fs_router import _get_api_prefix

    route_dir = Path("routers")
    file_path = Path("routers") / Path(*path_segments)
    prefix = ""

    result = _get_api_prefix(route_dir, prefix, file_path)
    expected = "/" + "/".join(path_segments)

    assert result == expected


@pytest.mark.parametrize(
    "prefix,expected_prefix",
    [
        ("", ""),
        ("api", "/api"),
        ("/api", "/api"),
        ("api/", "/api"),
        ("/api/", "/api"),
        ("v1/api", "/v1/api"),
        ("/v1/api", "/v1/api"),
    ],
)
def test_prefix_normalization(prefix, expected_prefix):
    """prefix normalization test"""
    from fastapi_fs_router.load_fs_router import _get_api_prefix

    route_dir = Path("routers")
    file_path = Path("routers/users")

    result = _get_api_prefix(route_dir, prefix, file_path)
    expected = expected_prefix + "/users" if expected_prefix else "/users"

    assert result == expected


def test_load_fs_router_with_real_routers():
    """test load_fs_router with real routers"""
    app = FastAPI()

    # test with real router directory
    load_fs_router(app, "tests/test_routers")

    # check if router is included
    assert len(app.routes) > 0

    # TestClient to test endpoint
    from fastapi.testclient import TestClient

    client = TestClient(app)

    # users router test
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json()["users"] == []

    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["user_id"] == 1

    # items router test
    response = client.get("/v1/items/")
    assert response.status_code == 200
    assert response.json()["items"] == []


def test_load_fs_router_with_prefix():
    """test load_fs_router with prefix"""
    app = FastAPI()

    # load router with prefix
    load_fs_router(app, "tests/test_routers", prefix="/api/v1")

    from fastapi.testclient import TestClient

    client = TestClient(app)

    # test endpoint with prefix
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    assert response.json()["users"] == []
