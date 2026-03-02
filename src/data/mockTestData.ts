export interface AssignedTest {
    id: string;
    title: string;
    year: string;
    branch: string;
    section: string;
    subject: string;
    date: string;
    startTime: string;
    endTime: string;
    createdBy: string;
}

// In-memory array for our mock session.
// Re-initializing won't persist across hard reloads, but serves the UI needs for now.
export let mockTestDatabase: AssignedTest[] = [
    {
        id: 'test-1',
        title: 'Midterm Evaluation',
        year: 'Third Year',
        branch: 'CSC',
        section: 'A',
        subject: 'Computer Networks',
        date: new Date().toISOString().split('T')[0], // Today
        startTime: '10:00',
        endTime: '11:00',
        createdBy: 'faculty'
    }
];

export const addMockTest = (test: Omit<AssignedTest, 'id'>) => {
    const newTest: AssignedTest = {
        ...test,
        id: `test-${Date.now()}`
    };
    // Push to the beginning to show newest first
    mockTestDatabase = [newTest, ...mockTestDatabase];
    return newTest;
};

export const getTestsByFaculty = (facultyUsername: string) => {
    return mockTestDatabase.filter(t => t.createdBy === facultyUsername);
};

export const getAvailableTestsForStudent = (year: string, branch: string, section: string) => {
    // Return tests that match the student's cohort
    return mockTestDatabase.filter(t =>
        t.year.toLowerCase() === year.toLowerCase() &&
        t.branch.toLowerCase() === branch.toLowerCase() &&
        t.section.toLowerCase() === section.toLowerCase()
    );
};
