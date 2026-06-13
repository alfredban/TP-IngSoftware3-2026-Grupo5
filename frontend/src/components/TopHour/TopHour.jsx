import React from 'react';
import styles from './TopHour.module.css';
import { Bar } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Tooltip,
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip);

const TopHour = ({ data }) => {

    if (!data || data.length === 0) {
        return <p style={{ color: 'red' }}>No se han recibido datos para mostrar.</p>;
    }

    const chartData = {
        labels: data.map(d => d.hour),
        datasets: [
            {
                data: data.map(d => d.messages),
                backgroundColor: 'rgba(99, 179, 237, 0.7)',
                borderRadius: 6,
            },
        ],
    };

    const options = {
        responsive: true,
        plugins: {
            legend: { display: false },
        },
        scales: {
            x: {
                ticks: { color: 'var(--color-text-muted)' },
                grid: { display: false },
            },
            y: {
                ticks: { color: 'var(--color-text-muted)' },
                grid: { color: 'rgba(255,255,255,0.05)' },
            },
        },
    };

    return (
        <div className={styles.boxCard}>
            <div className={styles.title}>Actividad por Hora</div>
            <p className={styles.subtitle}>Franja horaria con mayor actividad</p>
            <Bar data={chartData} options={options} />
        </div>
    );
};

export default TopHour;