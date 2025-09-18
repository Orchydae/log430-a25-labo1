"""
Store manager application
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from views.user_view import UserView
from views.product_view import ProductView

if __name__ == '__main__':
    while True:
        print("===== LE MAGASIN DU COIN =====")
        print("1. Utilisateurs")
        print("2. Produits")
        print("3. Quitter")
        choice = input("Choisissez une option: ").strip()

        if choice == "1":
            UserView.show_options()
        elif choice == "2":
            ProductView.show_options()
        elif choice == "3":
            print("Ciao bella!")
            break
        else:
            print("Option invalide.")