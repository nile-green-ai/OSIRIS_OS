"""
MAAT - BALANCE & EQUILIBRIUM SYSTEM
The cosmic law that maintains order

In Kemetic wisdom: Ma'at is truth, justice, balance, cosmic order
Mathematical representation: Ma'at = Σ = 0 (sum of all forces equals zero)

MA'AT enforces balance. When systems drift from equilibrium,
MA'AT corrects them. This is not morality - this is mathematics.
"""

from typing import Dict, Any, List, Tuple, Optional
import math


class MAAT:
    """
    Balance & Equilibrium System

    MA'AT maintains cosmic order through:
    - Conservation laws (energy, mass, momentum)
    - Error correction (prediction gap)
    - Homeostasis
    - System integrity checks
    - Balance enforcement
    """

    def __init__(self, agent_id: str, balance_threshold: float = 0.1):
        self.agent_id = agent_id
        self.balance_threshold = balance_threshold

        # The Scales of Ma'at
        self.balance_history: List[Dict[str, Any]] = []
        self.corrections_made: int = 0
        self.violations_detected: int = 0

        # Current balance state
        self.current_balance: float = 0.0
        self.is_balanced: bool = True

    # -------------------------
    # Core balance primitives
    # -------------------------

    def check_balance(self, system_state: Dict[str, float]) -> Tuple[bool, float]:
        """
        Check if a system is in balance.

        Ma'at = Σ = 0 (sum equals zero)

        For a system to be balanced, the sum of all forces/values
        should equal zero (or be within threshold).
        """
        total = float(sum(system_state.values()))
        is_balanced = abs(total) <= self.balance_threshold

        self.current_balance = total
        self.is_balanced = is_balanced

        self.balance_history.append({
            "state": system_state.copy(),
            "sum": total,
            "balanced": is_balanced,
            "threshold": self.balance_threshold,
        })

        if not is_balanced:
            self.violations_detected += 1

        return is_balanced, total

    def _apply_correction(self, system_state: Dict[str, float], imbalance: float) -> Dict[str, float]:
        """
        Apply correction to restore balance.

        Distribute the imbalance across all components proportionally.
        """
        if not system_state:
            return system_state

        correction_per_item = -imbalance / len(system_state)

        corrected_state = {
            key: float(value) + correction_per_item
            for key, value in system_state.items()
        }

        return corrected_state

    def enforce_balance(self, system_state: Dict[str, float]) -> Dict[str, float]:
        """
        Enforce balance on an unbalanced system.

        When Σ ≠ 0, MA'AT corrects it.
        """
        is_balanced, total = self.check_balance(system_state)

        if is_balanced:
            return system_state

        corrected_state = self._apply_correction(system_state, total)
        self.corrections_made += 1

        return corrected_state

    # -------------------------
    # Prediction error (Gap)
    # -------------------------

    def calculate_gap(self, prediction: List[float], reality: List[float]) -> float:
        """
        Calculate prediction error (the Gap).

        Gap = average absolute difference between prediction and reality.
        This is the error signal OSIRIS uses to transform the system.
        """
        if len(prediction) != len(reality) or len(prediction) == 0:
            self.violations_detected += 1
            return float("inf")

        diffs = [abs(float(p) - float(r)) for p, r in zip(prediction, reality)]
        gap = sum(diffs) / len(diffs)

        return gap

    # -------------------------
    # Conservation & entropy
    # -------------------------

    def validate_conservation(
        self,
        before_state: Dict[str, float],
        after_state: Dict[str, float],
        conserved_property: str = "total",
    ) -> bool:
        """
        Validate that a property was conserved across a transformation.

        Conservation laws: energy, mass, momentum must be preserved.
        Here we treat 'total' as the conserved scalar.
        """
        before_total = float(sum(before_state.values()))
        after_total = float(sum(after_state.values()))

        difference = abs(after_total - before_total)
        is_conserved = difference <= self.balance_threshold

        if not is_conserved:
            self.violations_detected += 1

        return is_conserved

    def calculate_entropy(self, system_state: Dict[str, float]) -> float:
        """
        Calculate system entropy (disorder).

        MA'AT seeks to minimize entropy (maintain order).
        """
        if not system_state:
            return 0.0

        values = [float(v) for v in system_state.values()]
        total = sum(values)

        if total == 0.0:
            return 0.0

        probabilities = [v / total for v in values if v > 0.0]
        if not probabilities:
            return 0.0

        entropy = -sum(p * math.log2(p) for p in probabilities if p > 0.0)
        return entropy

    # -------------------------
    # Homeostasis
    # -------------------------

    def check_homeostasis(
        self,
        current_value: float,
        target_value: float,
        tolerance: float = 0.1,
    ) -> Tuple[bool, float]:
        """
        Check if a system maintains homeostasis around a target value.

        Homeostasis = maintaining stable internal conditions.
        """
        deviation = abs(float(current_value) - float(target_value))
        in_homeostasis = deviation <= tolerance
        return in_homeostasis, deviation

    def restore_homeostasis(
        self,
        current_value: float,
        target_value: float,
        correction_rate: float = 0.5,
    ) -> float:
        """
        Restore homeostasis by moving toward target value.

        MA'AT gently guides the system back to balance.
        """
        deviation = float(target_value) - float(current_value)
        correction = deviation * correction_rate
        new_value = current_value + correction

        self.corrections_made += 1
        return new_value

    # -------------------------
    # Symbolic weighing
    # -------------------------

    def weigh_heart(self, heart: float, feather: float = 1.0) -> Dict[str, Any]:
        """
        The Weighing of the Heart ceremony.

        In Kemetic tradition: heart must be lighter than or equal to feather.
        Here: validate that a value meets the balance requirement.
        """
        heart_val = float(heart)
        feather_val = float(feather)

        passes = heart_val <= feather_val
        difference = heart_val - feather_val

        judgment = {
            "heart": heart_val,
            "feather": feather_val,
            "difference": difference,
            "passes": passes,
            "verdict": "BALANCED" if passes else "IMBALANCED",
        }

        if not passes:
            self.violations_detected += 1

        return judgment

    # -------------------------
    # High-level maintenance
    # -------------------------

    def maintain_order(self, system_state: Dict[str, float]) -> Dict[str, Any]:
        """
        Comprehensive order maintenance check.

        Runs MA'AT protocols:
        - Balance check
        - Entropy calculation
        - Correction if needed
        """
        is_balanced, total_sum = self.check_balance(system_state)
        entropy = self.calculate_entropy(system_state)

        needs_correction = (not is_balanced) or (entropy > 3.0)

        result: Dict[str, Any] = {
            "is_balanced": is_balanced,
            "sum": total_sum,
            "entropy": entropy,
            "needs_correction": needs_correction,
            "corrected_state": None,
        }

        if needs_correction:
            result["corrected_state"] = self.enforce_balance(system_state)

        return result

    # -------------------------
    # Metrics & reset
    # -------------------------

    def get_balance_statistics(self) -> Dict[str, Any]:
        """
        Get statistics on balance maintenance.
        """
        total_checks = len(self.balance_history)
        balanced_count = sum(1 for b in self.balance_history if b["balanced"])

        return {
            "total_balance_checks": total_checks,
            "balanced_count": balanced_count,
            "imbalanced_count": total_checks - balanced_count,
            "corrections_made": self.corrections_made,
            "violations_detected": self.violations_detected,
            "current_balance": self.current_balance,
            "is_currently_balanced": self.is_balanced,
            "balance_rate": (balanced_count / total_checks) if total_checks > 0 else 0.0,
        }

    def reset_balance_metrics(self) -> None:
        """
        Reset balance tracking metrics.
        """
        self.balance_history.clear()
        self.corrections_made = 0
        self.violations_detected = 0
        self.current_balance = 0.0
        self.is_balanced = True

