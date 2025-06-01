import React from 'react';
import { Box, Typography, Paper } from '@mui/material';
import { diffLines } from 'diff';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

const MutationDiff = ({ mutation }) => {
  if (!mutation) {
    return (
      <Box sx={{ p: 2, textAlign: 'center' }}>
        <Typography>No mutation in progress</Typography>
      </Box>
    );
  }

  const renderDiff = () => {
    const changes = diffLines(mutation.original_code, mutation.mutated_code);
    
    return changes.map((change, index) => {
      const style = {
        backgroundColor: change.added ? '#1b5e20' : change.removed ? '#b71c1c' : 'transparent',
        padding: '2px 0'
      };

      return (
        <Box key={index} sx={style}>
          <SyntaxHighlighter
            language="solidity"
            style={vscDarkPlus}
            customStyle={{
              margin: 0,
              padding: '0 8px',
              background: 'transparent'
            }}
          >
            {change.value}
          </SyntaxHighlighter>
        </Box>
      );
    });
  };

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Mutation Info */}
      <Paper sx={{ p: 2, mb: 2 }}>
        <Typography variant="subtitle1" gutterBottom>
          Mutation Details
        </Typography>
        <Typography variant="body2">
          Type: {mutation.type}
        </Typography>
        <Typography variant="body2">
          Timestamp: {new Date(mutation.timestamp).toLocaleString()}
        </Typography>
        <Typography variant="body2">
          Status: {mutation.status}
        </Typography>
      </Paper>

      {/* Code Diff */}
      <Paper sx={{ p: 2, flex: 1, overflow: 'auto' }}>
        <Typography variant="subtitle1" gutterBottom>
          Code Changes
        </Typography>
        <Box
          sx={{
            backgroundColor: '#1e1e1e',
            borderRadius: 1,
            overflow: 'auto',
            maxHeight: 'calc(100% - 40px)'
          }}
        >
          {renderDiff()}
        </Box>
      </Paper>
    </Box>
  );
};

export default MutationDiff; 