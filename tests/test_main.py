# Import TestClient to stimulate API requests
from fastapi.testclient import TestClient

# Import the FastAPI app instance from the controller module
from main import app

# Create a TestClient instance for the FastAPI app
client = TestClient(app)


# Define a test function for reading a specific sheep
def test_read_sheep():
    # Send a GET request to the endpoint "/sheep/1"
    response = client.get("/sheep/1")

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Assert that the response JSON matches the expected data
    assert response.json() == {
        # Expected JSON structure
        "id": 1,
        "name": "Spice",
        "breed": "Gotland",
        "sex": "ewe"
    }


# Define a test function for adding a new sheep
def test_add_sheep():
    # Prepare the new sheep data in a dictionary format.
    new_sheep_data = {
        "id": 7,
        "name": "Lorax",
        "breed": "Gotland",
        "sex": "ewe"
    }

    # Send a POST request to the endpoint "/sheep" with the new sheep data
    # Arguments should be endpoint and new sheep data
    response = client.post("/sheep", json=new_sheep_data)

    # Assert that the response status code is 201 (Created)
    assert response.status_code == 201

    # Assert that the response JSON matches the new sheep data
    assert response.json() == new_sheep_data

    # Verify that the sheep was actually added to the database by retrieving the new sheep by ID.
    # include an assert statement to see if the new sheep data can be retrieved.
    response = client.get(f"/sheep/{new_sheep_data['id']}")
    assert response.status_code == 200
    assert response.json() == new_sheep_data


### Extra Credit
#########################################################################################
def test_delete_sheep():
    #  Add a new sheep to delete
    sheep_to_delete = {
        "id": 8,
        "name": "Phlegm",
        "breed": "Merino",
        "sex": "ewe",
    }
    client.post("/sheep", json=sheep_to_delete)

    # Delete the newly added sheep
    response = client.delete(f"/sheep/{sheep_to_delete['id']}")
    assert response.status_code == 204

    # Verify it was deleted
    response = client.get(f"/sheep/{sheep_to_delete['id']}")
    assert response.status_code == 404


def test_update_sheep():
    # Add a new sheep to update
    sheep_to_update = {
        "id": 9,
        "name": "Rocky",
        "breed": "Suffolk",
        "sex": "ram",
    }
    client.post("/sheep", json=sheep_to_update)

    # Update the newly added sheep
    updated_sheep_data = {
        "id": 9,
        "name": "Sven",
        "breed": "Suffolk",
        "sex": "ram",
    }
    response = client.put(f"/sheep/{sheep_to_update['id']}", json=updated_sheep_data)
    assert response.status_code == 200
    assert response.json() == updated_sheep_data

    # Verify it was updated
    response = client.get(f"/sheep/{sheep_to_update['id']}")
    assert response.status_code == 200
    assert response.json() == updated_sheep_data


def test_read_all_sheep():
    response = client.get("/sheep")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0  # Make sure there’s at least one sheep in the list


