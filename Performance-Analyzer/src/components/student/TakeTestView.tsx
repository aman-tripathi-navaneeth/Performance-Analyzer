import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import { ArrowLeft, Clock, CheckCircle2 } from 'lucide-react';
import { API_BASE_URL } from '../../config';

interface Question {
    id: string;
    question: string;
    option_a: string;
    option_b: string;
    option_c: string;
    option_d: string;
}

interface TakeTestViewProps {
    testId: string;
    testName: string;
    studentRoll: string;
    onBack: () => void;
    onComplete: (score: number, total: number) => void;
}

export const TakeTestView = ({ testId, testName, studentRoll, onBack, onComplete }: TakeTestViewProps) => {
    const [questions, setQuestions] = useState<Question[]>([]);
    const [answers, setAnswers] = useState<Record<string, string>>({});
    const [isLoading, setIsLoading] = useState(true);
    const [isSubmitting, setIsSubmitting] = useState(false);

    // Pagination
    const [currentIndex, setCurrentIndex] = useState(0);

    useEffect(() => {
        const fetchQuestions = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/api/tests/${testId}/questions?student_roll=${studentRoll}`);
                if (response.ok) {
                    const data = await response.json();
                    setQuestions(data);
                } else {
                    toast.error("Failed to load test questions.");
                    onBack();
                }
            } catch (err) {
                console.error(err);
                toast.error("Connection error while loading test.");
                onBack();
            } finally {
                setIsLoading(false);
            }
        };

        fetchQuestions();
    }, [testId, onBack]);

    const handleOptionSelect = (value: string) => {
        const currentQuestion = questions[currentIndex];
        if (currentQuestion) {
            setAnswers(prev => ({
                ...prev,
                [currentQuestion.id]: value
            }));
        }
    };

    // Auto-submit rules (Fullscreen & Visibility)
    useEffect(() => {
        if (isLoading || questions.length === 0) return;

        const enterFullscreen = async () => {
            try {
                if (document.documentElement.requestFullscreen) {
                    await document.documentElement.requestFullscreen();
                }
            } catch (err) {
                console.error("Could not request fullscreen", err);
            }
        };

        const handleFullscreenChange = () => {
            if (!document.fullscreenElement) {
                toast.error("You exited fullscreen mode. Your test will be automatically submitted.", { duration: 5000 });
                handleSubmit(true);
            }
        };

        const handleVisibilityChange = () => {
            if (document.hidden) {
                toast.error("You switched tabs. Your test will be automatically submitted.", { duration: 5000 });
                handleSubmit(true);
            }
        };

        // Attempt fullscreen on mount
        enterFullscreen();

        document.addEventListener("fullscreenchange", handleFullscreenChange);
        document.addEventListener("visibilitychange", handleVisibilityChange);

        return () => {
            document.removeEventListener("fullscreenchange", handleFullscreenChange);
            document.removeEventListener("visibilitychange", handleVisibilityChange);
            // Exit fullscreen when component unmounts naturally
            if (document.fullscreenElement && document.exitFullscreen) {
                document.exitFullscreen().catch(err => console.error(err));
            }
        };
        // Add handleSubmit to deps via ref or disable exhaustive-deps so it doesn't constantly rebind
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [isLoading, questions.length]);

    const handleSubmit = async (forceSubmit = false) => {
        // Validation: Ensure all questions are answered, unless auto-submitting due to violation
        if (!forceSubmit && Object.keys(answers).length < questions.length) {
            toast.error("Please answer all questions before submitting.");
            return;
        }

        if (isSubmitting) return;

        setIsSubmitting(true);
        try {
            const response = await fetch(`${API_BASE_URL}/api/tests/${testId}/submit`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    student_roll: studentRoll,
                    answers: answers
                }),
            });

            if (response.ok) {
                const result = await response.json();
                toast.success(`Test submitted successfully! You scored ${result.score}/${result.total_questions}`);
                onComplete(result.score, result.total_questions);
            } else {
                toast.error("Failed to submit test.");
            }
        } catch (err) {
            console.error(err);
            toast.error("Connection error while submitting.");
        } finally {
            setIsSubmitting(false);
        }
    };

    if (isLoading) {
        return (
            <div className="flex flex-col items-center justify-center p-12 space-y-4">
                <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent"></div>
                <p className="text-muted-foreground animate-pulse">Loading test questions...</p>
            </div>
        );
    }

    if (questions.length === 0) {
        return (
            <div className="text-center p-12">
                <p className="text-muted-foreground mb-4">No questions found for this test.</p>
                <Button variant="outline" onClick={onBack}>Go Back</Button>
            </div>
        );
    }

    const currentQ = questions[currentIndex];
    const isFirstQuestion = currentIndex === 0;
    const isLastQuestion = currentIndex === questions.length - 1;
    const allAnswered = Object.keys(answers).length === questions.length;

    return (
        <Card className="w-full max-w-4xl mx-auto shadow-lg animate-fade-in border-primary/20">
            <CardHeader className="flex flex-row items-center justify-between border-b pb-4 bg-secondary/5">
                <div className="space-y-1">
                    <Button variant="ghost" size="sm" onClick={onBack} className="mb-2 -ml-2 text-muted-foreground">
                        <ArrowLeft className="h-4 w-4 mr-1" /> Exit Test
                    </Button>
                    <CardTitle className="text-2xl text-primary font-jetbrains">{testName}</CardTitle>
                </div>
                <div className="flex items-center space-x-2 bg-background p-2 px-4 rounded-full border shadow-sm">
                    <Clock className="w-4 h-4 text-muted-foreground" />
                    <span className="font-medium text-sm">
                        Question {currentIndex + 1} of {questions.length}
                    </span>
                </div>
            </CardHeader>
            <CardContent className="pt-8 pb-8 px-6 md:px-12">
                <div className="mb-8 p-4 bg-secondary/10 rounded-lg border border-border/50">
                    <h3 className="text-lg font-medium leading-relaxed">
                        <span className="text-primary mr-2">{currentIndex + 1}.</span>
                        {currentQ.question}
                    </h3>
                </div>

                <RadioGroup
                    value={answers[currentQ.id] || ""}
                    onValueChange={handleOptionSelect}
                    className="space-y-4"
                >
                    {[
                        { id: 'a', text: currentQ.option_a },
                        { id: 'b', text: currentQ.option_b },
                        { id: 'c', text: currentQ.option_c },
                        { id: 'd', text: currentQ.option_d }
                    ].map((opt) => (
                        <div key={opt.id} className={`
                            flex items-center space-x-3 p-4 rounded-lg border transition-all duration-200 cursor-pointer
                            ${answers[currentQ.id] === opt.text ? 'bg-primary/5 border-primary shadow-sm' : 'hover:bg-secondary/20 hover:border-border'}
                        `}
                            onClick={() => handleOptionSelect(opt.text)}
                        >
                            <RadioGroupItem value={opt.text} id={`option-${opt.id}`} />
                            <Label htmlFor={`option-${opt.id}`} className="flex-1 cursor-pointer text-base">
                                {opt.text}
                            </Label>
                        </div>
                    ))}
                </RadioGroup>
            </CardContent>
            <CardFooter className="flex justify-between border-t p-6 bg-secondary/5">
                <Button
                    variant="outline"
                    onClick={() => setCurrentIndex(prev => Math.max(0, prev - 1))}
                    disabled={isFirstQuestion}
                    className="w-24"
                >
                    Previous
                </Button>

                <div className="flex space-x-2">
                    {Object.keys(answers).length > 0 && (
                        <span className="text-sm text-muted-foreground flex items-center justify-center mr-4">
                            {Object.keys(answers).length} / {questions.length} answered
                        </span>
                    )}

                    {!isLastQuestion ? (
                        <Button
                            onClick={() => setCurrentIndex(prev => Math.min(questions.length - 1, prev + 1))}
                            className="w-24"
                        >
                            Next
                        </Button>
                    ) : (
                        <Button
                            onClick={() => handleSubmit(false)}
                            disabled={!allAnswered || isSubmitting}
                            className={`w-36 ${allAnswered ? 'bg-green-600 hover:bg-green-700 text-white' : ''}`}
                        >
                            {isSubmitting ? "Submitting..." : (
                                <>
                                    <CheckCircle2 className="w-4 h-4 mr-2" />
                                    Submit Test
                                </>
                            )}
                        </Button>
                    )}
                </div>
            </CardFooter>
        </Card>
    );
};
