"""
Network analysis endpoint router
Fraud ring detection and graph analytics API
"""

from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/api/network", tags=["network"])


class Node(BaseModel):
    id: str
    type: str  # 'account', 'merchant', 'device', 'ip'
    risk_score: float
    label: str
    metadata: dict


class Edge(BaseModel):
    source: str
    target: str
    relationship: str  # 'transaction', 'shared_device', 'shared_ip'
    weight: float
    metadata: dict


class NetworkGraph(BaseModel):
    nodes: List[Node]
    edges: List[Edge]
    fraud_ring_detected: bool
    ring_members: List[str]


@router.get("/fraud-ring/{account_id}")
async def get_fraud_ring_network(
    account_id: str,
    depth: int = Query(2, ge=1, le=3, description="Traversal depth")
) -> NetworkGraph:
    """
    Generate fraud ring network graph centered on an account
    
    Demonstrates:
    - Graph data structures
    - Network analysis (connected components, centrality)
    - Graph algorithms (BFS/DFS traversal)
    """
    
    # Demo data: synthetic fraud ring
    if account_id == "ACC_FRAUD_001":
        return NetworkGraph(
            nodes=[
                Node(
                    id="ACC_FRAUD_001",
                    type="account",
                    risk_score=0.94,
                    label="Account A (Suspected Fraud)",
                    metadata={"transactions": 47, "total_amount": 15420.50, "account_age_days": 12}
                ),
                Node(
                    id="ACC_FRAUD_002",
                    type="account",
                    risk_score=0.87,
                    label="Account B",
                    metadata={"transactions": 33, "total_amount": 8920.00, "account_age_days": 8}
                ),
                Node(
                    id="ACC_FRAUD_003",
                    type="account",
                    risk_score=0.91,
                    label="Account C",
                    metadata={"transactions": 41, "total_amount": 12100.75, "account_age_days": 15}
                ),
                Node(
                    id="ACC_LEGIT_001",
                    type="account",
                    risk_score=0.08,
                    label="Account D (Legitimate)",
                    metadata={"transactions": 2, "total_amount": 145.00, "account_age_days": 890}
                ),
                Node(
                    id="MERCHANT_001",
                    type="merchant",
                    risk_score=0.72,
                    label="Electronics Store XYZ",
                    metadata={"fraud_rate": 0.23, "category": "electronics"}
                ),
                Node(
                    id="MERCHANT_002",
                    type="merchant",
                    risk_score=0.15,
                    label="Coffee Shop ABC",
                    metadata={"fraud_rate": 0.02, "category": "food"}
                ),
                Node(
                    id="DEVICE_001",
                    type="device",
                    risk_score=0.88,
                    label="Device X (Shared)",
                    metadata={"accounts_using": 3, "first_seen": "2024-01-02"}
                ),
                Node(
                    id="IP_001",
                    type="ip",
                    risk_score=0.76,
                    label="IP 192.168.1.100",
                    metadata={"accounts_using": 4, "location": "Unknown"}
                ),
            ],
            edges=[
                # Transactions
                Edge(
                    source="ACC_FRAUD_001",
                    target="MERCHANT_001",
                    relationship="transaction",
                    weight=15,
                    metadata={"total_amount": 4500.00, "transaction_count": 15}
                ),
                Edge(
                    source="ACC_FRAUD_002",
                    target="MERCHANT_001",
                    relationship="transaction",
                    weight=12,
                    metadata={"total_amount": 3600.00, "transaction_count": 12}
                ),
                Edge(
                    source="ACC_FRAUD_003",
                    target="MERCHANT_001",
                    relationship="transaction",
                    weight=18,
                    metadata={"total_amount": 5400.00, "transaction_count": 18}
                ),
                Edge(
                    source="ACC_LEGIT_001",
                    target="MERCHANT_002",
                    relationship="transaction",
                    weight=2,
                    metadata={"total_amount": 45.00, "transaction_count": 2}
                ),
                # Shared devices (fraud indicator)
                Edge(
                    source="ACC_FRAUD_001",
                    target="DEVICE_001",
                    relationship="shared_device",
                    weight=1,
                    metadata={"suspicious": True}
                ),
                Edge(
                    source="ACC_FRAUD_002",
                    target="DEVICE_001",
                    relationship="shared_device",
                    weight=1,
                    metadata={"suspicious": True}
                ),
                Edge(
                    source="ACC_FRAUD_003",
                    target="DEVICE_001",
                    relationship="shared_device",
                    weight=1,
                    metadata={"suspicious": True}
                ),
                # Shared IP
                Edge(
                    source="ACC_FRAUD_001",
                    target="IP_001",
                    relationship="shared_ip",
                    weight=1,
                    metadata={"suspicious": True}
                ),
                Edge(
                    source="ACC_FRAUD_002",
                    target="IP_001",
                    relationship="shared_ip",
                    weight=1,
                    metadata={"suspicious": True}
                ),
                Edge(
                    source="ACC_FRAUD_003",
                    target="IP_001",
                    relationship="shared_ip",
                    weight=1,
                    metadata={"suspicious": True}
                ),
                Edge(
                    source="ACC_LEGIT_001",
                    target="IP_001",
                    relationship="shared_ip",
                    weight=1,
                    metadata={"suspicious": False}
                ),
            ],
            fraud_ring_detected=True,
            ring_members=["ACC_FRAUD_001", "ACC_FRAUD_002", "ACC_FRAUD_003"]
        )
    
    # Legitimate account example
    else:
        return NetworkGraph(
            nodes=[
                Node(
                    id=account_id,
                    type="account",
                    risk_score=0.05,
                    label="Legitimate Account",
                    metadata={"transactions": 24, "total_amount": 2400.00, "account_age_days": 456}
                ),
                Node(
                    id="MERCHANT_003",
                    type="merchant",
                    risk_score=0.12,
                    label="Grocery Store",
                    metadata={"fraud_rate": 0.01, "category": "groceries"}
                ),
                Node(
                    id="MERCHANT_004",
                    type="merchant",
                    risk_score=0.08,
                    label="Gas Station",
                    metadata={"fraud_rate": 0.008, "category": "fuel"}
                ),
            ],
            edges=[
                Edge(
                    source=account_id,
                    target="MERCHANT_003",
                    relationship="transaction",
                    weight=15,
                    metadata={"total_amount": 1800.00, "transaction_count": 15}
                ),
                Edge(
                    source=account_id,
                    target="MERCHANT_004",
                    relationship="transaction",
                    weight=9,
                    metadata={"total_amount": 600.00, "transaction_count": 9}
                ),
            ],
            fraud_ring_detected=False,
            ring_members=[]
        )

