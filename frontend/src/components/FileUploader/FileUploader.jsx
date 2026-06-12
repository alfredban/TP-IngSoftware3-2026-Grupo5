import { useNavigate } from 'react-router-dom';
import { useState, useRef } from 'react';
import { CloudUpload, FileText } from 'lucide-react';
import { Modal } from '../../components';
import styles from './FileUploader.module.css';

const FileUploader = () => {
    const navigate = useNavigate();
    const [file, setFile] = useState(null);
    const [isDragging, setIsDragging] = useState(false);
    const [errorModal, setErrorModal] = useState({ isOpen: false, message: '' });
    const fileInputRef = useRef(null);

    // Función para validar que sea .txt o .zip
    const isValidFile = (file) => {
        const validTypes = ['text/plain', 'application/zip', 'application/x-zip-compressed'];
        const validExtensions = ['.txt', '.zip'];
        
        const isTypeValid = validTypes.includes(file.type);
        const isExtensionValid = validExtensions.some(ext => file.name.toLowerCase().endsWith(ext));
        
        return isTypeValid || isExtensionValid;
    };

    const handleDragOver = (e) => {
        e.preventDefault();
        setIsDragging(true);
    };
    
    const handleDragLeave = () => setIsDragging(false);
    
    const handleDrop = (e) => {
        e.preventDefault();
        setIsDragging(false);
        const droppedFile = e.dataTransfer.files[0];
        
        if (droppedFile) {
            if (isValidFile(droppedFile)) {
                setFile(droppedFile);
            } else {
                setErrorModal({ isOpen: true, message: "Por favor, sube únicamente un archivo .txt o\u00A0.zip" });
            }
        }
    };

    const handleFileSelect = (e) => {
        const selectedFile = e.target.files[0];
        
        if (selectedFile) {
            if (isValidFile(selectedFile)) {
                setFile(selectedFile);
            } else {
                setErrorModal({ isOpen: true, message: "Por favor, sube únicamente un archivo .txt o\u00A0.zip" });
            }
        }
        
        // Limpiar el input para poder volver a elegir el mismo archivo si se cancela
        e.target.value = null; 
    };

    const formatFileSize = (bytes) => {
        if (bytes < 1024) return bytes + ' B';
        else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
        else return (bytes / 1048576).toFixed(1) + ' MB';
    };

    const handleAnalyze = () => {

        // TODO: Crear el fetch al backend y pasarle el file, recibir la data, comprobar errores y luego navegar al dashboard

        // Simulamos la respuesta exacta que traería el backend
        const mockBackendResponse = {
            filename: file.name,
            file_size: file.size,
            file_type: file.name.endsWith('.zip') ? "zip" : "txt",
            metrics: {
                total_messages: 15420,
                top_sender: "Juan",
                top_emoji: "😂",
                messages_by_hour: [
                    { hour: "18h", messages: 1200 },
                    { hour: "19h", messages: 1500 },
                    { hour: "20h", messages: 3200 }
                ],
                messages_by_day_of_week: [
                    { day: "Vie", messages: 2400 },
                    { day: "Sab", messages: 4500 },
                    { day: "Dom", messages: 3100 }
                ],
                wordcloud_data: [
                    { word: "jaja", frecuency: 850 },
                    { word: "hola", frecuency: 420 },
                    { word: "gracias", frecuency: 310 }
                ]
            },
            errors: []
        };

        navigate('/dashboard', { state: mockBackendResponse });
    };


    return (
        <>
            <div
                className={`${styles.uploadBox} ${isDragging ? styles.dragging : ''}`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
            >
                <div className={styles.iconContainer}>
                    <CloudUpload size={48} color="var(--color-text)" />
                </div>

                {!file ? (
                    <>
                        <div className={styles.textGroup}>
                            <h2 className="h4">Arrastra y suelta tu archivo aquí</h2>
                            <p className="text-body-sm">archivos soportados: .txt o .zip</p>
                        </div>

                        <button className="btn btn-primary" onClick={() => fileInputRef.current.click()}>
                            o selecciona un archivo
                        </button>
                    </>
                ) : (
                    <>
                        <div className={styles.textGroup}>
                            <h2 className="h4">Archivo seleccionado</h2>
                            <p className="text-body-sm">archivos soportados: .txt o .zip</p>
                        </div>

                        <div className={styles.fileInfoContainer}>
                            <FileText size={20} color="var(--color-text)" />
                            <span className={styles.fileName}>{file.name}</span>
                            <span className={styles.fileSize}>{formatFileSize(file.size)}</span>
                        </div>

                        <div className={styles.actions}>
                            <button className="btn btn-cancel" onClick={() => setFile(null)}>
                                Cancelar
                            </button>
                            {/* Combinamos clase global (btn) con clase de módulo (btnSuccess) */}
                            <button className={`btn ${styles.btnSuccess}`} onClick={handleAnalyze}>
                                Analizar archivo
                            </button>
                        </div>
                    </>
                )}

                <input
                    type="file"
                    ref={fileInputRef}
                    style={{ display: 'none' }}
                    accept=".txt,.zip"
                    onChange={handleFileSelect}
                />
            </div>

            <Modal 
                isOpen={errorModal.isOpen} 
                onClose={() => setErrorModal({ isOpen: false, message: '' })}
                title="Formato no soportado"
                message={errorModal.message}
                type="warning"
            />
        </>
    );
};

export default FileUploader;
