from app import app
from models import db, User, People, Planet, Favorite

def run_seed():
    with app.app_context():
        print("🌱 Iniciando la siembra de la base de datos...")

        # 1. Limpiar datos existentes (Opcional pero recomendable para evitar duplicados)
        db.session.query(Favorite).delete()
        db.session.query(People).delete()
        db.session.query(Planet).delete()
        db.session.query(User).delete()
        db.session.commit()

        # 2. Crear Usuarios
        user1 = User(email="luke@skywalker.com", password="password123", is_active=True)
        user2 = User(email="vader@empire.com", password="darkside123", is_active=True)
        
        db.session.add_all([user1, user2])
        db.session.commit()
        print("✅ Usuarios creados.")

        # 3. Crear Personajes (People)
        person1 = People(name="Luke Skywalker", gender="male", height="172", eye_color="blue")
        person2 = People(name="Darth Vader", gender="male", height="202", eye_color="yellow")
        person3 = People(name="Leia Organa", gender="female", height="150", eye_color="brown")

        db.session.add_all([person1, person2, person3])
        db.session.commit()
        print("✅ Personajes creados.")

        # 4. Crear Planetas (Planet)
        planet1 = Planet(name="Tatooine", climate="arid")
        planet2 = Planet(name="Alderaan", climate="temperate")
        planet3 = Planet(name="Hoth", climate="frozen")

        db.session.add_all([planet1, planet2, planet3])
        db.session.commit()
        print("✅ Planetas creados.")

        # 5. Crear Favoritos (Favorite)
        fav1 = Favorite(user_id=user1.id, people_id=person1.id)
        fav2 = Favorite(user_id=user1.id, planet_id=planet1.id)
        fav3 = Favorite(user_id=user2.id, people_id=person2.id)

        db.session.add_all([fav1, fav2, fav3])
        db.session.commit()
        print("✅ Favoritos asociados.")

        print("🎉 ¡Semilla ejecutada con éxito!")

if __name__ == "__main__":
    run_seed()