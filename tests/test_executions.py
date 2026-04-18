import pytest

def test_create_execution(client, headers):
    response = client.post("/api/v1/executions/", json={
        "job_id": "JOB-001",
        "job_name": "Test Pipeline",
        "input_params": "source=db1",
        "tags": "test"
    }, headers=headers)
    assert response.status_code == 201
    assert response.json()["job_name"] == "Test Pipeline"
    assert response.json()["status"] == "STARTED"

def test_create_execution_no_auth(client):
    response = client.post("/api/v1/executions/", json={
        "job_id": "JOB-002",
        "job_name": "Test Pipeline 2"
    })
    assert response.status_code == 403

def test_get_executions(client, headers):
    response = client.get("/api/v1/executions/", headers=headers)
    assert response.status_code == 200
    assert "data" in response.json()
    assert "total" in response.json()

def test_get_executions_filter_by_status(client, headers):
    response = client.get(
        "/api/v1/executions/?status=STARTED",
        headers=headers
    )
    assert response.status_code == 200

def test_update_execution(client, headers):
    # First create
    create = client.post("/api/v1/executions/", json={
        "job_id": "JOB-003",
        "job_name": "Update Test Pipeline"
    }, headers=headers)
    execution_id = create.json()["execution_id"]

    # Then update
    response = client.patch(f"/api/v1/executions/{execution_id}", json={
        "status": "SUCCESS",
        "output_summary": "Done",
        "duration_ms": 1000
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "SUCCESS"

def test_update_execution_not_found(client, headers):
    response = client.patch("/api/v1/executions/fake-id-000", json={
        "status": "FAILED",
        "error_details": "Something broke"
    }, headers=headers)
    assert response.status_code == 404

def test_get_single_execution(client, headers):
    create = client.post("/api/v1/executions/", json={
        "job_id": "JOB-004",
        "job_name": "Single Get Test"
    }, headers=headers)
    execution_id = create.json()["execution_id"]

    response = client.get(
        f"/api/v1/executions/{execution_id}",
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["id"] == execution_id