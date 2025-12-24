import React, { createContext, useState, useContext, useEffect } from 'react';

const GlobalStateContext = createContext();

export const GlobalStateProvider = ({ children }) => {
    // Initialize from localStorage if available
    const [jobIds, setJobIds] = useState(() => {
        const saved = localStorage.getItem('mobilesec_job_ids');
        if (saved) {
            return JSON.parse(saved);
        }
        return {
            apkscanner: null,
            secrethunter: null,
            cryptocheck: null,
            networkinspector: null,
            aiscanner: null
        };
    });

    // Save to localStorage whenever jobIds changes
    useEffect(() => {
        localStorage.setItem('mobilesec_job_ids', JSON.stringify(jobIds));
    }, [jobIds]);

    const updateJobId = (service, id) => {
        setJobIds(prev => ({
            ...prev,
            [service]: id
        }));
    };

    return (
        <GlobalStateContext.Provider value={{ jobIds, updateJobId }}>
            {children}
        </GlobalStateContext.Provider>
    );
};

export const useGlobalState = () => useContext(GlobalStateContext);
