from django.http.request import QueryDict
from django.shortcuts import render, HttpResponse
from django.http import HttpResponse
from AppCoder.models import Curso, Profesor, Estudiante , Entregable
from AppCoder.forms import CursoFormulario, ProfesorFormulario, EstudianteFormulario , EntregableFormulario

# Create your views here.

def curso(request):

      curso =  Curso(nombre="Desarrollo web", camada="19881")
      curso.save()
      documentoDeTexto = f"--->Curso: {curso.nombre}   Camada: {curso.camada}"


      return HttpResponse(documentoDeTexto)


def inicio(request):

      return render(request, "AppCoder/inicio.html")




def entregables(request):

      return render(request, "AppCoder/entregables.html")


def cursos(request):

      if request.method == 'POST':

            miFormulario = CursoFormulario(request.POST) #aquí mellega toda la información del html

            print(miFormulario)

            if miFormulario.is_valid:   #Si pasó la validación de Django

                  informacion = miFormulario.cleaned_data

                  curso = Curso (nombre=informacion['curso'], camada=informacion['camada']) 

                  curso.save()

                  return render(request, "AppCoder/inicio.html") #Vuelvo al inicio o a donde quieran

      else: 

            miFormulario= CursoFormulario() #Formulario vacio para construir el html

      return render(request, "AppCoder/cursos.html", {"miFormulario":miFormulario})




def profesores(request):

      if request.method == 'POST':

            miFormulario = ProfesorFormulario(request.POST) #aquí mellega toda la información del html

            print(miFormulario)

            if miFormulario.is_valid:   #Si pasó la validación de Django

                  informacion = miFormulario.cleaned_data

                  profesor = Profesor (nombre=informacion['nombre'], apellido=informacion['apellido'],
                   email=informacion['email'], profesion=informacion['profesion']) 

                  profesor.save()

                  return render(request, "AppCoder/inicio.html") #Vuelvo al inicio o a donde quieran

      else: 

            miFormulario= ProfesorFormulario() #Formulario vacio para construir el html

      return render(request, "AppCoder/profesores.html", {"miFormulario":miFormulario})






def buscar(request):

      if  request.GET["camada"]:

	      #respuesta = f"Estoy buscando la camada nro: {request.GET['camada'] }" 
            camada = request.GET['camada'] 
            cursos = Curso.objects.filter(camada__icontains=camada)

            return render(request, "AppCoder/inicio.html", {"cursos":cursos, "camada":camada})

      else: 

	      respuesta = "No enviaste datos"

      #No olvidar from django.http import HttpResponse
      return HttpResponse(respuesta)




def leerProfesores(request):

      profesores = Profesor.objects.all() #trae todos los profesores

      contexto= {"profesores":profesores} 

      return render(request, "AppCoder/leerProfesores.html",contexto)



def eliminarProfesor(request, profesor_nombre):

    profesor = Profesor.objects.get(nombre=profesor_nombre)
    profesor.delete()

    # vuelvo al menú
    profesores = Profesor.objects.all()  # trae todos los profesores

    contexto = {"profesores": profesores}

    return render(request, "AppCoder/leerProfesores.html", contexto)


def editarProfesor(request, profesor_nombre):

    # Recibe el nombre del profesor que vamos a modificar
    profesor = Profesor.objects.get(nombre=profesor_nombre)

    # Si es metodo POST hago lo mismo que el agregar
    if request.method == 'POST':

        # aquí mellega toda la información del html
        miFormulario = ProfesorFormulario(request.POST)

        print(miFormulario)

        if miFormulario.is_valid:  # Si pasó la validación de Django

            informacion = miFormulario.cleaned_data

            profesor.nombre = informacion['nombre']
            profesor.apellido = informacion['apellido']
            profesor.email = informacion['email']
            profesor.profesion = informacion['profesion']

            profesor.save()

            # Vuelvo al inicio o a donde quieran
            return render(request, "AppCoder/inicio.html")
    # En caso que no sea post
    else:
        # Creo el formulario con los datos que voy a modificar
        miFormulario = ProfesorFormulario(initial={'nombre': profesor.nombre, 'apellido': profesor.apellido,
                                                   'email': profesor.email, 'profesion': profesor.profesion})

    # Voy al html que me permite editar
    return render(request, "AppCoder/editarProfesor.html", {"miFormulario": miFormulario, "profesor_nombre": profesor_nombre})


from django.views.generic import ListView

class CursoList(ListView):

    model = Curso
    template_name = "AppCoder/cursos_list.html"


from django.views.generic.detail import DetailView


class CursoDetalle(DetailView):

    model = Curso
    template_name = "AppCoder/curso_detalle.html"
    
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

class CursoCreacion(CreateView):

    model = Curso
    success_url = "/AppCoder/curso/list"
    fields = ['nombre', 'camada']

from django.views.generic.edit import UpdateView

class CursoUpdate(UpdateView):

    model = Curso
    success_url = "/AppCoder/curso/list"
    fields = ['nombre', 'camada']


from django.views.generic.edit import DeleteView

class CursoDelete(DeleteView):

    model = Curso
    success_url = "/AppCoder/curso/list"



def estudiantes(request):

      if request.method == 'POST':

            miFormulario = EstudianteFormulario(request.POST) #aquí mellega toda la información del html

            print(miFormulario)

            if miFormulario.is_valid:   #Si pasó la validación de Django

                  informacion = miFormulario.cleaned_data

                  estudiante = Estudiante (nombre=informacion['nombre'], apellido=informacion['apellido'],
                   email=informacion['email']) 

                  estudiante.save()

                  return render(request, "AppCoder/inicio.html") #Vuelvo al inicio o a donde quieran

      else: 

            miFormulario= EstudianteFormulario() #Formulario vacio para construir el html

      return render(request, "AppCoder/estudiantes.html", {"miFormulario":miFormulario})


def leerEstudiantes(request):

      estudiantes = Estudiante.objects.all() #trae todos los profesores

      contexto= {"estudiantes": estudiantes} 

      return render(request, "AppCoder/leerEstudiantes.html",contexto)



def eliminarEstudiante(request, estudiante_nombre):

    estudiante = Estudiante.objects.get(nombre=estudiante_nombre)
    estudiante.delete()

    # vuelvo al menú
    estudiantes = Estudiante.objects.all()  # trae todos los estudiantes

    contexto = {"estudiantes": estudiantes}

    return render(request, "AppCoder/leerEstudiantes.html", contexto)




def editarEstudiante(request, estudiante_nombre):

    # Recibe el nombre del estudiante que vamos a modificar
    estudiante = Estudiante.objects.get(nombre=estudiante_nombre)

    # Si es metodo POST hago lo mismo que el agregar
    if request.method == 'POST':

        # aquí mellega toda la información del html
        miFormulario = EstudianteFormulario(request.POST)

        print(miFormulario)

        if miFormulario.is_valid:  # Si pasó la validación de Django

            informacion = miFormulario.cleaned_data

            estudiante.nombre = informacion['nombre']
            estudiante.apellido = informacion['apellido']
            estudiante.email = informacion['email']
            

            estudiante.save()

            # Vuelvo al inicio o a donde quieran
            return render(request, "AppCoder/inicio.html")
    # En caso que no sea post
    else:
        # Creo el formulario con los datos que voy a modificar
        miFormulario = EstudianteFormulario(initial={'nombre': estudiante.nombre, 'apellido': estudiante.apellido,
                                                   'email': estudiante.email})

    # Voy al html que me permite editar
    return render(request, "AppCoder/editarEstudiante.html", {"miFormulario": miFormulario, "estudiante_nombre": estudiante_nombre})


def entregables(request):

      if request.method == 'POST':

            miFormulario = EntregableFormulario(request.POST) #aquí mellega toda la información del html

            print(miFormulario)

            if miFormulario.is_valid:   #Si pasó la validación de Django

                  informacion = miFormulario.cleaned_data

                  entregable = Entregable (nombre=informacion['nombre'], fechaDeEntrega=informacion['fechaDeEntrega'], entregado = informacion['entregado']) 

                  entregable.save()

                  return render(request, "AppCoder/inicio.html") #Vuelvo al inicio o a donde quieran

      else: 

            miFormulario= EntregableFormulario() #Formulario vacio para construir el html

      return render(request, "AppCoder/entregables.html", {"miFormulario":miFormulario})


def leerEntregables(request):

      entregables = Entregable.objects.all() #trae todos los entregables

      contexto= {"entregables": entregables} 

      return render(request, "AppCoder/leerEntregables.html",contexto)



def eliminarEntregable(request, entregable_nombre):

    entregable = Entregable.objects.get(nombre=entregable_nombre)
    entregable.delete()

    # vuelvo al menú
    entregables = Entregable.objects.all()  # trae todos los entregables

    contexto = {"entregables": entregables}

    return render(request, "AppCoder/leerEntregables.html", contexto)




def editarEntregable(request, entregable_nombre):

    # Recibe el nombre del entregable que vamos a modificar
    entregable = Entregable.objects.get(nombre=entregable_nombre)

    # Si es metodo POST hago lo mismo que el agregar
    if request.method == 'POST':

        # aquí mellega toda la información del html
        miFormulario = EntregableFormulario(request.POST)

        print(miFormulario)

        if miFormulario.is_valid:  # Si pasó la validación de Django

            informacion = miFormulario.cleaned_data

            entregable.nombre = informacion['nombre']
            entregable.fechaDeEntrega = informacion['fechaDeEntrega']
            entregable.entregado = informacion['entregado']
            

            entregable.save()

            # Vuelvo al inicio o a donde quieran
            return render(request, "AppCoder/inicio.html")
    # En caso que no sea post
    else:
        # Creo el formulario con los datos que voy a modificar
        miFormulario = EntregableFormulario(initial={'nombre': entregable.nombre, 'fechaDeEntrega': entregable.fechaDeEntrega,
                                                   'entregado': entregable.entregado})

    # Voy al html que me permite editar
    return render(request, "AppCoder/editarEntregable.html", {"miFormulario": miFormulario, "entregable_nombre": entregable_nombre})