from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CarrierKind(str, Enum):
    TANGENT_VECTOR = "tangent_vector"
    COVECTOR = "covector"


class MatrixAction(str, Enum):
    DIRECT = "direct"
    INVERSE = "inverse"
    TRANSPOSE = "transpose"
    INVERSE_TRANSPOSE = "inverse_transpose"


@dataclass(frozen=True)
class TypedMap:
    domain: str
    codomain: str
    action: MatrixAction


@dataclass(frozen=True)
class TransportManifest:
    carrier_pair: tuple[CarrierKind, CarrierKind]
    tangent_forward: TypedMap
    tangent_reverse: TypedMap
    cotangent_pullback: TypedMap
    cotangent_reverse: TypedMap
    frame_variation_sign: int
    coframe_variation_sign: int
    basepoint_rule: str
    orientation_rule: str

    @classmethod
    def certified(cls) -> TransportManifest:
        return cls(
            (CarrierKind.TANGENT_VECTOR, CarrierKind.COVECTOR),
            TypedMap("T_x", "T_y", MatrixAction.DIRECT),
            TypedMap("T_y", "T_x", MatrixAction.INVERSE),
            TypedMap("T_y*", "T_x*", MatrixAction.TRANSPOSE),
            TypedMap("T_x*", "T_y*", MatrixAction.INVERSE_TRANSPOSE),
            -1,
            1,
            "based_holonomy_conjugacy",
            "both_orientations",
        )

    def validate(self) -> bool:
        maps = (
            self.tangent_forward,
            self.tangent_reverse,
            self.cotangent_pullback,
            self.cotangent_reverse,
        )
        types_are_exact = (
            type(self.carrier_pair) is tuple
            and len(self.carrier_pair) == 2
            and all(type(item) is CarrierKind for item in self.carrier_pair)
            and all(type(item) is TypedMap for item in maps)
            and all(
                type(item.domain) is str
                and type(item.codomain) is str
                and type(item.action) is MatrixAction
                for item in maps
            )
            and type(self.frame_variation_sign) is int
            and type(self.coframe_variation_sign) is int
            and type(self.basepoint_rule) is str
            and type(self.orientation_rule) is str
        )
        if (
            type(self) is not TransportManifest
            or not types_are_exact
            or self != TransportManifest.certified()
        ):
            raise ValueError("manifest differs from the approved v15.42 protocol")
        return True
