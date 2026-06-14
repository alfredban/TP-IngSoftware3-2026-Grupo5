import react from 'react';
import styles from './TopSender.module.css';
import { User } from 'lucide-react';

const TopSender = ({ data }) => {

    if (!data) {
        return <p style={{ color: 'red' }}>No se han recibido datos para mostrar.</p>;
    }

    return (
        <div className={styles.boxCard}>
            <div className={styles.infoContainer}>
                <div className={styles.title}>Usuario mas activo</div>
                <User className={styles.icon} />
            </div>

            <div className={styles.data}>{data}</div>

            <div className={styles.description}>Usuario que más mensajes envió</div>
        </div>
    );

};

export default TopSender;
