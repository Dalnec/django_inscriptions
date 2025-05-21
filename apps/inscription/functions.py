import mimetypes
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string

def send_voucher_email(group, to_email):
    subject = 'Registro de Inscripción'
    from_email = 'dalnec1405@gmail.com'
    # to_email = ['daleonco_1995@hotmail.com']

    context = {
        'group': {
            'code': group.vouchergroup,
            'activity': group.activity.title,
            'date': group.created
        },
        'inscriptions': group.fk_InscriptionGroup.all(),
        'tarifa': group.tarifa.description,
        'payment_method': group.paymentmethod.description,
        'total_amount': group.voucheramount
    }


    # email = EmailMessage(subject, body, from_email, to_email)
    text_content = 'Gracias por su inscripción. Adjuntamos el resumen y voucher.'
    html_content = render_to_string('email_inscription.html', context)

    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, "text/html")

    if group.voucherfile:
        mime_type, _ = mimetypes.guess_type(group.voucherfile.name)
        email.attach(
            group.voucherfile.name.split('/')[-1],
            group.voucherfile.read(),
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