import mimetypes
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string

def send_voucher_email(inscription_group, to_email):
    subject = 'Registro de Inscripción'
    body = 'Adjuntamos el comprobante de inscripción.'
    from_email = 'dalnec1405@gmail.com'
    # to_email = ['daleonco_1995@hotmail.com']

    context = {
        'group': {
            'code': inscription_group.vouchergroup,
            'activity': inscription_group.activity.title,
            'date': inscription_group.created
        },
        'inscriptions': inscription_group.fk_InscriptionGroup.all(),
        'tarifa': inscription_group.tarifa.description,
        'payment_method': inscription_group.paymentmethod.description,
        'total_amount': inscription_group.voucheramount
    }


    # email = EmailMessage(subject, body, from_email, to_email)
    text_content = 'Gracias por su inscripción. Adjuntamos el resumen y voucher.'
    html_content = render_to_string('email_inscription.html', context)

    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, "text/html")

    if inscription_group.voucherfile:
        mime_type, _ = mimetypes.guess_type(inscription_group.voucherfile.name)
        email.attach(
            inscription_group.voucherfile.name.split('/')[-1],
            inscription_group.voucherfile.read(),
            mime_type or 'application/octet-stream'
        )
    
    email.send()

def email_sender(subject='Inscripción', body=None, from_email='dalnec1405@gmail.com', to_email=['daleonco_1995@hotmail.com']):
        email = EmailMessage(
            subject,
            "body",
            from_email,
            to_email,
            # attachments=[
            #     (self.filename, output.getvalue(), 'application/vnd.ms-excel')
            # ]
        )
        email.send()