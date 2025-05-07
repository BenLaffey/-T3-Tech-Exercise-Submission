from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Contact
from .forms import ContactForm

def front_page(request):
    return render(request, "index_css.html")
    # return render(request, "index.html")


def add_contact(request):
    success = False
    added_contact = None
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            new_contact = form.save()
            success = True
            added_contact = new_contact
            return render(
                request,
                "add_contact_css.html", # "add_contact_css.html",
                {"form": form,
                 "added_contact": added_contact,
                 "success": success},
            )
    else:
        form = ContactForm()
    return render(
        request,
        "add_contact_css.html", # "add_contact_css.html",
        {"form": form,
         "added_contact": added_contact,
         "success": success},
    )


def search_contact(request):
    page_number = request.GET.get("page", 1)
    medication_name = request.GET.get("medication_name", "").strip()
    administration_notes = request.GET.get("administration_notes", "").strip()
    usage_time = request.GET.get("usage_time", "").strip()
    usage_importance = request.GET.get("usage_importance", "").strip()

    if request.method == "POST":
        medication_name = request.POST.get("medication_name", "").strip()
        administration_notes = request.POST.get("administration_notes", "").strip()
        usage_time = request.POST.get("usage_time", "").strip()
        usage_importance = request.POST.get("usage_importance", "").strip()
        # Reset to first page on new search
        page_number = 1

    if medication_name or administration_notes or usage_time or usage_importance:
        contacts = Contact.objects.filter(
            medication_name__icontains=medication_name, administration_notes__icontains=administration_notes, usage_time__icontains=usage_time, usage_importance__icontains=usage_importance
        ).order_by("id")  # Order by name to ensure consistency
    else:
        contacts = Contact.objects.all().order_by("id")  # Order the results

    paginator = Paginator(contacts, 10)
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "search_contact_css.html",
        # "search_contact.html",
        {"contacts": page_obj,
         "medication_name_query": medication_name,
         "administration_notes_query": administration_notes,
         "usage_time_query": usage_time,
	 "usage_importance_query": usage_importance},
    )

def edit_contact(request, contact_id, page_number):
    pn = request.GET.get("page", page_number)
    print(f"[DBG] edit_contact {contact_id}, {page_number}, {pn} <<<")
    success = False

    if request.method == "POST":
        contact = Contact.objects.get(id=contact_id)
        medication_name = request.POST.get("medication_name")
        administration_notes = request.POST.get("administration_notes")
        usage_time = request.POST.get("usage_time")
        usage_importance = request.POST.get("usage_importance")
        if contact.medication_name != medication_name or contact.administration_notes != administration_notes or contact.usage_time != usage_time or contact.usage_importance != usage_importance:
            contact.medication_name = medication_name
            contact.administration_notes = administration_notes
            contact.usage_time = usage_time
            contact.usage_importance = usage_importance
            contact.save()
            success = True

    contact_list = Contact.objects.all()
    paginator = Paginator(contact_list, 10)
    page_number = request.POST.get(
        "page", request.GET.get("page", page_number)
    )
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        # "edit_contact.html",
        "edit_contact_css.html",
        {
            "contacts": page_obj,
            "success": success,
            "updated_contact_id": contact_id,
        },
    )


def delete_contact(request, contact_id, page_number):
    print("[DBG] delete_contact called for ID:", contact_id)
    if request.method == "POST":
        contact = get_object_or_404(Contact, id=contact_id)
        contact.delete()
        # Redirect to the same page number after delete
        return redirect("edit_contact", contact_id=contact_id, page_number=page_number)
