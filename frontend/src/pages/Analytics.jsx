import { useState, useEffect } from 'react';
import api from '../lib/api';
import { Card, CardContent, CardHeader, CardTitle, Button } from '../components/ui';
import { BarChart, RefreshCw, Eye, Heart, MessageCircle, Repeat, Quote } from 'lucide-react';

export default function Analytics() {
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(false);
    const [insightsMap, setInsightsMap] = useState({}); // postId -> insights object

    useEffect(() => {
        fetchPosts();
    }, []);

    const fetchPosts = async () => {
        setLoading(true);
        try {
            const res = await api.get('/threads/my-posts');
            setPosts(res.data);
            // Fetch insights for each post (could be optimized to batch or on demand)
            res.data.forEach(post => fetchInsights(post.id));
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    const fetchInsights = async (mediaId) => {
        try {
            const res = await api.get(`/threads/insights/${mediaId}`);
            setInsightsMap(prev => ({ ...prev, [mediaId]: res.data }));
        } catch (error) {
            console.error(`Failed insights for ${mediaId}`, error);
        }
    };

    const Metric = ({ icon: Icon, value, label, color }) => (
        <div className="flex flex-col items-center p-2 bg-muted/30 rounded-lg">
            <Icon className={`w-4 h-4 mb-1 ${color}`} />
            <span className="font-bold text-lg">{value || 0}</span>
            <span className="text-[10px] uppercase tracking-wider text-muted-foreground">{label}</span>
        </div>
    );

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold tracking-tight">Analytics</h2>
                <Button onClick={fetchPosts} disabled={loading} size="sm">
                    <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
                    Refresh Data
                </Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {posts.map(post => {
                    const insights = insightsMap[post.id] || {};
                    return (
                        <Card key={post.id} className="overflow-hidden">
                            <CardHeader className="p-4 pb-2">
                                <div className="text-xs text-muted-foreground mb-1">
                                    {new Date(post.timestamp).toLocaleDateString()}
                                </div>
                                <div className="text-sm line-clamp-2 min-h-[2.5em]">
                                    {post.text || "(Media Post)"}
                                </div>
                            </CardHeader>
                            <CardContent className="p-4 pt-2">
                                <div className="grid grid-cols-5 gap-2">
                                    <Metric icon={Eye} value={insights.views} label="Views" color="text-blue-500" />
                                    <Metric icon={Heart} value={insights.likes} label="Likes" color="text-red-500" />
                                    <Metric icon={MessageCircle} value={insights.replies} label="Replies" color="text-green-500" />
                                    <Metric icon={Repeat} value={insights.reposts} label="Repost" color="text-purple-500" />
                                    <Metric icon={Quote} value={insights.quotes} label="Quotes" color="text-orange-500" />
                                </div>
                            </CardContent>
                        </Card>
                    );
                })}

                {posts.length === 0 && !loading && (
                    <div className="col-span-full text-center py-10 text-muted-foreground">
                        No posts found to analyze.
                    </div>
                )}
            </div>
        </div>
    );
}
