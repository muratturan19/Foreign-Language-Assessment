from __future__ import annotations

import base64
import binascii
import logging
import smtplib
import ssl
from email.message import EmailMessage
from email.utils import make_msgid

from fastapi import HTTPException, status

from ..config import get_settings
from ..models import EmailRequest, EmailResponse

logger = logging.getLogger(__name__)


def _build_email_message(payload: EmailRequest, sender: str) -> EmailMessage:
    message = EmailMessage()
    message["Subject"] = payload.subject
    message["From"] = sender
    message["To"] = payload.to

    plain_body = payload.body
    message.set_content(plain_body)

    if payload.links:
        links_html = "".join(f'<li><a href="{link}">{link}</a></li>' for link in payload.links)
        html_body = f"<p>{payload.body}</p>"
        if links_html:
            html_body += f"<ul>{links_html}</ul>"
        message.add_alternative(html_body, subtype="html")

    if payload.attachments:
        print(f"\n[EMAILER] Building email with {len(payload.attachments)} attachment(s)")
        logger.info("Building email with %d attachment(s)", len(payload.attachments))
        for idx, attachment in enumerate(payload.attachments):
            try:
                print(f"[EMAILER] Processing attachment {idx+1}/{len(payload.attachments)}: {attachment.filename}")
                print(f"[EMAILER]   Type: {attachment.content_type}, Encoded size: {len(attachment.data)} bytes")
                logger.debug(
                    "Processing attachment %d/%d: %s (type: %s, encoded size: %d bytes)",
                    idx + 1,
                    len(payload.attachments),
                    attachment.filename,
                    attachment.content_type,
                    len(attachment.data),
                )
                file_bytes = base64.b64decode(attachment.data, validate=True)
                print(f"[EMAILER] Attachment {attachment.filename} decoded successfully, size: {len(file_bytes)} bytes")
                logger.debug(
                    "Attachment %s decoded successfully, size: %d bytes",
                    attachment.filename,
                    len(file_bytes),
                )
            except (binascii.Error, ValueError) as exc:
                logger.error(
                    "Failed to decode email attachment %s (type: %s, encoded size: %d): %s",
                    attachment.filename,
                    attachment.content_type,
                    len(attachment.data) if attachment.data else 0,
                    exc,
                )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid attachment provided: {attachment.filename}",
                ) from exc

            maintype, subtype = "application", "octet-stream"
            if "/" in attachment.content_type:
                parts = attachment.content_type.split("/", 1)
                maintype, subtype = parts[0], parts[1]

            message.add_attachment(
                file_bytes,
                maintype=maintype,
                subtype=subtype,
                filename=attachment.filename,
            )
            print(f"[EMAILER] ✅ Attachment {attachment.filename} added successfully ({maintype}/{subtype}, {len(file_bytes)} bytes)")
            logger.info(
                "Attachment %s added successfully (%s/%s, %d bytes)",
                attachment.filename,
                maintype,
                subtype,
                len(file_bytes),
            )

    return message


def send_email(payload: EmailRequest) -> EmailResponse:
    settings = get_settings()
    missing = settings.email.missing_fields()
    if missing:
        logger.warning("Email configuration missing fields: %s", ", ".join(missing))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Email service is not configured: missing {', '.join(missing)}",
        )

    logger.info(
        "Sending email to %s with subject '%s' and %d attachment(s)",
        payload.to,
        payload.subject,
        len(payload.attachments) if payload.attachments else 0,
    )

    try:
        message = _build_email_message(payload, sender=str(settings.email.default_sender))
    except Exception as exc:
        logger.exception("Failed to build email message: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to build email message: {str(exc)}",
        ) from exc

    context = ssl.create_default_context()

    try:
        logger.debug("Connecting to SMTP server %s:%d", settings.email.smtp_host, settings.email.smtp_port)
        if settings.email.smtp_port == 465:
            with smtplib.SMTP_SSL(settings.email.smtp_host, settings.email.smtp_port, context=context) as server:
                logger.debug("Logging in to SMTP server as %s", settings.email.smtp_username)
                server.login(settings.email.smtp_username, settings.email.smtp_password)
                logger.debug("Sending email message")
                server.send_message(message)
        else:
            with smtplib.SMTP(settings.email.smtp_host, settings.email.smtp_port) as server:
                logger.debug("Starting TLS")
                server.starttls(context=context)
                logger.debug("Logging in to SMTP server as %s", settings.email.smtp_username)
                server.login(settings.email.smtp_username, settings.email.smtp_password)
                logger.debug("Sending email message")
                server.send_message(message)
    except Exception as exc:  # pragma: no cover - network interaction
        logger.exception(
            "Failed to send email to %s via %s:%d - Error: %s",
            payload.to,
            settings.email.smtp_host,
            settings.email.smtp_port,
            exc,
        )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Failed to send email: {str(exc)}",
        ) from exc

    message_id = make_msgid(domain=settings.email.smtp_host)
    logger.info("Email sent successfully to %s with message_id %s", payload.to, message_id)
    return EmailResponse(status="sent", message_id=message_id)
