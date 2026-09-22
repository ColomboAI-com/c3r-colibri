"""Strict Colibri telemetry parsing with non-authoritative C3R recommendations."""

from __future__ import annotations

from dataclasses import dataclass
import re

_HEADER = re.compile(r"^(?P<call>\d+) (?P<row>\d+) (?P<layer>\d+)(?P<experts>(?: \d+:-?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)+)$")
_EXPERT = re.compile(r" (?P<id>\d+):(?P<gate>-?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)")


@dataclass(frozen=True)
class RouteRecord:
    call: int
    row: int
    layer: int
    experts: tuple[tuple[int, float], ...]


def parse_route_record(line: str) -> RouteRecord:
    match = _HEADER.fullmatch(line.strip())
    if not match:
        raise ValueError("invalid Colibri ROUTE_TRACE record")
    experts = tuple((int(item["id"]), float(item["gate"])) for item in _EXPERT.finditer(match["experts"]))
    if not experts or len({expert for expert, _ in experts}) != len(experts):
        raise ValueError("route record must contain unique experts")
    return RouteRecord(int(match["call"]), int(match["row"]), int(match["layer"]), experts)


def shadow_recommendation(record: RouteRecord, max_experts: int) -> dict[str, object]:
    """Return evidence only; `authority` is intentionally immutable."""
    if max_experts < 1:
        raise ValueError("max_experts must be positive")
    ordered = sorted(record.experts, key=lambda item: (-item[1], item[0]))
    return {"schema_version": "1.0", "authority": "colibri-native", "mode": "shadow",
            "call": record.call, "row": record.row, "layer": record.layer,
            "observed_experts": [expert for expert, _ in record.experts],
            "recommended_experts": [expert for expert, _ in ordered[:max_experts]],
            "applied": False}

