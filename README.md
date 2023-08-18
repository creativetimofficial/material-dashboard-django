-- git clone https://github.com/espinosa98/proyecto_GI.git

- cd proyecto_GI

- crear un entorno virtual: python3 -m venv venv

- activar el entorno virtual: source venv/bin/activate

- instalar las dependencias: pip install -r requirements.txt

- configurar bd con postgresql

- correr migraciones: python manage.py makemigrations

- correr migraciones: python manage.py migrate

- correr servidor: python manage.py runserver