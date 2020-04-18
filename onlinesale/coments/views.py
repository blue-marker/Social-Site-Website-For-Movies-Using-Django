from django.contrib import messages
from django.contrib.contenttypes.models import ContentType

from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404

from .forms import ComentForm
from .models import Coment

def comment_thread(request,id):
    obj = get_object_or_404(Coment,id=id)
    # content_object= obj.content_object
    # content_id = obj.content_object.id

    initial_data = {"content_type": obj.content_type,"object_id": obj.object_id}  

    form = ComentForm(request.POST or None,initial=initial_data)
    # print(dir(form))
    # print(form.errors)
    if form.is_valid():
        print(form.cleaned_data)
        _,c_type = form.data.get("content_type").split('|')
        print(c_type.strip())
        content_type = ContentType.objects.get(model=c_type.strip())
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None
        
        if parent_id:
            parent_qs = Coment.objects.filter(id=parent_id)
            if parent_qs.exists():
                parent_obj = parent_qs.first()

        new_comment, created = Coment.objects.get_or_create(user=self.request.user,content_type=content_type,object_id=obj_id,content=content_data,parent=parent_obj)
    
    context={
        'comment':obj,
        'form':form,
    }
    return render(request,'coments/comment_thread.html',context)
