import { useState, useEffect } from 'react';
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { branchOptions, yearOptions } from "./trainingTypes";
import { getSections, subscribeToSections } from "../../data/mockSectionsData";

interface PerformanceFilterProps {
    year: string;
    setYear: (val: string) => void;
    branch: string;
    setBranch: (val: string) => void;
    section: string;
    setSection: (val: string) => void;
}

export const PerformanceFilter = ({
    year, setYear,
    branch, setBranch,
    section, setSection
}: PerformanceFilterProps) => {
    const [availableSections, setAvailableSections] = useState<string[]>([]);

    useEffect(() => {
        setAvailableSections(getSections());
        const unsubscribe = subscribeToSections(() => {
            setAvailableSections(getSections());
        });
        return unsubscribe;
    }, []);

    return (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8 p-6 glass-card rounded-xl">
            <div className="space-y-2">
                <Label className="text-sm font-medium">Year <span className="text-destructive">*</span></Label>
                <Select value={year} onValueChange={setYear}>
                    <SelectTrigger className="bg-background/50">
                        <SelectValue placeholder="Select Year" />
                    </SelectTrigger>
                    <SelectContent>
                        {yearOptions.map(y => (
                            <SelectItem key={y} value={y}>{y}</SelectItem>
                        ))}
                    </SelectContent>
                </Select>
            </div>

            <div className="space-y-2">
                <Label className="text-sm font-medium">Branch <span className="text-destructive">*</span></Label>
                <Select value={branch} onValueChange={setBranch}>
                    <SelectTrigger className="bg-background/50">
                        <SelectValue placeholder="Select Branch" />
                    </SelectTrigger>
                    <SelectContent>
                        {branchOptions.map(b => (
                            <SelectItem key={b} value={b}>{b}</SelectItem>
                        ))}
                    </SelectContent>
                </Select>
            </div>

            <div className="space-y-2">
                <Label className="text-sm font-medium">Section <span className="text-destructive">*</span></Label>
                <Select value={section} onValueChange={setSection}>
                    <SelectTrigger className="bg-background/50">
                        <SelectValue placeholder="Select Section" />
                    </SelectTrigger>
                    <SelectContent>
                        {availableSections.length === 0 ? (
                            <SelectItem value="none" disabled>No sections available</SelectItem>
                        ) : (
                            availableSections.map(s => (
                                <SelectItem key={s} value={s}>{s}</SelectItem>
                            ))
                        )}
                    </SelectContent>
                </Select>
            </div>
        </div>
    );
};
