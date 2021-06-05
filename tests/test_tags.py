
def test_get_tags_premade(ls_client):
    tag_list = ls_client.api.tags.all()
    assert(len(tag_list) == 5)
    for t in tag_list:
        assert(t.id)
