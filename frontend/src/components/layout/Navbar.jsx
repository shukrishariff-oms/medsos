import { Link, useLocation } from 'react-router-dom';
import { PenSquare, Inbox, BarChart2, Radio, Link as LinkIcon } from 'lucide-react';
import { cn } from '../ui';

export function Navbar() {
    const location = useLocation();

    const navItems = [
        { path: '/compose', label: 'Compose', icon: PenSquare },
        { path: '/inbox', label: 'Inbox', icon: Inbox },
        { path: '/analytics', label: 'Analytics', icon: BarChart2 },
        { path: '/connect', label: 'Connect', icon: LinkIcon },
    ];

    return (
        <nav className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
            <div className="container flex h-14 items-center">
                <div className="mr-4 hidden md:flex">
                    <Link to="/" className="mr-6 flex items-center space-x-2">
                        <Radio className="h-6 w-6" />
                        <span className="hidden font-bold sm:inline-block">ThreadOS</span>
                    </Link>
                    <nav className="flex items-center space-x-6 text-sm font-medium">
                        {navItems.map((item) => (
                            <Link
                                key={item.path}
                                to={item.path}
                                className={cn(
                                    "transition-colors hover:text-foreground/80",
                                    location.pathname === item.path ? "text-foreground" : "text-foreground/60"
                                )}
                            >
                                <div className="flex items-center gap-2">
                                    <item.icon className="h-4 w-4" />
                                    <span>{item.label}</span>
                                </div>
                            </Link>
                        ))}
                    </nav>
                </div>
            </div>
        </nav>
    );
}
