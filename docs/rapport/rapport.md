> 💡 Question 1 : Quelles commandes avez-vous utilisées pour effectuer les opérations UPDATE et DELETE dans MySQL ? Avez-vous uniquement utilisé Python ou également du SQL ? Veuillez inclure le code pour illustrer votre réponse.
- UPDATE:
  ```sql
  UPDATE users SET name = %s, email = %s WHERE id = %s
  ```
- DELETE:
  ```sql
  DELETE FROM users WHERE id = %s
  ```
Ce sont des commandes SQL standard exécutées via Python avec mysql.connector. Ainsi, j'ai utilisé le langage Python et SQL: Python pour la connexion, la transaction et le passage de paramètres et SQL pour exprimer les opérations UPDATE et DELETE.

- CODE:
  ```
  def update(self, user) -> int:
        """ Update given user in MySQL 
        Returns number of affected rows
        """
        if not hasattr(user, 'id') or user.id is None:
            raise ValueError("User ID is required for update operation.")
        sql = "UPDATE users SET name = %s, email = %s WHERE id = %s"
        try:
            self.cursor.execute(sql, (user.name, user.email, user.id))
            self.conn.commit()
            return self.cursor.rowcount
        except Exception:
            self.conn.rollback()
            raise

    def delete(self, user_id) -> int:
        """ Delete user from MySQL with given user ID 
        Returns number of affected rows
        """
        sql = "DELETE FROM users WHERE id = %s"
        try:
            self.cursor.execute(sql, (user_id,))
            self.conn.commit()
            return self.cursor.rowcount
        except Exception:
            self.conn.rollback()
            raise

> 💡 Question 2 : Quelles commandes avez-vous utilisées pour effectuer les opérations dans MongoDB ? Avez-vous uniquement utilisé Python ou également du SQL ? Veuillez inclure le code pour illustrer votre réponse.

Aucun SQL a été utilisé pour les opérations MongoDB. Ceci dit, voici les commandes qui ont été utilisées pour effectuer les opérations dans MongoDB:
- find() pour la lecture:
  ```
  def select_all(self):
        """
        Return List[User]. Supports docs that use either `_id` (int) or `id` (int).
        """
        rows = self.users.find({}, {"_id": 1, "id": 1, "name": 1, "email": 1})
    
- insert_one() pour insérer:
  ```
  def insert(self, user: User):
        [...]
        self.users.insert_one(doc)

- update_one({...}, {"$set": {...}}) pour modifier:
  ```
  def update(self, user: User) -> int:
        [...]
        result = self.users.update_one({"_id": int(user.id)}, {"$set": doc})
        return result.modified_count

- delete_one({...}) pour supprimer:
  ```
  def delete(self, user_id: int) -> int:
        """
        Delete user from MongoDB with given user ID.
        """
        result = self.users.delete_one({"_id": int(user_id)})
        return result.deleted_count

> 💡 Question 3 : Comment avez-vous implémenté votre product_view.py ? Est-ce qu’il importe directement la ProductDAO ? Veuillez inclure le code pour illustrer votre réponse.

La vue `product_view.py` n'importe pas directement la `ProductDAO`. Cette dernière passe par le contrôleur `ProductController` pour respecter le patron MVC. 
- `product_view.py`:
  ```
  class ProductView:
    @staticmethod
    def show_options():
        """ Show menu with operation options which can be selected by the user """
        controller = ProductController()
        while True:
            print("\n1. Montrer la liste de produits\n2. Ajouter un produit\n3. Retour au menu principal")
            choice = input("Choisissez une option: ")

            if choice == '1':
                products = controller.list_products()
                ProductView.show_products(products)
    
- `ProductController`:
  ```
  class ProductController:
    def __init__(self):
        self.dao = ProductDAO()

> 💡 Question 4 : Si nous devions créer une application permettant d’associer des achats d'articles aux utilisateurs (Users → Products), comment structurerions-nous les données dans MySQL par rapport à MongoDB ?

Si on veut associer des achats d'articles aux utilisateurs, on crée une table d'association `purchases` qui représente la relation many-to-many entre ces deux entités. 
- MySQL (relationnel):
  ```
    -- Créer le tableau Users
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(80) NOT NULL,
        email VARCHAR(80) NOT NULL
    );

    -- Créer le tableau Products
    CREATE TABLE IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(80) NOT NULL,
        brand VARCHAR(20) NOT NULL,
        price DECIMAL(10, 2) NOT NULL
    );

    -- Table d'associations des achats (User - Product)
    CREATE TABLE IF NOT EXISTS purchases (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        product_id INT NOT NULL,
        quantity INT NOT NULL DEFAULT 1,
        price_paid DECIMAL(10,2) NOT NULL,
        purchased_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    )

Au niveau de MongoDB, on stocke les données dans des objets qui référencent les users et les products. 
- MongoDB:
  ```
  db.purchases.insertOne({
  userId: 1, productId: 3, quantity: 2, pricePaid: 199.99, purchasedAt: new Date()
  })