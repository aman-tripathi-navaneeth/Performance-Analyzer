import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Trash2, PlusCircle, LayoutGrid } from 'lucide-react';
import { toast } from "sonner";
import { API_BASE_URL } from '../../config';

const ManageSections = () => {
    const [sections, setSections] = useState<string[]>([]);
    const [newSection, setNewSection] = useState("");

    const fetchSections = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/sections`);
            if (response.ok) {
                const data = await response.json();
                setSections(data.map((s: any) => s.name));
            }
        } catch (err) {
            console.error("Failed to fetch sections", err);
        }
    };

    useEffect(() => {
        fetchSections();
    }, []);

    const handleAddSection = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const response = await fetch(`${API_BASE_URL}/api/sections/add`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: newSection.trim().toUpperCase(),
                    branch: "ALL", // Default values for now
                    year: "ALL"
                }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to add section');
            }

            toast.success(`Section ${newSection.trim().toUpperCase()} added successfully.`);
            setNewSection("");
            fetchSections(); // Refresh list from DB
        } catch (err: any) {
            toast.error(err.message || "Error connecting to backend");
        }
    };

    const handleRemoveSection = (section: string) => {
        toast.info("Remove section functionality to be implemented in backend");
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
