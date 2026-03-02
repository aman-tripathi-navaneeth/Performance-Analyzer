import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { AssignedTest } from "../../data/mockTestData";
import { format } from "date-fns";
import { Clock, Users } from 'lucide-react';

interface TestListProps {
    tests: AssignedTest[];
}

export const TestList = ({ tests }: TestListProps) => {
    return (
        <Card className="animate-fade-in shadow-sm">
            <CardHeader>
                <CardTitle>Created Tests</CardTitle>
                <CardDescription>A list of all the tests you have assigned to your classes.</CardDescription>
            </CardHeader>
            <CardContent>
                {tests.length === 0 ? (
                    <div className="flex flex-col items-center justify-center p-8 text-center bg-secondary/10 rounded-lg">
                        <h3 className="font-medium text-lg">No Tests Created Yet</h3>
                        <p className="text-muted-foreground mt-1">Submit the form above to deploy your first assigned test.</p>
                    </div>
                ) : (
                    <div className="rounded-md border">
                        <Table>
                            <TableHeader className="bg-muted/50">
                                <TableRow>
                                    <TableHead>Title & Subject</TableHead>
                                    <TableHead>Assigned To</TableHead>
                                    <TableHead>Schedule</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {tests.map(test => (
                                    <TableRow key={test.id}>
                                        <TableCell>
                                            <div className="font-medium">{test.title}</div>
                                            <div className="text-sm text-muted-foreground">{test.subject}</div>
                                        </TableCell>
                                        <TableCell>
                                            <div className="flex flex-col gap-1 text-sm">
                                                <div className="flex items-center gap-1.5 text-muted-foreground">
                                                    <Users size={14} className="text-primary/70" />
                                                    {test.year} - {test.branch}
                                                </div>
                                                <span className="font-medium pl-5">Section {test.section}</span>
                                            </div>
                                        </TableCell>
                                        <TableCell>
                                            <div className="flex flex-col gap-1 text-sm">
                                                <div className="font-medium">
                                                    {format(new Date(test.date), 'MMM d, yyyy')}
                                                </div>
                                                <div className="flex items-center gap-1.5 text-muted-foreground">
                                                    <Clock size={14} className="text-primary/70" />
                                                    {test.startTime} - {test.endTime}
                                                </div>
                                            </div>
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </div>
                )}
            </CardContent>
        </Card>
    );
};
