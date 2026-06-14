import { FileUploader } from '../../components';
import styles from './Upload.module.css';

const Upload = () => {
    return (
        <div className={styles.pageContainer}>
            {/* Usamos utilidades globales (h1, text-body-lg, text-muted) */}
            <h1 className="h1">WhatsApp Analyzer</h1>

            <p className={`text-body-lg text-muted ${styles.pageSubtitle}`}>
                Descubre las estadísticas reales de tus chats. Carga tu archivo exportado y obtén métricas detalladas al instante.
            </p>

            <FileUploader />
        </div>
    );
};

export default Upload;
