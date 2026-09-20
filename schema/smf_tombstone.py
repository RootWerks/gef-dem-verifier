import struct
from dataclasses import dataclass
from typing import Literal

SMF_TOMBSTONE_FMT = ">BHd32s32s32s32s"
SMF_TOMBSTONE_LEN = struct.calcsize(SMF_TOMBSTONE_FMT)

@dataclass
class SMFTombstone:
    record_type: Literal[3, 5]
    disposition: int
    delta_val: float
    r_iss: bytes
    r_prep: bytes
    delta_root: bytes
    e_token_hash: bytes

    def pack(self) -> bytes:
        return struct.pack(
            SMF_TOMBSTONE_FMT,
            self.record_type,
            self.disposition,
            self.delta_val,
            self.r_iss,
            self.r_prep,
            self.delta_root,
            self.e_token_hash,
        )

    @classmethod
    def unpack(cls, data: bytes) -> "SMFTombstone":
        if len(data) != SMF_TOMBSTONE_LEN:
            raise ValueError(f"SMF tombstone alignment mismatch: expected {SMF_TOMBSTONE_LEN} bytes, got {len(data)}")
        unpacked = struct.unpack(SMF_TOMBSTONE_FMT, data)
        return cls(
            record_type=unpacked[0],
            disposition=unpacked,
            delta_val=unpacked,
            r_iss=unpacked[3],
            r_prep=unpacked[4],
            delta_root=unpacked[5],
            e_token_hash=unpacked[6],
        )
