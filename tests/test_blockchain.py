from src.blockchain import PermissionedBlockchain
def test_chain_commit_and_revocation():
    c = PermissionedBlockchain()
    c.commit("registration", {"vehicle_id":"v1", "commitment":"abc"})
    c.commit("revocation", {"vehicle_id":"v1"})
    assert c.is_revoked("v1")
    assert c.audit()
