from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


def worker_email(id):
    url = f"http://127.0.0.1:8000/admin/clue/workerresult/{id}/change/"
    context = {
        "url": url,
    }
    html_content = render_to_string("worker-email.html", context=context).strip()

    subject = "Worker task completed."
    recipients = ["rayiszafar@gmail.com"]
    reply_to = ["noreply@worker.com"]
    msg = EmailMultiAlternatives(
        subject,
        html_content,
        "rayiszafar@gmail.com",
        recipients,
        reply_to=reply_to,
    )
    msg.content_subtype = "html"
    msg.mixed_subtype = "related"
    msg.send()
    return True
