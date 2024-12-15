from src.models.Indicator import Indicator
from src.data_acess.IndicatorRepository import IndicatorRepository

import logging
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

class IndicatorController:
    def __init__(self):
        try:
            self.indicator_repository = IndicatorRepository()
        except Exception as e:
            logging.error("Error initializing IndicatorController: %s", e)
            raise

    def get_indicators(self) -> list[Indicator]:
        try:
            indicators = self.indicator_repository.get_indicators()
            return [Indicator(ind[0], ind[1], ind[2], ind[3]) for ind in indicators]
        except Exception as e:
            logging.error("Error getting indicators: %s", e)
            return []

    def get_indicator_by_id(self, indicator_id: int) -> Indicator | None:
        try:
            indicator = self.indicator_repository.get_indicator_by_id(indicator_id)
            if indicator:
                return Indicator(indicator[0], indicator[1], indicator[2], indicator[3])
            return None
        except Exception as e:
            logging.error("Error getting indicator by ID (%s): %s", indicator_id, e)
            return None

    def insert_indicator(self, name: str, value: float, asset_id: int) -> None:
        try:
            self.indicator_repository.insert_indicator(name, value, asset_id)
        except Exception as e:
            logging.error("Error inserting indicator (name: %s): %s", name, e)

    def delete_indicator(self, indicator_id: int) -> None:
        try:
            self.indicator_repository.delete_indicator(indicator_id)
        except Exception as e:
            logging.error("Error deleting indicator (ID: %s): %s", indicator_id, e)

    def update_indicator(self, indicator_id: int, name: str = None, value: float = None, asset_id: int = None) -> None:
        try:
            self.indicator_repository.update_indicator(indicator_id, name, value, asset_id)
        except Exception as e:
            logging.error("Error updating indicator (ID: %s): %s", indicator_id, e)

    def get_indicators_by_name(self, name: str) -> list[Indicator]:
        try:
            indicators = self.indicator_repository.get_indicators_by_name(name)
            return [Indicator(ind[0], ind[1], ind[2], ind[3]) for ind in indicators]
        except Exception as e:
            logging.error("Error getting indicators by name (%s): %s", name, e)
            return []

    def get_indicators_by_value(self, min_value: float, max_value: float) -> list[Indicator]:
        try:
            indicators = self.indicator_repository.get_indicators_by_value(min_value, max_value)
            return [Indicator(ind[0], ind[1], ind[2], ind[3]) for ind in indicators]
        except Exception as e:
            logging.error("Error getting indicators by value range (%s - %s): %s", min_value, max_value, e)
            return []

    def get_indicators_by_asset(self, asset_id: int) -> list[Indicator]:
        try:
            indicators = self.indicator_repository.get_indicators_by_asset(asset_id)
            return [Indicator(ind[0], ind[1], ind[2], ind[3]) for ind in indicators]
        except Exception as e:
            logging.error("Error getting indicators by asset (ID: %s): %s", asset_id, e)
            return []
