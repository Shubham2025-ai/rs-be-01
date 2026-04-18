def test_get_audit_trail(client, headers):
    # Create execution first
    create = client.post("/api/v1/executions/", json={
        "job_id": "JOB-AUDIT",
        "job_name": "Audit Test Pipeline"
    }, headers=headers)
    execution_id = create.json()["execution_id"]

    # Get audit trail
    response = client.get(
        f"/api/v1/executions/{execution_id}/audit",
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["execution_id"] == execution_id
    assert response.json()["total_events"] >= 1
    assert len(response.json()["audit_trail"]) >= 1

def test_audit_trail_not_found(client, headers):
    response = client.get(
        "/api/v1/executions/fake-id-999/audit",
        headers=headers
    )
    assert response.status_code == 404

def test_summary_stats(client, headers):
    response = client.get(
        "/api/v1/executions/summary/stats",
        headers=headers
    )
    assert response.status_code == 200
    assert "total_executions" in response.json()
    assert "success_rate_percent" in response.json()
    assert "average_duration_ms" in response.json()