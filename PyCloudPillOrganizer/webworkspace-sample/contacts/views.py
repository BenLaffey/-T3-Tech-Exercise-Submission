from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Contact
from .forms import ContactForm

def front_page(request):
    return render(request, "index.html")
    # return render(request, "index_css.html")


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
    name = request.GET.get("name", "").strip()
    phone = request.GET.get("phone", "").strip()

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        # Reset to first page on new search
        page_number = 1

    if name or phone:
        contacts = Contact.objects.filter(
            name__icontains=name, phone__icontains=phone
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
         "name_query": name,
         "phone_query": phone},
    )

def edit_contact(request, contact_id, page_number):
    pn = request.GET.get("page", page_number)
    print(f"[DBG] edit_contact {contact_id}, {page_number}, {pn} <<<")
    success = False

    if request.method == "POST":
        contact = Contact.objects.get(id=contact_id)
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        if contact.name != name or contact.phone != phone:
            contact.name = name
            contact.phone = phone
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
