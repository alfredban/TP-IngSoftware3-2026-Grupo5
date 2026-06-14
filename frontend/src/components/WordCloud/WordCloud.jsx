import React, { useRef, useEffect, useState } from 'react';
import styles from './WordCloud.module.css';

const WordCloud = ({ data }) => {
    const canvasRef = useRef(null);
    const containerRef = useRef(null);
    const [dimensions, setDimensions] = useState(null);

    useEffect(() => {
        const measure = () => {
            if (!containerRef.current) return;
            const width = containerRef.current.offsetWidth;
            if (width > 0) setDimensions({ width, height: Math.floor(width * 0.6) });
        };
        measure();
        const raf = requestAnimationFrame(measure);
        const observer = new ResizeObserver(measure);
        if (containerRef.current) observer.observe(containerRef.current);
        return () => { cancelAnimationFrame(raf); observer.disconnect(); };
    }, []);

    useEffect(() => {
        if (!canvasRef.current || !dimensions || !data?.length) return;

        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        const { width, height } = dimensions;

        canvas.width = width;
        canvas.height = height;
        ctx.clearRect(0, 0, width, height);

        const palette = ['#4D4E4BC', '#96ACB7', '#36558F', '#40376E', '#48233C', '#f472b6'];

        const minVal = Math.min(...data.map(d => d.frecuency));
        const maxVal = Math.max(...data.map(d => d.frecuency));
        const fontSize = (val) => Math.floor(12 + ((val - minVal) / (maxVal - minVal)) * 32);

        // Ordenar de mayor a menor para colocar primero las más grandes
        const sorted = [...data].sort((a, b) => b.frecuency - a.frecuency);

        const placed = []; // { x, y, w, h }

        const overlaps = (x, y, w, h) => {
            const pad = 6;
            return placed.some(p =>
                x - pad < p.x + p.w &&
                x + w + pad > p.x &&
                y - pad < p.y + p.h &&
                y + h + pad > p.y
            );
        };

        const cx = width / 2;
        const cy = height / 2;

        sorted.forEach((item, i) => {
            const fs = fontSize(item.frecuency);
            ctx.font = `bold ${fs}px Ubuntu, sans-serif`;
            const tw = ctx.measureText(item.word).width;
            const th = fs * 1.2;

            // Búsqueda en espiral desde el centro
            let placed_word = false;
            for (let r = 0; r < Math.max(width, height); r += 3) {
                for (let angle = 0; angle < Math.PI * 2; angle += 0.2) {
                    const x = cx + r * Math.cos(angle) - tw / 2;
                    const y = cy + r * Math.sin(angle) + th / 2;

                    if (x < 4 || x + tw > width - 4 || y - th < 4 || y > height - 4) continue;
                    if (!overlaps(x, y - th, tw, th)) {
                        ctx.fillStyle = palette[i % palette.length];
                        ctx.fillText(item.word, x, y);
                        placed.push({ x, y: y - th, w: tw, h: th });
                        placed_word = true;
                        break;
                    }
                }
                if (placed_word) break;
            }
        });
    }, [dimensions, data]);

    if (!data || data.length === 0) {
        return <p className={styles.wordcloudEmpty}>No hay datos para la nube de palabras.</p>;
    }

    return (
        <div className={styles.boxCard}>
            <h2>Nube de Palabras</h2>
            <p>Palabras más frecuentes del chat</p>
            <div ref={containerRef} className={styles.wordcloudContainer}>
                <canvas ref={canvasRef} style={{ display: 'block', width: '100%' }} />
            </div>
        </div>
    );
};

export default WordCloud;