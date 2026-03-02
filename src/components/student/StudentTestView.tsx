import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { getAvailableTestsForStudent, AssignedTest } from '../../data/mockTestData';
import { format } from "date-fns";
import { PlayCircle, Clock, CalendarDays } from 'lucide-react';
import { toast } from "sonner";

interface StudentTestViewProps {
    year: string;
    branch: string;
    section: string;
}

export const StudentTestView = ({ year, branch, section }: StudentTestViewProps) => {
    const [availableTests, setAvailableTests] = useState<AssignedTest[]>([]);

    useEffect(() => {
        // Fetch tests matching student's exact cohort
        const tests = getAvailableTestsForStudent(year, branch, section);
        setAvailableTests(tests);
    }, [year, branch, section]);

    const handleStartTest = (testTitle: string) => {
        toast.info(`Starting test: ${testTitle}. Exam engine placeholder!`);
    };

    return (
        <div className="space-y-6 animate-fade-in">
            <div className="flex items-center justify-between mb-4">
                <div>
                    <h2 className="text-xl font-bold">Available Tests</h2>
                    <p className="text-muted-foreground">Tests assigned to {year}, {branch} Section {section}</p>
                </div>
            </div>

            {availableTests.length === 0 ? (
                <Card className="border-dashed bg-secondary/5">
                    <CardContent className="flex flex-col items-center justify-center py-16 text-center">
                        <div className="h-16 w-16 bg-primary/10 rounded-full flex items-center justify-center mb-4">
                            <CalendarDays className="h-8 w-8 text-primary/60" />
                        </div>
                        <h3 className="text-lg font-medium mb-1">No Tests Available</h3>
                        <p className="text-muted-foreground max-w-sm mx-auto">
                            You're all caught up! There are no active tests assigned to your class section at the moment.
                        </p>
                    </CardContent>
                </Card>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                    {availableTests.map((test) => (
                        <Card key={test.id} className="border border-border/50 hover:border-primary/50 transition-colors shadow-sm relative overflow-hidden group">
                            <div className="absolute top-0 left-0 w-1 h-full bg-primary" />
                            <CardHeader className="pb-3">
                                <div className="flex justify-between items-start mb-1">
                                    <span className="text-xs font-medium px-2.5 py-1 bg-primary/10 text-primary rounded-full">
                                        {test.subject}
                                    </span>
                                    <span className="text-xs text-muted-foreground flex items-center gap-1">
                                        <Clock size={12} />
                                        {test.startTime}
                                    </span>
                                </div>
                                <CardTitle className="text-xl">{test.title}</CardTitle>
                                <CardDescription>
                                    Date: {format(new Date(test.date), 'MMMM d, yyyy')} <br />
                                    Duration: {test.startTime} to {test.endTime}
                                </CardDescription>
                            </CardHeader>
                            <CardContent className="pt-2">
                                <Button
                                    onClick={() => handleStartTest(test.title)}
                                    className="w-full group-hover:bg-primary group-hover:text-primary-foreground transition-all"
                                    variant="outline"
                                >
                                    <PlayCircle size={16} className="mr-2" />
                                    Start Test
                                </Button>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            )}
        </div>
    );
};
