from app import state

def test_reset_state_clears_all():
    # arrange: state'i kirlet
    state._MEMBERS["1"] = {"id": "1"}
    state._CLASSES["10"] = {"id": "10"}
    state._CLASS_COUNTS["10"] = 1
    state._RESERVATIONS["r1"] = {"id": "r1"}

    # act
    state.reset_state()

    # assert
    assert state._MEMBERS == {}
    assert state._CLASSES == {}
    assert state._CLASS_COUNTS == {}
    assert state._RESERVATIONS == {}
