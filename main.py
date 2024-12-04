#from http.client import HTTPException

from fastapi import FastAPI, HTTPException, status, Response
from starlette.status import HTTP_204_NO_CONTENT

from models.db import db
from models.models import Sheep

app = FastAPI()

@app.get("/sheep/{id}", response_model=Sheep)
def read_sheep(id: int):
    if id not in db.data:
        raise HTTPException(status_code=404, detail="Sheep not found")
    return db.get_sheep(id)

@app.post("/sheep/", response_model=Sheep, status_code=status.HTTP_201_CREATED)
def add_sheep(sheep: Sheep):
    # Check if the sheep ID already exists to avoid duplicates
    if sheep.id in db.data:
        raise HTTPException(status_code=400, detail="Sheep with this iD already exists")
    # Add the new sheep to the database
    db.data[sheep.id] = sheep
    return sheep # Return the newly added sheep data

### Extra Credit
#########################################################################################
# Delete a sheep by ID
@app.delete("/sheep/{id}", status_code=HTTP_204_NO_CONTENT)
def delete_sheep(id: int):
    if id not in db.data:
        raise HTTPException(status_code=404, detail="Sheep not found")
    del db.data[id]
    return Response(status_code=204)  # Explicit 204 return


# Update a sheep by ID
@app.put("/sheep/{id}", response_model=Sheep)
def update_sheep(id: int, updated_sheep: Sheep):
    if id not in db.data:
        raise HTTPException(status_code=404, detail="Sheep not found")
    db.data[id] = updated_sheep
    return updated_sheep

# Read all sheep
@app.get("/sheep/", response_model=list[Sheep])
def read_all_sheep():
    return list(db.data.values())