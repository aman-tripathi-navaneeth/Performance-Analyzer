import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { toast } from "sonner";
import { branchOptions, yearOptions, subjectOptions } from './trainingTypes';
import { addMockTest } from '../../data/mockTestData';
import { getSections, subscribeToSections } from '../../data/mockSectionsData';

interface CreateTestFormProps {
    facultyUsername: string;
    onTestCreated: () => void;
}

export const CreateTestForm = ({ facultyUsername, onTestCreated }: CreateTestFormProps) => {
    const [title, setTitle] = useState('');
    const [year, setYear] = useState('');
    const [branch, setBranch] = useState('');
    const [section, setSection] = useState('');
    const [subject, setSubject] = useState('');
    const [date, setDate] = useState('');
    const [startTime, setStartTime] = useState('');
    const [endTime, setEndTime] = useState('');

    const [availableSections, setAvailableSections] = useState<string[]>([]);
    const [isSubmitting, setIsSubmitting] = useState(false);

    useEffect(() => {
        setAvailableSections(getSections());
        const unsubscribe = subscribeToSections(() => {
            setAvailableSections(getSections());
        });
        return unsubscribe;
    }, []);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!title || !year || !branch || !section || !subject || !date || !startTime || !endTime) {
            toast.error('Please fill in all required fields to create a test.');
            return;
        }

        setIsSubmitting(true);

        // Simulate API delay
        setTimeout(() => {
            addMockTest({
                title,
                year,
                branch,
                section,
                subject,
                date,
                startTime,
                endTime,
                createdBy: facultyUsername
            });

            toast.success('Test created successfully!');

            // Reset form
            setTitle('');
            setYear('');
            setBranch('');
            setSection('');
            setSubject('');
            setDate('');
            setStartTime('');
            setEndTime('');
            setIsSubmitting(false);

            onTestCreated();
        }, 600);
    };

    return (
        <Card className="shadow-md border border-border/50 animate-fade-in">
            <CardHeader>
                <CardTitle>Create New Test</CardTitle>
                <CardDescription>Configure a new test assigned to a specific class section.</CardDescription>
            </CardHeader>
            <CardContent>
                <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="space-y-2">
                        <Label>Test Title <span className="text-destructive">*</span></Label>
                        <Input
                            value={title}
                            onChange={e => setTitle(e.target.value)}
                            placeholder="e.g. Midterm Evaluation 1"
                            required
                        />
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        <div className="space-y-2">
                            <Label>Year <span className="text-destructive">*</span></Label>
                            <Select value={year} onValueChange={setYear} required>
                                <SelectTrigger><SelectValue placeholder="Select Year" /></SelectTrigger>
                                <SelectContent>
                                    {yearOptions.map(y => <SelectItem key={y} value={y}>{y}</SelectItem>)}
                                </SelectContent>
                            </Select>
                        </div>

                        <div className="space-y-2">
                            <Label>Branch <span className="text-destructive">*</span></Label>
                            <Select value={branch} onValueChange={setBranch} required>
                                <SelectTrigger><SelectValue placeholder="Select Branch" /></SelectTrigger>
                                <SelectContent>
                                    {branchOptions.map(b => <SelectItem key={b} value={b}>{b}</SelectItem>)}
                                </SelectContent>
                            </Select>
                        </div>

                        <div className="space-y-2">
                            <Label>Section <span className="text-destructive">*</span></Label>
                            <Select value={section} onValueChange={setSection} required>
                                <SelectTrigger><SelectValue placeholder="Select Section" /></SelectTrigger>
                                <SelectContent>
                                    {availableSections.length === 0 ? (
                                        <SelectItem value="none" disabled>No sections available</SelectItem>
                                    ) : (
                                        availableSections.map(s => <SelectItem key={s} value={s}>{s}</SelectItem>)
                                    )}
                                </SelectContent>
                            </Select>
                        </div>

                        <div className="space-y-2">
                            <Label>Subject <span className="text-destructive">*</span></Label>
                            <Select value={subject} onValueChange={setSubject} required>
                                <SelectTrigger><SelectValue placeholder="Select Subject" /></SelectTrigger>
                                <SelectContent>
                                    {subjectOptions.map(s => <SelectItem key={s} value={s}>{s}</SelectItem>)}
                                </SelectContent>
                            </Select>
                        </div>

                        <div className="space-y-2">
                            <Label>Date <span className="text-destructive">*</span></Label>
                            <Input
                                type="date"
                                value={date}
                                onChange={e => setDate(e.target.value)}
                                required
                            />
                        </div>

                        <div className="space-y-2">
                            <Label>Start Time <span className="text-destructive">*</span></Label>
                            <Input
                                type="time"
                                value={startTime}
                                onChange={e => setStartTime(e.target.value)}
                                required
                            />
                        </div>

                        <div className="space-y-2">
                            <Label>End Time <span className="text-destructive">*</span></Label>
                            <Input
                                type="time"
                                value={endTime}
                                onChange={e => setEndTime(e.target.value)}
                                required
                            />
                        </div>
                    </div>

                    <Button type="submit" className="w-full text-md py-6 mt-4" disabled={isSubmitting}>
                        {isSubmitting ? "Creating..." : "Create Assigned Test"}
                    </Button>
                </form>
            </CardContent>
        </Card>
    );
};
