

def toByteUInt(n):
    return n.to_bytes(8, "big", signed=False)

def fromByteUInt(s):
    return int.from_bytes(s, "big", signed=False)
