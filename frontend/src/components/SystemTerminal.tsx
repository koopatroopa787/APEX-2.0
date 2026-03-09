import React from 'react';

interface Log {
    id: string;
    msg: string;
    timestamp: string;
}

export const SystemTerminal: React.FC<{ logs?: Log[] }> = ({ logs = [] }) => {
    return (
        <footer className="border-t border-[#2A2A2A] bg-black py-2 px-4 overflow-hidden mt-auto">
            <div className="flex whitespace-nowrap text-[10px] font-mono text-slate-400 gap-8 animate-marquee">
                <span className="font-bold tracking-[0.2em] text-white/40 uppercase">SYSTEM_LOGS:</span>

                {logs.length > 0 ? logs.map((log: any, i: number) => (
                    <span key={log.id || i} className={`uppercase font-mono ${log.type === 'error' ? 'text-[#FF3B30] font-bold' :
                            log.type === 'warning' ? 'text-yellow-500 font-bold' :
                                'text-white'
                        }`}>
                        &gt;&gt; {log.msg}
                    </span>
                )) : (
                    <span className="text-white uppercase">&gt;&gt; SYSTEM_READY [STABLE]</span>
                )}

                {/* Repeat for seamless loop effect */}
                {logs.length > 0 && logs.map((log: any, i: number) => (
                    <span key={`repeat-${log.id || i}`} className={`uppercase font-mono ${log.type === 'error' ? 'text-[#FF3B30] font-bold' :
                            log.type === 'warning' ? 'text-yellow-500 font-bold' :
                                'text-white'
                        }`}>
                        &gt;&gt; {log.msg}
                    </span>
                ))}
            </div>
        </footer>
    );
};
