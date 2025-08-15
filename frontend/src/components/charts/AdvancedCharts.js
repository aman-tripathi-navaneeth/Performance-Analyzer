import React, { useState, useMemo, useEffect } from "react";
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  ScatterChart,
  Scatter,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  ComposedChart,
  ReferenceLine,
} from "recharts";
import "./AdvancedCharts.css";

// Chart styling configuration for better visibility
const chartStyle = {
  backgroundColor: "#ffffff",
  fontSize: "14px",
  color: "#1F2937",
};

const axisStyle = {
  fontSize: "12px",
  fill: "#374151",
  stroke: "#D1D5DB",
};

// Theme helpers for light/dark modes
const getThemeStyles = (theme = "light") => {
  const isDark = theme === "dark";
  return {
    axisTick: isDark ? "#E5E7EB" : "#374151",
    axisLine: isDark ? "#334155" : "#D1D5DB",
    grid: isDark ? "#1F2937" : "#E5E7EB",
    legendText: isDark ? "#E5E7EB" : "#374151",
    titleText: isDark ? "#F8FAFC" : "#111827",
    subtitleText: isDark ? "#CBD5E1" : "#6B7280",
  };
};

const tooltipStyle = {
  backgroundColor: "#ffffff",
  border: "1px solid #E5E7EB",
  borderRadius: "8px",
  padding: "12px",
  boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
  fontSize: "12px",
  color: "#1F2937",
};

// Performance Bar Chart Component
export const PerformanceBarChart = ({
  data,
  title = "Subject Performance Analysis",
  subtitle = "Average performance scores across different subjects",
  xKey = "name",
  yKey = "value",
  color = "#7C3AED",
  showMean = true,
  showTarget = false,
  targetValue = 80,
  height = 450,
  onBarClick,
  customTooltip,
  showGrid = true,
  showLegend = true,
}) => {
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-4 border border-gray-200 rounded-lg shadow-xl backdrop-blur-sm">
          <p className="font-semibold text-gray-900 text-sm mb-2">{label}</p>
          <p className="text-blue-600 font-medium">
            Performance: {payload[0].value.toFixed(1)}%
          </p>
          {data.students && (
            <p className="text-green-600 font-medium">
              Students: {data.students}
            </p>
          )}
          {data.assessments && (
            <p className="text-purple-600 font-medium">
              Assessments: {data.assessments}
            </p>
          )}
          {customTooltip && customTooltip(data)}
        </div>
      );
    }
    return null;
  };

  const meanValue = data.reduce((sum, item) => sum + (item[yKey] || 0), 0) / data.length;

  return (
    <div className="bg-white p-4 rounded-xl shadow-lg border border-gray-100">
      <div className="mb-4">
        <h3 className="text-xl font-semibold text-gray-900 mb-1">{title}</h3>
        <p className="text-sm text-gray-600">{subtitle}</p>
      </div>
      <div className="bg-gradient-to-br from-gray-50 to-gray-100 p-4 rounded-xl border border-gray-200">
        <ResponsiveContainer width="100%" height={height}>
          <BarChart
            data={data}
            margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
            onClick={(data) => onBarClick && onBarClick(data)}
            style={chartStyle}
          >
            {showGrid && (
              <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" strokeWidth={1} />
            )}
            <XAxis
              dataKey={xKey}
              style={axisStyle}
              tick={{ fill: "#374151", fontSize: 12, fontWeight: "500" }}
              axisLine={{ stroke: "#D1D5DB" }}
              tickLine={{ stroke: "#D1D5DB" }}
              angle={-45}
              textAnchor="end"
              height={60}
              interval={0}
              label={{ 
                value: "Subjects", 
                position: "bottom", 
                offset: 50,
                style: { textAnchor: "middle", fontSize: 14, fontWeight: "600", fill: "#374151" }
              }}
            />
            <YAxis
              style={axisStyle}
              tick={{ fill: "#374151", fontSize: 12 }}
              domain={[0, 100]}
              axisLine={{ stroke: "#D1D5DB" }}
              tickLine={{ stroke: "#D1D5DB" }}
              label={{ 
                value: "Performance Score (%)", 
                angle: -90, 
                position: "insideLeft",
                style: { textAnchor: "middle", fontSize: 14, fontWeight: "600", fill: "#374151" }
              }}
            />
            <Tooltip content={<CustomTooltip />} />
            {showLegend && (
              <Legend 
                wrapperStyle={{ 
                  paddingTop: '20px',
                  fontSize: '14px',
                  color: '#374151'
                }}
              />
            )}
            <Bar
              dataKey={yKey}
              name="Performance Score"
              fill={color}
              radius={[6, 6, 0, 0]}
              stroke={color}
              strokeWidth={1}
            />
            {showMean && (
              <Line
                type="monotone"
                dataKey={() => meanValue}
                stroke="#EF4444"
                strokeWidth={2}
                strokeDasharray="5 5"
                name={`Mean (${meanValue.toFixed(1)}%)`}
              />
            )}
            {showTarget && (
              <Line
                type="monotone"
                dataKey={() => targetValue}
                stroke="#10B981"
                strokeWidth={2}
                strokeDasharray="3 3"
                name={`Target (${targetValue}%)`}
              />
            )}
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

// Trend Line Chart Component
export const TrendLineChart = ({
  data,
  title = "Performance Trends Analysis",
  subtitle = "Performance progression over time periods",
  xKey = "period",
  yKey = "value",
  color = "#7C3AED",
  height = 450,
  smooth = true,
  area = false,
  showGrid = true,
  showLegend = true,
}) => {
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-4 border border-gray-200 rounded-lg shadow-xl backdrop-blur-sm">
          <p className="font-semibold text-gray-900 text-sm mb-2">{label}</p>
          <p className="text-blue-600 font-medium">
            Performance: {payload[0].value.toFixed(1)}%
          </p>
          {data.change && (
            <p className={`font-medium ${data.change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
              Change: {data.change >= 0 ? '+' : ''}{data.change.toFixed(1)}%
            </p>
          )}
          {data.assessments && (
            <p className="text-purple-600 font-medium">
              Assessments: {data.assessments}
            </p>
          )}
        </div>
      );
    }
    return null;
  };

  const ChartComponent = area ? AreaChart : LineChart;
  const DataComponent = area ? Area : Line;

  return (
    <div className="bg-white p-4 rounded-xl shadow-lg border border-gray-100">
      <div className="mb-4">
        <h3 className="text-xl font-semibold text-gray-900 mb-1">{title}</h3>
        <p className="text-sm text-gray-600">{subtitle}</p>
      </div>
      <div className="bg-gradient-to-br from-gray-50 to-gray-100 p-4 rounded-xl border border-gray-200">
        <ResponsiveContainer width="100%" height={height}>
          <ChartComponent
            data={data}
            margin={{ top: 20, right: 30, left: 20, bottom: 20 }}
            style={chartStyle}
          >
            {showGrid && (
              <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" strokeWidth={1} />
            )}
            <XAxis
              dataKey={xKey}
              style={axisStyle}
              tick={{ fill: "#374151", fontSize: 12, fontWeight: "500" }}
              axisLine={{ stroke: "#D1D5DB" }}
              tickLine={{ stroke: "#D1D5DB" }}
              label={{ 
                value: "Time Period", 
                position: "bottom", 
                offset: 10,
                style: { textAnchor: "middle", fontSize: 14, fontWeight: "600", fill: "#374151" }
              }}
            />
            <YAxis
              style={axisStyle}
              tick={{ fill: "#374151", fontSize: 12 }}
              domain={[0, 100]}
              axisLine={{ stroke: "#D1D5DB" }}
              tickLine={{ stroke: "#D1D5DB" }}
              label={{ 
                value: "Performance Score (%)", 
                angle: -90, 
                position: "insideLeft",
                style: { textAnchor: "middle", fontSize: 14, fontWeight: "600", fill: "#374151" }
              }}
            />
            <Tooltip content={<CustomTooltip />} />
            {showLegend && (
              <Legend 
                wrapperStyle={{ 
                  paddingTop: '20px',
                  fontSize: '14px',
                  color: '#374151'
                }}
              />
            )}
            <DataComponent
              type={smooth ? "monotone" : "linear"}
              dataKey={yKey}
              name="Performance Score"
              stroke={color}
              fill={area ? color : "none"}
              fillOpacity={area ? 0.3 : 1}
              strokeWidth={4}
              dot={{ fill: color, strokeWidth: 2, r: 6 }}
              activeDot={{ r: 8, stroke: color, strokeWidth: 3 }}
            />
          </ChartComponent>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

// Scatter Plot Chart Component
export const ScatterPlotChart = ({
  data,
  title = "Performance Correlation Analysis",
  subtitle = "Relationship between different performance metrics",
  xKey = "x",
  yKey = "y",
  color = "#7C3AED",
  height = 450,
  onPointClick,
  showGrid = true,
  showLegend = true,
}) => {
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const point = payload[0].payload;
      return (
        <div className="bg-white p-4 border border-gray-200 rounded-lg shadow-xl backdrop-blur-sm">
          <p className="font-semibold text-gray-900 text-sm mb-2">
            {point.name || `Point ${label}`}
          </p>
          <p className="text-blue-600 font-medium">
            {getAxisLabel(xKey)}: {point[xKey].toFixed(1)}%
          </p>
          <p className="text-green-600 font-medium">
            {getAxisLabel(yKey)}: {point[yKey].toFixed(1)}%
          </p>
          {point.grade && (
            <p className="text-purple-600 font-medium">
              Grade: {point.grade}
            </p>
          )}
          {point.subject && (
            <p className="text-orange-600 font-medium">
              Subject: {point.subject}
            </p>
          )}
        </div>
      );
    }
    return null;
  };

  const getAxisLabel = (key) => {
    const labels = {
      x: "Overall Performance",
      y: "Subject Performance", 
      overall: "Overall Performance",
      subject: "Subject Performance",
      attendance: "Attendance Rate",
      participation: "Participation Score"
    };
    return labels[key] || key.charAt(0).toUpperCase() + key.slice(1);
  };

  return (
    <div className="bg-white p-4 rounded-xl shadow-lg border border-gray-100">
      <div className="mb-4">
        <h3 className="text-xl font-semibold text-gray-900 mb-1">{title}</h3>
        <p className="text-sm text-gray-600">{subtitle}</p>
      </div>
      <div className="bg-gradient-to-br from-gray-50 to-gray-100 p-4 rounded-xl border border-gray-200">
        <ResponsiveContainer width="100%" height={height}>
          <ScatterChart
            data={data}
            margin={{ top: 20, right: 30, left: 20, bottom: 20 }}
            style={chartStyle}
          >
            {showGrid && (
              <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" strokeWidth={1} />
            )}
            <XAxis
              dataKey={xKey}
              style={axisStyle}
              tick={{ fill: "#374151", fontSize: 12, fontWeight: "500" }}
              axisLine={{ stroke: "#D1D5DB" }}
              tickLine={{ stroke: "#D1D5DB" }}
              domain={[0, 100]}
              label={{ 
                value: `${getAxisLabel(xKey)} (%)`, 
                position: "bottom", 
                offset: 10,
                style: { textAnchor: "middle", fontSize: 14, fontWeight: "600", fill: "#374151" }
              }}
            />
            <YAxis
              dataKey={yKey}
              style={axisStyle}
              tick={{ fill: "#374151", fontSize: 12 }}
              axisLine={{ stroke: "#D1D5DB" }}
              tickLine={{ stroke: "#D1D5DB" }}
              domain={[0, 100]}
              label={{ 
                value: `${getAxisLabel(yKey)} (%)`, 
                angle: -90, 
                position: "insideLeft",
                style: { textAnchor: "middle", fontSize: 14, fontWeight: "600", fill: "#374151" }
              }}
            />
            <Tooltip content={<CustomTooltip />} />
            {showLegend && (
              <Legend 
                wrapperStyle={{ 
                  paddingTop: '20px',
                  fontSize: '14px',
                  color: '#374151'
                }}
              />
            )}
            <Scatter
              dataKey={yKey}
              name="Performance Points"
              fill={color}
              stroke={color}
              strokeWidth={1}
              onClick={(data) => onPointClick && onPointClick(data)}
            />
          </ScatterChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

// Distribution Pie Chart Component
export const DistributionPieChart = ({
  data,
  title = "Grade Distribution Analysis",
  subtitle = "Distribution of students across different grade levels",
  dataKey = "value",
  nameKey = "name",
  colors = [
    "#7C3AED",
    "#06B6D4",
    "#10B981",
    "#F59E0B",
    "#EF4444",
    "#6366F1",
    "#22C55E",
    "#A78BFA",
    "#F472B6",
    "#60A5FA",
  ],
  height = 450,
  showPercentage = true,
  onSliceClick,
  showLegend = true,
}) => {
  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0];
      const total = data.payload.total || data.payload.value;
      const percentage = ((data.value / total) * 100).toFixed(1);
      return (
        <div className="bg-white p-4 border border-gray-200 rounded-lg shadow-xl backdrop-blur-sm">
          <p className="font-semibold text-gray-900 text-sm mb-2">{data.name}</p>
          <p className="text-blue-600 font-medium">
            Students: {data.value}
          </p>
          <p className="text-green-600 font-medium">
            Percentage: {percentage}%
          </p>
          {data.payload.total && (
            <p className="text-purple-600 font-medium">
              Total: {data.payload.total}
            </p>
          )}
        </div>
      );
    }
    return null;
  };

  const CustomLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent, index }) => {
    if (!showPercentage || percent < 0.05) return null;
    
    const RADIAN = Math.PI / 180;
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    return (
      <text
        x={x}
        y={y}
        fill="white"
        textAnchor={x > cx ? "start" : "end"}
        dominantBaseline="central"
        fontSize={12}
        fontWeight="600"
      >
        {`${(percent * 100).toFixed(0)}%`}
      </text>
    );
  };

  return (
    <div className="bg-white p-4 rounded-xl shadow-lg border border-gray-100">
      <div className="mb-4">
        <h3 className="text-xl font-semibold text-gray-900 mb-1">{title}</h3>
        <p className="text-sm text-gray-600">{subtitle}</p>
      </div>
      <div className="bg-gradient-to-br from-gray-50 to-gray-100 p-4 rounded-xl border border-gray-200">
        <ResponsiveContainer width="100%" height={height}>
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={<CustomLabel />}
              outerRadius={height / 3}
              fill="#8884d8"
              dataKey={dataKey}
              nameKey={nameKey}
              onClick={(data) => onSliceClick && onSliceClick(data)}
            >
              {data.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={colors[index % colors.length]}
                  stroke="#ffffff"
                  strokeWidth={2}
                />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
            {showLegend && (
              <Legend 
                wrapperStyle={{ 
                  paddingTop: '20px',
                  fontSize: '14px',
                  color: '#374151'
                }}
              />
            )}
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

// Performance Radar Chart Component
export const PerformanceRadarChart = ({
  data,
  title = "Multi-dimensional Performance Analysis",
  subtitle = "Performance comparison across different subjects and metrics",
  dataKey = "value",
  nameKey = "subject",
  color = "#7C3AED",
  height = 450,
  showTarget = false,
  targetData = null,
  showLegend = true,
}) => {
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-4 border border-gray-200 rounded-lg shadow-xl backdrop-blur-sm">
          <p className="font-semibold text-gray-900 text-sm mb-2">{label}</p>
          <p className="text-blue-600 font-medium">
            Performance: {payload[0].value.toFixed(1)}%
          </p>
          {data.target && (
            <p className="text-green-600 font-medium">
              Target: {data.target}%
            </p>
          )}
          {data.difference && (
            <p className={`font-medium ${data.difference >= 0 ? 'text-green-600' : 'text-red-600'}`}>
              Difference: {data.difference >= 0 ? '+' : ''}{data.difference.toFixed(1)}%
            </p>
          )}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-white p-4 rounded-xl shadow-lg border border-gray-100">
      <div className="mb-4">
        <h3 className="text-xl font-semibold text-gray-900 mb-1">{title}</h3>
        <p className="text-sm text-gray-600">{subtitle}</p>
      </div>
      <div className="bg-gradient-to-br from-gray-50 to-gray-100 p-4 rounded-xl border border-gray-200">
        <ResponsiveContainer width="100%" height={height}>
          <RadarChart data={data}>
            <PolarGrid stroke="#E5E7EB" strokeWidth={1} />
            <PolarAngleAxis
              dataKey={nameKey}
              tick={{ fill: "#374151", fontSize: 12, fontWeight: "500" }}
            />
            <PolarRadiusAxis
              angle={90}
              domain={[0, 100]}
              tick={{ fill: "#374151", fontSize: 12 }}
              label={{ 
                value: "Performance Score (%)", 
                position: "insideTop",
                offset: 10,
                style: { textAnchor: "middle", fontSize: 14, fontWeight: "600", fill: "#374151" }
              }}
            />
            <Tooltip content={<CustomTooltip />} />
            {showLegend && (
              <Legend 
                wrapperStyle={{ 
                  paddingTop: '20px',
                  fontSize: '14px',
                  color: '#374151'
                }}
              />
            )}
            <Radar
              name="Current Performance"
              dataKey={dataKey}
              stroke={color}
              fill={color}
              fillOpacity={0.3}
              strokeWidth={3}
            />
            {showTarget && targetData && (
              <Radar
                name="Target Performance"
                dataKey="target"
                stroke="#EF4444"
                fill="#EF4444"
                fillOpacity={0.1}
                strokeWidth={2}
                strokeDasharray="5 5"
              />
            )}
          </RadarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

// Performance Composed Chart Component
export const PerformanceComposedChart = ({
  data,
  title = "Comprehensive Performance Analysis",
  subtitle = "Multi-metric performance comparison with trends and areas",
  height = 500,
  showBars = true,
  showLines = true,
  showAreas = false,
  onChartClick,
  showGrid = true,
  showLegend = true,
  barColor = "#7C3AED",
  lineColor = "#06B6D4",
  areaColor = "#A78BFA",
}) => {
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-4 border border-gray-200 rounded-lg shadow-xl backdrop-blur-sm">
          <p className="font-semibold text-gray-900 text-sm mb-2">{label}</p>
          {payload.map((entry, index) => (
            <p
              key={index}
              className="font-medium text-sm"
              style={{ color: entry.color }}
            >
              {entry.name}: {entry.value.toFixed(1)}%
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-white p-4 rounded-xl shadow-lg border border-gray-100">
      <div className="mb-4">
        <h3 className="text-xl font-semibold text-gray-900 mb-1">{title}</h3>
        <p className="text-sm text-gray-600">{subtitle}</p>
      </div>
      <div className="bg-gradient-to-br from-gray-50 to-gray-100 p-4 rounded-xl border border-gray-200">
        <ResponsiveContainer width="100%" height={height}>
          <ComposedChart
            data={data}
            margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
            onClick={(data) => onChartClick && onChartClick(data)}
            style={chartStyle}
          >
            {showGrid && (
              <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" strokeWidth={1} />
            )}
            <XAxis
              dataKey="name"
              style={axisStyle}
              tick={{ fill: "#374151", fontSize: 12, fontWeight: "500" }}
              axisLine={{ stroke: "#D1D5DB" }}
              tickLine={{ stroke: "#D1D5DB" }}
              angle={-45}
              textAnchor="end"
              height={60}
              interval={0}
              label={{ 
                value: "Subjects", 
                position: "bottom", 
                offset: 50,
                style: { textAnchor: "middle", fontSize: 14, fontWeight: "600", fill: "#374151" }
              }}
            />
            <YAxis
              style={axisStyle}
              tick={{ fill: "#374151", fontSize: 12 }}
              domain={[0, 100]}
              axisLine={{ stroke: "#D1D5DB" }}
              tickLine={{ stroke: "#D1D5DB" }}
              label={{ 
                value: "Performance Score (%)", 
                angle: -90, 
                position: "insideLeft",
                style: { textAnchor: "middle", fontSize: 14, fontWeight: "600", fill: "#374151" }
              }}
            />
            <Tooltip content={<CustomTooltip />} />
            {showLegend && (
              <Legend 
                wrapperStyle={{ 
                  paddingTop: '20px',
                  fontSize: '14px',
                  color: '#374151'
                }}
              />
            )}
            {showBars && (
              <Bar
                dataKey="performance"
                name="Current Performance"
                fill={barColor}
                radius={[6, 6, 0, 0]}
                stroke={barColor}
                strokeWidth={1}
              />
            )}
            {showLines && (
              <Line
                type="monotone"
                dataKey="trend"
                name="Performance Trend"
                stroke={lineColor}
                strokeWidth={4}
                dot={{ fill: lineColor, strokeWidth: 2, r: 6 }}
                activeDot={{ r: 8, stroke: lineColor, strokeWidth: 3 }}
              />
            )}
            {showAreas && (
              <Area
                type="monotone"
                dataKey="area"
                name="Performance Range"
                fill={areaColor}
                fillOpacity={0.3}
                stroke={areaColor}
                strokeWidth={2}
              />
            )}
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

// Chart Configuration Component
export const ChartConfig = ({ config, onConfigChange }) => {
  const [showSaved, setShowSaved] = useState(false);

  const handleChange = (next) => {
    onConfigChange(next);
    setShowSaved(true);
    window.clearTimeout(window.__chartCfgToastTimer);
    window.__chartCfgToastTimer = window.setTimeout(() => setShowSaved(false), 1200);
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200">
      <div className="px-5 pt-5">
        <h3 className="text-lg font-semibold text-gray-900">Chart Settings</h3>
        {showSaved && (
          <div className="mt-2 inline-flex items-center gap-2 text-sm text-green-700 bg-green-50 border border-green-200 px-3 py-1 rounded-md">
            <span>✅ Settings auto-saved</span>
          </div>
        )}
      </div>

      <div className="mt-4 px-5 pb-5">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {/* Theme */}
          <div className="flex flex-col gap-2">
            <label className="text-sm font-medium text-gray-700">Theme</label>
            <select
              value={config.theme}
              onChange={(e) => handleChange({ ...config, theme: e.target.value })}
              className="w-full px-3 py-2 bg-white text-gray-900 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="light">Light</option>
              <option value="dark">Dark</option>
            </select>
          </div>

          {/* Animation */}
          <div className="flex flex-col gap-2">
            <label className="text-sm font-medium text-gray-700">Animation</label>
            <select
              value={config.animation}
              onChange={(e) => handleChange({ ...config, animation: e.target.value })}
              className="w-full px-3 py-2 bg-white text-gray-900 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="smooth">Smooth</option>
              <option value="none">None</option>
            </select>
          </div>

          {/* Show Grid */}
          <div className="flex items-center justify-between sm:justify-start sm:gap-3 py-1">
            <label htmlFor="showGrid" className="text-sm font-medium text-gray-700">Show Grid</label>
            <input
              type="checkbox"
              id="showGrid"
              checked={config.showGrid}
              onChange={(e) => handleChange({ ...config, showGrid: e.target.checked })}
              className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
          </div>

          {/* Show Legend */}
          <div className="flex items-center justify-between sm:justify-start sm:gap-3 py-1">
            <label htmlFor="showLegend" className="text-sm font-medium text-gray-700">Show Legend</label>
            <input
              type="checkbox"
              id="showLegend"
              checked={config.showLegend}
              onChange={(e) => handleChange({ ...config, showLegend: e.target.checked })}
              className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
          </div>
        </div>
      </div>

      {/* Divider to separate from insights */}
      <div className="border-t border-gray-200 mx-5" />
      <div className="h-5" />
    </div>
  );
}; 