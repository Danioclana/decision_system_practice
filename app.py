from fastapi import FastAPI
import uvicorn
from src.controllers.AssetController import AssetController
from src.controllers.IndicatorController import IndicatorController
from src.controllers.CategoryController import CategoryController

app = FastAPI()

# Controllers
assetController = AssetController()
indicatorController = IndicatorController()
categoryController = CategoryController()

# ---------------------------
# Routes for AssetController
# ---------------------------
@app.get("/assets/new")
def create_asset(name: str, type: str, category_id: str):
    assetController.insert_asset(name, type, category_id)
    return {"message": f"Asset '{name}' created successfully"}

@app.get("/assets")
def get_assets():
    return assetController.get_assets()

@app.get("/assets/{asset_id}")
def get_asset(asset_id: int):
    asset = assetController.get_asset_by_id(asset_id)
    return asset if asset else {"error": f"Asset with ID {asset_id} not found"}

@app.get("/assets/{asset_id}/update")
def update_asset(asset_id: int, name: str = None, type: str = None, category_id: str = None):
    assetController.update_asset(asset_id, name, type, category_id)
    return {"message": f"Asset ID {asset_id} updated successfully"}

@app.get("/assets/{asset_id}/delete")
def delete_asset(asset_id: int):
    assetController.delete_asset(asset_id)
    return {"message": f"Asset ID {asset_id} deleted successfully"}

@app.get("/assets/category_id/{category_id}")
def get_assets_by_category(category_id: id):
    return assetController.get_assets_by_category(category_id)

@app.get("/assets/type/{type}")
def get_assets_by_type(type: str):
    return assetController.get_assets_by_type(type)

@app.get("/assets/name/{name}")
def get_assets_by_name(name: str):
    return assetController.get_assets_by_name(name)

@app.get("/indicators/new")
def create_indicator(name: str, value: float, asset_id: int):
    indicatorController.insert_indicator(name, value, asset_id)
    return {"message": f"Indicator '{name}' created successfully"}

@app.get("/indicators")
def get_indicators():
    return indicatorController.get_indicators()

@app.get("/indicators/{indicator_id}")
def get_indicator(indicator_id: int):
    indicator = indicatorController.get_indicator_by_id(indicator_id)
    return indicator if indicator else {"error": f"Indicator with ID {indicator_id} not found"}

@app.get("/indicators/{indicator_id}/update")
def update_indicator(indicator_id: int, name: str = None, value: float = None, asset_id: int = None):
    indicatorController.update_indicator(indicator_id, name, value, asset_id)
    return {"message": f"Indicator ID {indicator_id} updated successfully"}

@app.get("/indicators/{indicator_id}/delete")
def delete_indicator(indicator_id: int):
    indicatorController.delete_indicator(indicator_id)
    return {"message": f"Indicator ID {indicator_id} deleted successfully"}

@app.get("/indicators/asset/{asset_id}")
def get_indicators_by_asset(asset_id: int):
    return indicatorController.get_indicators_by_asset(asset_id)

@app.get("/indicators/name/{name}")
def get_indicators_by_name(name: str):
    return indicatorController.get_indicators_by_name(name)

@app.get("/indicators/value")
def get_indicators_by_value(min_value: float, max_value: float):
    return indicatorController.get_indicators_by_value(min_value, max_value)

@app.get("/categories")
def get_categories():
    return categoryController.get_categories()

@app.get("/categories/new")
def create_category(name: str, description: str):
    categoryController.insert_category(name, description)
    return {"message": f"Category '{name}' created successfully"}

@app.get("/categories/{category_id}")
def get_category(category_id: int):
    category = categoryController.get_category_by_id(category_id)
    return category if category else {"error": f"Category with ID {category_id} not found"}

@app.get("/categories/{category_id}/update")
def update_category(category_id: int, name: str = None):
    categoryController.update_category(category_id, name)
    return {"message": f"Category ID {category_id} updated successfully"}

@app.get("/categories/{category_id}/delete")
def delete_category(category_id: int):
    categoryController.delete_category(category_id)
    return {"message": f"Category ID {category_id} deleted successfully"}

# ---------------------------
# Main server entry point
# ---------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
