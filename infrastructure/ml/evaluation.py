from __future__ import annotations
import math


def regression_metrics(actual: list[float], predicted: list[float]) -> dict[str, float]:
    if len(actual) != len(predicted):
        raise ValueError("actual and predicted must have the same length")
    if not actual:
        return {"mae": 0.0, "rmse": 0.0, "mape": 0.0}
    errors = [abs(a - p) for a, p in zip(actual, predicted)]
    squared_errors = [(a - p) ** 2 for a, p in zip(actual, predicted)]
    percentage_errors = [abs((a - p) / (a if a != 0 else 1)) for a, p in zip(actual, predicted)]
    return {
        "mae": sum(errors) / len(errors),
        "rmse": math.sqrt(sum(squared_errors) / len(squared_errors)),
        "mape": (sum(percentage_errors) / len(percentage_errors)) * 100,
    }
