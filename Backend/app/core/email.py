import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

logger = logging.getLogger(__name__)


def send_reset_password_email(recipient_email: str, recipient_name: str, username: str, new_password: str) -> bool:
    """
    Sends an HTML formatted reset password email to the target user
    using SMTP credentials configured in .env (SMTP_HOST, SMTP_PORT, SMTP_USER, etc.).
    """
    if not recipient_email or "@" not in recipient_email:
        logger.warning(f"Email tidak dikirim: Alamat email '{recipient_email}' tidak valid untuk user '{username}'.")
        return False

    smtp_host = settings.SMTP_HOST
    smtp_port = settings.SMTP_PORT
    smtp_user = settings.SMTP_USER
    smtp_password = settings.SMTP_PASSWORD
    from_email = settings.EMAILS_FROM_EMAIL or f"{smtp_user}@{smtp_host}"

    subject = f"SIMLABA Kota Tegal - Reset Password Akun ({username})"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: 'Plus Jakarta Sans', Arial, sans-serif; background-color: #f8f8f4; color: #1e293b; margin: 0; padding: 20px; }}
            .container {{ max-width: 580px; margin: 0 auto; background: #ffffff; border-radius: 16px; padding: 32px; border: 2px solid #e2e8f0; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }}
            .header {{ text-align: center; border-bottom: 2px solid #308e87; padding-bottom: 16px; margin-bottom: 24px; }}
            .brand {{ font-size: 20px; font-weight: 900; color: #308e87; letter-spacing: -0.5px; }}
            .badge {{ display: inline-block; background: #308e87; color: #ffffff; font-size: 10px; font-weight: 800; padding: 2px 8px; border-radius: 4px; uppercase; margin-left: 6px; }}
            .content {{ font-size: 14px; line-height: 1.6; color: #334155; }}
            .password-box {{ background: #0f172a; color: #34d399; font-family: monospace; font-size: 24px; font-weight: bold; text-align: center; padding: 16px; border-radius: 12px; letter-spacing: 3px; margin: 20px 0; border: 2px solid #10b981; }}
            .footer {{ text-align: center; font-size: 11px; color: #94a3b8; margin-top: 28px; border-top: 1px solid #f1f5f9; padding-top: 16px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <span class="brand">SIMLABA</span><span class="badge">Kota Tegal</span>
                <p style="margin: 4px 0 0 0; font-size: 11px; color: #64748b; font-weight: 600;">Sistem Informasi Laporan Perkembangan Pembangunan</p>
            </div>
            <div class="content">
                <p>Yth. <strong>{recipient_name or username}</strong>,</p>
                <p>Password untuk akun SIMLABA Anda (<strong>{username}</strong>) telah di-reset secara otomatis oleh Administrator System.</p>
                <p>Berikut adalah password baru Anda (8 Karakter Acak):</p>
                
                <div class="password-box">{new_password}</div>

                <p style="font-size: 12px; color: #64748b;">
                    ⚠️ Demi keamanan, harap segera masuk dan perbarui password Anda secara berkala pada aplikasi SIMLABA.
                </p>
            </div>
            <div class="footer">
                &copy; 2026 Pemerintah Kota Tegal — Bapperida Kota Tegal<br/>
                Pesan otomatis ini dikirim melalui server SMTP {smtp_host}.
            </div>
        </div>
    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = recipient_email
    msg.attach(MIMEText(html_content, "html"))

    try:
        if settings.SMTP_SSL or smtp_port == 465:
            with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=10) as server:
                if smtp_user and smtp_password:
                    server.login(smtp_user, smtp_password)
                server.sendmail(from_email, [recipient_email], msg.as_string())
        else:
            with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
                if settings.SMTP_TLS:
                    server.starttls()
                if smtp_user and smtp_password:
                    server.login(smtp_user, smtp_password)
                server.sendmail(from_email, [recipient_email], msg.as_string())

        logger.info(f"Email reset password berhasil dikirim ke {recipient_email} via SMTP ({smtp_host}:{smtp_port})")
        return True
    except Exception as e:
        logger.error(f"Gagal mengirim email reset password ke {recipient_email} via SMTP ({smtp_host}:{smtp_port}): {str(e)}")
        try:
            with smtplib.SMTP(smtp_host, 25, timeout=5) as server:
                if smtp_user and smtp_password:
                    try:
                        server.login(smtp_user, smtp_password)
                    except Exception:
                        pass
                server.sendmail(from_email, [recipient_email], msg.as_string())
            logger.info(f"Email reset password berhasil dikirim via fallback port 25 ke {recipient_email}")
            return True
        except Exception as fallback_err:
            logger.error(f"Fallback SMTP port 25 juga gagal: {str(fallback_err)}")
            return False
