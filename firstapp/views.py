from django.http import HttpResponse

from django.shortcuts import render
from .forms import ImageForm
 
def products(request, productid):
    output = "<h2>Product № {0}</h2>".format(productid)
    return HttpResponse(output)
 
def users(request, id, name):

    localV =123+78

    output = """<h2>   Пользователь: {1}, 
			 id: {0}  local: {2} </h2>""".format(id, name,localV-1)
    return HttpResponse(output)


def image_upload_view(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            imf = 'img/' + form.instance.image.name
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance

            import numpy as np
            from tensorflow import keras

            className=['Пакет','Мяч','Банан','Подшипник','Банка','Конверт','Бутылка','Деньги','Флакон','Игрушка']
            model=keras.models.load_model('mmga3.h5')
            img = np.array(keras.preprocessing.image.load_img(imf, target_size=(71,71))).astype('float32')/255
            classIndex = np.argmax(model(img.reshape(1,71,71,3)))
            
            img_obj.title = 'Класс: '+ className[classIndex]
            
            return render(request, 'index.html', {'form': form, 'img_obj': img_obj})
    else:
        form = ImageForm()
    return render(request, 'index.html', {'form': form})
