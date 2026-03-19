from __future__ import annotations
from application.ports.output_ports import MLModelPort


class MovingAverageForecastModel(MLModelPort):
    def train_and_forecast(self, series: list[float], horizon: int) -> list[float]:
        if not series:
            return [0.0] * horizon
        window = min(3, len(series))
        avg = sum(series[-window:]) / window
        return [float(avg) for _ in range(horizon)]


class RandomForestForecastModel(MLModelPort):
    """Fallback deterministic trend model that preserves the interchangeable ML port."""

    def train_and_forecast(self, series: list[float], horizon: int) -> list[float]:
        if not series:
            return [0.0] * horizon
        if len(series) == 1:
            return [float(series[0])] * horizon
        deltas = [series[index] - series[index - 1] for index in range(1, len(series))]
        avg_delta = sum(deltas) / len(deltas)
        last_value = float(series[-1])
        forecast: list[float] = []
        for step in range(1, horizon + 1):
            forecast.append(max(0.0, last_value + avg_delta * step))
        return forecast
