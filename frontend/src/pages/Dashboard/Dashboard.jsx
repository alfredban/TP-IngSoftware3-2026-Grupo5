import { useLocation, Navigate, useNavigate } from 'react-router-dom'

import { TotalMessages, TopSender, TopEmoji, TopDays, WordCloud, TopHour } from '../../components';
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
		<div>
			<div style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
				<div>
					<h1 className="h1">Dashboard de Análisis</h1>
					{/* botontoprev */}
					<button className="btn btn-primary" onClick={() => navigate('/upload')}>Volver al inicio</button>
				</div>

				<p className="text-body-md text-success">
					Archivo analizado con éxito: {backendData.filename}
				</p>
			</div>

			<div style={{ display: 'flex', justifyContent: 'center', gap: '2rem', flexWrap: 'wrap', padding: '0 2rem' }}>
				<div>
					<TopSender data={backendData.metrics.top_sender} />
				</div>
				<div>
					<TopEmoji data={backendData.metrics.top_emoji} />
				</div>
				<div>
					<TotalMessages data={backendData.metrics.total_messages} />
				</div>
			</div>

			<div style={{ display: 'flex', justifyContent: 'center', gap: '2rem', flexWrap: 'wrap', padding: '2rem' }}>
				<div style={{ width: '100%', maxWidth: '650px' }}>
					<TopHour data={backendData.metrics.messages_by_hour} />
				</div>
				<div style={{ width: '100%', maxWidth: '650px' }}>
					<TopDays data={backendData.metrics.messages_by_day_of_week} />
				</div>
			</div>

			<div>
				<WordCloud data={backendData?.metrics?.wordcloud_data} />
			</div>

		</div>
	);
};

export default Dashboard;