import { useLocation, Navigate } from 'react-router-dom';

const Dashboard = () => {
    const location = useLocation();

    // Se recibe el JSON completo del backend
    const backendData = location.state;

    // Si alguien entra a /dashboard sin subir un archivo, lo devolvemos al upload
    if (!backendData) {
        return <Navigate to="/upload" replace />;
    }

    return (
        <div style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
            <h1 className="h1">Dashboard de Análisis</h1>

            <h2 className="h2 text-warning">ESTO ES SOLO DE PRUEBA PARA EL PASAJE DE INFORMACIÓN ENTRE UPLOAD Y EL DASHBOARD</h2>

            <p className="text-body-md text-success">
                Archivo analizado con éxito: {backendData.filename}
            </p>

            <div style={{ marginTop: '2rem' }}>
                <h3 className="h3">Respuesta cruda del servidor:</h3>

                {/* Cuadro oscuro para mostrar el JSON estructurado */}
                <pre style={{
                    backgroundColor: 'var(--color-bg)',
                    color: 'var(--color-text)',
                    padding: '1.5rem',
                    borderRadius: '8px',
                    overflowX: 'auto',
                    border: '1px solid var(--color-btn-secondary)'
                }}>
                    {JSON.stringify(backendData, null, 2)}
                </pre>
            </div>
        </div>
    );
};

export default Dashboard;
