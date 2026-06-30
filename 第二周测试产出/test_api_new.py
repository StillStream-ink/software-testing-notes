import requests
import pytest

#基础URL
BASE_URL = "https://jsonplaceholder.typicode.com"

#1.GET /posts  -获取所有帖子
def test_get_all_posts():
    response = requests.get(f"{BASE_URL}/posts")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    print(f"获取到{len(data)}条帖子")

#2.GET /posts/{id} -获取单个帖子（参数化）
@pytest.mark.parametrize("post_id",[1,2,3,4,5])
def test_get_single_post(post_id):
    response = requests.get(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == post_id
    assert "title" in data
    assert "body" in data
    print(f"帖子{post_id}:{data['title'][:30]}...")

#3.POST/posts -创建新帖子
def test_create_post():
    new_data = {
        "title":"我的第二周接口测试",
        "body":"这是通过Python自动创建的帖子",
        "userID":1
    }
    response = requests.post(f"{BASE_URL}/posts",json=new_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == new_data["title"]
    assert data["body"] == new_data["body"]
    print(f"创建成功，新帖子ID：{data['id']}")

#4.GET /posts/99999 -不存在的帖子（404）
def test_get_nonexistent_post():
    response = requests.get(f"{BASE_URL}/posts/99999")
    assert response.status_code == 404
    print("不存在的帖子返回404，符合预期")
