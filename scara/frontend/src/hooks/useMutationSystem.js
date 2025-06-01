import { useState, useEffect } from 'react';
import { Web3Provider } from '@ethersproject/providers';
import { Contract } from '@ethersproject/contracts';

const useMutationSystem = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [dnaSequence, setDnaSequence] = useState(null);
  const [logicTree, setLogicTree] = useState(null);
  const [triggerHistory, setTriggerHistory] = useState([]);
  const [currentMutation, setCurrentMutation] = useState(null);
  const [simulationResults, setSimulationResults] = useState(null);

  useEffect(() => {
    const initializeSystem = async () => {
      try {
        // Initialize Web3 provider
        const provider = new Web3Provider(window.ethereum);
        await provider.send('eth_requestAccounts', []);
        const signer = provider.getSigner();

        // Load contract ABI and address
        const contractAddress = process.env.REACT_APP_CONTRACT_ADDRESS;
        const contractABI = require('../contracts/MutationSystem.json');
        const contract = new Contract(contractAddress, contractABI, signer);

        // Set up event listeners
        contract.on('MutationProposed', (mutationId, type, timestamp) => {
          fetchMutationDetails(mutationId);
        });

        contract.on('TriggerActivated', (triggerId, weight, timestamp) => {
          fetchTriggerHistory();
        });

        // Initial data fetch
        await Promise.all([
          fetchDnaSequence(),
          fetchLogicTree(),
          fetchTriggerHistory(),
          fetchCurrentMutation(),
          fetchSimulationResults()
        ]);

        setLoading(false);
      } catch (err) {
        setError(err);
        setLoading(false);
      }
    };

    initializeSystem();

    // Cleanup
    return () => {
      // Remove event listeners
    };
  }, []);

  const fetchDnaSequence = async () => {
    try {
      const response = await fetch('/api/mutation/dna-sequence');
      const data = await response.json();
      setDnaSequence(data);
    } catch (err) {
      console.error('Error fetching DNA sequence:', err);
    }
  };

  const fetchLogicTree = async () => {
    try {
      const response = await fetch('/api/mutation/logic-tree');
      const data = await response.json();
      setLogicTree(data);
    } catch (err) {
      console.error('Error fetching logic tree:', err);
    }
  };

  const fetchTriggerHistory = async () => {
    try {
      const response = await fetch('/api/mutation/trigger-history');
      const data = await response.json();
      setTriggerHistory(data);
    } catch (err) {
      console.error('Error fetching trigger history:', err);
    }
  };

  const fetchMutationDetails = async (mutationId) => {
    try {
      const response = await fetch(`/api/mutation/${mutationId}`);
      const data = await response.json();
      setCurrentMutation(data);
    } catch (err) {
      console.error('Error fetching mutation details:', err);
    }
  };

  const fetchCurrentMutation = async () => {
    try {
      const response = await fetch('/api/mutation/current');
      const data = await response.json();
      setCurrentMutation(data);
    } catch (err) {
      console.error('Error fetching current mutation:', err);
    }
  };

  const fetchSimulationResults = async () => {
    try {
      const response = await fetch('/api/mutation/simulation-results');
      const data = await response.json();
      setSimulationResults(data);
    } catch (err) {
      console.error('Error fetching simulation results:', err);
    }
  };

  return {
    loading,
    error,
    dnaSequence,
    logicTree,
    triggerHistory,
    currentMutation,
    simulationResults
  };
};

export default useMutationSystem; 