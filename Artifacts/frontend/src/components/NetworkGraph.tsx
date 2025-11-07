import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';

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

interface NetworkGraphProps {
  data: NetworkData;
  width?: number;
  height?: number;
}

export const NetworkGraph: React.FC<NetworkGraphProps> = ({
  data,
  width = 800,
  height = 600
}) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);

  useEffect(() => {
    if (!svgRef.current || !data) return;

    // Clear previous graph
    d3.select(svgRef.current).selectAll('*').remove();

    const svg = d3.select(svgRef.current);
    
    // Create graph container
    const container = svg.append('g');

    // Define arrow markers for directed edges
    svg.append('defs').selectAll('marker')
      .data(['transaction', 'shared_device', 'shared_ip'])
      .enter().append('marker')
      .attr('id', d => `arrow-${d}`)
      .attr('viewBox', '0 -5 10 10')
      .attr('refX', 20)
      .attr('refY', 0)
      .attr('markerWidth', 6)
      .attr('markerHeight', 6)
      .attr('orient', 'auto')
      .append('path')
      .attr('d', 'M0,-5L10,0L0,5')
      .attr('fill', d => getEdgeColor(d));

    // Create force simulation
    const simulation = d3.forceSimulation(data.nodes as any)
      .force('link', d3.forceLink(data.edges)
        .id((d: any) => d.id)
        .distance(d => 100))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide().radius(40));

    // Draw edges
    const links = container.append('g')
      .selectAll('line')
      .data(data.edges)
      .enter().append('line')
      .attr('stroke', d => getEdgeColor(d.relationship))
      .attr('stroke-width', d => Math.sqrt(d.weight) * 2)
      .attr('stroke-opacity', 0.6)
      .attr('marker-end', d => `url(#arrow-${d.relationship})`);

    // Draw nodes
    const nodes = container.append('g')
      .selectAll('circle')
      .data(data.nodes)
      .enter().append('circle')
      .attr('r', d => d.type === 'account' ? 20 : 15)
      .attr('fill', d => getNodeColor(d))
      .attr('stroke', d => data.ring_members.includes(d.id) ? '#dc2626' : '#fff')
      .attr('stroke-width', d => data.ring_members.includes(d.id) ? 4 : 2)
      .style('cursor', 'pointer')
      .on('click', (event, d) => {
        setSelectedNode(d);
        event.stopPropagation();
      })
      .call(d3.drag<any, any>()
        .on('start', dragStarted)
        .on('drag', dragged)
        .on('end', dragEnded) as any);

    // Add node labels
    const labels = container.append('g')
      .selectAll('text')
      .data(data.nodes)
      .enter().append('text')
      .text(d => d.id)
      .attr('font-size', 10)
      .attr('dx', 25)
      .attr('dy', 5);

    // Add zoom behavior
    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.5, 3])
      .on('zoom', (event) => {
        container.attr('transform', event.transform);
      });

    svg.call(zoom as any);

    // Update positions on simulation tick
    simulation.on('tick', () => {
      links
        .attr('x1', (d: any) => d.source.x)
        .attr('y1', (d: any) => d.source.y)
        .attr('x2', (d: any) => d.target.x)
        .attr('y2', (d: any) => d.target.y);

      nodes
        .attr('cx', (d: any) => d.x)
        .attr('cy', (d: any) => d.y);

      labels
        .attr('x', (d: any) => d.x)
        .attr('y', (d: any) => d.y);
    });

    // Drag functions
    function dragStarted(event: any) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      event.subject.fx = event.subject.x;
      event.subject.fy = event.subject.y;
    }

    function dragged(event: any) {
      event.subject.fx = event.x;
      event.subject.fy = event.y;
    }

    function dragEnded(event: any) {
      if (!event.active) simulation.alphaTarget(0);
      event.subject.fx = null;
      event.subject.fy = null;
    }

    return () => {
      simulation.stop();
    };
  }, [data, width, height]);

  return (
    <div className="relative">
      <svg
        ref={svgRef}
        width={width}
        height={height}
        className="border border-[#2a2a2a] rounded bg-[#121212] text-[#e5e5e5]"
        onClick={() => setSelectedNode(null)}
      />
      
      {/* Legend */}
      <div className="absolute top-4 right-4 bg-[#151515] border border-[#2a2a2a] p-4 rounded shadow-lg text-sm text-[#e5e5e5]">
        <h3 className="font-semibold mb-2 text-white">Legend</h3>
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded-full bg-blue-500"></div>
            <span className="text-gray-200">Account</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded-full bg-purple-500"></div>
            <span className="text-gray-200">Merchant</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded-full bg-green-500"></div>
            <span className="text-gray-200">Device</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded-full bg-orange-500"></div>
            <span className="text-gray-200">IP Address</span>
          </div>
          <div className="border-t pt-2 mt-2">
            <div className="flex items-center gap-2">
              <div className="w-8 h-0.5 bg-gray-600"></div>
              <span className="text-gray-300">Transaction</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-8 h-0.5 bg-red-600"></div>
              <span className="text-gray-300">Shared Device</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-8 h-0.5 bg-yellow-600"></div>
              <span className="text-gray-300">Shared IP</span>
            </div>
          </div>
        </div>
        {data.fraud_ring_detected && (
          <div className="mt-3 pt-3 border-t border-[#2a2a2a]">
            <div className="flex items-center gap-2 text-red-400 font-semibold">
              <div className="w-4 h-4 rounded-full border-4 border-red-600"></div>
              <span>Fraud Ring Member</span>
            </div>
          </div>
        )}
      </div>

      {/* Node Details Panel */}
      {selectedNode && (
        <div className="absolute bottom-4 left-4 bg-[#151515] border border-[#2a2a2a] p-4 rounded shadow-lg max-w-sm text-[#e5e5e5]">
          <h3 className="font-semibold text-lg mb-2 text-white">{selectedNode.label}</h3>
          <div className="text-sm space-y-1">
            <div className="flex justify-between">
              <span className="text-gray-300">Type:</span>
              <span className="font-medium capitalize text-gray-100">{selectedNode.type}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-300">Risk Score:</span>
              <span className={`font-bold ${
                selectedNode.risk_score > 0.7 ? 'text-red-600' :
                selectedNode.risk_score > 0.3 ? 'text-yellow-400' :
                'text-green-400'
              }`}>
                {(selectedNode.risk_score * 100).toFixed(1)}%
              </span>
            </div>
            {selectedNode.metadata && Object.entries(selectedNode.metadata).map(([key, value]) => (
              <div key={key} className="flex justify-between">
                <span className="text-gray-300 capitalize">{key.replace(/_/g, ' ')}:</span>
                <span className="font-medium text-gray-100">{String(value)}</span>
              </div>
            ))}
            {data.ring_members.includes(selectedNode.id) && (
              <div className="mt-2 pt-2 border-t border-[#2a2a2a]">
                <span className="text-red-400 font-semibold">⚠️ Fraud Ring Member</span>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

// Helper functions
function getNodeColor(node: Node): string {
  const colors: Record<string, string> = {
    account: '#3b82f6',   // blue
    merchant: '#8b5cf6',  // purple
    device: '#10b981',    // green
    ip: '#f59e0b',        // orange
  };
  
  // Darken color for high-risk nodes
  if (node.risk_score > 0.7) {
    const color = d3.color(colors[node.type]);
    return color ? color.darker(1).toString() : colors[node.type];
  }
  
  return colors[node.type] || '#6b7280';
}

function getEdgeColor(relationship: string): string {
  const colors: Record<string, string> = {
    transaction: '#6b7280',
    shared_device: '#dc2626',
    shared_ip: '#f59e0b',
  };
  return colors[relationship] || '#6b7280';
}

