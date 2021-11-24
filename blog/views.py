from django.shortcuts import render, redirect, get_object_or_404
from .forms import MoveForm
from .models import Equipement, Animal


# Create your views here.
def animal_list(request):
    animaux = Animal.objects.all()
    equipements = Equipement.objects.all()
    return render(request, 'blog/animal_list.html', {'animaux': animaux,
                                                     'equipements': equipements})


def animal_detail(request, id_animal):
    animal = get_object_or_404(Animal, id_animal=id_animal)
    equipement = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
    message = ''
    if request.method == "POST":

        form = MoveForm(request.POST, instance=animal)
        equipement.disponibilite = "libre"
        equipement.save()
        form.save(commit=False)
        nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)

        ## Vérification de la disponibilité du nouvel équipement ##
        if nouveau_lieu.disponibilite == 'occupé':
            form = MoveForm()
            message = "L'équipement choisi n'est pas disponible"
            return render(request,
                          'blog/animal_detail.html',
                          {'animal': animal, 'form': form, 'message': message})

        ## Vérification de la possibilité des changements choisi en fonction de l'état initial de l'animal ##
        if animal.etat == 'affamé' and animal.lieu.id_equip != 'mangeoire':
            form = MoveForm()
            message = f"{id_animal} est affamé et ne peut pas se rendre dans {animal.lieu.id_equip}"
            return render(request,
                          'blog/animal_detail.html',
                          {'animal': animal, 'form': form, 'message': message})

        if animal.etat == 'repus' and animal.lieu.id_equip != 'roue':
            form = MoveForm()
            message = f"{id_animal} est repus et ne peut pas se rendre dans {animal.lieu.id_equip}"
            return render(request,
                          'blog/animal_detail.html',
                          {'animal': animal, 'form': form, 'message': message})

        if animal.etat == 'fatigué' and animal.lieu.id_equip != 'nid':
            form = MoveForm()
            message = f"{id_animal} est fatigué et ne peut pas se rendre dans {animal.lieu.id_equip}"
            return render(request,
                          'blog/animal_detail.html',
                          {'animal': animal, 'form': form, 'message': message})

        if animal.etat == 'endormi' and animal.lieu.id_equip != 'litière':
            form = MoveForm()
            message = f"{id_animal} est endormi et ne peut pas se rendre dans {animal.lieu.id_equip}"
            return render(request,
                          'blog/animal_detail.html',
                          {'animal': animal, 'form': form, 'message': message})

        ## Changement de l'état de l'animal ##
        if animal.lieu.id_equip != 'litière':
            nouveau_lieu.disponibilite = "occupé"

        if animal.lieu.id_equip == 'mangeoire':
            animal.etat = 'repus'

        if animal.lieu.id_equip == 'nid':
            animal.etat = 'endormi'

        if animal.lieu.id_equip == 'litière':
            animal.etat = 'affamé'

        if animal.lieu.id_equip == 'roue':
            animal.etat = 'fatigué'

        nouveau_lieu.save()
        animal.save()
        return redirect('animal_list')


    else:
        form = MoveForm()
        return render(request,
                      'blog/animal_detail.html',
                      {'animal': animal, 'form': form, 'message': message})
