import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import api from '../lib/api';
import { Button, Card, CardContent, CardHeader, CardTitle } from '../components/ui';
import { Link as LinkIcon, CheckCircle, Loader2 } from 'lucide-react';

export default function Connect() {
    const [searchParams] = useSearchParams();
    const [loading, setLoading] = useState(false);
    const [connected, setConnected] = useState(false);
    const [username, setUsername] = useState('');

    useEffect(() => {
        if (searchParams.get('connected') === 'true') {
            setConnected(true);
            setUsername(searchParams.get('username') || '');
        }
        checkConnection();
    }, [searchParams]);

    const checkConnection = async () => {
        try {
            // Updated endpoint to match new router mounting
            const res = await api.get('/threads/me');
            setConnected(true);
            setUsername(res.data.username || 'User');
        } catch (error) {
            // Not connected
            setConnected(false);
        }
    };

    const handleConnect = async () => {
        setLoading(true);
        try {
            const res = await api.post('/auth/threads/start');
            window.location.href = res.data.url;
        } catch (error) {
            console.error("Failed to start auth", error);
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-[60vh]">
            <Card className="w-[350px]">
                <CardHeader>
                    <CardTitle className="text-center flex items-center justify-center gap-2">
                        <LinkIcon className="w-6 h-6" />
                        Connect Threads
                    </CardTitle>
                </CardHeader>
                <CardContent className="flex flex-col items-center gap-4">
                    {connected ? (
                        <>
                            <div className="text-green-500 flex flex-col items-center gap-2">
                                <CheckCircle className="w-12 h-12" />
                                <span className="font-medium">Connected as @{username}</span>
                            </div>
                            <p className="text-sm text-muted-foreground text-center">
                                You're ready to use ThreadOS.
                            </p>
                        </>
                    ) : (
                        <>
                            <p className="text-sm text-muted-foreground text-center">
                                Sign in with your Threads account to start managing your posts.
                            </p>
                            <Button onClick={handleConnect} disabled={loading} className="w-full">
                                {loading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : null}
                                Connect with Threads
                            </Button>
                        </>
                    )}
                </CardContent>
            </Card>
        </div>
    );
}
