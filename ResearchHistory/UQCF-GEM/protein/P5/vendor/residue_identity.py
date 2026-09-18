from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional


@dataclass(frozen=True, slots=True)
class ResidueId:
    """Canonical PDB residue identity: (chain_id, resseq, insertion_code)."""

    chain_id: str
    resseq: int
    insertion_code: str = ""

    def __post_init__(self) -> None:
        chain_id = str(self.chain_id).strip()
        insertion_code = str(self.insertion_code).strip()

        if len(chain_id) > 1:
            raise ValueError(
                f"Invalid PDB chain ID {self.chain_id!r}; expected at most one character."
            )
        if len(insertion_code) > 1:
            raise ValueError(
                f"Invalid PDB insertion code {self.insertion_code!r}; expected at most one character."
            )

        object.__setattr__(self, "chain_id", chain_id)
        object.__setattr__(self, "resseq", int(self.resseq))
        object.__setattr__(self, "insertion_code", insertion_code)

    def __str__(self) -> str:
        return f"{self.chain_id}:{self.resseq}{self.insertion_code}"

    def display(self) -> str:
        return str(self)


def residue_id_from_pdb_line(line: str) -> ResidueId:
    """Parse canonical residue identity from fixed-width PDB columns 22-27."""

    if len(line) < 27:
        raise ValueError("PDB record is too short to contain a residue identity.")

    return ResidueId(
        chain_id=line[21],
        resseq=int(line[22:26]),
        insertion_code=line[26],
    )


def _display_chain_id(chain_id: str) -> str:
    return chain_id if chain_id else "<blank>"


def resolve_pdb_residue(
    residue_ids: Iterable[ResidueId],
    *,
    pos: int,
    selected_chain_id: Optional[str] = None,
    mutation_chain_id: Optional[str] = None,
    insertion_code_is_specified: bool = False,
    insertion_code: Optional[str] = None,
) -> ResidueId:
    """Resolve one PDB-numbered mutation target without silent first-match behavior."""

    selected_chain = (
        str(selected_chain_id).strip()
        if selected_chain_id is not None
        else None
    )
    mutation_chain = (
        str(mutation_chain_id).strip()
        if mutation_chain_id is not None
        else None
    )

    if (
        selected_chain is not None
        and mutation_chain is not None
        and selected_chain != mutation_chain
    ):
        raise ValueError(
            f"Mutation chain {_display_chain_id(mutation_chain)} conflicts with selected PDB chain "
            f"{_display_chain_id(selected_chain)}."
        )

    effective_chain = mutation_chain if mutation_chain is not None else selected_chain
    candidates = [
        residue_id
        for residue_id in residue_ids
        if residue_id.resseq == int(pos)
        and (effective_chain is None or residue_id.chain_id == effective_chain)
    ]

    if insertion_code_is_specified:
        requested_icode = "" if insertion_code is None else str(insertion_code).strip()
        if len(requested_icode) > 1:
            raise ValueError(
                f"Invalid PDB insertion code {insertion_code!r}; expected at most one character."
            )
        candidates = [
            residue_id
            for residue_id in candidates
            if residue_id.insertion_code == requested_icode
        ]

    if not candidates:
        if effective_chain is not None:
            suffix = ""
            if insertion_code_is_specified:
                suffix = "" if insertion_code is None else str(insertion_code).strip()
            target = f"{effective_chain}:{int(pos)}{suffix}"
            raise ValueError(f"Mutation error: PDB residue {target} not found.")
        raise ValueError(f"Mutation error: PDB residue {int(pos)} not found.")

    if len(candidates) == 1:
        return candidates[0]

    candidate_text = ", ".join(str(residue_id) for residue_id in candidates)
    chains = {residue_id.chain_id for residue_id in candidates}

    if effective_chain is None and len(chains) > 1:
        raise ValueError(
            f"Ambiguous PDB residue {int(pos)}. "
            f"Candidates: {candidate_text}. "
            "Specify chain_id explicitly."
        )

    chain_label = effective_chain
    if chain_label is None:
        chain_label = candidates[0].chain_id

    raise ValueError(
        f"Ambiguous PDB residue {int(pos)} in chain {_display_chain_id(chain_label)}. "
        f"Candidates: {candidate_text}. "
        "Specify insertion_code explicitly."
    )
