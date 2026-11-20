from src.crypto_schnorr import generate_keypair, sign, verify, aggregate_with_components, aggregate_verify
def test_single_and_aggregate_signature():
    messages, sigs, pubs = [], [], []
    for i in range(4):
        sk, pk = generate_keypair()
        msg = f"vehicle-{i}".encode()
        sig = sign(msg, sk)
        assert verify(msg, sig, pk)
        messages.append(msg); sigs.append(sig); pubs.append(pk)
    packet = aggregate_with_components(sigs)
    assert aggregate_verify(messages, packet, pubs)
