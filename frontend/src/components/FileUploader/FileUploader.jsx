import { useNavigate } from 'react-router-dom';
import { useState, useRef } from 'react';
import { CloudUpload, FileText } from 'lucide-react';
import { Modal } from '../../components';
import styles from './FileUploader.module.css';

const FileUploader = () => {
    const navigate = useNavigate();
    const [file, setFile] = useState(null);
    const [isDragging, setIsDragging] = useState(false);
    const [errorModal, setErrorModal] = useState({ isOpen: false, title: '', message: '', type: 'warning' });
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
                setErrorModal({ isOpen: true, type: 'warning', title: "Archivo no compatible", message: "Solo se permite subir un archivo .txt o .zip" });
            }
        }
    };

    const handleFileSelect = (e) => {
        const selectedFile = e.target.files[0];

        if (selectedFile) {
            if (isValidFile(selectedFile)) {
                setFile(selectedFile);
            } else {
                setErrorModal({ isOpen: true, type: 'warning', title: "Archivo no compatible", message: "Solo se permite subir un archivo .txt o .zip" });
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

    const handleAnalyze = async () => {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const res = await fetch('http://localhost:8000/api/upload', {
                method: 'POST',
                body: formData,
            });

            const data = await res.json();

            if (!res.ok || data.errors?.length > 0) {
                const mensajeError = data.errors?.[0]?.info || 'Error al procesar el archivo';
                const tituloError = data.errors?.[0]?.error || 'Error';
                setErrorModal({ isOpen: true, type: 'error', title: tituloError, message: mensajeError });
                return;
            }

            navigate('/dashboard', { state: data });

        } catch (err) {
            setErrorModal({ isOpen: true, type: 'error', title: 'Error de conexión', message: <>No se pudo conectar con el servidor.<br />Intente de nuevo mas tarde</> });
        }
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
                onClose={() => setErrorModal({ isOpen: false, title: '', message: '', type: 'warning' })}
                title={errorModal.title}
                message={errorModal.message}
                type={errorModal.type}
            />
        </>
    );
};

export default FileUploader;
