from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .forms import ReportForm, PatientForm
from .models import Patient


class HomePageView(TemplateView):
    template_name = 'uploadApp/home.html'


class UploadPageView(TemplateView):
    template_name = 'uploadApp/upload.html'


class ReportPageView(TemplateView):
    template_name = 'uploadApp/report.html'


# model = torch.device("cpu")
# model = torch.load(settings.ML_PATH)
# model.eval()


@login_required
def upload(request):
    form = PatientForm()

    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            print('FORM VALID')
            patient = form.save(commit=False)
            patient.doctor = request.user
            patient.save()
        context = {'form': form, 'patient': patient, 'hospital': request.user.hospital}
        return render(request, 'uploadApp/upload.html', context)

    if request.method == 'GET':
        context = {'form': form, 'hospital': request.user.hospital}
        return render(request, 'uploadApp/upload.html', context)


# def index(request):
#     image_uri = None
#     predicted_label = None
#
#     if request.method == 'POST':
#
#         form = ImageUploadForm(request.POST, request.FILES)
#
#         if form.is_valid():
#             image = form.cleaned_data['image']
#             image_bytes = image.file.read()
#             encoded_img = base64.b64encode(image_bytes).decode('ascii')
#             image_uri = 'data:%s;base64,%s' % ('image/jpeg', encoded_img)
#
#             try:
#                 predicted_label = get_prediction(image_bytes)
#             except RuntimeError as re:
#                 print(re)
#
#     else:
#         form = ImageUploadForm()
#
#     context = {
#         'form': form,
#         'image_uri': image_uri,
#         'predicted_label': predicted_label,
#     }
#     return render(request, 'image_classification/index.html', context)


@login_required
def report(request):
    reportForm = ReportForm()

    if request.method == 'GET':
        patients = Patient.objects.filter(doctor=request.user)
        return render(request, 'uploadApp/report.html',
                      {'patients': patients, 'reportForm': reportForm, 'hospital': request.user.hospital})


@login_required
def comment(request, id):
    if request.method == 'POST':
        patientScan = Patient.objects.get(pk=id)
        doctor = request.user
        form = ReportForm(request.POST)

        if form.is_valid():
            print('FORM VALID')
            comment = form.save(commit=False)
            comment.doctor = doctor
            comment.patientScan = patientScan
            comment.save()
        return redirect('report')


def page404(request, exception):
    return render(request, '404.html')
