import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { getSections, addSection, removeSection, subscribeToSections } from '../../data/mockSectionsData';
import { Trash2, PlusCircle, LayoutGrid } from 'lucide-react';
import { toast } from "sonner";

const ManageSections = () => {
    const [sections, setSections] = useState<string[]>([]);
    const [newSection, setNewSection] = useState("");

    useEffect(() => {
        setSections(getSections());
        const unsubscribe = subscribeToSections(() => {
            setSections(getSections());
        });
        return unsubscribe;
    }, []);

    const handleAddSection = (e: React.FormEvent) => {
        e.preventDefault();
        try {
            addSection(newSection);
            toast.success(`Section ${newSection.trim().toUpperCase()} added successfully.`);
            setNewSection("");
        } catch (err: any) {
            toast.error(err.message);
        }
    };

    const handleRemoveSection = (section: string) => {
        try {
            removeSection(section);
            toast.success(`Section ${section} removed.`);
        } catch (err: any) {
            toast.error("Failed to remove section.");
        }
    };

    return (
        <div className="space-y-6 animate-in slide-in-from-bottom-4 duration-500">
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <LayoutGrid size={20} className="text-primary" />
                        Class Sections
                    </CardTitle>
                    <CardDescription>
                        Manage the available sections dynamically. Changes will be reflected globally across the Faculty and Student hubs.
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-8">

                    <form onSubmit={handleAddSection} className="flex flex-col sm:flex-row gap-4 items-end max-w-md">
                        <div className="space-y-2 flex-1">
                            <Label>New Section Name</Label>
                            <Input
                                value={newSection}
                                onChange={(e) => setNewSection(e.target.value.toUpperCase())}
                                placeholder="e.g. D"
                                maxLength={3}
                            />
                        </div>
                        <Button type="submit" disabled={!newSection.trim()}>
                            <PlusCircle size={16} className="mr-2" />
                            Add Section
                        </Button>
                    </form>

                    <div>
                        <h3 className="text-sm font-medium mb-4 text-muted-foreground">Current Sections</h3>
                        {sections.length === 0 ? (
                            <p className="text-sm border border-dashed rounded-lg p-6 text-center text-muted-foreground bg-secondary/10">
                                No sections defined.
                            </p>
                        ) : (
                            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
                                {sections.map(section => (
                                    <div key={section} className="flex items-center justify-between border bg-card rounded-lg p-3 shadow-sm group">
                                        <span className="font-semibold text-lg ml-2">{section}</span>
                                        <Button
                                            variant="ghost"
                                            size="icon"
                                            onClick={() => handleRemoveSection(section)}
                                            className="text-muted-foreground hover:text-destructive hover:bg-destructive/10 h-8 w-8"
                                        >
                                            <Trash2 size={16} />
                                        </Button>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>

                </CardContent>
            </Card>
        </div>
    );
};

export default ManageSections;
