import { useState, useEffect } from 'react';
import { getAuthStatus, createPost, listPosts, deletePost } from '../lib/api';
import { Button, Card, CardContent, CardHeader, CardTitle } from '../components/ui';
import { Toast } from '../components/ui/Toast';
import { Send, Loader2, RefreshCw, Trash2, AlertCircle } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Compose() {
    const [text, setText] = useState('');
    const [loading, setLoading] = useState(false);
    const [isConnected, setIsConnected] = useState(null); // null = checking
    const [posts, setPosts] = useState([]);
    const [toast, setToast] = useState(null); // { message, type, details }

    const MAX_CHARS = 500;

    // 1. Check Connection Status
    useEffect(() => {
        checkConnection();
        fetchPosts();
    }, []);

    const checkConnection = async () => {
        try {
            const status = await getAuthStatus();
            setIsConnected(status.connected);
        } catch (error) {
            console.error("Failed to check status", error);
            setIsConnected(false);
        }
    };

    const fetchPosts = async () => {
        try {
            const data = await listPosts();
            if (Array.isArray(data)) {
                setPosts(data);
            } else {
                console.error("Unexpected posts data format:", data);
                setPosts([]);
            }
        } catch (error) {
            console.error("Failed to fetch posts", error);
        }
    };

    const handlePost = async () => {
        if (!text.trim()) return;
        setLoading(true);
        try {
            await createPost(text);
            setToast({ message: "Post published successfully!", type: "success" });
            setText('');
            fetchPosts(); // Refresh list
        } catch (error) {
            console.error(error);
            const msg = error.response?.data?.detail || "Failed to publish post.";
            setToast({ message: "Failed to publish post.", type: "error", details: msg });
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (mediaId) => {
        if (!confirm("Are you sure you want to delete this post?")) return;
        try {
            await deletePost(mediaId);
            setToast({ message: "Post deleted.", type: "success" });
            fetchPosts();
        } catch (error) {
            setToast({ message: "Failed to delete post.", type: "error" });
        }
    }

    if (isConnected === null) {
        return <div className="flex justify-center p-12"><Loader2 className="animate-spin text-gray-400" /></div>;
    }

    if (isConnected === false) {
        return (
            <div className="max-w-md mx-auto mt-12 text-center space-y-4">
                <div className="bg-yellow-50 p-6 rounded-lg border border-yellow-200">
                    <AlertCircle className="w-12 h-12 text-yellow-500 mx-auto mb-2" />
                    <h2 className="text-xl font-semibold text-yellow-800">Connection Required</h2>
                    <p className="text-yellow-700 mt-2">You must connect your Threads account to compose posts.</p>
                    <Link to="/connect" className="inline-block mt-4">
                        <Button>Connect Threads</Button>
                    </Link>
                </div>
            </div>
        );
    }

    return (
        <div className="max-w-2xl mx-auto space-y-6">
            {toast && <Toast {...toast} onClose={() => setToast(null)} />}

            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Send className="w-5 h-5" />
                        New Thread
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="relative">
                        <textarea
                            className="w-full min-h-[150px] p-4 rounded-md border text-sm focus:outline-none focus:ring-2 focus:ring-ring resize-none"
                            placeholder="What's new?"
                            value={text}
                            onChange={(e) => {
                                if (e.target.value.length <= MAX_CHARS) setText(e.target.value);
                            }}
                        />
                        <div className="absolute bottom-3 right-3 text-xs text-muted-foreground bg-white/80 px-2 py-1 rounded">
                            <span className={text.length > 450 ? "text-orange-500 font-bold" : ""}>
                                {text.length}
                            </span>
                            / {MAX_CHARS}
                        </div>
                    </div>

                    <div className="mt-4 flex justify-end">
                        <Button onClick={handlePost} disabled={loading || !text.trim()}>
                            {loading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Send className="mr-2 h-4 w-4" />}
                            Post to Threads
                        </Button>
                    </div>
                </CardContent>
            </Card>

            <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold text-gray-700">Recent Posts</h3>
                <Button variant="ghost" size="sm" onClick={fetchPosts}>
                    <RefreshCw className="w-4 h-4 mr-1" /> Refresh
                </Button>
            </div>

            <div className="space-y-4">
                {posts.map((post) => (
                    <Card key={post.id} className="overflow-hidden">
                        <CardContent className="p-4">
                            <div className="flex justify-between items-start gap-4">
                                <p className="text-sm whitespace-pre-wrap flex-1">{post.text}</p>
                                <div className="flex flex-col items-end gap-2">
                                    <span className={`text-[10px] uppercase font-bold px-2 py-1 rounded-full ${post.status === 'PUBLISHED' ? 'bg-green-100 text-green-700' :
                                        post.status === 'FAILED' ? 'bg-red-100 text-red-700' :
                                            'bg-gray-100 text-gray-700'
                                        }`}>
                                        {post.status}
                                    </span>
                                    <span className="text-xs text-gray-400">
                                        {new Date(post.created_at).toLocaleDateString()}
                                    </span>
                                </div>
                            </div>
                            {post.error_message && (
                                <div className="mt-2 text-xs bg-red-50 text-red-600 p-2 rounded">
                                    Error: {post.error_message}
                                </div>
                            )}
                            <div className="mt-3 flex justify-end border-t pt-2">
                                {(post.status === 'PUBLISHED' || post.status === 'FAILED') && (
                                    <button
                                        onClick={() => handleDelete(post.threads_media_id || "local-" + post.id)}
                                        className="text-gray-400 hover:text-red-500 transition-colors"
                                        title="Delete"
                                    >
                                        <Trash2 className="w-4 h-4" />
                                    </button>
                                )}
                            </div>
                        </CardContent>
                    </Card>
                ))}
                {posts.length === 0 && (
                    <div className="text-center py-8 text-gray-500 bg-gray-50 rounded-lg border border-dashed">
                        No recent posts found.
                    </div>
                )}
            </div>
        </div>
    );
}
