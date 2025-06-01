import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar
} from 'recharts';
import { Box, Typography, Paper, Grid } from '@mui/material';

const SimulationResults = ({ results }) => {
  if (!results) {
    return (
      <Box sx={{ p: 2, textAlign: 'center' }}>
        <Typography>No simulation results available</Typography>
      </Box>
    );
  }

  const processMetricsData = () => {
    return results.metrics_history.map(metric => ({
      timestamp: new Date(metric.timestamp).toLocaleTimeString(),
      gas_usage: metric.gas_usage,
      execution_time: metric.execution_time,
      success_rate: metric.success_rate * 100,
      error_rate: metric.error_rate * 100,
      memory_usage: metric.memory_usage
    }));
  };

  const data = processMetricsData();

  return (
    <Grid container spacing={2}>
      {/* Performance Metrics */}
      <Grid item xs={12}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="subtitle1" gutterBottom>
            Performance Metrics Over Time
          </Typography>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="timestamp" />
              <YAxis yAxisId="left" />
              <YAxis yAxisId="right" orientation="right" />
              <Tooltip />
              <Legend />
              <Line
                yAxisId="left"
                type="monotone"
                dataKey="gas_usage"
                stroke="#8884d8"
                name="Gas Usage"
              />
              <Line
                yAxisId="left"
                type="monotone"
                dataKey="memory_usage"
                stroke="#82ca9d"
                name="Memory Usage"
              />
              <Line
                yAxisId="right"
                type="monotone"
                dataKey="success_rate"
                stroke="#ffc658"
                name="Success Rate (%)"
              />
              <Line
                yAxisId="right"
                type="monotone"
                dataKey="error_rate"
                stroke="#ff8042"
                name="Error Rate (%)"
              />
            </LineChart>
          </ResponsiveContainer>
        </Paper>
      </Grid>

      {/* Success/Error Distribution */}
      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="subtitle1" gutterBottom>
            Success/Error Distribution
          </Typography>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="timestamp" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="success_rate" fill="#82ca9d" name="Success Rate (%)" />
              <Bar dataKey="error_rate" fill="#ff8042" name="Error Rate (%)" />
            </BarChart>
          </ResponsiveContainer>
        </Paper>
      </Grid>

      {/* Resource Usage */}
      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="subtitle1" gutterBottom>
            Resource Usage
          </Typography>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="timestamp" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="gas_usage" fill="#8884d8" name="Gas Usage" />
              <Bar dataKey="memory_usage" fill="#82ca9d" name="Memory Usage" />
            </BarChart>
          </ResponsiveContainer>
        </Paper>
      </Grid>

      {/* Summary Statistics */}
      <Grid item xs={12}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="subtitle1" gutterBottom>
            Summary Statistics
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={6} md={3}>
              <Typography variant="body2" color="text.secondary">
                Average Gas Usage
              </Typography>
              <Typography variant="h6">
                {Math.round(data.reduce((acc, curr) => acc + curr.gas_usage, 0) / data.length)}
              </Typography>
            </Grid>
            <Grid item xs={6} md={3}>
              <Typography variant="body2" color="text.secondary">
                Average Success Rate
              </Typography>
              <Typography variant="h6">
                {Math.round(data.reduce((acc, curr) => acc + curr.success_rate, 0) / data.length)}%
              </Typography>
            </Grid>
            <Grid item xs={6} md={3}>
              <Typography variant="body2" color="text.secondary">
                Average Memory Usage
              </Typography>
              <Typography variant="h6">
                {Math.round(data.reduce((acc, curr) => acc + curr.memory_usage, 0) / data.length)}
              </Typography>
            </Grid>
            <Grid item xs={6} md={3}>
              <Typography variant="body2" color="text.secondary">
                Total Simulations
              </Typography>
              <Typography variant="h6">
                {data.length}
              </Typography>
            </Grid>
          </Grid>
        </Paper>
      </Grid>
    </Grid>
  );
};

export default SimulationResults; 