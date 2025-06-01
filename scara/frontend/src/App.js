import React, { useState, useEffect } from 'react';
import { Box, Container, Grid, Paper, Typography } from '@mui/material';
import DNAStrand from './components/DNAStrand';
import LogicTree from './components/LogicTree';
import TriggerHistory from './components/TriggerHistory';
import MutationDiff from './components/MutationDiff';
import SimulationResults from './components/SimulationResults';
import { useMutationSystem } from './hooks/useMutationSystem';

function App() {
  const {
    dnaSequence,
    logicTree,
    triggerHistory,
    currentMutation,
    simulationResults,
    loading,
    error
  } = useMutationSystem();

  if (loading) {
    return <Typography>Loading mutation system...</Typography>;
  }

  if (error) {
    return <Typography color="error">Error: {error.message}</Typography>;
  }

  return (
    <Container maxWidth="xl">
      <Box sx={{ my: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          SCARA Mutation System
        </Typography>
        
        <Grid container spacing={3}>
          {/* DNA Strand Visualization */}
          <Grid item xs={12} md={6}>
            <Paper elevation={3} sx={{ p: 2, height: '400px' }}>
              <Typography variant="h6" gutterBottom>
                DNA Evolution
              </Typography>
              <DNAStrand sequence={dnaSequence} />
            </Paper>
          </Grid>

          {/* Logic Tree Visualization */}
          <Grid item xs={12} md={6}>
            <Paper elevation={3} sx={{ p: 2, height: '400px' }}>
              <Typography variant="h6" gutterBottom>
                Logic Tree
              </Typography>
              <LogicTree tree={logicTree} />
            </Paper>
          </Grid>

          {/* Trigger History */}
          <Grid item xs={12} md={6}>
            <Paper elevation={3} sx={{ p: 2, height: '400px' }}>
              <Typography variant="h6" gutterBottom>
                Trigger History
              </Typography>
              <TriggerHistory history={triggerHistory} />
            </Paper>
          </Grid>

          {/* Current Mutation */}
          <Grid item xs={12} md={6}>
            <Paper elevation={3} sx={{ p: 2, height: '400px' }}>
              <Typography variant="h6" gutterBottom>
                Current Mutation
              </Typography>
              <MutationDiff mutation={currentMutation} />
            </Paper>
          </Grid>

          {/* Simulation Results */}
          <Grid item xs={12}>
            <Paper elevation={3} sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Simulation Results
              </Typography>
              <SimulationResults results={simulationResults} />
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
}

export default App; 