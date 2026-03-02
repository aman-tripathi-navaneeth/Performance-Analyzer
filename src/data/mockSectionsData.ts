// Simple observer pattern to let components know when sections update
type Listener = () => void;
const listeners: Set<Listener> = new Set();

// Initial mock state
let availableSections: string[] = ['A', 'B', 'C'];

export const getSections = () => {
    return [...availableSections];
};

export const addSection = (section: string) => {
    const normalized = section.trim().toUpperCase();
    if (!normalized) {
        throw new Error("Section name cannot be empty.");
    }
    if (availableSections.includes(normalized)) {
        throw new Error("Section already exists.");
    }
    availableSections = [...availableSections, normalized].sort();
    notifyListeners();
    return availableSections;
};

export const removeSection = (section: string) => {
    const normalized = section.trim().toUpperCase();
    availableSections = availableSections.filter(s => s !== normalized);
    notifyListeners();
    return availableSections;
};

export const subscribeToSections = (listener: Listener) => {
    listeners.add(listener);
    return () => {
        listeners.delete(listener);
    };
};

const notifyListeners = () => {
    listeners.forEach(listener => listener());
};
