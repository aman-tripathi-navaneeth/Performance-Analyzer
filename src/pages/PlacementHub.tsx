import { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import Navbar from '../components/Navbar';
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { toast } from "sonner";
import { Briefcase, Award, ExternalLink, UserCircle, Camera } from 'lucide-react';
import { format } from "date-fns";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { StudentTestView } from '../components/student/StudentTestView';

const PlacementHub = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [activeTab, setActiveTab] = useState('jobs');
  const [profilePicture, setProfilePicture] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const userStr = localStorage.getItem('user');
    if (userStr) {
      try {
        const user = JSON.parse(userStr);
        if (user.role === 'student') {
          setUsername(user.username);
        }
      } catch (e) {
        // Ignore JSON parse errors
      }
    }
  }, []);

  const studentData = {
    name: "Rahul Kumar",
    rollNumber: username || "216K1A0501",
    batch: "2021-2025",
    year: "Third Year",
    branch: "CSC", // Hardcoded to match our initial mock data
    section: "A",
    email: "rahul.k@student.ideal.edu"
  };

  const availableJobs = [
    {
      id: '1',
      company: 'TechSolutions Inc.',
      package: '12 LPA',
      requirements: {
        minPercentage: 75,
        certification: 'AWS Cloud Practitioner'
      },
      lastDate: new Date('2025-05-15'),
      applicationUrl: 'https://example.com/apply'
    },
    {
      id: '2',
      company: 'Innovate Systems',
      package: '8.5 LPA',
      requirements: {
        minPercentage: 70,
        certification: null
      },
      lastDate: new Date('2025-05-20'),
      applicationUrl: 'https://example.com/apply'
    },
    {
      id: '3',
      company: 'Digital Dynamics',
      package: '10 LPA',
      requirements: {
        minPercentage: 80,
        certification: 'React Developer'
      },
      lastDate: new Date('2025-05-25'),
      applicationUrl: 'https://example.com/apply'
    }
  ];

  const handleLogout = () => {
    localStorage.removeItem('user');
    setProfilePicture(null);
    toast.success('Logged out successfully');
    navigate('/');
  };

  const handleProfilePictureUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // Simulate upload
      toast.loading('Uploading profile picture...');

      setTimeout(() => {
        const reader = new FileReader();
        reader.onload = () => {
          setProfilePicture(reader.result as string);
          toast.dismiss();
          toast.success('Profile picture updated successfully');
        };
        reader.readAsDataURL(file);
      }, 1000);
    }
  };

  const triggerFileInput = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="min-h-screen bg-space-gradient">
      <Navbar />

      <div className="pt-32 pb-20 container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <span className="inline-block px-3 py-1 rounded-full text-xs font-medium bg-primary/20 text-primary mb-3">
            Student Dashboard
          </span>
          <h1 className="text-3xl md:text-5xl font-bold mb-4 cosmic-text">
            Your Campus Placement Portal
          </h1>
          <p className="text-lg max-w-2xl mx-auto text-muted-foreground">
            Manage your placement journey and professional development
          </p>
        </motion.div>

        <div className="max-w-6xl mx-auto">
          <Card className="mb-8 overflow-hidden cosmic-card">
            <div className="flex flex-col md:flex-row">
              <div className="md:w-1/4 bg-secondary/20 p-6 flex flex-col items-center justify-center border-r border-border/10">
                <div className="relative mb-4 group">
                  <Avatar className="w-28 h-28 border-2 border-primary/20">
                    <AvatarImage src={profilePicture || undefined} />
                    <AvatarFallback className="text-3xl bg-primary/10">
                      {studentData.name.charAt(0)}
                    </AvatarFallback>
                  </Avatar>

                  <div
                    className="absolute inset-0 bg-black/30 backdrop-blur-sm rounded-full 
                             flex items-center justify-center opacity-0 group-hover:opacity-100
                             transition-opacity duration-200 cursor-pointer"
                    onClick={triggerFileInput}
                  >
                    <Camera className="text-white" size={24} />
                  </div>

                  <input
                    type="file"
                    ref={fileInputRef}
                    accept="image/*"
                    className="hidden"
                    onChange={handleProfilePictureUpload}
                  />
                </div>

                <Button
                  variant="outline"
                  size="sm"
                  className="mb-2 w-full bg-secondary/20 hover:bg-secondary/40"
                  onClick={triggerFileInput}
                >
                  <Camera size={14} className="mr-2" />
                  Update Photo
                </Button>

                <Button
                  variant="outline"
                  size="sm"
                  className="w-full text-destructive hover:text-destructive"
                  onClick={handleLogout}
                >
                  Logout
                </Button>
              </div>

              <div className="md:w-3/4 p-6">
                <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
                  <UserCircle size={24} />
                  {studentData.name}
                </h2>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-muted-foreground">Roll Number</p>
                    <p className="font-medium">{studentData.rollNumber}</p>
                  </div>

                  <div>
                    <p className="text-sm text-muted-foreground">Email</p>
                    <p className="font-medium">{studentData.email}</p>
                  </div>

                  <div>
                    <p className="text-sm text-muted-foreground">Batch</p>
                    <p className="font-medium">{studentData.batch}</p>
                  </div>

                  <div>
                    <p className="text-sm text-muted-foreground">Branch</p>
                    <p className="font-medium">{studentData.branch}</p>
                  </div>
                </div>
              </div>
            </div>
          </Card>

          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="mb-6 w-full justify-start overflow-x-auto">
              <TabsTrigger value="jobs" className="flex items-center gap-2">
                <Briefcase size={16} />
                Available Jobs
              </TabsTrigger>
              <TabsTrigger value="tests" className="flex items-center gap-2">
                <Award size={16} />
                Available Tests
              </TabsTrigger>

            </TabsList>

            <TabsContent value="jobs" className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {availableJobs.map(job => (
                  <Card key={job.id} className="cosmic-card overflow-hidden">
                    <CardHeader className="pb-2">
                      <div className="flex justify-between items-start">
                        <div>
                          <CardTitle className="text-xl mb-1">{job.company}</CardTitle>
                          <CardDescription>Package: {job.package}</CardDescription>
                        </div>
                        <span className="px-2 py-1 bg-secondary/30 rounded-md text-xs">
                          {format(job.lastDate, 'MMM d, yyyy')}
                        </span>
                      </div>
                    </CardHeader>

                    <CardContent className="pt-2">
                      <div className="mb-4">
                        <p className="text-sm text-muted-foreground mb-1">Requirements:</p>
                        <ul className="space-y-1">
                          <li className="text-sm flex items-center gap-2">
                            <div className="w-2 h-2 rounded-full bg-primary/60" />
                            <span>Min. Percentage: {job.requirements.minPercentage}%</span>
                          </li>
                          {job.requirements.certification && (
                            <li className="text-sm flex items-center gap-2">
                              <div className="w-2 h-2 rounded-full bg-primary/60" />
                              <span>Certification: {job.requirements.certification}</span>
                            </li>
                          )}
                        </ul>
                      </div>

                      <div className="mt-4 pt-4 border-t border-border/10 flex justify-between items-center">
                        <span className="text-xs text-muted-foreground">
                          Apply before {format(job.lastDate, 'MMM d, yyyy')}
                        </span>

                        <Button
                          size="sm"
                          className="bg-cosmic-500 hover:bg-cosmic-600 transition-colors text-white"
                          onClick={() => {
                            toast.success(`Application link for ${job.company} opened`);
                            window.open(job.applicationUrl, '_blank');
                          }}
                        >
                          <ExternalLink size={14} className="mr-1" />
                          Apply
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            <TabsContent value="tests" className="space-y-6">
              <StudentTestView
                year={studentData.year}
                branch={studentData.branch}
                section={studentData.section}
              />
            </TabsContent>


          </Tabs>
        </div>
      </div>
    </div>
  );
};

export default PlacementHub;
