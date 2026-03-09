import React, { useState, useEffect } from 'react';
import { useWebSocket } from './hooks/useWebSocket';
import DashboardOverview from './components/DashboardOverview';
import QueryAnalytics from './components/QueryAnalytics';
import ProductionScore from './components/ProductionScore';
import { AgentRegistry } from './components/AgentRegistry';
import { SystemTerminal } from './components/SystemTerminal';
import { AgentDetailModal } from './components/AgentDetailModal';

const SystemClock = () => {
    const [time, setTime] = useState(new Date().toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit', second: '2-digit' }));

    useEffect(() => {
        const timer = setInterval(() => {
            setTime(new Date().toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit', second: '2-digit' }));
        }, 1000);
        return () => clearInterval(timer);
    }, []);

    return <span className="text-white text-[11px] font-bold">{time}</span>;
};

function App() {
    const { data, isConnected } = useWebSocket('ws://localhost:8000/ws');
    const [selectedAgentId, setSelectedAgentId] = useState<string | null>(null);

    // Get the live agent object so the modal updates in real-time
    const selectedAgent = data?.agents?.find((a: any) => a.id === selectedAgentId) || null;

    return (
        <div className="bg-black text-slate-100 font-display min-h-screen flex flex-col overflow-x-hidden selection:bg-[#ff382e] selection:text-white">
            {/* Header */}
            <header className="flex items-center justify-between whitespace-nowrap border-b border-[#2A2A2A] px-10 py-5 bg-black sticky top-0 z-50">
                <div className="flex items-center gap-3">
                    <div className="size-6 text-white flex items-center justify-center border border-white rounded-sm">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M12 2L2 22H22L12 2Z" stroke="white" strokeWidth="2" strokeLinejoin="round" />
                        </svg>
                    </div>
                    <h1 className="text-white text-[16px] font-bold tracking-[0.2em] font-mono uppercase mt-0.5">APEX.NEXUS</h1>
                </div>
                <div className="flex gap-4 font-mono">
                    <div className="flex items-center gap-2 px-4 py-1.5 rounded-full border border-[#2A2A2A] bg-[#111]">
                        <span className="text-slate-500 text-[10px]">SYSTEM_TIME:</span>
                        <SystemClock />
                    </div>
                    <div className="flex items-center gap-2 px-4 py-1.5 rounded-full border border-[#2A2A2A] bg-[#111]">
                        <span className="text-slate-500 text-[10px]">TELEMETRY:</span>
                        <span className="text-white text-[11px] font-bold uppercase">{isConnected ? 'ONLINE' : 'OFFLINE'}</span>
                        <span className="relative flex h-2 w-2 ml-1">
                            <span className={`absolute inline-flex h-full w-full rounded-full ${isConnected ? 'bg-white' : 'bg-[#FF3B30]'} opacity-40`}></span>
                            <span className={`relative inline-flex rounded-full h-2 w-2 ${isConnected ? 'bg-white' : 'bg-[#FF3B30]'}`}></span>
                        </span>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="flex-1 p-6 md:p-10 grid grid-cols-1 lg:grid-cols-4 gap-6">
                {/* Left Column: KPIs & Analytics (3/4th width) */}
                <div className="lg:col-span-3 flex flex-col gap-6">
                    <DashboardOverview />
                    <div className="glass-panel rounded-xl p-6 flex-1 flex flex-col min-h-[400px]">
                        <QueryAnalytics data={data} />
                    </div>
                </div>

                {/* Right Column: Agent Registry */}
                <div className="flex flex-col gap-6">
                    <div className="glass-panel rounded-xl flex flex-col h-full min-h-[500px]">
                        <div className="p-4 border-b border-[#2A2A2A] flex justify-between items-center bg-[#0a0a0a] rounded-t-xl">
                            <h3 className="text-slate-300 text-xs font-mono tracking-wider uppercase">AGENT_REGISTRY</h3>
                            <span className="text-xs font-mono text-slate-500 uppercase">TOTAL: {data?.agents?.length || 0}</span>
                        </div>
                        <div className="flex-1 overflow-y-auto p-2">
                            <AgentRegistry agents={data?.agents} onSelect={(agent) => setSelectedAgentId(agent.id)} />
                        </div>
                    </div>
                </div>
            </main>

            {/* Footer Ticker */}
            <SystemTerminal logs={data?.alerts} />

            {/* Agent Detail Overlay */}
            <AgentDetailModal
                agent={selectedAgent}
                onClose={() => setSelectedAgentId(null)}
            />
        </div>
    );
}

export default App;
