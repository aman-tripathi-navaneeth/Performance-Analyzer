import { useState, useEffect } from 'react';
import { CreateTestForm } from './CreateTestForm';
import { TestList } from './TestList';
import { getTestsByFaculty, AssignedTest } from '../../data/mockTestData';

interface CreateTestTabProps {
    facultyUsername: string;
}

export const CreateTestTab = ({ facultyUsername }: CreateTestTabProps) => {
    const [createdTests, setCreatedTests] = useState<AssignedTest[]>([]);

    const fetchTests = () => {
        const list = getTestsByFaculty(facultyUsername);
        setCreatedTests(list);
    };

    useEffect(() => {
        fetchTests();
    }, [facultyUsername]);

    return (
        <div className="space-y-8">
            {/* Create Test Form Section */}
            <CreateTestForm
                facultyUsername={facultyUsername}
                onTestCreated={fetchTests}
            />

            {/* Renders previous tests */}
            <TestList tests={createdTests} />
        </div>
    );
};
