import { useState, useEffect } from 'react';
import api from '../api/client';
import { Card, CardContent, CardHeader, CardTitle, Button } from '../components/ui';
import { MessageSquare, RefreshCw, Loader2 } from 'lucide-react';

export default function Inbox() {
    const [posts, setPosts] = useState([]);
    const [selectedPostId, setSelectedPostId] = useState(null);
    const [replies, setReplies] = useState([]);
    const [replyText, setReplyText] = useState('');
    const [loading, setLoading] = useState(false);
    const [repliesLoading, setRepliesLoading] = useState(false);

    useEffect(() => {
        fetchPosts();
    }, []);

    const fetchPosts = async () => {
        setLoading(true);
        try {
            const res = await api.get('/threads/my-posts');
            setPosts(res.data);
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    const handlePostClick = async (postId) => {
        setSelectedPostId(postId);
        setRepliesLoading(true);
        setReplies([]);
        try {
            const res = await api.get(`/threads/post/${postId}/replies`);
            setReplies(res.data);
        } catch (error) {
            console.error(error);
        } finally {
            setRepliesLoading(false);
        }
    };

    const handleReply = async () => {
        if (!replyText.trim() || !selectedPostId) return;

        try {
            // This assumes we are replying to the main post for now, 
            // but robust inbox allows replying to specific comments.
            // The UI here is simplified: Reply to the Thread (Post).
            await api.post('/threads/reply', {
                text: replyText,
                parent_media_id: selectedPostId
            });
            setReplyText('');
            // Refresh replies
            handlePostClick(selectedPostId);
        } catch (error) {
            console.error("Failed to reply", error);
        }
    }

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 h-[80vh]">
            {/* Posts List */}
            <Card className="flex flex-col h-full"> // Updated: h-full
                <CardHeader className="flex flex-row items-center justify-between">
                    <CardTitle>My Threads</CardTitle>
                    <Button variant="ghost" size="icon" onClick={fetchPosts}>
                        <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
                    </Button>
                </CardHeader>
                <CardContent className="flex-1 overflow-auto">
                    <div className="space-y-2">
                        {posts.map((post) => (
                            <div
                                key={post.id}
                                onClick={() => handlePostClick(post.id)}
                                className={`p-3 rounded-lg border cursor-pointer transition-colors hover:bg-accent ${selectedPostId === post.id ? 'bg-accent' : ''
                                    }`}
                            >
                                <p className="text-sm line-clamp-2">{post.text || '(Media Post)'}</p>
                                <span className="text-xs text-muted-foreground">
                                    {new Date(post.timestamp).toLocaleDateString()}
                                </span>
                            </div>
                        ))}
                    </div>
                </CardContent>
            </Card>

            {/* Replies View */}
            <Card className="flex flex-col h-full">
                <CardHeader>
                    <CardTitle>
                        {selectedPostId ? 'Replies' : 'Select a post'}
                    </CardTitle>
                </CardHeader>
                <CardContent className="flex-1 flex flex-col">
                    {selectedPostId ? (
                        <>
                            <div className="flex-1 overflow-auto space-y-4 mb-4">
                                {repliesLoading ? (
                                    <div className="flex justify-center p-4">
                                        <Loader2 className="w-6 h-6 animate-spin" />
                                    </div>
                                ) : replies.length === 0 ? (
                                    <p className="text-sm text-muted-foreground text-center p-4">
                                        No replies yet.
                                    </p>
                                ) : (
                                    replies.map((reply) => (
                                        <div key={reply.id} className="bg-muted/50 p-3 rounded-md">
                                            <div className="flex justify-between items-start mb-1">
                                                <span className="font-semibold text-xs">@{reply.username}</span>
                                                <span className="text-xs text-muted-foreground">
                                                    {new Date(reply.timestamp).toLocaleDateString()}
                                                </span>
                                            </div>
                                            <p className="text-sm">{reply.text}</p>
                                        </div>
                                    ))
                                )}
                            </div>

                            <div className="mt-auto pt-2 border-t">
                                <textarea
                                    className="w-full p-2 text-sm border rounded-md min-h-[80px]"
                                    placeholder="Write a reply..."
                                    value={replyText}
                                    onChange={e => setReplyText(e.target.value)}
                                />
                                <div className="flex justify-end mt-2">
                                    <Button size="sm" onClick={handleReply} disabled={!replyText.trim()}>Reply</Button>
                                </div>
                            </div>
                        </>
                    ) : (
                        <div className="h-full flex flex-col items-center justify-center text-muted-foreground">
                            <MessageSquare className="w-12 h-12 mb-2 opacity-20" />
                            <p>Select a thread to view and reply to comments</p>
                        </div>
                    )}
                </CardContent>
            </Card>
        </div>
    );
}
