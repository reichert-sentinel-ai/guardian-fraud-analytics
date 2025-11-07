import React, { useState, useEffect } from 'react';
import { NetworkGraph } from '../components/NetworkGraph';
import '../styles/dark-theme.css';

interface Node {
  id: string;
  type: string;
  risk_score: number;
  label: string;
  metadata: any;
}

interface Edge {
  source: string;
  target: string;
  relationship: string;
  weight: number;
  metadata: any;
}

interface NetworkData {
  nodes: Node[];
  edges: Edge[];
  fraud_ring_detected: boolean;
  ring_members: string[];
}

export const NetworkAnalysisPage: React.FC = () => {
  const [accountId, setAccountId] = useState('ACC_FRAUD_001');
  const [networkData, setNetworkData] = useState<NetworkData | null>(null);
  const [loading, setLoading] = useState(false);

  const loadNetwork = async (accId: string) => {
    setLoading(true);
    try {
      const response = await fetch(`/api/network/fraud-ring/${accId}?depth=2`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setNetworkData(data);
    } catch (error) {
      console.error('Failed to load network:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadNetwork(accountId);
  }, [accountId]);

  return (
    <div className="p-8 min-h-screen bg-[#0f0f0f] text-[#e5e5e5] transition-colors">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold mb-2 text-white">Fraud Ring Network Analysis</h1>
        <p className="text-gray-300 mb-8">
          Interactive graph visualization showing connections between accounts, devices, and merchants
        </p>

        {/* Account Selector */}
        <div className="bg-[#151515] border border-[#2a2a2a] p-6 rounded-lg shadow-lg mb-6">
          <h2 className="text-xl font-semibold mb-4 text-white">Select Account to Analyze</h2>
          <div className="flex gap-4">
            <button
              onClick={() => setAccountId('ACC_FRAUD_001')}
              className={`px-6 py-3 rounded-lg font-medium transition-all ${
                accountId === 'ACC_FRAUD_001'
                  ? 'bg-red-500 text-white'
                  : 'bg-[#1f1f1f] text-gray-200 hover:bg-[#2a2a2a]'
              }`}
            >
              Fraud Ring Example
            </button>
            <button
              onClick={() => setAccountId('ACC_LEGIT_001')}
              className={`px-6 py-3 rounded-lg font-medium transition-all ${
                accountId === 'ACC_LEGIT_001'
                  ? 'bg-green-500 text-white'
                  : 'bg-[#1f1f1f] text-gray-200 hover:bg-[#2a2a2a]'
              }`}
            >
              Legitimate Example
            </button>
          </div>
        </div>

        {/* Fraud Alert */}
        {networkData?.fraud_ring_detected && (
          <div className="bg-red-900/20 border-l-4 border-red-500/70 p-6 rounded-r-lg mb-6">
            <div className="flex items-center gap-3">
              <div className="text-3xl">🚨</div>
              <div className="text-red-100">
                <h3 className="text-lg font-semibold text-red-300">Fraud Ring Detected</h3>
                <p className="text-red-200">
                  {networkData.ring_members.length} connected accounts sharing devices and IP addresses.
                  This pattern is highly suspicious and warrants immediate investigation.
                </p>
                <div className="mt-2 text-sm text-red-200">
                  <strong>Ring Members:</strong> {networkData.ring_members.join(', ')}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Network Graph */}
        <div className="bg-[#151515] border border-[#2a2a2a] p-6 rounded-lg shadow-xl mb-6">
          <h2 className="text-xl font-semibold mb-4">Network Visualization</h2>
          <p className="text-sm text-gray-300 mb-4">
            <strong>Tip:</strong> Click and drag nodes to explore. Scroll to zoom. Click nodes for details.
          </p>
          {loading ? (
            <div className="flex items-center justify-center h-96">
              <div className="text-gray-400">Loading network...</div>
            </div>
          ) : networkData ? (
            <NetworkGraph data={networkData} width={1000} height={600} />
          ) : (
            <div className="text-gray-400 text-center p-8">No data available</div>
          )}
        </div>

        {/* Graph Metrics */}
        {networkData && (
          <div className="bg-[#151515] border border-[#2a2a2a] p-6 rounded-lg shadow-lg mb-6">
            <h2 className="text-xl font-semibold mb-4">Network Metrics</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="p-4 bg-blue-900/20 border border-blue-600/40 rounded-lg">
                <div className="text-sm text-blue-300 font-medium">Total Nodes</div>
                <div className="text-2xl font-bold text-blue-200">{networkData.nodes.length}</div>
              </div>
              <div className="p-4 bg-purple-900/20 border border-purple-600/40 rounded-lg">
                <div className="text-sm text-purple-300 font-medium">Total Connections</div>
                <div className="text-2xl font-bold text-purple-200">{networkData.edges.length}</div>
              </div>
              <div className="p-4 bg-green-900/20 border border-green-600/40 rounded-lg">
                <div className="text-sm text-green-300 font-medium">Density</div>
                <div className="text-2xl font-bold text-green-200">
                  {(networkData.edges.length / (networkData.nodes.length * (networkData.nodes.length - 1)) * 100).toFixed(1)}%
                </div>
              </div>
              <div className="p-4 bg-red-900/20 border border-red-600/40 rounded-lg">
                <div className="text-sm text-red-300 font-medium">High-Risk Nodes</div>
                <div className="text-2xl font-bold text-red-200">
                  {networkData.nodes.filter(n => n.risk_score > 0.7).length}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* How It Works */}
        <div className="bg-[#151515] border border-[#2a2a2a] p-6 rounded-lg shadow-lg mb-6">
          <h2 className="text-xl font-semibold mb-4 text-white">How Fraud Ring Detection Works</h2>
          <div className="grid md:grid-cols-3 gap-6 text-sm">
            <div>
              <h3 className="font-semibold text-purple-300 mb-2">1. Connection Discovery</h3>
              <p className="text-gray-300">
                Graph traversal algorithms (BFS/DFS) find all entities connected to the suspect account
                within a specified depth (typically 2-3 hops).
              </p>
            </div>
            <div>
              <h3 className="font-semibold text-purple-300 mb-2">2. Pattern Analysis</h3>
              <p className="text-gray-300">
                Community detection algorithms identify tightly connected clusters. Shared devices/IPs
                among multiple accounts are strong fraud indicators.
              </p>
            </div>
            <div>
              <h3 className="font-semibold text-purple-300 mb-2">3. Risk Scoring</h3>
              <p className="text-gray-300">
                Network centrality measures (PageRank, betweenness) combined with transaction patterns
                calculate overall risk scores for each node.
              </p>
            </div>
          </div>
        </div>

        {/* Skills Demonstrated */}
        <div className="bg-gradient-to-r from-purple-900/30 to-blue-900/30 border-l-4 border-purple-500/70 p-6 rounded-r-lg">
          <h3 className="text-lg font-semibold mb-2 text-purple-200">
            🎓 Skills Demonstrated
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-gray-200">
            <div>
              <strong className="text-purple-200">Graph Theory:</strong>
              <ul className="mt-1 space-y-0.5">
                <li>• Graph data structures</li>
                <li>• BFS/DFS traversal</li>
                <li>• Community detection</li>
                <li>• Centrality measures</li>
              </ul>
            </div>
            <div>
              <strong className="text-purple-200">Data Visualization:</strong>
              <ul className="mt-1 space-y-0.5">
                <li>• D3.js force simulation</li>
                <li>• Interactive graphics</li>
                <li>• Drag & zoom</li>
                <li>• Dynamic layouts</li>
              </ul>
            </div>
            <div>
              <strong className="text-purple-200">Database:</strong>
              <ul className="mt-1 space-y-0.5">
                <li>• Neo4j / graph DBs</li>
                <li>• Cypher queries</li>
                <li>• Graph modeling</li>
                <li>• Query optimization</li>
              </ul>
            </div>
            <div>
              <strong className="text-purple-200">Domain Expertise:</strong>
              <ul className="mt-1 space-y-0.5">
                <li>• Fraud typologies</li>
                <li>• Ring detection</li>
                <li>• Network forensics</li>
                <li>• Investigation workflows</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

