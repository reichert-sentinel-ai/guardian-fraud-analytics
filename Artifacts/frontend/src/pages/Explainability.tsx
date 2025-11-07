import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';
import '../styles/dark-theme.css';

interface ShapExplanation {
  transaction_id: string;
  predicted_fraud_probability: number;
  prediction_label: string;
  shap_values: Record<string, number>;
  base_value: number;
  feature_values: Record<string, any>;
}

export const ExplainabilityDemo: React.FC = () => {
  const [selectedTxn, setSelectedTxn] = useState<string>('TXN_001');
  const [explanation, setExplanation] = useState<ShapExplanation | null>(null);
  const [loading, setLoading] = useState(false);

  const sampleTransactions = [
    { id: 'TXN_001', description: 'High-Risk Fraud (94% confidence)', type: 'fraud' },
    { id: 'TXN_002', description: 'Borderline Case (52% confidence)', type: 'borderline' },
    { id: 'TXN_003', description: 'Clearly Legitimate (2% confidence)', type: 'legitimate' },
  ];

  const explainTransaction = async (txnId: string) => {
    setLoading(true);
    try {
      const response = await fetch('/api/explainability/explain', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ transaction_id: txnId })
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setExplanation(data);
    } catch (error) {
      console.error('Failed to load explanation:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    explainTransaction(selectedTxn);
  }, [selectedTxn]);

  if (loading || !explanation) {
    return <div className="p-8 text-center">Loading explanation...</div>;
  }

  // Prepare SHAP values for visualization
  const shapData = Object.entries(explanation.shap_values)
    .map(([feature, value]) => ({
      feature: feature.replace(/_/g, ' '),
      value: value,
      absValue: Math.abs(value)
    }))
    .sort((a, b) => b.absValue - a.absValue);

  const maxAbsValue = Math.max(...shapData.map(d => Math.abs(d.value)));

  return (
    <div className="p-8 bg-gray-50 min-h-screen">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold mb-2">Explainable AI Demo</h1>
        <p className="text-gray-600 mb-8">
          SHAP (SHapley Additive exPlanations) - Understanding why the model made its prediction
        </p>

        {/* Transaction Selector */}
        <div className="bg-white p-6 rounded-lg shadow mb-6">
          <h2 className="text-xl font-semibold mb-4">Select a Transaction to Explain</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {sampleTransactions.map(txn => (
              <button
                key={txn.id}
                onClick={() => setSelectedTxn(txn.id)}
                className={`p-4 rounded-lg border-2 text-left transition-all ${
                  selectedTxn === txn.id
                    ? 'border-purple-500 bg-purple-50'
                    : 'border-gray-200 hover:border-purple-300'
                }`}
              >
                <div className="font-mono text-sm text-gray-500">{txn.id}</div>
                <div className="font-medium mt-1">{txn.description}</div>
                <div className={`text-xs mt-2 px-2 py-1 rounded inline-block ${
                  txn.type === 'fraud' ? 'bg-red-100 text-red-800' :
                  txn.type === 'legitimate' ? 'bg-green-100 text-green-800' :
                  'bg-yellow-100 text-yellow-800'
                }`}>
                  {txn.type.toUpperCase()}
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Prediction Result */}
        <div className="bg-white p-6 rounded-lg shadow mb-6">
          <h2 className="text-xl font-semibold mb-4">Model Prediction</h2>
          <div className="flex items-center justify-between">
            <div>
              <div className="text-sm text-gray-600 mb-1">Fraud Probability</div>
              <div className="text-4xl font-bold">
                {(explanation.predicted_fraud_probability * 100).toFixed(1)}%
              </div>
            </div>
            <div className={`px-6 py-3 rounded-lg font-bold text-2xl ${
              explanation.prediction_label === 'FRAUD'
                ? 'bg-red-100 text-red-800'
                : 'bg-green-100 text-green-800'
            }`}>
              {explanation.prediction_label}
            </div>
          </div>

          {/* Probability Bar */}
          <div className="mt-4">
            <div className="flex justify-between text-sm text-gray-600 mb-1">
              <span>Legitimate</span>
              <span>Threshold (50%)</span>
              <span>Fraud</span>
            </div>
            <div className="relative h-8 bg-gray-200 rounded-full overflow-hidden">
              <div
                className="absolute h-full bg-gradient-to-r from-green-400 via-yellow-400 to-red-500"
                style={{ width: '100%' }}
              />
              <div
                className="absolute h-full w-1 bg-black"
                style={{ left: '50%' }}
              />
              <div
                className="absolute h-full w-3 bg-white border-2 border-black rounded-full"
                style={{ left: `${explanation.predicted_fraud_probability * 100}%`, transform: 'translateX(-50%)' }}
              />
            </div>
          </div>
        </div>

        {/* SHAP Explanation */}
        <div className="bg-white p-6 rounded-lg shadow mb-6">
          <h2 className="text-xl font-semibold mb-2">Feature Contribution (SHAP Values)</h2>
          <p className="text-sm text-gray-600 mb-4">
            How much each feature pushed the prediction toward FRAUD (positive) or LEGITIMATE (negative)
          </p>

          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={shapData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" domain={[-maxAbsValue * 1.1, maxAbsValue * 1.1]} />
              <YAxis dataKey="feature" type="category" width={200} />
              <Tooltip 
                formatter={(value: number) => value.toFixed(3)}
                labelFormatter={(label) => `Feature: ${label}`}
              />
              <Bar dataKey="value" name="SHAP Value">
                {shapData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.value > 0 ? '#ef4444' : '#10b981'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>

          <div className="mt-4 flex gap-6 text-sm">
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-red-500 rounded"></div>
              <span>Pushes toward FRAUD</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-green-500 rounded"></div>
              <span>Pushes toward LEGITIMATE</span>
            </div>
          </div>
        </div>

        {/* Feature Details Table */}
        <div className="bg-white p-6 rounded-lg shadow mb-6">
          <h2 className="text-xl font-semibold mb-4">Feature Details</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-gray-50">
                <tr>
                  <th className="text-left p-3 font-semibold">Feature</th>
                  <th className="text-right p-3 font-semibold">Value</th>
                  <th className="text-right p-3 font-semibold">SHAP Impact</th>
                  <th className="text-left p-3 font-semibold">Interpretation</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                {shapData.map((item, idx) => {
                  const featureKey = item.feature.replace(/ /g, '_');
                  const featureValue = explanation.feature_values[featureKey];
                  
                  return (
                    <tr key={idx} className="hover:bg-gray-50">
                      <td className="p-3 font-medium">{item.feature}</td>
                      <td className="p-3 text-right font-mono">{formatFeatureValue(featureValue)}</td>
                      <td className={`p-3 text-right font-bold ${
                        item.value > 0 ? 'text-red-600' : 'text-green-600'
                      }`}>
                        {item.value > 0 ? '+' : ''}{item.value.toFixed(3)}
                      </td>
                      <td className="p-3 text-gray-600">
                        {getInterpretation(featureKey, item.value, featureValue)}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* How to Read This */}
        <div className="bg-blue-50 border-l-4 border-blue-500 p-6 rounded-r-lg mb-6">
          <h3 className="text-lg font-semibold mb-3 text-blue-900">📖 How to Read This Explanation</h3>
          <div className="space-y-2 text-sm text-blue-800">
            <p>
              <strong>Base Value ({(explanation.base_value * 100).toFixed(2)}%):</strong> The average fraud rate 
              in our dataset. Every prediction starts here.
            </p>
            <p>
              <strong>SHAP Values:</strong> Each feature either increases (red) or decreases (green) the 
              fraud probability from the base value.
            </p>
            <p>
              <strong>Final Prediction:</strong> Base value + sum of all SHAP values = 
              {' '}{(explanation.predicted_fraud_probability * 100).toFixed(1)}% fraud probability
            </p>
            <p>
              <strong>Example:</strong> "Transaction velocity +0.28" means this feature alone increased 
              the fraud probability by 28 percentage points.
            </p>
          </div>
        </div>

        {/* Why This Matters */}
        <div className="bg-white p-6 rounded-lg shadow mb-6">
          <h2 className="text-xl font-semibold mb-4">💡 Why Explainability Matters</h2>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-semibold text-purple-800 mb-2">Regulatory Compliance</h3>
              <ul className="text-sm space-y-1 text-gray-700">
                <li>• GDPR "right to explanation"</li>
                <li>• Fair Credit Reporting Act</li>
                <li>• EU AI Act requirements</li>
                <li>• Court admissibility</li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold text-purple-800 mb-2">Operational Benefits</h3>
              <ul className="text-sm space-y-1 text-gray-700">
                <li>• Faster fraud investigations</li>
                <li>• Build trust with investigators</li>
                <li>• Identify data quality issues</li>
                <li>• Model debugging & improvement</li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold text-purple-800 mb-2">Model Validation</h3>
              <ul className="text-sm space-y-1 text-gray-700">
                <li>• Verify model logic makes sense</li>
                <li>• Detect bias and fairness issues</li>
                <li>• Catch data leakage</li>
                <li>• Understand model limitations</li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold text-purple-800 mb-2">Customer Communication</h3>
              <ul className="text-sm space-y-1 text-gray-700">
                <li>• Explain declined transactions</li>
                <li>• Reduce customer frustration</li>
                <li>• Improve appeal process</li>
                <li>• Build customer trust</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Skills Demonstrated */}
        <div className="bg-gradient-to-r from-purple-50 to-blue-50 border-l-4 border-purple-500 p-6 rounded-r-lg">
          <h3 className="text-lg font-semibold mb-2 text-purple-900">
            🎓 Skills Demonstrated on This Page
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm">
            <div>
              <strong className="text-purple-800">Explainable AI:</strong>
              <ul className="mt-1 text-gray-700">
                <li>• SHAP implementation</li>
                <li>• Feature attribution</li>
                <li>• Model interpretability</li>
              </ul>
            </div>
            <div>
              <strong className="text-purple-800">Data Visualization:</strong>
              <ul className="mt-1 text-gray-700">
                <li>• Waterfall charts</li>
                <li>• Interactive tooltips</li>
                <li>• Color coding</li>
              </ul>
            </div>
            <div>
              <strong className="text-purple-800">Domain Knowledge:</strong>
              <ul className="mt-1 text-gray-700">
                <li>• Regulatory requirements</li>
                <li>• Fraud investigation</li>
                <li>• Business impact</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Helper functions
function formatFeatureValue(value: any): string {
  if (typeof value === 'number') {
    return value % 1 === 0 ? value.toString() : value.toFixed(2);
  }
  return String(value);
}

function getInterpretation(feature: string, shapValue: number, featureValue: any): string {
  const interpretations: Record<string, (shap: number, val: any) => string> = {
    'transaction_velocity_24h': (s, v) => 
      v > 20 ? 'Very high velocity - suspicious' : 'Normal velocity',
    'amount_deviation_from_avg': (s, v) =>
      v > 3 ? 'Highly unusual amount for this user' : 'Typical amount',
    'merchant_risk_score': (s, v) =>
      v > 0.7 ? 'High-risk merchant' : 'Reputable merchant',
    'cross_border_flag': (s, v) =>
      v === 1 ? 'Cross-border adds risk' : 'Domestic transaction',
    'device_fingerprint_mismatch': (s, v) =>
      v === 1 ? 'New/unrecognized device' : 'Known device',
    'account_age_days': (s, v) =>
      v < 30 ? 'Very new account - higher risk' : 'Established account',
  };

  const interpreter = interpretations[feature];
  return interpreter ? interpreter(shapValue, featureValue) : 
    shapValue > 0 ? 'Increases fraud risk' : 'Decreases fraud risk';
}

