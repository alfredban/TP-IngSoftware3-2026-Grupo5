import { AlertTriangle, XCircle, CheckCircle, Info } from 'lucide-react';
import styles from './Modal.module.css';

const Modal = ({ isOpen, onClose, title, message, type = 'warning' }) => {
    if (!isOpen) return null;

    let Icon;
    let iconColorClass;
    let wrapperBorderColor;

    switch (type) {
        case 'error':
            Icon = XCircle;
            iconColorClass = 'text-error';
            wrapperBorderColor = 'rgba(248, 113, 113, 0.2)';
            break;
        case 'success':
            Icon = CheckCircle;
            iconColorClass = 'text-success';
            wrapperBorderColor = 'rgba(72, 187, 120, 0.2)';
            break;
        case 'info':
            Icon = Info;
            iconColorClass = 'text-info';
            wrapperBorderColor = 'rgba(98, 182, 203, 0.2)';
            break;
        case 'warning':
        default:
            Icon = AlertTriangle;
            iconColorClass = 'text-warning';
            wrapperBorderColor = 'rgba(236, 201, 75, 0.2)';
            break;
    }

    return (
        <div className={styles.modalOverlay} onClick={onClose}>
            <div className={styles.modalContent} onClick={(e) => e.stopPropagation()}>
                <div className={styles.iconWrapper} style={{ borderColor: wrapperBorderColor }}>
                    <Icon size={36} className={iconColorClass} />
                </div>
                
                <h3 className="h3" style={{ margin: '1rem 0 0.5rem 0', color: 'var(--color-text)' }}>
                    {title}
                </h3>
                
                <p className="text-body-md" style={{ color: 'var(--color-text-muted)', marginBottom: '2rem', textAlign: 'center', lineHeight: '1.5' }}>
                    {message}
                </p>
                
                <div className={styles.modalFooter}>
                    <button className="btn btn-primary" style={{ width: '100%' }} onClick={onClose}>
                        Entendido
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Modal;
