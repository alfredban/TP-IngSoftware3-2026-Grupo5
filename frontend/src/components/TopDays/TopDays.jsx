import React from 'react';
import styles from './TopDays.module.css';

const TopDays = ({ data }) => {

    if (!data || data.length === 0) {
        return <p style={{ color: 'red' }}>No se han recibido datos para mostrar.</p>;
    }

    const topDay = data.reduce((max, current) =>
        current.messages > max.messages ? current : max
    , data[0]);

    return (
        <div className={styles.boxCard}>

            <div className={styles.icon}>
                <svg className="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 24 24">
                    <path fillRule="evenodd" d="M6 2a1 1 0 0 1 1 1v1h10V3a1 1 0 1 1 2 0v1h1a2 2 0 0 1 2 2v13a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h1V3a1 1 0 0 1 1-1Zm13 7H5v9h14V9Z" clipRule="evenodd"/>
                </svg>
            </div>

            <div className={styles.title}>Actividad Semanal</div>
            <div>
                <h3 className={styles.name}>{topDay.day}</h3>
                <p className={styles.title}>Día con mayor actividad</p>
            </div>
        </div>
    );
};

export default TopDays;