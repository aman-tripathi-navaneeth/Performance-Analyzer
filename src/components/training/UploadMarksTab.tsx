import { useState, useRef } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { UploadCloud, FileSpreadsheet, CheckCircle2, TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { toast } from "sonner";
import * as XLSX from 'xlsx';

interface ParsedStudentData {
  rollNumber: string;
  name: string;
  marks: number;
}

export const UploadMarksTab = () => {
  const [year, setYear] = useState('');
  const [branch, setBranch] = useState('');
  const [section, setSection] = useState('');
  const [subject, setSubject] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  
  // Analysis State
  const [parsedData, setParsedData] = useState<ParsedStudentData[]>([]);
  const [classAverage, setClassAverage] = useState(0);
  const [highestMark, setHighestMark] = useState(0);
  const [lowestMark, setLowestMark] = useState(0);
  
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      validateAndSetFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const validateAndSetFile = (selectedFile: File) => {
    const validExtensions = ['.xlsx', '.xls', '.pdf'];
    const fileExtension = selectedFile.name.substring(selectedFile.name.lastIndexOf('.')).toLowerCase();
    
    if (validExtensions.includes(fileExtension)) {
      setFile(selectedFile);
    } else {
      toast.error("Invalid file type. Please upload .xlsx, .xls, or .pdf");
    }
  };

  const processExcelData = (fileToRead: File) => {
    const reader = new FileReader();

    reader.onload = (e) => {
      try {
        const data = e.target?.result;
        const workbook = XLSX.read(data, { type: 'binary' });
        const firstSheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[firstSheetName];
        
        // Convert to JSON
        const rawJson: any[] = XLSX.utils.sheet_to_json(worksheet);
        
        // Map raw JSON to our structure (assuming common column names)
        const mappedData: ParsedStudentData[] = rawJson.map(row => {
          // Try to intelligently find the right columns regardless of exact casing
          const rollKey = Object.keys(row).find(k => k.toLowerCase().includes('roll')) || 'RollNo';
          const nameKey = Object.keys(row).find(k => k.toLowerCase().includes('name')) || 'Name';
          const marksKey = Object.keys(row).find(k => k.toLowerCase().includes('mark') || k.toLowerCase().includes('score')) || 'Marks';
          
          return {
            rollNumber: String(row[rollKey] || 'Unknown'),
            name: String(row[nameKey] || 'Unknown Student'),
            marks: Number(row[marksKey] || 0)
          };
        }).filter(student => !isNaN(student.marks)); // Filter out invalid rows

        if (mappedData.length === 0) {
          toast.error("Could not find valid 'Marks' data in the uploaded sheet.");
          setIsUploading(false);
          return;
        }

        // Calculate Stats
        const totalMarks = mappedData.reduce((acc, curr) => acc + curr.marks, 0);
        const avg = mappedData.length > 0 ? totalMarks / mappedData.length : 0;
        const highest = Math.max(...mappedData.map(s => s.marks));
        const lowest = Math.min(...mappedData.map(s => s.marks));

        setParsedData(mappedData);
        setClassAverage(Number(avg.toFixed(2)));
        setHighestMark(highest);
        setLowestMark(lowest);
        
        toast.success(`Successfully analyzed marks for ${mappedData.length} students!`);
      } catch (error) {
        console.error("Excel parsing error:", error);
        toast.error("Failed to parse the Excel file. Ensure it is formatted correctly.");
      } finally {
        setIsUploading(false);
      }
    };

    reader.readAsBinaryString(fileToRead);
  };

  const handleSimulatePDFParsing = () => {
    // PDF extraction pure client-side is very complex without a backend OCR tool.
    // For Phase 1, we will simulate a successful read.
    setTimeout(() => {
      const simulatedData: ParsedStudentData[] = [
        { rollNumber: "216K1A0501", name: "Rahul Kumar", marks: 85 },
        { rollNumber: "216K1A0502", name: "Priya Sharma", marks: 92 },
        { rollNumber: "216K1A0503", name: "Amit Singh", marks: 78 },
        { rollNumber: "216K1A0504", name: "Sneha Reddy", marks: 88 }
      ];

      const totalMarks = simulatedData.reduce((acc, curr) => acc + curr.marks, 0);
      setClassAverage(Number((totalMarks / simulatedData.length).toFixed(2)));
      setHighestMark(92);
      setLowestMark(78);
      setParsedData(simulatedData);

      toast.success("PDF analyzed (Simulated Mock Data)");
      setIsUploading(false);
    }, 1500);
  };

  const handleSubmit = () => {
    if (!year || !branch || !section || !subject) {
      toast.error("Please fill in all required Subject Metadata fields.");
      return;
    }
    
    if (!file) {
      toast.error("Please upload a file to proceed.");
      return;
    }

    setIsUploading(true);
    toast.loading("Parsing document and extracting marks...");
    
    // Slight delay to allow UI to show loading state
    setTimeout(() => {
      toast.dismiss();
      const isPdf = file.name.toLowerCase().endsWith('.pdf');
      
      if (isPdf) {
        handleSimulatePDFParsing();
      } else {
        processExcelData(file);
      }
    }, 500);
  };

  const resetForm = () => {
    setFile(null);
    setParsedData([]);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  const renderDifferenceIcon = (marks: number, average: number) => {
    const diff = marks - average;
    if (diff > 0) return <span className="text-green-500 flex items-center gap-1"><TrendingUp size={16}/> +{diff.toFixed(1)}</span>;
    if (diff < 0) return <span className="text-destructive flex items-center gap-1"><TrendingDown size={16}/> {diff.toFixed(1)}</span>;
    return <span className="text-muted-foreground flex items-center gap-1"><Minus size={16}/> 0.0</span>;
  };

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Upload Section */}
      {parsedData.length === 0 ? (
        <Card className="shadow-md border border-border/50">
          <CardHeader>
            <CardTitle>Upload Subject Marks</CardTitle>
            <CardDescription>Upload an Excel sheet or PDF containing student roll numbers and marks.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-8">
            {/* Metadata Fields */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="space-y-2">
                <Label>Year <span className="text-destructive">*</span></Label>
                <Select value={year} onValueChange={setYear}>
                  <SelectTrigger><SelectValue placeholder="Select Year" /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="1">First Year</SelectItem>
                    <SelectItem value="2">Second Year</SelectItem>
                    <SelectItem value="3">Third Year</SelectItem>
                    <SelectItem value="4">Fourth Year</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Branch <span className="text-destructive">*</span></Label>
                <Select value={branch} onValueChange={setBranch}>
                  <SelectTrigger><SelectValue placeholder="Select Branch" /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="CSE">CSE</SelectItem>
                    <SelectItem value="CSC">CSC</SelectItem>
                    <SelectItem value="COS">COS</SelectItem>
                    <SelectItem value="MEC">MEC</SelectItem>
                    <SelectItem value="CIVIL">CIVIL</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Section <span className="text-destructive">*</span></Label>
                <Input 
                  value={section} 
                  onChange={(e) => setSection(e.target.value.toUpperCase())} 
                  placeholder="e.g. A" 
                  maxLength={2}
                />
              </div>

              <div className="space-y-2">
                <Label>Subject Name <span className="text-destructive">*</span></Label>
                <Input 
                  value={subject} 
                  onChange={(e) => setSubject(e.target.value)} 
                  placeholder="e.g. Data Structures" 
                />
              </div>
            </div>

            {/* Drag & Drop Upload Area */}
            <div 
              className={`border-2 border-dashed rounded-xl p-10 text-center transition-colors
                ${file ? 'border-primary/50 bg-primary/5' : 'border-border/50 hover:border-primary/50 hover:bg-secondary/20'}
              `}
              onDragOver={handleDragOver}
              onDrop={handleDrop}
            >
              <input 
                type="file" 
                ref={fileInputRef} 
                className="hidden" 
                accept=".xlsx, .xls, .pdf"
                onChange={handleFileChange}
              />
              
              {!file ? (
                <div className="flex flex-col items-center gap-4 cursor-pointer" onClick={() => fileInputRef.current?.click()}>
                  <div className="h-16 w-16 bg-secondary/50 rounded-full flex items-center justify-center">
                    <UploadCloud className="h-8 w-8 text-muted-foreground" />
                  </div>
                  <div>
                    <p className="font-medium text-lg">Click to upload or drag & drop</p>
                    <p className="text-sm text-muted-foreground mt-1">Accepts Excel (.xlsx, .xls) and PDF</p>
                  </div>
                </div>
              ) : (
                <div className="flex flex-col items-center gap-4">
                  <div className="h-16 w-16 bg-primary/10 rounded-full flex items-center justify-center">
                    <FileSpreadsheet className="h-8 w-8 text-primary" />
                  </div>
                  <div>
                    <p className="font-medium text-lg flex items-center justify-center gap-2">
                      <CheckCircle2 className="h-5 w-5 text-green-500"/> {file.name}
                    </p>
                    <p className="text-sm text-muted-foreground mt-1">{(file.size / 1024).toFixed(2)} KB</p>
                  </div>
                  <Button variant="outline" size="sm" onClick={(e) => { e.stopPropagation(); setFile(null); }}>
                    Remove File
                  </Button>
                </div>
              )}
            </div>

            <Button 
              className="w-full py-6 text-lg" 
              onClick={handleSubmit} 
              disabled={isUploading}
            >
              {isUploading ? "Processing..." : "Extract & Analyze Marks"}
            </Button>
          </CardContent>
        </Card>
      ) : (
        /* Analysis Results View */
        <div className="space-y-6 animate-in slide-in-from-bottom-4 duration-500">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold">{subject} - Section {section}</h2>
              <p className="text-muted-foreground">Year {year} | Branch {branch} | {parsedData.length} Students Evaluated</p>
            </div>
            <Button variant="outline" onClick={resetForm}>Upload Another Sheet</Button>
          </div>

          {/* Quick Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card className="bg-primary/5 border-primary/20">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <p className="text-sm font-medium text-muted-foreground">Class Average</p>
                  <TrendingUp className="h-4 w-4 text-primary" />
                </div>
                <p className="text-3xl font-bold mt-2">{classAverage}</p>
              </CardContent>
            </Card>
            <Card className="bg-green-500/5 border-green-500/20">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <p className="text-sm font-medium text-muted-foreground">Highest Mark</p>
                  <TrendingUp className="h-4 w-4 text-green-500" />
                </div>
                <p className="text-3xl font-bold mt-2 text-green-600 dark:text-green-400">{highestMark}</p>
              </CardContent>
            </Card>
            <Card className="bg-destructive/5 border-destructive/20">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <p className="text-sm font-medium text-muted-foreground">Lowest Mark</p>
                  <TrendingDown className="h-4 w-4 text-destructive" />
                </div>
                <p className="text-3xl font-bold mt-2 text-destructive">{lowestMark}</p>
              </CardContent>
            </Card>
          </div>

          {/* Detailed Table View */}
          <Card>
            <CardHeader>
              <CardTitle>Detailed Student Performance</CardTitle>
              <CardDescription>Individual marks compared against the class average of {classAverage}.</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="rounded-md border">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Roll Number</TableHead>
                      <TableHead>Student Name</TableHead>
                      <TableHead className="text-right">Marks</TableHead>
                      <TableHead className="text-right">Vs Average</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {parsedData.map((student, idx) => (
                      <TableRow key={idx}>
                        <TableCell className="font-medium">{student.rollNumber}</TableCell>
                        <TableCell>{student.name}</TableCell>
                        <TableCell className="text-right font-bold">{student.marks}</TableCell>
                        <TableCell className="text-right flex justify-end">
                          {renderDifferenceIcon(student.marks, classAverage)}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};
