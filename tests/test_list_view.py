import pytest

from paramutils import ListView


@pytest.fixture
def lv():
    return ListView([1, 2, 3])


def test_append(lv):
    with pytest.raises(TypeError):
        lv.append(4)

    assert len(lv) == 3


def test_clear(lv):
    with pytest.raises(TypeError):
        lv.clear()

    assert len(lv) == 3


def test_delitem(lv):
    with pytest.raises(TypeError):
        del lv[1]

    assert len(lv) == 3


def test_extend(lv):
    with pytest.raises(TypeError):
        lv.extend([4, 5, 6])

    assert len(lv) == 3


def test_plus_equals(lv):
    with pytest.raises(TypeError):
        lv += [4, 5, 6]

    assert len(lv) == 3


def test_setitem(lv):
    with pytest.raises(TypeError):
        lv[1] = 10


def test_set_slice(lv):
    with pytest.raises(TypeError):
        lv[0:2] = [4, 5]

    with pytest.raises(TypeError):
        lv[0:2] = [4, 5, 6, 7]

    assert len(lv) == 3


def test_star_equals(lv):
    with pytest.raises(TypeError):
        lv *= 5

    assert len(lv) == 3


def test_del_slice(lv):
    with pytest.raises(TypeError):
        del lv[0:2]

    assert len(lv) == 3


def test_sort(lv):
    with pytest.raises(TypeError):
        lv.sort()


def test_insert(lv):
    with pytest.raises(TypeError):
        lv.insert(1, 1)

    assert len(lv) == 3


def test_view_reflects_updates():
    orig_list = [1, 2, 3]
    lv = ListView(orig_list)

    assert len(lv) == 3

    orig_list.append(4)

    assert len(lv) == 4
    assert lv[3] == 4


def test_slicing(lv):
    slice_ = lv[0:2]
    assert slice_ == [1, 2]


def test_min(lv):
    assert min(lv) == 1


def test_max(lv):
    assert max(lv) == 3


def test_count():
    lv = ListView([1, 2, 1, 4, 1])
    assert lv.count(1) == 3


def test_pop(lv):
    with pytest.raises(TypeError):
        lv.pop()
    with pytest.raises(TypeError):
        lv.pop(1)

    assert len(lv) == 3


def test_remove(lv):
    with pytest.raises(TypeError):
        lv.remove(2)

    assert len(lv) == 3


def test_reverse(lv):
    with pytest.raises(TypeError):
        lv.reverse()

    assert len(lv) == 3
    assert lv == [1, 2, 3]


def test_in(lv):
    assert 2 in lv
    assert 4 not in lv


def test_union(lv):
    new_lv = lv + [4, 5]
    assert new_lv == [1, 2, 3, 4, 5]


def test_multiplication(lv):
    new_lv = lv * 2

    assert len(new_lv) == 6
    assert new_lv[0:3] == lv
    assert new_lv[3:6] == lv


def test_index(lv):
    assert lv.index(2) == 1


def test_no_constructor_arguments():
    empty_lv = ListView()
    assert len(empty_lv) == 0
