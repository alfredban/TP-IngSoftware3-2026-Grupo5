import { useLocation, Navigate, useNavigate } from 'react-router-dom'
import { TotalMessages, TopSender, TopEmoji, TopDays, WordCloud, TopHour } from '../../components';
import styles from './Dashboard.module.css';
import { MoveLeft } from 'lucide-react';

const Dashboard = () => {
	const location = useLocation();
	const navigate = useNavigate();

	// Se recibe el JSON completo del backend
	const backendData = location.state;

	// Si alguien entra a /dashboard sin subir un archivo, lo devolvemos al upload
	if (!backendData) {
		return <Navigate to="/upload" replace />;
	}

	return (
		<div className={styles.container}>
			<div className={styles.header}>
				<div className={styles.title}>
					<h1>Dashboard de Análisis</h1>
					<button className={`btn btn-primary ${styles.button}`} onClick={() => navigate('/upload')}><MoveLeft /> Analizar otro archivo</button>
				</div>

				<p className={styles.filename}>
					<span>Archivo analizado:</span> {backendData.filename}
				</p>
			</div>

			<div className={styles.metricsContainer}>
				<div className={styles.boxSender}><TopSender data={backendData.metrics.top_sender} /></div>
				<div className={styles.boxEmoji}><TopEmoji data={backendData.metrics.top_emoji} /></div>
				<div className={styles.boxTotal}><TotalMessages data={backendData.metrics.total_messages} /></div>
				<div className={styles.boxHour}><TopHour data={backendData.metrics.messages_by_hour} /></div>
				<div className={styles.boxDays}><TopDays data={backendData.metrics.messages_by_day_of_week} /></div>
				<div className={styles.boxWordCloud}><WordCloud data={backendData?.metrics?.wordcloud_data} /></div>
			</div>

		</div>
	);
};

export default Dashboard;