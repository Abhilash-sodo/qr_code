from django.shortcuts import render
from .forms import QrCodeForm
import qrcode
import os
from django.conf import settings


def generate_qr_code(request):
    if request.method == 'POST':
        form = QrCodeForm(request.POST)
        if form.is_valid():
            res_name = form.cleaned_data['restaurant_name']
            url = form.cleaned_data['url']
            # return render(request,'qr_code.html',{'res_name':res_name,'url':url})
        
            # Generate QR Code
            qr = qrcode.make(url)
            file_name = res_name.replace( ' ', '_').lower() + '_menu.png'
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            qr.save(file_path)
            
            #Create a image url
            image_url = os.path.join(settings.MEDIA_URL, file_name)
            context = {
                "res_name"  : res_name,
                "image_url": image_url,
                "file_name": file_name,
            }
            return render(request, 'qr_result.html', context)  
    else:  
        form = QrCodeForm()
        context = {
            'form': form,
            }
        return render(request,'generate_qr_code.html',context)