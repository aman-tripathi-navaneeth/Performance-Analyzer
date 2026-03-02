import { useState } from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { Filter } from 'lucide-react';
import { PerformanceFilter } from './PerformanceFilter';
import { ClassGraph } from './ClassGraph';
import { StudentGraph } from './StudentGraph';
import { getFilteredClassData } from '../../data/mockPerformanceData';
import { ClassPerformanceData } from './trainingTypes';

export const ViewPerformanceTab = () => {
    const [year, setYear] = useState('');
    const [branch, setBranch] = useState('');
    const [section, setSection] = useState('');

    const [filteredData, setFilteredData] = useState<ClassPerformanceData | null>(null);

    // Auto-fetch data when all 3 filters are selected
    const handleFilterUpdate = (type: 'year' | 'branch' | 'section', value: string) => {
        let newYear = year;
        let newBranch = branch;
        let newSection = section;

        if (type === 'year') { newYear = value; setYear(value); }
        if (type === 'branch') { newBranch = value; setBranch(value); }
        if (type === 'section') { newSection = value; setSection(value); }

        if (newYear && newBranch && newSection && newSection.trim() !== '') {
            const data = getFilteredClassData(newYear, newBranch, newSection.trim());
            setFilteredData(data || null);
        } else {
            setFilteredData(null);
        }
    };

    return (
        <div className="space-y-8 animate-fade-in">
            <div className="mb-2">
                <h3 className="text-xl font-semibold mb-2">Class Performance Filters</h3>
                <p className="text-sm text-muted-foreground">Select year, branch, and section to load analytics data.</p>
            </div>

            <PerformanceFilter
                year={year} setYear={(v) => handleFilterUpdate('year', v)}
                branch={branch} setBranch={(v) => handleFilterUpdate('branch', v)}
                section={section} setSection={(v) => handleFilterUpdate('section', v)}
            />

            {filteredData ? (
                <div className="space-y-8">
                    {/* Class Overall Performance Section */}
                    <div className="space-y-4">
                        <h3 className="text-2xl font-bold tracking-tight">Overall Class Performance</h3>
                        <ClassGraph data={filteredData} />
                    </div>

                    <div className="my-8 border-t border-border/50"></div>

                    {/* Individual Student Performance Section */}
                    <div className="space-y-4">
                        <h3 className="text-2xl font-bold tracking-tight">Student Analysis</h3>
                        <StudentGraph data={filteredData} />
                    </div>
                </div>
            ) : (
                <Card className="border-dashed bg-background/50">
                    <CardContent className="flex flex-col items-center justify-center py-20 text-center">
                        <div className="h-16 w-16 bg-primary/10 rounded-full flex items-center justify-center mb-4">
                            <Filter className="h-8 w-8 text-primary" />
                        </div>
                        <h4 className="text-xl font-medium mb-2">No Data Available</h4>
                        <p className="text-muted-foreground max-w-md">
                            Please complete all three filters (Year, Branch, Section) to view the class and student performance analytics. Currently available for testing: Third Year/CSC/A and Second Year/CSE/B.
                        </p>
                    </CardContent>
                </Card>
            )}
        </div>
    );
};
