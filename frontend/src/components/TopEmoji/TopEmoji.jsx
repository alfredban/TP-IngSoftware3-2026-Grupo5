import react from 'react';
import styles from './TopEmoji.module.css';
import { Smile } from 'lucide-react';

const TopEmoji = ({ data }) => {

    if (!data) {
        return <p style={{ color: 'red' }}>No se han recibido datos para mostrar.</p>;
    }

    return (
        <div className={styles.boxCard}>
            <div className={styles.infoContainer}>
                <div className={styles.title}>Emoji favorito del grupo</div>
                <Smile className={styles.icon} />
            </div>

            <div className={styles.data}>{data}</div>

            <div className={styles.description}>Emoji más utilizado</div>
        </div>
    );

};

export default TopEmoji;
