import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, Legend } from 'recharts';
import { Activity } from 'lucide-react';
import { API_BASE_URL } from '../../config';

interface StudentAnalyticsViewProps {
    rollNumber: string;
}

export const StudentAnalyticsView = ({ rollNumber }: StudentAnalyticsViewProps) => {
    const [analyticsData, setAnalyticsData] = useState<any[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        if (!rollNumber || rollNumber === 'unknown_roll') return;

        const fetchAnalytics = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/api/students/${rollNumber}/analytics`);
                if (response.ok) {
                    const data = await response.json();

                    // Transform data slightly to make it easier for recharts, grouping by subject/date if we wanted,
                    // but since sources might differ, we can just plot them as individual events
                    setAnalyticsData(data.map((item: any) => ({
                        name: `${item.subject} (${item.date})`,
                        score: item.score,
                        max_score: item.max_score,
                        source: item.source,
                        percentage: Math.round((item.score / item.max_score) * 100)
                    })));
                }
            } catch (err) {
                console.error("Failed to fetch analytics", err);
            } finally {
                setIsLoading(false);
            }
        };

        fetchAnalytics();
    }, [rollNumber]);

    if (isLoading) {
        return (
            <div className="flex justify-center items-center py-12">
                <p className="text-muted-foreground animate-pulse">Loading analytics...</p>
            </div>
        );
    }

    if (analyticsData.length === 0) {
        return (
            <Card className="border-dashed bg-secondary/5">
                <CardContent className="flex flex-col items-center justify-center py-16 text-center">
                    <div className="h-16 w-16 bg-primary/10 rounded-full flex items-center justify-center mb-4">
                        <Activity className="h-8 w-8 text-primary/60" />
                    </div>
                    <h3 className="text-lg font-medium mb-1">No Analytics Available</h3>
                    <p className="text-muted-foreground max-w-sm mx-auto">
                        We don't have any performance data for you yet. Complete some tests or ask your faculty to upload your internal marks!
                    </p>
                </CardContent>
            </Card>
        );
    }

    // Split data by source for different charts or visualization methods
    const aiTests = analyticsData.filter(d => d.source === "AI Generated Test");
    const internalMarks = analyticsData.filter(d => d.source === "Internal Excel Upload");

    return (
        <div className="space-y-6 animate-fade-in">
            <h2 className="text-xl font-bold mb-4">Your Performance Analytics</h2>

            {aiTests.length > 0 && (
                <Card className="border border-border/50 shadow-sm">
                    <CardHeader>
                        <CardTitle className="text-lg">AI Generated Tests</CardTitle>
                        <CardDescription>Your performance on randomly generated AI tests.</CardDescription>
                    </CardHeader>
                    <CardContent className="h-[300px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={aiTests} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                                <CartesianGrid strokeDasharray="3 3" opacity={0.2} />
                                <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                                <YAxis domain={[0, 100]} tick={{ fontSize: 12 }} />
                                <Tooltip
                                    formatter={(value: number, name: string, props: any) => [`${value}% (${props.payload.score}/${props.payload.max_score})`, 'Percentage']}
                                />
                                <Legend />
                                <Bar dataKey="percentage" fill="hsl(var(--primary))" name="Score (%)" radius={[4, 4, 0, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    </CardContent>
                </Card>
            )}

            {internalMarks.length > 0 && (
                <Card className="border border-border/50 shadow-sm">
                    <CardHeader>
                        <CardTitle className="text-lg">Internal Assessments</CardTitle>
                        <CardDescription>Your performance on faculty uploaded internal marks.</CardDescription>
                    </CardHeader>
                    <CardContent className="h-[300px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={internalMarks} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                                <CartesianGrid strokeDasharray="3 3" opacity={0.2} />
                                <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                                <YAxis domain={[0, 100]} tick={{ fontSize: 12 }} />
                                <Tooltip
                                    formatter={(value: number, name: string, props: any) => [`${value}% (${props.payload.score}/${props.payload.max_score})`, 'Percentage']}
                                />
                                <Legend />
                                <Bar dataKey="percentage" fill="hsl(var(--destructive))" name="Score (%)" radius={[4, 4, 0, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    </CardContent>
                </Card>
            )}
        </div>
    );
};
