import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const QueryAnalytics = ({ data }: { data: any }) => {
    if (!data || !data.historical_queries) return null;

    return (
        <div className="flex flex-col h-full">
            <div className="flex justify-between items-start mb-8">
                <div>
                    <p className="text-slate-400 text-[10px] font-mono tracking-wider mb-2 uppercase">QUERY INTELLIGENCE ROUTING</p>
                    <h2 className="text-white text-2xl font-bold tracking-tight">Optimization Active</h2>
                </div>
                <div className="flex items-center gap-2 border border-[#2A2A2A] rounded-md px-3 py-1 bg-[#1A1A1A]/50">
                    <span className="w-2 h-2 rounded-full bg-[#ff382e]"></span>
                    <span className="text-[10px] font-mono text-slate-300">RL Pathing</span>
                </div>
            </div>

            <div className="flex-1 min-h-[250px] w-full mt-4">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={data.historical_queries} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                        <XAxis
                            dataKey="time"
                            stroke="#222"
                            fontSize={10}
                            tickLine={false}
                            axisLine={false}
                            dy={10}
                            fontFamily="JetBrains Mono"
                        />
                        <YAxis
                            stroke="#222"
                            fontSize={10}
                            tickLine={false}
                            axisLine={false}
                            fontFamily="JetBrains Mono"
                        />
                        <CartesianGrid strokeDasharray="3 3" stroke="#222" vertical={true} horizontal={true} />
                        <Tooltip
                            contentStyle={{
                                backgroundColor: '#000',
                                border: '1px solid #2A2A2A',
                                borderRadius: '4px',
                                fontSize: '10px',
                                textTransform: 'uppercase',
                                fontFamily: 'JetBrains Mono',
                                color: '#fff'
                            }}
                            itemStyle={{ color: '#fff', padding: 0 }}
                            cursor={{ stroke: '#FFFFFF', strokeWidth: 0.5, strokeDasharray: '4 4' }}
                        />
                        {/* Alternative Path (Gray Solid) */}
                        <Line
                            type="linear"
                            dataKey="sonnet"
                            stroke="#555555"
                            strokeWidth={2}
                            dot={false}
                            activeDot={{ r: 4, fill: '#555555', strokeWidth: 0 }}
                            name="BALANCED"
                        />
                        {/* Premium Path (White Dashed) over Gray */}
                        <Line
                            type="linear"
                            dataKey="gpt4"
                            stroke="#FFFFFF"
                            strokeWidth={2}
                            strokeDasharray="6 6"
                            dot={{ fill: '#FFFFFF', r: 5, strokeWidth: 0 }}
                            activeDot={{ r: 7, strokeWidth: 0, fill: '#FFFFFF' }}
                            name="PREMIUM"
                        />
                    </LineChart>
                </ResponsiveContainer>
            </div>

            {/* X Axis Range Labels are already drawn by XAxis, so keeping it clean */}
            <div className="flex justify-between px-2 mt-4 text-[10px] font-mono text-slate-500">
                <span>0s</span>
                <span>1s</span>
                <span>2s</span>
                <span>3s</span>
                <span>4s</span>
                <span>5s</span>
            </div>
        </div>
    );
};

export default QueryAnalytics;
