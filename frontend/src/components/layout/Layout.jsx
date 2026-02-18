import { Navbar } from './Navbar';

export function Layout({ children }) {
    return (
        <div className="flex min-h-screen flex-col bg-background">
            <Navbar />
            <main className="flex-1 container py-6">
                {children}
            </main>
        </div>
    );
}
