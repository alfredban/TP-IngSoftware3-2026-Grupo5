import react from 'react';
import styles from './TotalMessages.module.css';
import { MessageSquare } from 'lucide-react';

const TotalMessages = ({ data }) => {

    if (!data) {
        return <p style={{ color: 'red' }}>No se han recibido datos para mostrar.</p>;
    }

    return (
        <div className={styles.boxCard}>
            <div className={styles.infoContainer}>
                <div className={styles.title}>Mensajes totales</div>
                <MessageSquare className={styles.icon} />
            </div>

            <div className={styles.data}>{data}</div>

            <div className={styles.description}>En base al todo el historial del chat</div>
        </div>
    );

};

export default TotalMessages;
