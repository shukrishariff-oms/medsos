import React, { useEffect } from 'react';
import { cn } from '../ui';
import { X } from 'lucide-react';

export function Toast({ message, type = 'success', onClose, duration = 3000, details }) {
    useEffect(() => {
        if (duration) {
            const timer = setTimeout(() => {
                onClose();
            }, duration);
            return () => clearTimeout(timer);
        }
    }, [duration, onClose]);

    return (
        <div className={cn(
            "fixed bottom-4 right-4 p-4 rounded-md shadow-lg border flex items-start gap-3 z-50 animate-in slide-in-from-bottom-5 fade-in duration-300",
            type === 'success' ? "bg-white border-green-200 text-green-800" : "bg-white border-red-200 text-red-800"
        )}>
            <div className="flex-1">
                <p className="font-medium text-sm">{message}</p>

                {details && (
                    <div className="mt-2 text-xs bg-gray-50 p-2 rounded border border-gray-100 font-mono text-gray-600 overflow-x-auto max-w-[280px]">
                        {details}
                    </div>
                )}
            </div>
            <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
                <X size={16} />
            </button>
        </div>
    );
}
