import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { Box, Typography, Paper } from '@mui/material';

const TriggerHistory = ({ history }) => {
  if (!history || history.length === 0) {
    return (
      <Box sx={{ p: 2, textAlign: 'center' }}>
        <Typography>No trigger history available</Typography>
      </Box>
    );
  }

  // Process history data for charts
  const processHistoryData = () => {
    return history.map(trigger => ({
      timestamp: new Date(trigger.timestamp).toLocaleTimeString(),
      weight: trigger.weight,
      type: trigger.type,
      success: trigger.success ? 1 : 0
    }));
  };

  const data = processHistoryData();

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Trigger Type Distribution */}
      <Paper sx={{ p: 2, mb: 2 }}>
        <Typography variant="subtitle1" gutterBottom>
          Trigger Type Distribution
        </Typography>
        <ResponsiveContainer width="100%" height={100}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="timestamp" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line
              type="monotone"
              dataKey="weight"
              stroke="#8884d8"
              name="Trigger Weight"
            />
            <Line
              type="monotone"
              dataKey="success"
              stroke="#82ca9d"
              name="Success Rate"
            />
          </LineChart>
        </ResponsiveContainer>
      </Paper>

      {/* Recent Triggers List */}
      <Paper sx={{ p: 2, flex: 1, overflow: 'auto' }}>
        <Typography variant="subtitle1" gutterBottom>
          Recent Triggers
        </Typography>
        {history.slice(0, 5).map((trigger, index) => (
          <Box
            key={index}
            sx={{
              p: 1,
              mb: 1,
              border: '1px solid',
              borderColor: 'divider',
              borderRadius: 1
            }}
          >
            <Typography variant="body2">
              Type: {trigger.type}
            </Typography>
            <Typography variant="body2">
              Weight: {trigger.weight.toFixed(2)}
            </Typography>
            <Typography variant="body2">
              Time: {new Date(trigger.timestamp).toLocaleString()}
            </Typography>
            <Typography
              variant="body2"
              color={trigger.success ? 'success.main' : 'error.main'}
            >
              Status: {trigger.success ? 'Success' : 'Failed'}
            </Typography>
          </Box>
        ))}
      </Paper>
    </Box>
  );
};

export default TriggerHistory; 