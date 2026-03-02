import { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { FileUp, BarChart2, PlusCircle } from 'lucide-react';
import { UploadMarksTab } from './UploadMarksTab';
import { ViewPerformanceTab } from './ViewPerformanceTab';
import { CreateTestTab } from './CreateTestTab';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface FacultyDashboardProps {
  facultyUsername: string;
}

const FacultyDashboard = ({ facultyUsername }: FacultyDashboardProps) => {
  const [activeTab, setActiveTab] = useState<string>("upload-marks");

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold">Faculty Dashboard</h2>
          <p className="text-muted-foreground">
            Welcome, <span className="font-medium text-primary">{facultyUsername}</span>
          </p>
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="mb-6 flex-wrap h-auto gap-2">
          <TabsTrigger value="upload-marks" className="flex items-center gap-2">
            <FileUp size={16} />
            Upload Subject Marks
          </TabsTrigger>
          <TabsTrigger value="view-performance" className="flex items-center gap-2">
            <BarChart2 size={16} />
            View Class & Student Performance
          </TabsTrigger>
          <TabsTrigger value="create-test" className="flex items-center gap-2">
            <PlusCircle size={16} />
            Create Tests
          </TabsTrigger>
        </TabsList>

        <TabsContent value="upload-marks" className="space-y-6">
          <UploadMarksTab />
        </TabsContent>

        <TabsContent value="view-performance" className="space-y-6">
          <ViewPerformanceTab />
        </TabsContent>

        <TabsContent value="create-test" className="space-y-6">
          <CreateTestTab facultyUsername={facultyUsername} />
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default FacultyDashboard;
