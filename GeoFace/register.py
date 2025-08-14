from modules.face_recognition import register_face
from modules.database import init_db

def main():
    init_db()
    name = input("Enter employee name: ")
    img_path = register_face(name)
    print(f"Successfully registered {name}!")

if __name__ == "__main__":
    main()