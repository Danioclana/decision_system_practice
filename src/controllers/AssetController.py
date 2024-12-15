from src.models.Asset import Asset
from src.data_acess.AssetRepository import AssetRepository

import logging
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

class AssetController:
    def __init__(self):
        try:
            self.asset_repository = AssetRepository()
        except Exception as e:
            logging.error("Error initializing AssetController: %s", e)
            raise

    def get_assets(self) -> list[Asset]:
        try:
            assets = self.asset_repository.get_assets()
            return [Asset(asset[0], asset[1], asset[2], asset[3]) for asset in assets]
        except Exception as e:
            logging.error("Error getting assets: %s", e)
            return []

    def insert_asset(self, name: str, type: str, category_id: str) -> None:
        try:
            self.asset_repository.insert_asset(name, type, category_id)
        except Exception as e:
            logging.error("Error inserting asset (name: %s, type: %s, category: %s): %s", name, type, category_id, e)

    def delete_asset(self, asset_id: int) -> None:
        try:
            self.asset_repository.delete_asset(asset_id)
        except Exception as e:
            logging.error("Error deleting asset (ID: %s): %s", asset_id, e)

    def update_asset(self, asset_id: int, name: str = None, type: str = None, category_id: str = None) -> None:
        try:
            self.asset_repository.update_asset(asset_id, name, type, category_id)
        except Exception as e:
            logging.error("Error updating asset (ID: %s): %s", asset_id, e)

    def get_asset_by_id(self, asset_id: int) -> Asset | None:
        try:
            asset = self.asset_repository.get_asset_by_id(asset_id)
            if asset:
                return Asset(asset[0], asset[1], asset[2], asset[3])
            logging.warning("No asset found with ID: %s", asset_id)
            return None
        except Exception as e:
            logging.error("Error getting asset by ID (%s): %s", asset_id, e)
            return None

    def get_assets_by_category(self, category_id: str) -> list[Asset]:
        try:
            assets = self.asset_repository.get_assets_by_category(category_id)
            return [Asset(asset[0], asset[1], asset[2], asset[3]) for asset in assets]
        except Exception as e:
            logging.error("Error getting assets by category (%s): %s", category_id, e)
            return []

    def get_assets_by_type(self, type: str) -> list[Asset]:
        try:
            assets = self.asset_repository.get_assets_by_type(type)
            return [Asset(asset[0], asset[1], asset[2], asset[3]) for asset in assets]
        except Exception as e:
            logging.error("Error getting assets by type (%s): %s", type, e)
            return []

    def get_assets_by_name(self, name: str) -> list[Asset]:
        try:
            assets = self.asset_repository.get_assets_by_name(name)
            return [Asset(asset[0], asset[1], asset[2], asset[3]) for asset in assets]
        except Exception as e:
            logging.error("Error getting assets by name (%s): %s", name, e)
            return []
