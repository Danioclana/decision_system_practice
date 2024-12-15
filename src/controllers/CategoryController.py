from src.models.Category import Category
from src.data_acess.CategoryRepository import CategoryRepository

import logging
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

class CategoryController:
    def __init__(self):
        try:
            self.category_repository = CategoryRepository()
        except Exception as e:
            logging.error("Error initializing CategoryController: %s", e)
            raise

    def get_categories(self) -> list[Category]:
        try:
            categories = self.category_repository.get_categories()
            return [Category(cat[0], cat[1], cat[2]) for cat in categories]
        except Exception as e:
            logging.error("Error getting categories: %s", e)
            return []

    def insert_category(self, name: str, description: str) -> None:
        try:
            self.category_repository.insert_category(name, description)
        except Exception as e:
            logging.error("Error inserting category (name: %s): %s", name, e)

    def delete_category(self, category_id: int) -> None:
        try:
            self.category_repository.delete_category(category_id)
        except Exception as e:
            logging.error("Error deleting category (ID: %s): %s", category_id, e)

    def update_category(self, category_id: int, name: str = None) -> None:
        try:
            self.category_repository.update_category(category_id, name)
        except Exception as e:
            logging.error("Error updating category (ID: %s): %s", category_id, e)

    def get_category_by_id(self, category_id: int) -> Category | None:
        try:
            category = self.category_repository.get_category_by_id(category_id)
            if category:
                return Category(category[0], category[1])
            logging.warning("No category found with ID: %s", category_id)
            return None
        except Exception as e:
            logging.error("Error getting category by ID (%s): %s", category_id, e)
            return None