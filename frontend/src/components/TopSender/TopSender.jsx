import react from 'react';
import styles from './TopSender.module.css';

const TopSender = ({ data }) => {

    if (!data) {
        return <p style={{ color: 'red' }}>No se han recibido datos para mostrar.</p>;
    }

    return (
        

        <div className={styles.boxCard}>

            <div className={styles.icon}>   
            <svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 24 24">
             <path fillRule="evenodd" d="M12 4a4 4 0 1 0 0 8 4 4 0 0 0 0-8Zm-2 9a4 4 0 0 0-4 4v1a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2v-1a4 4 0 0 0-4-4h-4Z" clipRule="evenodd"/>
            </svg>
            </div>

            <div className={styles.title}>Usuario más activo</div>
            <div>
                
                <h3 className={styles.name}>{data}</h3>
                <p className={styles.title}>Usuario que envió más mensajes</p>
            </div>
        </div>

    );

};

export default TopSender;
