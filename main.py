from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel
import time

from fastapi.responses import RedirectResponse

app = FastAPI()

class Item(BaseModel):
	name: str
	price: float
	brand: Optional[str] = None

inventory = {}
'''{
	1: {
		"name": "Milk",
		"price": 3.99,
		"brand": "Regular"
	},
	2: {
		"name": "Chocolate",
		"price": 2.99,
		"brand": "No Brand"
	}
}'''

# redirects to /docs page 그러나 페이지 상 메세지 띄우는 법 아직 모름
@app.get("/")
def home():
	print("This page contains no message, will redirect")
	time.sleep(5)
	response = RedirectResponse(url='/docs')
	return response
	#return {"This is a home page, move to http://127.0.0.1/docs"}

'''
@app.get("/redirect")
async def redirect():
    response = RedirectResponse(url='/redirected')
    return response

@app.get("/redirected")
async def redirected():
    return {"message": "you've been redirected"}
'''

@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(None, description="The ID of the item you'd like to view", gt=0, lt=3)):
	return inventory[item_id]

@app.get("/get-by-name")
def get_item(*, name: Optional[str] = None, test: int):
	for item_id in inventory:
		if inventory[item_id].name == name:
			return inventory[item_id]

	raise HTTPException(status_code=404, detail="Item name not found.")
	# return {"Data": "Not Found"}

@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
	if item_id in inventory:
		raise HTTPException(status_code=404, detail="Item ID already exists.")
		# return{"Error: Item ID already exists."}

	inventory[item_id] = item
	return inventory[item_id]

# update(put) 해당하는 function 정상 작동 되지 않음 더 찾아볼 것
@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: Item):
	if item_id not in inventory:
		raise HTTPException(status_code=404, detail="Item ID does not exist.")
		# return {"Error": "Item ID does not exist."}

	if item.name != None:
		inventory[item_id].name = item.name
	if item.price != None:
		inventory[item_id].price = item.price
	if item.brand != None:
		inventory[item_id].brand = item.brand

	return inventory[item_id]

@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="The ID of the item you'd like to delete.")):
	if item_id not in inventory:
		raise HTTPException(status_code=404, detail="Item ID does not exist.")
		# return {"Error": "ID does not exist."}

	del inventory[item_id]


'''
@app.get("/")
def home():
	return {"Data": "Testing"}

@app.get("/about")
def about():
	return {"Data": "About"}
'''