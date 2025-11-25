# Filtrer un QuerySet de ForeignKey dans un ModelForm avec Django

## 📚 Objectif pédagogique

Ce projet illustre une technique importante en Django : **comment filtrer dynamiquement les choix d'une ForeignKey dans un ModelForm en fonction de l'utilisateur connecté**, en utilisant une Class-Based View (CBV).

## 🎯 Cas d'usage

Imaginons une application de gestion de rendez-vous vétérinaires :
- Un utilisateur possède plusieurs animaux
- Lors de la création d'un rendez-vous, l'utilisateur doit choisir **uniquement parmi ses propres animaux**
- Sans filtrage, tous les animaux de tous les utilisateurs seraient visibles dans le formulaire !

## 🏗️ Architecture du projet

### 1. Les modèles (`pets/models.py`)

```python
class Animal(models.Model):
    breed = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    veterinarian = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # Lien avec le propriétaire

class Appointment(models.Model):
    date = models.DateTimeField()
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)  # Lien avec l'animal
    reason = models.CharField(max_length=200)
```

**Point clé** : `Appointment` a une ForeignKey vers `Animal`, et `Animal` a une ForeignKey vers `User`.

### 2. Le formulaire (`pets/forms.py`)

```python
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'animal', 'reason']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # 🎯 FILTRAGE : on ne montre que les animaux de l'utilisateur
            self.fields["animal"].queryset = Animal.objects.filter(owner=user)
```

**🔑 Technique utilisée** :
- On surcharge la méthode `__init__` du formulaire
- On accepte un paramètre `user` personnalisé
- On filtre le queryset du champ `animal` : `Animal.objects.filter(owner=user)`
- Résultat : le menu déroulant ne contient que les animaux de l'utilisateur

### 3. La vue (`pets/views.py`)

```python
class AppointmentCreateView(CreateView):
    form_class = AppointmentForm
    template_name = 'pets/appointment_form.html'
    success_url = reverse_lazy('home')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user  # 🚀 On passe l'utilisateur au formulaire
        return kwargs
```

**🔑 Technique utilisée** :
- On utilise une CBV (`CreateView`) qui gère automatiquement GET et POST
- On surcharge `get_form_kwargs()` pour injecter l'utilisateur connecté dans le formulaire
- `self.request.user` contient l'utilisateur courant
- On ajoute `user` aux kwargs, qui seront transmis au `__init__` du formulaire

## 💡 Pourquoi cette approche ?

### ✅ Solution élégante (bonne)
- **Séparation des responsabilités** : le formulaire gère le filtrage, la vue injecte les dépendances
- **Réutilisabilité** : le formulaire peut être utilisé avec différents utilisateurs
- **Testabilité** : on peut tester le formulaire indépendamment de la vue
- **Sécurité** : impossible de créer un rendez-vous pour l'animal d'un autre utilisateur